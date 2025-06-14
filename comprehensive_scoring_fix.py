#!/usr/bin/env python3
"""
Comprehensive fix for all scoring and display issues
"""

import os
import psycopg2
from utils.ml_enhanced_scoring import assess_document_with_ml

def fix_all_scoring_issues():
    """Fix all scoring and display issues comprehensively"""
    
    # Connect to PostgreSQL database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    print("=== COMPREHENSIVE SCORING FIX ===")
    
    # Get all documents for analysis
    cursor.execute("SELECT id, title, content, topic FROM documents WHERE content IS NOT NULL")
    all_docs = cursor.fetchall()
    
    print(f"Analyzing {len(all_docs)} documents for scoring corrections...")
    
    fixed_count = 0
    for doc_id, title, content, current_topic in all_docs:
        try:
            # Apply ML-enhanced scoring
            ml_scores = assess_document_with_ml(content, title)
            
            # Determine if any scores are problematic
            needs_fix = False
            
            # Check current scores
            cursor.execute("""
                SELECT ai_cybersecurity_score, quantum_cybersecurity_score, 
                       ai_ethics_score, quantum_ethics_score 
                FROM documents WHERE id = %s
            """, (doc_id,))
            current_scores = cursor.fetchone()
            
            # Check for problematic scores
            if current_scores:
                ai_cyber, q_cyber, ai_ethics, q_ethics = current_scores
                
                # Flag unrealistic AI scores (>85)
                if ai_cyber and ai_cyber > 85:
                    needs_fix = True
                    print(f"  Fixing unrealistic AI Cybersecurity score: {ai_cyber} -> {ml_scores.get('ai_cybersecurity_score', 'N/A')}")
                
                # Flag quantum scores on pure AI documents
                if current_topic == 'AI' and (q_cyber is not None or q_ethics is not None):
                    needs_fix = True
                    print(f"  Removing quantum scores from AI document: {title[:50]}...")
                
                # Flag AI scores on pure quantum documents  
                if current_topic == 'Quantum' and not any(['ai' in content.lower(), 'artificial intelligence' in content.lower()]):
                    if ai_cyber or ai_ethics:
                        needs_fix = True
                        print(f"  Checking AI scores on quantum document: {title[:50]}...")
            
            if needs_fix or not current_scores:
                # Update with ML-enhanced scores
                cursor.execute("""
                    UPDATE documents 
                    SET ai_cybersecurity_score = %s,
                        quantum_cybersecurity_score = %s,
                        ai_ethics_score = %s,
                        quantum_ethics_score = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (
                    ml_scores.get('ai_cybersecurity_score'),
                    ml_scores.get('quantum_cybersecurity_score'),
                    ml_scores.get('ai_ethics_score'),
                    ml_scores.get('quantum_ethics_score'),
                    doc_id
                ))
                fixed_count += 1
                
        except Exception as e:
            print(f"  Error processing document {doc_id}: {str(e)}")
    
    # Commit all changes
    conn.commit()
    
    print(f"\n✓ Fixed scoring for {fixed_count} documents")
    
    # Verification section
    print(f"\n=== VERIFICATION RESULTS ===")
    
    # Check for remaining problematic scores
    cursor.execute("""
        SELECT COUNT(*) FROM documents 
        WHERE ai_cybersecurity_score > 85 
        OR (topic = 'AI' AND (quantum_cybersecurity_score IS NOT NULL OR quantum_ethics_score IS NOT NULL))
    """)
    problem_count = cursor.fetchone()[0]
    
    if problem_count == 0:
        print("✅ All scoring issues resolved!")
    else:
        print(f"⚠️  {problem_count} documents still have scoring issues")
    
    # Show sample of corrected documents
    cursor.execute("""
        SELECT title, ai_cybersecurity_score, quantum_cybersecurity_score, 
               ai_ethics_score, quantum_ethics_score, topic
        FROM documents 
        ORDER BY updated_at DESC 
        LIMIT 5
    """)
    
    recent_docs = cursor.fetchall()
    print(f"\nRecent scoring updates:")
    for title, ai_cyber, q_cyber, ai_ethics, q_ethics, topic in recent_docs:
        print(f"  {title[:40]}... ({topic})")
        print(f"    AI: Cyber={ai_cyber}, Ethics={ai_ethics}")
        print(f"    Quantum: Cyber={q_cyber}, Ethics={q_ethics}")
    
    conn.close()
    print(f"\n✓ Comprehensive scoring fix complete!")

if __name__ == "__main__":
    fix_all_scoring_issues()