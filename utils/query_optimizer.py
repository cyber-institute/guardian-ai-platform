"""
Database Query Optimization for GUARDIAN
Optimizes database queries for better performance
"""

import streamlit as st
from typing import Dict, List, Optional
import time

class QueryOptimizer:
    """Optimizes database queries and caching strategies"""
    
    @staticmethod
    @st.cache_data(ttl=1800, max_entries=50)  # 30 minutes
    def get_documents_batch(limit: int = 50, offset: int = 0):
        """Optimized batch document loading with minimal fields"""
        try:
            from utils.database import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Optimized query with only essential fields for listing
            query = """
                SELECT id, title, author_organization, document_type, 
                       publish_date, content_preview, url,
                       ai_cybersecurity_score, quantum_cybersecurity_score,
                       ai_ethics_score, quantum_ethics_score
                FROM documents 
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, (limit, offset))
            results = cursor.fetchall()
            
            documents = []
            for row in results:
                doc = {
                    'id': row[0],
                    'title': row[1] or 'Untitled Document',
                    'author_organization': row[2] or 'Unknown',
                    'document_type': row[3] or 'Document',
                    'publish_date': row[4],
                    'content_preview': row[5] or 'No preview available',
                    'url': row[6],
                    'ai_cybersecurity_score': row[7],
                    'quantum_cybersecurity_score': row[8], 
                    'ai_ethics_score': row[9],
                    'quantum_ethics_score': row[10]
                }
                documents.append(doc)
            
            return documents
            
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return []
    
    @staticmethod
    @st.cache_data(ttl=3600, max_entries=100)  # 1 hour
    def get_document_content(doc_id: str):
        """Load full document content only when needed"""
        try:
            from utils.database import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT content FROM documents WHERE id = %s", (doc_id,))
            result = cursor.fetchone()
            return result[0] if result else ""
            
        except Exception:
            return ""
    
    @staticmethod
    @st.cache_data(ttl=7200)  # 2 hours
    def get_repository_stats():
        """Cache repository statistics for dashboard"""
        try:
            from utils.database import get_db_connection
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Single query for all stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_docs,
                    AVG(ai_cybersecurity_score) as avg_ai_cyber,
                    AVG(quantum_cybersecurity_score) as avg_q_cyber,
                    AVG(ai_ethics_score) as avg_ai_ethics,
                    AVG(quantum_ethics_score) as avg_q_ethics,
                    COUNT(DISTINCT document_type) as doc_types
                FROM documents
                WHERE ai_cybersecurity_score IS NOT NULL
            """)
            
            result = cursor.fetchone()
            if result:
                return {
                    'total_documents': result[0],
                    'avg_ai_cybersecurity': round(result[1] or 0, 1),
                    'avg_quantum_cybersecurity': round(result[2] or 0, 1),
                    'avg_ai_ethics': round(result[3] or 0, 1),
                    'avg_quantum_ethics': round(result[4] or 0, 1),
                    'document_types': result[5]
                }
            return {}
            
        except Exception:
            return {}
    
    @staticmethod
    def optimize_session_queries():
        """Optimize queries based on session patterns"""
        # Track frequently accessed documents
        if 'frequent_docs' not in st.session_state:
            st.session_state.frequent_docs = {}
        
        # Preload popular documents
        popular_threshold = 3
        for doc_id, access_count in st.session_state.frequent_docs.items():
            if access_count >= popular_threshold:
                QueryOptimizer.get_document_content(doc_id)

# Global query optimizer
query_optimizer = QueryOptimizer()