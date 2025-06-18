#!/usr/bin/env python3
"""
Emergency restore of UNESCO document - stop automated corruption
"""

import os
import psycopg2
from datetime import datetime

def restore_unesco_document():
    """Restore UNESCO document to correct state and prevent further corruption"""
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        print("🚨 Emergency UNESCO Document Restoration")
        print("=" * 45)
        
        # Restore correct metadata for document ID 63
        cursor.execute("""
            UPDATE documents 
            SET title = %s,
                document_type = %s,
                organization = %s,
                author_organization = %s,
                topic = %s,
                ai_cybersecurity_score = %s,
                ai_ethics_score = %s,
                url_status = %s,
                url_valid = %s,
                updated_at = %s
            WHERE id = %s
        """, (
            "Recommendation on the Ethics of Artificial Intelligence - UNESCO Digital Library",
            "Policy",
            "UNESCO",
            "UNESCO",
            "AI",
            100,
            100,
            'valid',
            True,
            datetime.now(),
            63
        ))
        
        conn.commit()
        print("✅ UNESCO document restored to correct state")
        
        # Verify restoration
        cursor.execute("SELECT title, document_type, organization, ai_cybersecurity_score, ai_ethics_score FROM documents WHERE id = 63")
        doc = cursor.fetchone()
        if doc:
            print(f"   Title: {doc[0][:50]}...")
            print(f"   Type: {doc[1]}")
            print(f"   Organization: {doc[2]}")
            print(f"   AI Cyber Score: {doc[3]}")
            print(f"   AI Ethics Score: {doc[4]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    restore_unesco_document()