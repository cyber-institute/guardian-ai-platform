"""
Performance Cache for Document Scoring
Caches expensive scoring operations to improve page load times
"""

import streamlit as st
import hashlib
from typing import Dict, Any, Optional

class PerformanceCache:
    """Simple cache for expensive operations"""
    
    @staticmethod
    def get_cache_key(content: str, title: str) -> str:
        """Generate cache key from content and title"""
        content_hash = hashlib.md5((content + title).encode()).hexdigest()[:16]
        return f"scores_{content_hash}"
    
    @staticmethod
    def get_cached_scores(content: str, title: str) -> Optional[Dict[str, Any]]:
        """Get cached scores if available"""
        if 'score_cache' not in st.session_state:
            st.session_state.score_cache = {}
        
        cache_key = PerformanceCache.get_cache_key(content, title)
        return st.session_state.score_cache.get(cache_key)
    
    @staticmethod
    def cache_scores(content: str, title: str, scores: Dict[str, Any]) -> None:
        """Cache scores for future use"""
        if 'score_cache' not in st.session_state:
            st.session_state.score_cache = {}
        
        cache_key = PerformanceCache.get_cache_key(content, title)
        st.session_state.score_cache[cache_key] = scores
        
        # Limit cache size to prevent memory issues
        if len(st.session_state.score_cache) > 100:
            # Remove oldest entries (simple FIFO)
            keys = list(st.session_state.score_cache.keys())
            for key in keys[:20]:  # Remove 20 oldest
                del st.session_state.score_cache[key]

def get_cached_comprehensive_scores(content: str, title: str) -> Dict[str, Any]:
    """Get comprehensive scores with caching"""
    # Try cache first
    cached = PerformanceCache.get_cached_scores(content, title)
    if cached:
        return cached
    
    # Calculate scores if not cached
    from utils.comprehensive_scoring import comprehensive_document_scoring
    scores = comprehensive_document_scoring(content, title)
    
    # Cache the results
    PerformanceCache.cache_scores(content, title, scores)
    
    return scores

def clear_score_cache():
    """Clear the score cache"""
    if 'score_cache' in st.session_state:
        st.session_state.score_cache = {}