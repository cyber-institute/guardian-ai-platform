"""
Update document URLs using the enhanced URL discovery system
"""

import logging
from utils.database import db_manager
from utils.auto_url_discovery import auto_url_discovery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_all_document_urls():
    """Update URLs for all documents that don't have valid URLs"""
    try:
        # Fetch all documents
        docs = db_manager.fetch_documents()
        logger.info(f"Processing {len(docs)} documents for URL discovery...")
        
        updated_count = 0
        
        for doc in docs:
            doc_id = doc.get('id')
            title = doc.get('title', '')
            existing_url = doc.get('source', '')
            
            # Skip if already has valid URL
            if existing_url and existing_url.startswith('http') and existing_url != 'Link pending':
                logger.info(f"Doc {doc_id} already has URL: {existing_url[:50]}...")
                continue
            
            # Discover URL
            discovered_url = auto_url_discovery.get_document_url(doc)
            
            if discovered_url:
                logger.info(f"✓ Updated doc {doc_id}: {title[:50]}...")
                logger.info(f"  URL: {discovered_url}")
                updated_count += 1
            else:
                logger.info(f"✗ No URL found for doc {doc_id}: {title[:50]}...")
        
        logger.info(f"URL discovery complete: {updated_count} documents updated")
        return updated_count
        
    except Exception as e:
        logger.error(f"URL discovery failed: {e}")
        return 0

if __name__ == "__main__":
    update_all_document_urls()