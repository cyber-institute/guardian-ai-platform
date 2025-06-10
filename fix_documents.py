#!/usr/bin/env python3
"""
Fix document metadata and thumbnail generation issues
"""

import os
import sys
import re
from utils.database import get_db_connection
from utils.thumbnail_generator import generate_thumbnail_for_document

def clean_html_artifacts(text):
    """Remove all HTML artifacts completely"""
    if not text:
        return ""
    
    # Remove all HTML tags
    text = re.sub(r'<[^>]*>', '', str(text))
    # Remove HTML entities
    text = re.sub(r'&[a-zA-Z0-9#]+;', '', text)
    # Clean up extra whitespace
    text = ' '.join(text.split()).strip()
    return text

def update_document_metadata():
    """Update documents with proper metadata and thumbnails"""
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Get all documents
        cursor.execute("SELECT id, title, content, file_path FROM documents")
        documents = cursor.fetchall()
        
        updates_made = 0
        
        for doc_id, title, content, file_path in documents:
            
            # Extract better metadata based on content
            new_title = title
            new_org = "Unknown"
            new_doc_type = "Policy Document"
            
            if content:
                content_lower = content.lower()
                
                # NIST document detection
                if 'nist' in content_lower or 'national institute of standards' in content_lower:
                    new_org = "NIST"
                    if 'artificial intelligence' in content_lower:
                        new_title = "NIST AI Risk Management Framework"
                        new_doc_type = "Framework"
                
                # EU document detection  
                elif 'europa.eu' in title.lower() or 'european' in content_lower:
                    new_org = "European Union"
                    if 'artificial intelligence' in content_lower:
                        new_title = "EU AI Act Implementation Guidelines"
                        new_doc_type = "Regulation"
            
            # Clean all fields
            clean_title = clean_html_artifacts(new_title)
            clean_org = clean_html_artifacts(new_org)
            clean_doc_type = clean_html_artifacts(new_doc_type)
            
            # Update database
            cursor.execute("""
                UPDATE documents 
                SET title = %s, 
                    author_organization = %s, 
                    document_type = %s,
                    publish_date = CURRENT_DATE
                WHERE id = %s
            """, (clean_title, clean_org, clean_doc_type, doc_id))
            
            # Generate thumbnail
            try:
                generate_thumbnail_for_document(doc_id)
                print(f"Updated document {doc_id}: {clean_title}")
                updates_made += 1
            except Exception as e:
                print(f"Thumbnail generation failed for doc {doc_id}: {e}")
        
        conn.commit()
        print(f"Successfully updated {updates_made} documents")
        
    except Exception as e:
        print(f"Error updating documents: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_document_metadata()