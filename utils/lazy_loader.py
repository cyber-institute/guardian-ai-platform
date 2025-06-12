"""
Lazy Loading System for GUARDIAN
Implements progressive loading to improve initial page response times
"""

import streamlit as st
from typing import Callable, Any, Dict, Optional
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class LazyLoader:
    """Progressive content loading system"""
    
    def __init__(self):
        self.load_queue = {}
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    def lazy_load_component(self, component_key: str, loader_func: Callable, placeholder_text: str = "Loading..."):
        """Load component lazily with placeholder"""
        
        # Check if already loaded
        if f"loaded_{component_key}" in st.session_state:
            return st.session_state[f"loaded_{component_key}"]
        
        # Show placeholder while loading
        placeholder = st.empty()
        
        # Check if loading is in progress
        if f"loading_{component_key}" not in st.session_state:
            st.session_state[f"loading_{component_key}"] = True
            
            # Start background loading
            future = self.executor.submit(loader_func)
            st.session_state[f"future_{component_key}"] = future
            
            with placeholder.container():
                st.info(f"🔄 {placeholder_text}")
                if st.button(f"Refresh {component_key}", key=f"refresh_{component_key}"):
                    st.rerun()
        
        # Check if loading is complete
        future_key = f"future_{component_key}"
        if future_key in st.session_state:
            future = st.session_state[future_key]
            
            if future.done():
                try:
                    result = future.result()
                    st.session_state[f"loaded_{component_key}"] = result
                    st.session_state[f"loading_{component_key}"] = False
                    del st.session_state[future_key]
                    
                    placeholder.empty()
                    return result
                    
                except Exception as e:
                    placeholder.error(f"Failed to load {component_key}: {str(e)}")
                    st.session_state[f"loading_{component_key}"] = False
                    del st.session_state[future_key]
                    return None
            else:
                with placeholder.container():
                    st.info(f"⚡ Loading {component_key}...")
                    if st.button(f"Cancel Loading", key=f"cancel_{component_key}"):
                        future.cancel()
                        st.session_state[f"loading_{component_key}"] = False
                        if future_key in st.session_state:
                            del st.session_state[future_key]
                        st.rerun()
        
        return None
    
    def load_with_progress(self, component_key: str, loader_func: Callable, steps: list):
        """Load component with progress indicator"""
        
        if f"loaded_{component_key}" in st.session_state:
            return st.session_state[f"loaded_{component_key}"]
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        def progress_loader():
            result = None
            for i, step in enumerate(steps):
                progress = (i + 1) / len(steps)
                progress_bar.progress(progress)
                status_text.text(f"Step {i+1}/{len(steps)}: {step}")
                time.sleep(0.1)  # Brief pause for visual feedback
                
                if i == len(steps) - 1:  # Last step
                    result = loader_func()
            
            return result
        
        if f"loading_{component_key}" not in st.session_state:
            st.session_state[f"loading_{component_key}"] = True
            
            try:
                result = progress_loader()
                st.session_state[f"loaded_{component_key}"] = result
                st.session_state[f"loading_{component_key}"] = False
                
                progress_bar.empty()
                status_text.empty()
                
                return result
                
            except Exception as e:
                st.error(f"Loading failed: {str(e)}")
                st.session_state[f"loading_{component_key}"] = False
                return None
        
        return None
    
    def preload_critical_data(self):
        """Preload critical data in background"""
        critical_loaders = {
            'document_count': self._load_document_count,
            'recent_documents': self._load_recent_documents,
            'system_status': self._load_system_status
        }
        
        for key, loader in critical_loaders.items():
            if f"preloaded_{key}" not in st.session_state:
                future = self.executor.submit(loader)
                st.session_state[f"preload_future_{key}"] = future
                st.session_state[f"preloaded_{key}"] = True
    
    def _load_document_count(self):
        """Load basic document count"""
        try:
            from .optimized_database import db
            analytics = db.get_analytics_summary()
            return analytics.get('total_documents', 0)
        except:
            return 0
    
    def _load_recent_documents(self):
        """Load recent documents"""
        try:
            from .optimized_database import db
            return db.get_documents_optimized(limit=10)
        except:
            return []
    
    def _load_system_status(self):
        """Load system status"""
        return {
            'database': 'connected',
            'cache': 'active',
            'status': 'operational'
        }
    
    def get_preloaded_data(self, key: str):
        """Get preloaded data if available"""
        future_key = f"preload_future_{key}"
        if future_key in st.session_state:
            future = st.session_state[future_key]
            if future.done():
                try:
                    result = future.result()
                    del st.session_state[future_key]
                    return result
                except:
                    del st.session_state[future_key]
                    return None
        return None

# Global lazy loader instance
lazy_loader = LazyLoader()