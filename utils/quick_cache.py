"""
Simple caching system for immediate performance improvement
"""

import streamlit as st
import time
from typing import Any, Optional

def cache_with_ttl(key: str, ttl_seconds: int = 300):
    """Simple caching decorator with TTL"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache_key = f"{key}_{hash(str(args) + str(kwargs))}"
            
            # Check cache
            if cache_key in st.session_state:
                cached_data = st.session_state[cache_key]
                if time.time() - cached_data['timestamp'] < ttl_seconds:
                    return cached_data['data']
            
            # Execute and cache
            result = func(*args, **kwargs)
            st.session_state[cache_key] = {
                'data': result,
                'timestamp': time.time()
            }
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached data"""
    keys_to_remove = [k for k in st.session_state.keys() if 'timestamp' in str(st.session_state.get(k, {}))]
    for key in keys_to_remove:
        del st.session_state[key]