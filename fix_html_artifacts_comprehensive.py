#!/usr/bin/env python3
"""
Comprehensive HTML Artifacts Fix
Uses Multi-LLM system to re-extract all metadata and eliminate HTML artifacts completely
"""

import os
import psycopg2
from utils.multi_llm_metadata_extractor import extract_clean_metadata

def comprehensive_metadata_cleanup():
    """Re-extract all metadata using Multi-LLM system to eliminate HTML artifacts"""
    print("Starting comprehensive metadata cleanup using Multi-LLM extraction...")
    
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            print("DATABASE_URL environment variable not found")
            return
            
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get all documents
        cursor.execute("SELECT id, content, title FROM documents")
        documents = cursor.fetchall()
        
        print(f"Processing {len(documents)} documents with Multi-LLM metadata extraction...")
        
        updated_count = 0
        for doc_id, content, filename in documents:
            if content:
                print(f"Processing document {doc_id}...")
                
                # Extract clean metadata using Multi-LLM system
                clean_metadata = extract_clean_metadata(content, filename or "")
                
                # Update document with clean metadata
                cursor.execute("""
                    UPDATE documents 
                    SET title = %s, 
                        author_organization = %s, 
                        publish_date = %s,
                        document_type = %s
                    WHERE id = %s
                """, (
                    clean_metadata.get('title') or 'Unknown',
                    clean_metadata.get('author_organization') or 'Unknown', 
                    clean_metadata.get('publish_date'),
                    clean_metadata.get('document_type') or 'Document',
                    doc_id
                ))
                
                updated_count += 1
                print(f"  → Updated with clean metadata")
        
        conn.commit()
        conn.close()
        
        print(f"\nCompleted! Updated {updated_count} documents with clean metadata.")
        
    except Exception as e:
        print(f"Error during comprehensive cleanup: {e}")

def validate_no_html_artifacts():
    """Validate that no HTML artifacts remain anywhere in the system"""
    print("\nValidating complete elimination of HTML artifacts...")
    
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            print("DATABASE_URL environment variable not found")
            return
            
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Check all text fields for HTML artifacts
        cursor.execute("""
            SELECT id, title, author_organization, publish_date::text, document_type 
            FROM documents
        """)
        documents = cursor.fetchall()
        
        html_patterns = [
            '<', '>', '&lt;', '&gt;', '&amp;', '&nbsp;',
            '</div>', '<div>', '<span>', '</span>', '<p>', '</p>',
            'style=', 'class=', 'id=', 'href='
        ]
        
        artifacts_found = 0
        for doc_id, title, org, date, doc_type in documents:
            fields = [title, org, date, doc_type]
            
            for i, field in enumerate(fields):
                if field and isinstance(field, str):
                    for pattern in html_patterns:
                        if pattern in field:
                            field_names = ['title', 'organization', 'date', 'type']
                            print(f"WARNING: Document {doc_id} {field_names[i]} contains '{pattern}': {field[:100]}")
                            artifacts_found += 1
                            break
        
        if artifacts_found == 0:
            print("✓ SUCCESS: No HTML artifacts found in any metadata fields")
        else:
            print(f"✗ Found {artifacts_found} fields with HTML artifacts")
        
        conn.close()
        
    except Exception as e:
        print(f"Error validating cleanup: {e}")

if __name__ == "__main__":
    comprehensive_metadata_cleanup()
    validate_no_html_artifacts()