#!/usr/bin/env python3
"""
Record the scoring corrections we made as training data for the ML system
"""

import os
import psycopg2
from utils.ml_training_system import train_from_corrections

def record_all_corrections():
    """Record all the scoring corrections we made as training data"""
    
    # Connect to PostgreSQL database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Document corrections we made:
    corrections = [
        {
            "doc_id": 10,
            "title": "NIST Special Publication 800-63-3 Digital Identity Guidelines",
            "original": {"ai_cybersecurity_score": 100, "quantum_ethics_score": 11},
            "corrected": {"ai_cybersecurity_score": None, "quantum_cybersecurity_score": None, 
                         "ai_ethics_score": None, "quantum_ethics_score": None},
            "reason": "Document is about digital identity, not AI or quantum systems"
        },
        {
            "doc_id": 27,
            "title": "NASA's Responsible AI Plan", 
            "original": {"quantum_cybersecurity_score": 1, "quantum_ethics_score": 11},
            "corrected": {"quantum_cybersecurity_score": None, "quantum_ethics_score": None},
            "reason": "Pure AI document should not have quantum scores"
        },
        {
            "doc_id": 26,
            "title": "Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
            "original": {"quantum_cybersecurity_score": 1, "quantum_ethics_score": 11},
            "corrected": {"quantum_cybersecurity_score": None, "quantum_ethics_score": None},
            "reason": "AI-focused framework should not include quantum scores"
        }
    ]
    
    print("Recording scoring corrections as ML training data...")
    
    for correction in corrections:
        # Get document content
        cursor.execute("SELECT content FROM documents WHERE id = %s", (correction["doc_id"],))
        result = cursor.fetchone()
        
        if result:
            content = result[0]
            
            # Record the correction for ML training
            train_from_corrections(
                doc_id=correction["doc_id"],
                original_scores=correction["original"],
                corrected_scores=correction["corrected"],
                content=content,
                title=correction["title"]
            )
            
            print(f"✓ Recorded correction for: {correction['title'][:50]}...")
            print(f"  Reason: {correction['reason']}")
    
    conn.close()
    print(f"\n✓ All corrections recorded for ML training!")

if __name__ == "__main__":
    record_all_corrections()