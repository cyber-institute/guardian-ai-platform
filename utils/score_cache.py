"""
Score Caching System for GUARDIAN
Caches computed scores to avoid expensive recalculation
"""

import streamlit as st
import json
import hashlib
from typing import Dict, Optional

class ScoreCache:
    """Manages cached scoring results for fast document loading"""
    
    def __init__(self):
        self.cache_key = "guardian_score_cache"
        self.metadata_key = "guardian_cache_metadata"
        
        # Initialize cache in session state if not exists
        if self.cache_key not in st.session_state:
            st.session_state[self.cache_key] = {}
        
        if self.metadata_key not in st.session_state:
            st.session_state[self.metadata_key] = {
                'last_refresh': None,
                'cache_hits': 0,
                'cache_misses': 0
            }
    
    def get_document_hash(self, doc_id: str, title: str, content_preview: str) -> str:
        """Generate unique hash for document to detect changes"""
        content = f"{doc_id}_{title}_{content_preview[:100]}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_cached_scores(self, doc_id: str, title: str, content_preview: str) -> Optional[Dict]:
        """Retrieve cached scores if available and valid"""
        doc_hash = self.get_document_hash(doc_id, title, content_preview)
        cache = st.session_state[self.cache_key]
        
        if doc_hash in cache:
            st.session_state[self.metadata_key]['cache_hits'] += 1
            return cache[doc_hash]['scores']
        
        st.session_state[self.metadata_key]['cache_misses'] += 1
        return None
    
    def cache_scores(self, doc_id: str, title: str, content_preview: str, scores: Dict):
        """Store computed scores in cache"""
        doc_hash = self.get_document_hash(doc_id, title, content_preview)
        
        st.session_state[self.cache_key][doc_hash] = {
            'doc_id': doc_id,
            'title': title[:50] + "..." if len(title) > 50 else title,
            'scores': scores,
            'cached_at': st.session_state.get('current_time', 'unknown')
        }
    
    def clear_cache(self):
        """Clear all cached scores"""
        st.session_state[self.cache_key] = {}
        st.session_state[self.metadata_key] = {
            'last_refresh': 'Manual refresh',
            'cache_hits': 0,
            'cache_misses': 0
        }
    
    def get_cache_stats(self) -> Dict:
        """Get cache performance statistics"""
        metadata = st.session_state[self.metadata_key]
        cache_size = len(st.session_state[self.cache_key])
        
        total_requests = metadata['cache_hits'] + metadata['cache_misses']
        hit_rate = (metadata['cache_hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cached_documents': cache_size,
            'cache_hits': metadata['cache_hits'],
            'cache_misses': metadata['cache_misses'],
            'hit_rate': round(hit_rate, 1),
            'last_refresh': metadata['last_refresh']
        }

# Global score cache instance
score_cache = ScoreCache()