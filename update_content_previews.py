#!/usr/bin/env python3
"""
Update content previews for all documents using the intelligent summarizer
"""

import os
import psycopg2
from utils.intelligent_content_summarizer import generate_intelligent_content_preview

def update_all_content_previews():
    """Update content previews for all documents using intelligent summarizer"""
    
    # Connect to PostgreSQL database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get all documents
    cursor.execute("SELECT id, content, title, document_type FROM documents WHERE content IS NOT NULL")
    documents = cursor.fetchall()
    
    print(f"Updating content previews for {len(documents)} documents...")
    
    updated_count = 0
    for doc_id, content, title, doc_type in documents:
        try:
            # Generate intelligent summary
            intelligent_summary = generate_intelligent_content_preview(
                content=content,
                title=title or "Document",
                doc_type=doc_type or "Document"
            )
            
            if intelligent_summary and len(intelligent_summary.strip()) > 10:
                # Update the document with new content preview
                cursor.execute(
                    "UPDATE documents SET content_preview = %s WHERE id = %s",
                    (intelligent_summary, doc_id)
                )
                updated_count += 1
                print(f"✓ Updated document {doc_id}: {title[:50]}...")
            else:
                print(f"✗ Failed to generate summary for document {doc_id}")
                
        except Exception as e:
            print(f"✗ Error processing document {doc_id}: {str(e)}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n✓ Successfully updated {updated_count} content previews!")
    print("Content previews now analyze entire documents instead of just first paragraphs.")

if __name__ == "__main__":
    update_all_content_previews()