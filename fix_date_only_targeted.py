#!/usr/bin/env python3
"""
Targeted DATE-only fix for UNESCO document
This script ONLY modifies the publication_date field without touching any other metadata
"""

import os
import psycopg2
from datetime import datetime

def fix_unesco_date_only():
    """Fix ONLY the publication date for UNESCO document ID 63"""
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Backup current state
        cursor.execute("""
            SELECT title, document_type, organization, publication_date, 
                   ai_cybersecurity_score, ai_ethics_score, url_status, url_valid
            FROM documents WHERE id = 63
        """)
        
        current_state = cursor.fetchone()
        print("Current UNESCO state:")
        print(f"Title: {current_state[0]}")
        print(f"Type: {current_state[1]}")
        print(f"Organization: {current_state[2]}")
        print(f"Date: {current_state[3]}")
        print(f"Scores: {current_state[4]}/{current_state[5]}")
        print(f"URL Status: {current_state[6]}")
        print(f"URL Valid: {current_state[7]}")
        
        # ONLY update the publication_date field - preserve everything else
        cursor.execute("""
            UPDATE documents 
            SET publication_date = %s
            WHERE id = 63
        """, ('2021-11-23',))
        
        conn.commit()
        
        # Verify ONLY the date changed
        cursor.execute("""
            SELECT title, document_type, organization, publication_date, 
                   ai_cybersecurity_score, ai_ethics_score, url_status, url_valid
            FROM documents WHERE id = 63
        """)
        
        new_state = cursor.fetchone()
        print("\nAfter DATE-only fix:")
        print(f"Title: {new_state[0]}")
        print(f"Type: {new_state[1]}")
        print(f"Organization: {new_state[2]}")
        print(f"Date: {new_state[3]} <- FIXED")
        print(f"Scores: {new_state[4]}/{new_state[5]}")
        print(f"URL Status: {new_state[6]}")
        print(f"URL Valid: {new_state[7]}")
        
        # Verify no other fields changed
        if (current_state[0] == new_state[0] and  # title unchanged
            current_state[1] == new_state[1] and  # type unchanged
            current_state[2] == new_state[2] and  # org unchanged
            current_state[4] == new_state[4] and  # ai_cyber unchanged
            current_state[5] == new_state[5] and  # ai_ethics unchanged
            current_state[6] == new_state[6] and  # url_status unchanged
            current_state[7] == new_state[7]):    # url_valid unchanged
            
            print("\n✅ SUCCESS: Only publication_date was modified")
            print("✅ All other metadata preserved")
        else:
            print("\n❌ WARNING: Other fields were unexpectedly modified")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Targeted DATE-only fix for UNESCO document")
    print("=" * 50)
    fix_unesco_date_only()