"""
Create ML training patterns for NIST AI framework correction
"""

import sqlite3
import json
from datetime import datetime
import hashlib

def create_training_patterns():
    """Create ML training patterns based on NIST correction"""
    
    db_path = "ml_training.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Initialize database if needed
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id TEXT,
            original_extraction TEXT,
            verified_extraction TEXT,
            user_corrections TEXT,
            content_sample TEXT,
            extraction_confidence TEXT,
            timestamp TEXT,
            document_type TEXT,
            source_type TEXT,
            content_hash TEXT UNIQUE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learned_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_id TEXT UNIQUE,
            pattern_type TEXT,
            trigger_conditions TEXT,
            correction_rule TEXT,
            confidence_score REAL,
            usage_count INTEGER,
            success_rate REAL,
            created_at TEXT,
            last_updated TEXT
        )
    """)
    
    # Create verification pattern for NIST correction
    original_extraction = {
        'title': 'NIST AI Risk Management Framework',
        'topic': 'General',
        'organization': '',
        'framework_scores': {}
    }
    
    verified_extraction = {
        'title': 'NIST AI Risk Management Framework',
        'topic': 'AI',
        'organization': 'NIST',
        'framework_scores': {
            'ai_cybersecurity': 45,
            'ai_ethics': 10
        }
    }
    
    user_corrections = {
        'topic': {
            'original': 'General',
            'corrected': 'AI',
            'correction_type': 'field_replaced'
        },
        'framework_scores': {
            'original': {},
            'corrected': {'ai_cybersecurity': 45, 'ai_ethics': 10},
            'correction_type': 'missing_field_added'
        }
    }
    
    content_sample = """NIST has developed a framework to better manage risks to individuals, organizations, and society associated with artificial intelligence (AI). The NIST AI Risk Management Framework provides guidance for trustworthy AI systems."""
    
    content_hash = hashlib.md5(content_sample.encode()).hexdigest()
    
    # Store verification pattern
    cursor.execute("""
        INSERT OR REPLACE INTO verification_patterns 
        (document_id, original_extraction, verified_extraction, user_corrections,
         content_sample, extraction_confidence, timestamp, document_type, 
         source_type, content_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        '43',
        json.dumps(original_extraction),
        json.dumps(verified_extraction),
        json.dumps(user_corrections),
        content_sample,
        json.dumps({'topic': 0.0, 'framework_scores': 0.0}),
        datetime.now().isoformat(),
        'government_framework',
        'manual_correction',
        content_hash
    ))
    
    # Create learned patterns
    patterns = [
        {
            'pattern_id': 'ai_framework_topic',
            'pattern_type': 'topic',
            'trigger_conditions': ['ai risk management', 'artificial intelligence framework', 'ai governance', 'nist ai'],
            'correction_rule': json.dumps({
                'topic': 'AI',
                'requires_ai_scoring': True,
                'confidence_threshold': 0.9
            }),
            'confidence_score': 0.92
        },
        {
            'pattern_id': 'nist_organization',
            'pattern_type': 'organization',
            'trigger_conditions': ['nist', 'national institute of standards'],
            'correction_rule': json.dumps({
                'organization': 'NIST',
                'government_source': True,
                'confidence_threshold': 0.95
            }),
            'confidence_score': 0.95
        },
        {
            'pattern_id': 'ai_framework_scoring',
            'pattern_type': 'scoring',
            'trigger_conditions': ['ai framework', 'ai risk', 'ai governance', 'artificial intelligence'],
            'correction_rule': json.dumps({
                'required_scores': ['ai_cybersecurity', 'ai_ethics'],
                'score_calculation': 'content_analysis',
                'confidence_threshold': 0.85
            }),
            'confidence_score': 0.88
        }
    ]
    
    for pattern in patterns:
        pattern_id = pattern['pattern_id']
        
        cursor.execute("""
            INSERT OR REPLACE INTO learned_patterns 
            (pattern_id, pattern_type, trigger_conditions, correction_rule,
             confidence_score, usage_count, success_rate, created_at, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pattern_id,
            pattern['pattern_type'],
            json.dumps(pattern['trigger_conditions']),
            pattern['correction_rule'],
            pattern['confidence_score'],
            1,  # Initial usage count
            1.0,  # Perfect success rate initially
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
    
    conn.commit()
    conn.close()
    
    print("ML training patterns created successfully:")
    print("• AI Framework Topic Classification Pattern")
    print("• NIST Organization Recognition Pattern") 
    print("• AI Framework Scoring Requirements Pattern")

if __name__ == "__main__":
    create_training_patterns()