#!/usr/bin/env python3
"""
Test the scoring fixes to ensure pure AI documents don't get quantum scores
"""

import os
import psycopg2

def test_scoring_fixes():
    """Test that pure AI documents no longer have quantum scores"""
    
    # Connect to PostgreSQL database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Check for pure AI documents that should not have quantum scores
    cursor.execute("""
        SELECT id, title, topic, quantum_cybersecurity_score, quantum_ethics_score 
        FROM documents 
        WHERE topic = 'AI' 
        AND (quantum_cybersecurity_score IS NOT NULL OR quantum_ethics_score IS NOT NULL)
    """)
    
    ai_docs_with_quantum_scores = cursor.fetchall()
    
    print("=== SCORING FIX VERIFICATION ===")
    print(f"Pure AI documents with quantum scores: {len(ai_docs_with_quantum_scores)}")
    
    if ai_docs_with_quantum_scores:
        print("\n❌ ISSUE: Found AI documents with quantum scores:")
        for doc_id, title, topic, q_cyber, q_ethics in ai_docs_with_quantum_scores:
            print(f"  - ID {doc_id}: {title}")
            print(f"    Topic: {topic}")
            print(f"    Quantum Cyber: {q_cyber}, Quantum Ethics: {q_ethics}")
    else:
        print("\n✅ SUCCESS: No pure AI documents have quantum scores")
    
    # Check quantum documents to ensure they still have scores
    cursor.execute("""
        SELECT id, title, topic, quantum_cybersecurity_score, quantum_ethics_score 
        FROM documents 
        WHERE topic = 'Quantum'
    """)
    
    quantum_docs = cursor.fetchall()
    print(f"\nQuantum documents found: {len(quantum_docs)}")
    
    for doc_id, title, topic, q_cyber, q_ethics in quantum_docs:
        print(f"  - ID {doc_id}: {title}")
        print(f"    Quantum Cyber: {q_cyber}, Quantum Ethics: {q_ethics}")
    
    # Check title fix
    cursor.execute("SELECT title FROM documents WHERE id = 27")
    nasa_title = cursor.fetchone()
    if nasa_title:
        print(f"\nNASA document title: '{nasa_title[0]}'")
        if "NASA's" in nasa_title[0]:
            print("✅ SUCCESS: NASA title has correct apostrophe")
        else:
            print("❌ ISSUE: NASA title still missing apostrophe")
    
    conn.close()
    print("\n✓ Scoring verification complete!")

if __name__ == "__main__":
    test_scoring_fixes()