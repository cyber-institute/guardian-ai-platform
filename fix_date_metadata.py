#!/usr/bin/env python3
"""
Fix Date Metadata HTML Artifacts
Cleans existing corrupted date metadata in the database
"""

import os
import re
import psycopg2
from utils.document_metadata_extractor import clean_date_metadata

def fix_corrupted_date_metadata():
    """Clean all corrupted date metadata in the database"""
    print("Starting date metadata cleanup...")
    
    try:
        # Connect to PostgreSQL database
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            print("DATABASE_URL environment variable not found")
            return
            
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get all documents with date metadata
        cursor.execute("SELECT id, publish_date FROM documents WHERE publish_date IS NOT NULL")
        documents = cursor.fetchall()
        
        print(f"Found {len(documents)} documents with date metadata")
        
        fixed_count = 0
        for doc_id, current_date in documents:
            if current_date and isinstance(current_date, str):
                # Check if date contains HTML artifacts
                if any(artifact in current_date for artifact in ['<', '>', '&', 'style=', 'div', 'span']):
                    print(f"Document {doc_id}: Found corrupted date: {current_date[:50]}")
                    
                    # Clean the date
                    cleaned_date = clean_date_metadata(current_date)
                    
                    if cleaned_date and cleaned_date != current_date:
                        # Update the database
                        cursor.execute(
                            "UPDATE documents SET publish_date = ? WHERE id = ?",
                            (cleaned_date, doc_id)
                        )
                        print(f"  → Fixed to: {cleaned_date}")
                        fixed_count += 1
                    else:
                        # If cleaning failed, set to Unknown
                        cursor.execute(
                            "UPDATE documents SET publish_date = ? WHERE id = ?",
                            ('Unknown', doc_id)
                        )
                        print(f"  → Set to: Unknown (cleaning failed)")
                        fixed_count += 1
        
        conn.commit()
        conn.close()
        
        print(f"\nCompleted! Fixed {fixed_count} corrupted date entries.")
        
    except Exception as e:
        print(f"Error fixing date metadata: {e}")

def validate_date_cleanup():
    """Validate that no HTML artifacts remain in date metadata"""
    print("\nValidating date metadata cleanup...")
    
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            print("DATABASE_URL environment variable not found")
            return
            
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check for remaining HTML artifacts
        cursor.execute("SELECT id, publish_date FROM documents WHERE publish_date IS NOT NULL")
        documents = cursor.fetchall()
        
        html_artifacts = ['<', '>', '&', 'style=', 'div', 'span', 'class=', 'id=']
        corrupted_found = 0
        
        for doc_id, date_value in documents:
            if date_value and isinstance(date_value, str):
                for artifact in html_artifacts:
                    if artifact in date_value:
                        print(f"WARNING: Document {doc_id} still has artifact '{artifact}' in date: {date_value}")
                        corrupted_found += 1
                        break
        
        if corrupted_found == 0:
            print("✓ All date metadata is clean - no HTML artifacts found")
        else:
            print(f"✗ Found {corrupted_found} documents with remaining HTML artifacts")
        
        conn.close()
        
    except Exception as e:
        print(f"Error validating cleanup: {e}")

if __name__ == "__main__":
    fix_corrupted_date_metadata()
    validate_date_cleanup()