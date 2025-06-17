"""
Automatic URL Discovery Integration
Seamlessly integrates URL discovery into document display system
"""

import logging
from typing import Optional, Dict
from utils.restore_url_discovery import URLDiscoverySystem
from utils.database import db_manager

logger = logging.getLogger(__name__)

class AutoURLDiscovery:
    def __init__(self):
        self.url_discovery = URLDiscoverySystem()
        self._url_cache = {}
    
    def get_document_url(self, doc: Dict) -> Optional[str]:
        """
        Get document URL, discovering it if not available
        """
        doc_id = doc.get('id')
        title = doc.get('title', '')
        organization = doc.get('author_organization', '')
        doc_type = doc.get('document_type', '')
        
        # Check if URL already exists and is valid
        existing_url = doc.get('source')
        if existing_url and existing_url.startswith('http') and existing_url != 'Link pending':
            return existing_url
        
        # Check cache first
        cache_key = f"{doc_id}_{hash(title)}"
        if cache_key in self._url_cache:
            return self._url_cache[cache_key]
        
        # Discover new URL
        try:
            discovered_url = self.url_discovery.discover_document_url(title, organization, doc_type)
            
            if discovered_url:
                # Update database with discovered URL
                self._update_document_url(doc_id, discovered_url)
                self._url_cache[cache_key] = discovered_url
                logger.info(f"Discovered and updated URL for doc {doc_id}: {discovered_url}")
                return discovered_url
            else:
                # Cache negative result to avoid repeated searches
                self._url_cache[cache_key] = None
                
        except Exception as e:
            logger.error(f"URL discovery failed for doc {doc_id}: {e}")
            self._url_cache[cache_key] = None
        
        return None
    
    def _update_document_url(self, doc_id: int, url: str):
        """Update document URL in database"""
        try:
            db_manager.update_document_metadata(doc_id, {
                'source': url,
                'url_valid': True,
                'url_status': 'active'
            })
        except Exception as e:
            logger.error(f"Failed to update URL for doc {doc_id}: {e}")
    
    def batch_discover_urls(self, docs: list) -> Dict[int, str]:
        """
        Batch discover URLs for multiple documents
        """
        discovered_urls = {}
        
        for doc in docs:
            doc_id = doc.get('id')
            if not doc.get('source') or doc.get('source') == 'Link pending':
                url = self.get_document_url(doc)
                if url:
                    discovered_urls[doc_id] = url
        
        return discovered_urls

# Global instance for reuse
auto_url_discovery = AutoURLDiscovery()