#!/usr/bin/env python3
"""
Fix NIST document scoring using ML-enhanced analysis
"""

import os
import psycopg2
from utils.ml_enhanced_scoring import assess_document_with_ml

def fix_nist_document_scoring():
    """Fix the NIST document scoring issues using ML-enhanced analysis"""
    
    # Connect to PostgreSQL database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get NIST documents with problematic scoring
    cursor.execute("""
        SELECT id, title, content 
        FROM documents 
        WHERE title LIKE '%NIST%' 
        AND (ai_cybersecurity_score = 100 OR quantum_ethics_score > 0)
    """)
    
    nist_docs = cursor.fetchall()
    
    print(f"=== FIXING NIST DOCUMENT SCORING ===")
    print(f"Found {len(nist_docs)} NIST documents with scoring issues")
    
    for doc_id, title, content in nist_docs:
        print(f"\nAnalyzing: {title}")
        
        # Apply ML-enhanced scoring
        ml_scores = assess_document_with_ml(content, title)
        
        print(f"ML Analysis Results:")
        print(f"  - AI Cybersecurity: {ml_scores.get('ai_cybersecurity_score', 'N/A')}")
        print(f"  - Quantum Cybersecurity: {ml_scores.get('quantum_cybersecurity_score', 'N/A')}")
        print(f"  - AI Ethics: {ml_scores.get('ai_ethics_score', 'N/A')}")
        print(f"  - Quantum Ethics: {ml_scores.get('quantum_ethics_score', 'N/A')}")
        
        # Update database with corrected scores
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
        
        print(f"✓ Updated document {doc_id} with corrected scores")
    
    # Commit changes
    conn.commit()
    
    # Verify the fixes
    print(f"\n=== VERIFICATION ===")
    cursor.execute("""
        SELECT id, title, ai_cybersecurity_score, quantum_cybersecurity_score, 
               ai_ethics_score, quantum_ethics_score
        FROM documents 
        WHERE title LIKE '%NIST%'
    """)
    
    updated_docs = cursor.fetchall()
    for doc_id, title, ai_cyber, q_cyber, ai_ethics, q_ethics in updated_docs:
        print(f"\n{title[:50]}...")
        print(f"  AI Cyber: {ai_cyber}, Quantum Cyber: {q_cyber}")
        print(f"  AI Ethics: {ai_ethics}, Quantum Ethics: {q_ethics}")
    
    conn.close()
    print(f"\n✓ NIST document scoring fixes complete!")

if __name__ == "__main__":
    fix_nist_document_scoring()