"""
Memory Management System for GUARDIAN
Optimizes memory usage for better performance
"""

import streamlit as st
import gc
import psutil
import os
from typing import Dict, Any

class MemoryManager:
    """Manages memory usage and optimization for GUARDIAN"""
    
    @staticmethod
    def cleanup_session_state():
        """Remove old session state entries to free memory"""
        keys_to_remove = []
        
        for key in st.session_state.keys():
            # Remove old cached scoring results
            if key.startswith('score_cache_') and len(st.session_state.keys()) > 100:
                keys_to_remove.append(key)
            
            # Remove old modal data
            if key.startswith('modal_doc_data_') and key not in st.session_state.get('active_modals', []):
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del st.session_state[key]
    
    @staticmethod
    def get_memory_usage():
        """Get current memory usage statistics"""
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        return {
            'rss': memory_info.rss / 1024 / 1024,  # MB
            'vms': memory_info.vms / 1024 / 1024,  # MB
            'percent': process.memory_percent()
        }
    
    @staticmethod
    def force_garbage_collection():
        """Force garbage collection to free memory"""
        gc.collect()
    
    @staticmethod
    def optimize_document_data(docs):
        """Optimize document data structure for memory efficiency"""
        optimized_docs = []
        
        for doc in docs:
            # Keep only essential fields for display
            optimized_doc = {
                'id': doc.get('id'),
                'title': doc.get('title', '')[:200],  # Truncate long titles
                'author_organization': doc.get('author_organization', '')[:100],
                'document_type': doc.get('document_type', ''),
                'publish_date': doc.get('publish_date', ''),
                'content_preview': doc.get('content_preview', '')[:300],  # Limit preview
                'url': doc.get('url', ''),
                # Keep scoring fields
                'ai_cybersecurity_score': doc.get('ai_cybersecurity_score'),
                'quantum_cybersecurity_score': doc.get('quantum_cybersecurity_score'),
                'ai_ethics_score': doc.get('ai_ethics_score'),
                'quantum_ethics_score': doc.get('quantum_ethics_score')
            }
            optimized_docs.append(optimized_doc)
        
        return optimized_docs

# Global memory manager instance
memory_manager = MemoryManager()