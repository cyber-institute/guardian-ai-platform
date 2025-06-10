"""
Retroactive Document Updater
Updates all existing documents with improved metadata extraction
"""

import logging
from utils.database import DatabaseManager
from utils.fallback_analyzer import extract_metadata_fallback
from utils.comprehensive_scoring import comprehensive_document_scoring

logger = logging.getLogger(__name__)

def update_all_documents_metadata():
    """
    Reprocess all existing documents with current improved metadata extraction.
    This applies the latest title, organization, date, and type extraction to all docs.
    """
    
    db = DatabaseManager()
    
    try:
        # Fetch all documents
        documents = db.fetch_documents()
        
        if not documents:
            logger.info("No documents found to update")
            return 0
        
        updated_count = 0
        
        for doc in documents:
            try:
                doc_id = doc.get('id')
                content = doc.get('content', '') or doc.get('text_content', '')
                source = doc.get('source', '')
                
                if not content:
                    logger.warning(f"Document {doc_id} has no content, skipping")
                    continue
                
                # Extract improved metadata
                new_metadata = extract_metadata_fallback(content, source)
                
                # Get updated scoring
                title_for_scoring = new_metadata.get('title', '') or 'Untitled'
                new_scores = comprehensive_document_scoring(content, title_for_scoring)
                
                # Update document in database
                update_query = """
                UPDATE documents 
                SET title = :title,
                    author_organization = :author_organization,
                    publish_date = :publish_date,
                    document_type = :document_type,
                    content_preview = :content_preview,
                    ai_cybersecurity_score = :ai_cybersecurity_score,
                    quantum_cybersecurity_score = :quantum_cybersecurity_score,
                    ai_ethics_score = :ai_ethics_score,
                    quantum_ethics_score = :quantum_ethics_score,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = :doc_id
                """
                
                params = {
                    'title': new_metadata.get('title', doc.get('title', 'Untitled')),
                    'author_organization': new_metadata.get('author_organization', 'Unknown'),
                    'publish_date': new_metadata.get('publish_date'),
                    'document_type': new_metadata.get('document_type', 'Report'),
                    'content_preview': new_metadata.get('content_preview', ''),
                    'ai_cybersecurity_score': new_scores.get('ai_cybersecurity'),
                    'quantum_cybersecurity_score': new_scores.get('quantum_cybersecurity'),
                    'ai_ethics_score': new_scores.get('ai_ethics'),
                    'quantum_ethics_score': new_scores.get('quantum_ethics'),
                    'doc_id': doc_id
                }
                
                result = db.execute_query(update_query, params)
                
                if result is not None:
                    updated_count += 1
                    logger.info(f"Updated document {doc_id}: {new_metadata.get('title', 'Untitled')}")
                else:
                    logger.error(f"Failed to update document {doc_id}")
                    
            except Exception as e:
                logger.error(f"Error updating document {doc_id}: {e}")
                continue
        
        logger.info(f"Successfully updated {updated_count} documents")
        return updated_count
        
    except Exception as e:
        logger.error(f"Error in retroactive update: {e}")
        return 0

def check_if_update_needed():
    """
    Check if documents need metadata updates by comparing existing vs new extraction.
    Returns True if updates would improve the data quality.
    """
    
    db = DatabaseManager()
    
    try:
        # Sample a few documents to check if updates are needed
        sample_query = """
        SELECT id, title, content, text_content, source, author_organization
        FROM documents 
        ORDER BY created_at DESC 
        LIMIT 3
        """
        
        sample_docs = db.execute_query(sample_query)
        
        if not sample_docs:
            return False
        
        updates_needed = 0
        
        for doc in sample_docs:
            content = doc.get('content', '') or doc.get('text_content', '')
            source = doc.get('source', '')
            current_title = doc.get('title', '')
            current_org = doc.get('author_organization', '')
            
            if content:
                new_metadata = extract_metadata_fallback(content, source)
                new_title = new_metadata.get('title', '')
                new_org = new_metadata.get('author_organization', '')
                
                # Check if new extraction would be an improvement
                if (new_title and new_title != current_title and 
                    not any(bad in new_title.lower() for bad in ['webpage', 'document from', 'untitled'])):
                    updates_needed += 1
                elif (new_org and new_org != current_org and new_org != 'Unknown'):
                    updates_needed += 1
        
        return updates_needed > 0
        
    except Exception as e:
        logger.error(f"Error checking update need: {e}")
        return False