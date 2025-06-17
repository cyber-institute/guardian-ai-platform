"""
Force update all content previews with enhanced intelligent summaries
"""

import sys
import os
sys.path.append('.')

from utils.database import get_db_connection
from utils.intelligent_preview import generate_intelligent_preview

def force_update_all_previews():
    """Force regenerate all content previews with enhanced system"""
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all documents with content
        cursor.execute("""
            SELECT id, title, clean_content, content, text_content 
            FROM documents 
            WHERE (clean_content IS NOT NULL AND clean_content != '') 
               OR (content IS NOT NULL AND content != '')
               OR (text_content IS NOT NULL AND text_content != '')
        """)
        
        documents = cursor.fetchall()
        print(f"Found {len(documents)} documents to update")
        
        updated_count = 0
        for doc in documents:
            doc_id, title, clean_content, content, text_content = doc
            
            # Get the best available content
            raw_content = clean_content or content or text_content or ""
            
            if len(raw_content) > 100:
                try:
                    # Generate enhanced preview
                    enhanced_preview = generate_intelligent_preview(title or "Document", raw_content)
                    
                    # Update database
                    cursor.execute("""
                        UPDATE documents 
                        SET content_preview = %s 
                        WHERE id = %s
                    """, (enhanced_preview, doc_id))
                    
                    updated_count += 1
                    print(f"Updated preview for: {title[:50]}...")
                    
                except Exception as e:
                    print(f"Error updating {title}: {e}")
        
        conn.commit()
        print(f"Successfully updated {updated_count} document previews")
        
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    force_update_all_previews()