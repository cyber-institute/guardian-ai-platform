#!/usr/bin/env python3
"""
Apply Comprehensive Enhanced Scoring to All Documents
Updates all documents in the repository with the fixed enhanced scoring system
"""

import os
import psycopg2
from utils.comprehensive_scoring import comprehensive_document_scoring
import time

def apply_enhanced_scoring_to_all():
    """Apply enhanced scoring to all documents in the database"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        # Get all documents
        cursor.execute('SELECT id, title, content FROM documents WHERE content IS NOT NULL ORDER BY id')
        documents = cursor.fetchall()
        
        print(f"Found {len(documents)} documents to process")
        print("="*60)
        
        updated_count = 0
        failed_count = 0
        
        for doc_id, title, content in documents:
            try:
                # Skip if content is too short
                if not content or len(content.strip()) < 100:
                    print(f"Skipping document {doc_id} - insufficient content")
                    continue
                
                # Apply comprehensive scoring
                scores = comprehensive_document_scoring(content, title)
                
                # Update database with new scores
                cursor.execute('''
                    UPDATE documents 
                    SET ai_cybersecurity_score = %s,
                        ai_ethics_score = %s,
                        quantum_cybersecurity_score = %s,
                        quantum_ethics_score = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                ''', (
                    scores.get('ai_cybersecurity'),
                    scores.get('ai_ethics'),
                    scores.get('quantum_cybersecurity'),
                    scores.get('quantum_ethics'),
                    doc_id
                ))
                
                updated_count += 1
                
                # Show progress for significant documents
                if any(score is not None and score > 0 for score in scores.values()):
                    print(f"✓ Document {doc_id}: {title[:50]}...")
                    for framework, score in scores.items():
                        if score is not None and score > 0:
                            print(f"    {framework}: {score}")
                    print()
                
                # Commit every 10 documents
                if updated_count % 10 == 0:
                    conn.commit()
                    print(f"Progress: {updated_count}/{len(documents)} documents processed")
                
            except Exception as e:
                failed_count += 1
                print(f"✗ Failed to process document {doc_id}: {e}")
                continue
        
        # Final commit
        conn.commit()
        
        print("="*60)
        print(f"Enhanced scoring application complete!")
        print(f"Successfully updated: {updated_count} documents")
        print(f"Failed: {failed_count} documents")
        
        # Show summary of updated scores
        cursor.execute('''
            SELECT 
                COUNT(*) as total_docs,
                COUNT(CASE WHEN ai_cybersecurity_score IS NOT NULL THEN 1 END) as ai_cyber,
                COUNT(CASE WHEN quantum_cybersecurity_score IS NOT NULL THEN 1 END) as quantum_cyber,
                COUNT(CASE WHEN ai_ethics_score IS NOT NULL THEN 1 END) as ai_ethics,
                COUNT(CASE WHEN quantum_ethics_score IS NOT NULL THEN 1 END) as quantum_ethics
            FROM documents
        ''')
        
        stats = cursor.fetchone()
        print(f"\nScoring Statistics:")
        print(f"Total documents: {stats[0]}")
        print(f"AI Cybersecurity scores: {stats[1]}")
        print(f"Quantum Cybersecurity scores: {stats[2]}")
        print(f"AI Ethics scores: {stats[3]}")
        print(f"Quantum Ethics scores: {stats[4]}")
        
    except Exception as e:
        print(f"Error during enhanced scoring application: {e}")
        conn.rollback()
        
    finally:
        cursor.close()
        conn.close()

def verify_nsm10_fix():
    """Verify NSM-10 has the correct enhanced scores"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT title, ai_cybersecurity_score, quantum_cybersecurity_score, ai_ethics_score, quantum_ethics_score
            FROM documents 
            WHERE id = 48
        ''')
        
        result = cursor.fetchone()
        if result:
            title, ai_cyber, quantum_cyber, ai_ethics, quantum_ethics = result
            print("NSM-10 Verification:")
            print(f"Title: {title}")
            print(f"AI Cybersecurity: {ai_cyber}")
            print(f"Quantum Cybersecurity: {quantum_cyber}")
            print(f"AI Ethics: {ai_ethics}")
            print(f"Quantum Ethics: {quantum_ethics}")
            
            if quantum_cyber == 60:
                print("✓ NSM-10 quantum cybersecurity score correctly updated to 60")
            else:
                print(f"✗ NSM-10 quantum cybersecurity score is {quantum_cyber}, expected 60")
        else:
            print("✗ NSM-10 document not found")
            
    except Exception as e:
        print(f"Error verifying NSM-10: {e}")
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Starting comprehensive enhanced scoring application...")
    print("This will update all documents with the fixed scoring system")
    print()
    
    # First verify NSM-10 is fixed
    verify_nsm10_fix()
    print()
    
    # Apply enhanced scoring to all documents
    apply_enhanced_scoring_to_all()
    
    print("\nEnhanced scoring application completed!")