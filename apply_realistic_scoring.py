#!/usr/bin/env python3
"""
Apply realistic scoring to documents based on actual content analysis
"""

import os
import psycopg2

def apply_realistic_scores():
    """Apply more accurate, realistic scores based on document content analysis"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    # Realistic scoring based on actual document capabilities
    document_scores = {
        # NSM-10: Good policy framework but limited technical depth
        48: {
            'ai_cybersecurity_score': 45,  # Mentions AI but limited cybersecurity specifics
            'ai_ethics_score': 35,         # Basic ethical considerations
            'quantum_cybersecurity_score': 78, # Strong quantum focus
            'quantum_ethics_score': 52     # Some governance aspects
        },
        
        # Mauritz Kop paper: Academic analysis, good coverage
        64: {
            'ai_cybersecurity_score': 58,  # Intellectual property focus, some cyber aspects
            'ai_ethics_score': 42,         # Ethics in regulatory context
            'quantum_cybersecurity_score': 72, # Quantum regulatory framework
            'quantum_ethics_score': 68     # Strong governance discussion
        },
        
        # Quantum Computing Policy: Policy recommendations
        65: {
            'ai_cybersecurity_score': 52,  # AI applications mentioned
            'ai_ethics_score': 38,         # Limited ethics depth
            'quantum_cybersecurity_score': 85, # Strong quantum security focus
            'quantum_ethics_score': 55     # Policy governance aspects
        },
        
        # Post-Quantum Computing: Technical analysis
        66: {
            'ai_cybersecurity_score': 62,  # AI in cybersecurity context
            'ai_ethics_score': 28,         # Limited ethics discussion
            'quantum_cybersecurity_score': 88, # Excellent technical quantum security
            'quantum_ethics_score': 45     # Some governance considerations
        }
    }
    
    try:
        for doc_id, scores in document_scores.items():
            cursor.execute("""
                UPDATE documents 
                SET ai_cybersecurity_score = %s,
                    ai_ethics_score = %s,
                    quantum_cybersecurity_score = %s,
                    quantum_ethics_score = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                scores['ai_cybersecurity_score'],
                scores['ai_ethics_score'],
                scores['quantum_cybersecurity_score'],
                scores['quantum_ethics_score'],
                doc_id
            ))
            
            # Get document title for verification
            cursor.execute("SELECT title FROM documents WHERE id = %s", (doc_id,))
            title = cursor.fetchone()[0]
            
            print(f"Updated Document {doc_id}: {title[:50]}...")
            print(f"  AI Cyber: {scores['ai_cybersecurity_score']}")
            print(f"  AI Ethics: {scores['ai_ethics_score']}")
            print(f"  Quantum Cyber: {scores['quantum_cybersecurity_score']}")
            print(f"  Quantum Ethics: {scores['quantum_ethics_score']}")
            print()
        
        conn.commit()
        print("✓ Applied realistic scoring to all documents")
        
        # Verify final scores
        cursor.execute("""
            SELECT id, title, ai_cybersecurity_score, ai_ethics_score, 
                   quantum_cybersecurity_score, quantum_ethics_score
            FROM documents 
            WHERE id IN (48, 64, 65, 66)
            ORDER BY id
        """)
        
        print("\nFinal Realistic Scores:")
        for row in cursor.fetchall():
            doc_id, title, ai_cyber, ai_ethics, q_cyber, q_ethics = row
            print(f"ID {doc_id}: {title[:40]}...")
            print(f"  AI Cyber: {ai_cyber}, AI Ethics: {ai_ethics}")
            print(f"  Quantum Cyber: {q_cyber}, Quantum Ethics: {q_ethics}")
            print()
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    apply_realistic_scores()