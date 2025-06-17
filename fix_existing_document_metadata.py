"""
Fix existing document metadata by applying enhanced OCR extraction
"""

from utils.database import db_manager
from utils.enhanced_ocr_metadata import extract_enhanced_metadata_from_content
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_all_document_metadata():
    """Apply enhanced metadata extraction to all existing documents"""
    
    docs = db_manager.fetch_documents()
    logger.info(f"Processing {len(docs)} documents for metadata enhancement...")
    
    updated_count = 0
    
    for doc in docs:
        doc_id = doc.get('id')
        content = doc.get('content', '')
        current_title = doc.get('title', '')
        
        if not content or len(content.strip()) < 50:
            logger.info(f"Skipping document {doc_id} - insufficient content")
            continue
        
        # Apply enhanced metadata extraction
        try:
            enhanced_metadata = extract_enhanced_metadata_from_content(content)
            
            new_title = enhanced_metadata.get('title', current_title)
            new_org = enhanced_metadata.get('author_organization', 'Unknown')
            new_type = enhanced_metadata.get('document_type', 'Document')
            
            # Only update if we got meaningful improvements
            if (new_title != 'Document Title Not Extracted' and 
                len(new_title) > 10 and 
                new_title != current_title):
                
                logger.info(f"Updating document {doc_id}:")
                logger.info(f"  Old title: {current_title[:50]}...")
                logger.info(f"  New title: {new_title[:50]}...")
                logger.info(f"  Organization: {new_org}")
                logger.info(f"  Type: {new_type}")
                
                # Update document in database
                update_query = """
                UPDATE documents 
                SET title = %s, 
                    author_organization = %s, 
                    organization = %s,
                    document_type = %s,
                    extraction_method = %s
                WHERE id = %s
                """
                
                db_manager.execute_query(update_query, (
                    new_title,
                    new_org, 
                    new_org,
                    new_type,
                    'ENHANCED_OCR_RETROACTIVE',
                    doc_id
                ))
                
                updated_count += 1
                
        except Exception as e:
            logger.error(f"Error processing document {doc_id}: {e}")
            continue
    
    logger.info(f"Metadata enhancement complete: {updated_count} documents updated")
    return updated_count

if __name__ == "__main__":
    fix_all_document_metadata()