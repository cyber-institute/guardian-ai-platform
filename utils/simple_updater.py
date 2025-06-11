"""
Simple document updater for retroactive metadata improvements
"""

import logging
from utils.database import DatabaseManager
from utils.fallback_analyzer import extract_metadata_fallback

logger = logging.getLogger(__name__)

def update_document_metadata():
    """Update all documents with improved metadata extraction."""
    
    db = DatabaseManager()
    
    # Get all documents
    query = "SELECT id, title, content, text_content, source FROM documents ORDER BY id"
    documents = db.execute_query(query)
    
    if not documents:
        return 0
    
    updated_count = 0
    
    for doc in documents:
        try:
            doc_id = doc['id']
            content = doc.get('content') or doc.get('text_content', '')
            source = doc.get('source', '')
            
            if not content:
                continue
            
            # Skip documents with manually corrected metadata
            current_title = doc.get('title', '')
            current_org = doc.get('author_organization', '')
            
            # Protected documents - never update these
            protected_patterns = [
                'NASA', 'NIST', 'RESPONSIBLE AI PLAN', 
                'National Institute of Standards', 'ARTIFICIAL INTELLIGENCE RISK',
                'DIGITAL IDENTITY GUIDELINES'
            ]
            
            if (any(pattern in current_title.upper() for pattern in protected_patterns) or
                any(pattern in current_org.upper() for pattern in protected_patterns) or
                doc_id in [10, 26, 27, 28, 29]):  # Specific document IDs to protect
                logger.info(f"Skipping document {doc_id} - manually corrected metadata")
                continue
            
            # Extract improved metadata
            metadata = extract_metadata_fallback(content, source)
            
            # Update document
            update_query = """
            UPDATE documents 
            SET title = %s,
                author_organization = %s,
                publish_date = %s,
                document_type = %s,
                content_preview = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """
            
            # Use direct database connection to avoid parameter issues
            import psycopg2
            import os
            
            conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
            cur = conn.cursor()
            
            cur.execute(update_query, (
                metadata.get('title', doc.get('title', 'Untitled')),
                metadata.get('author_organization', 'Unknown'),
                metadata.get('publish_date'),
                metadata.get('document_type', 'Report'),
                metadata.get('content_preview', ''),
                doc_id
            ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            updated_count += 1
            logger.info(f"Updated document {doc_id}")
            
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")
            continue
    
    return updated_count