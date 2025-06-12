"""
Cache Refresh Utilities for GUARDIAN
Provides functions to refresh cached data after database updates
"""

import streamlit as st

def refresh_all_caches():
    """Clear all Streamlit caches to ensure fresh data display"""
    try:
        # Clear all cached data
        st.cache_data.clear()
        
        # Clear any cached resources
        if hasattr(st, 'cache_resource'):
            st.cache_resource.clear()
        
        return True
    except Exception as e:
        print(f"Cache refresh error: {e}")
        return False

def refresh_document_caches():
    """Clear document-related caches specifically"""
    try:
        # Import functions that have caches to clear them specifically
        from all_docs_tab import fetch_documents_cached
        from utils.optimized_deletions import get_documents_for_deletion
        
        # Clear specific function caches
        fetch_documents_cached.clear()
        get_documents_for_deletion.clear()
        
        return True
    except Exception as e:
        print(f"Document cache refresh error: {e}")
        return False