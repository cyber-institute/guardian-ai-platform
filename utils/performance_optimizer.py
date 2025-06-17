"""
Performance Optimization Module for GUARDIAN
Multiple strategies to improve speed without losing capabilities
"""

import streamlit as st
from typing import Dict, List, Any
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor

class PerformanceOptimizer:
    """Comprehensive performance optimization for GUARDIAN"""
    
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.cache_stats = {}
    
    @staticmethod
    @st.cache_data(ttl=1800, max_entries=1000)  # 30 minutes, 1000 entries
    def cache_document_metadata(doc_id, title, author, organization):
        """Cache document metadata separately from content"""
        return {
            'id': doc_id,
            'title': title,
            'author': author,
            'organization': organization
        }
    
    @staticmethod
    @st.cache_data(ttl=3600, max_entries=500)  # 1 hour for analysis results
    def cache_synthesis_results(content_hash, title_hash):
        """Cache synthesis results with content hash for faster retrieval"""
        return None  # Placeholder - will be populated by synthesis engine
    
    @staticmethod
    def optimize_database_queries():
        """Optimize database connection and query patterns"""
        return {
            'batch_size': 50,
            'connection_pool_size': 5,
            'query_timeout': 30,
            'use_prepared_statements': True
        }
    
    @staticmethod
    def preload_critical_data():
        """Preload frequently accessed data in session state"""
        if 'preloaded_docs' not in st.session_state:
            st.session_state.preloaded_docs = True
            # Trigger background loading of most recent documents
    
    def parallel_score_calculation(self, documents: List[Dict]) -> List[Dict]:
        """Calculate scores for multiple documents in parallel"""
        futures = []
        
        for doc in documents:
            future = self.executor.submit(
                self._calculate_single_score, 
                doc.get('content', ''), 
                doc.get('title', '')
            )
            futures.append((doc, future))
        
        results = []
        for doc, future in futures:
            try:
                scores = future.result(timeout=10)  # 10 second timeout per document
                doc['scores'] = scores
                results.append(doc)
            except Exception as e:
                # Keep document but mark scoring as failed
                doc['scores'] = {'error': str(e)}
                results.append(doc)
        
        return results
    
    def _calculate_single_score(self, content: str, title: str) -> Dict:
        """Calculate score for a single document"""
        try:
            from utils.comprehensive_scoring import multi_llm_intelligent_scoring
            return multi_llm_intelligent_scoring(content, title)
        except Exception as e:
            return {'error': str(e)}

# Global optimizer instance
performance_optimizer = PerformanceOptimizer()