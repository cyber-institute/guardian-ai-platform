#!/usr/bin/env python3
"""
Fix NSM-10 document scoring - apply comprehensive scoring to policy document
"""

import os
import sys
import psycopg2

# Add utils to path
sys.path.append('utils')
from comprehensive_scoring import comprehensive_document_scoring

def fix_nsm10_scoring():
    """Apply comprehensive scoring to NSM-10 document"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        # Get the NSM-10 document content
        cursor.execute("SELECT id, title, content FROM documents WHERE id = 48")
        result = cursor.fetchone()
        
        if not result:
            print("NSM-10 document not found")
            return
        
        doc_id, title, content = result
        print(f"Processing NSM-10: {title[:50]}...")
        
        if content:
            # Apply comprehensive scoring
            scores = comprehensive_document_scoring(content, title)
            
            print(f"Calculated scores:")
            print(f"  AI Cybersecurity: {scores.get('ai_cybersecurity_score', 'N/A')}")
            print(f"  AI Ethics: {scores.get('ai_ethics_score', 'N/A')}")
            print(f"  Quantum Cybersecurity: {scores.get('quantum_cybersecurity_score', 'N/A')}")
            print(f"  Quantum Ethics: {scores.get('quantum_ethics_score', 'N/A')}")
            
            # Update database with scores
            cursor.execute("""
                UPDATE documents 
                SET ai_cybersecurity_score = %s,
                    ai_ethics_score = %s,
                    quantum_cybersecurity_score = %s,
                    quantum_ethics_score = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                scores.get('ai_cybersecurity_score'),
                scores.get('ai_ethics_score'), 
                scores.get('quantum_cybersecurity_score'),
                scores.get('quantum_ethics_score'),
                doc_id
            ))
            
            conn.commit()
            print("✓ NSM-10 scoring updated successfully")
            
        else:
            print("No content found for NSM-10 document")
        
        # Verify final state
        cursor.execute("""
            SELECT title, document_type, topic, source,
                   ai_cybersecurity_score, ai_ethics_score, 
                   quantum_cybersecurity_score, quantum_ethics_score
            FROM documents WHERE id = 48
        """)
        
        final_result = cursor.fetchone()
        if final_result:
            print(f"\nFinal NSM-10 state:")
            print(f"  Title: {final_result[0][:60]}...")
            print(f"  Type: {final_result[1]}")  
            print(f"  Topic: {final_result[2]}")
            print(f"  Source: {final_result[3][:50]}...")
            print(f"  AI Cyber: {final_result[4]}")
            print(f"  AI Ethics: {final_result[5]}")
            print(f"  Quantum Cyber: {final_result[6]}")
            print(f"  Quantum Ethics: {final_result[7]}")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_nsm10_scoring()