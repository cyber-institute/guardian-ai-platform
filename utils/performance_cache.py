"""
Performance Caching System for GUARDIAN
Implements intelligent caching to reduce database load and improve response times
"""

import streamlit as st
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import functools
import time

class PerformanceCache:
    """High-performance caching system for GUARDIAN"""
    
    def __init__(self):
        self.cache_ttl = {
            'documents': 300,  # 5 minutes
            'scores': 600,     # 10 minutes
            'analytics': 900,  # 15 minutes
            'metadata': 1800   # 30 minutes
        }
    
    @staticmethod
    def get_cache_key(prefix: str, *args, **kwargs) -> str:
        """Generate cache key from function arguments"""
        key_data = {
            'args': args,
            'kwargs': kwargs,
            'timestamp': int(time.time() / 300)  # 5-minute buckets
        }
        key_string = f"{prefix}_{json.dumps(key_data, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def cache_function(self, cache_type: str = 'documents', ttl: Optional[int] = None):
        """Decorator for caching function results"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self.get_cache_key(func.__name__, *args, **kwargs)
                
                # Check if cached result exists and is valid
                if cache_key in st.session_state:
                    cached_data = st.session_state[cache_key]
                    if cached_data.get('expires_at', 0) > time.time():
                        return cached_data['data']
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                
                expiry_time = time.time() + (ttl or self.cache_ttl.get(cache_type, 300))
                st.session_state[cache_key] = {
                    'data': result,
                    'expires_at': expiry_time,
                    'created_at': time.time()
                }
                
                return result
            return wrapper
        return decorator
    
    def clear_cache(self, pattern: Optional[str] = None):
        """Clear cache entries matching pattern"""
        if pattern:
            keys_to_remove = [k for k in st.session_state.keys() if pattern in k]
        else:
            keys_to_remove = [k for k in st.session_state.keys() if isinstance(st.session_state[k], dict) and 'expires_at' in st.session_state[k]]
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        cache_entries = [v for v in st.session_state.values() if isinstance(v, dict) and 'expires_at' in v]
        
        return {
            'total_entries': len(cache_entries),
            'expired_entries': sum(1 for entry in cache_entries if entry['expires_at'] < time.time()),
            'cache_size_mb': sum(len(str(entry)) for entry in cache_entries) / (1024 * 1024)
        }

# Global cache instance
cache = PerformanceCache()