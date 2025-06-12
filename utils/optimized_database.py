"""
Optimized Database Operations for GUARDIAN
Implements connection pooling, query optimization, and batch operations
"""

import psycopg2
from psycopg2 import pool
import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
import logging
from .performance_cache import cache

logger = logging.getLogger(__name__)

class OptimizedDatabase:
    """High-performance database operations with connection pooling"""
    
    def __init__(self):
        self._connection_pool = None
        self.pool_size = 5
        self.max_connections = 20
    
    def get_connection_pool(self):
        """Get or create connection pool"""
        if self._connection_pool is None:
            try:
                import os
                database_url = os.getenv('DATABASE_URL')
                if not database_url:
                    raise ValueError("DATABASE_URL not found")
                
                self._connection_pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=self.pool_size,
                    dsn=database_url,
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
                logger.info("Database connection pool created")
                
            except Exception as e:
                logger.error(f"Failed to create connection pool: {e}")
                # Fallback to single connection
                return self.get_single_connection()
        
        return self._connection_pool
    
    def get_single_connection(self):
        """Fallback single connection method"""
        import os
        database_url = os.getenv('DATABASE_URL')
        conn = psycopg2.connect(database_url, cursor_factory=psycopg2.extras.RealDictCursor)
        return conn
    
    def get_connection(self):
        """Get database connection from pool or single connection"""
        pool = self.get_connection_pool()
        if hasattr(pool, 'getconn'):
            return pool.getconn()
        else:
            return pool
    
    def return_connection(self, conn):
        """Return connection to pool"""
        pool = self.get_connection_pool()
        if hasattr(pool, 'putconn'):
            pool.putconn(conn)
        else:
            conn.close()
    
    @cache.cache_function('documents', ttl=300)
    def get_documents_optimized(self, limit: int = 100, offset: int = 0, filters: Optional[Dict] = None) -> List[Dict]:
        """Optimized document retrieval with pagination and filtering"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Build optimized query with selective columns
            base_query = """
            SELECT id, title, url, content_type, ai_cybersecurity_score, 
                   quantum_cybersecurity_score, ai_ethics_score, quantum_ethics_score,
                   created_at, detected_region, summary
            FROM documents
            """
            
            where_clauses = []
            params = []
            
            if filters:
                if filters.get('content_type'):
                    where_clauses.append("content_type = %s")
                    params.append(filters['content_type'])
                
                if filters.get('min_ai_score'):
                    where_clauses.append("ai_cybersecurity_score >= %s")
                    params.append(filters['min_ai_score'])
                
                if filters.get('region'):
                    where_clauses.append("detected_region = %s")
                    params.append(filters['region'])
            
            if where_clauses:
                base_query += " WHERE " + " AND ".join(where_clauses)
            
            base_query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(base_query, params)
            documents = cursor.fetchall()
            
            cursor.close()
            return [dict(doc) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error in get_documents_optimized: {e}")
            return []
        finally:
            if conn:
                self.return_connection(conn)
    
    @cache.cache_function('analytics', ttl=600)
    def get_analytics_summary(self) -> Dict[str, Any]:
        """Get optimized analytics summary"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Single query for all analytics
            cursor.execute("""
            SELECT 
                COUNT(*) as total_documents,
                COUNT(CASE WHEN ai_cybersecurity_score > 0 THEN 1 END) as ai_cyber_scored,
                COUNT(CASE WHEN quantum_cybersecurity_score > 0 THEN 1 END) as quantum_cyber_scored,
                COUNT(CASE WHEN ai_ethics_score > 0 THEN 1 END) as ai_ethics_scored,
                COUNT(CASE WHEN quantum_ethics_score > 0 THEN 1 END) as quantum_ethics_scored,
                AVG(NULLIF(ai_cybersecurity_score, 0)) as avg_ai_cyber,
                AVG(NULLIF(quantum_cybersecurity_score, 0)) as avg_quantum_cyber,
                AVG(NULLIF(ai_ethics_score, 0)) as avg_ai_ethics,
                AVG(NULLIF(quantum_ethics_score, 0)) as avg_quantum_ethics,
                COUNT(DISTINCT content_type) as content_types,
                COUNT(DISTINCT detected_region) as regions
            FROM documents
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            return dict(result) if result else {}
            
        except Exception as e:
            logger.error(f"Error in get_analytics_summary: {e}")
            return {}
        finally:
            if conn:
                self.return_connection(conn)
    
    @cache.cache_function('metadata', ttl=900)  
    def get_content_types(self) -> List[str]:
        """Get unique content types"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT DISTINCT content_type FROM documents WHERE content_type IS NOT NULL ORDER BY content_type")
            results = cursor.fetchall()
            cursor.close()
            
            return [row['content_type'] for row in results]
            
        except Exception as e:
            logger.error(f"Error in get_content_types: {e}")
            return []
        finally:
            if conn:
                self.return_connection(conn)
    
    @cache.cache_function('metadata', ttl=900)
    def get_regions(self) -> List[str]:
        """Get unique regions"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT DISTINCT detected_region FROM documents WHERE detected_region IS NOT NULL ORDER BY detected_region")
            results = cursor.fetchall()
            cursor.close()
            
            return [row['detected_region'] for row in results]
            
        except Exception as e:
            logger.error(f"Error in get_regions: {e}")
            return []
        finally:
            if conn:
                self.return_connection(conn)
    
    def batch_update_scores(self, updates: List[Tuple[int, Dict[str, Any]]]) -> bool:
        """Batch update document scores"""
        if not updates:
            return True
            
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Clear relevant cache
            cache.clear_cache('documents')
            cache.clear_cache('analytics')
            
            for doc_id, scores in updates:
                update_fields = []
                params = []
                
                for field, value in scores.items():
                    if value is not None:
                        update_fields.append(f"{field} = %s")
                        params.append(value)
                
                if update_fields:
                    query = f"UPDATE documents SET {', '.join(update_fields)} WHERE id = %s"
                    params.append(doc_id)
                    cursor.execute(query, params)
            
            conn.commit()
            cursor.close()
            return True
            
        except Exception as e:
            logger.error(f"Error in batch_update_scores: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                self.return_connection(conn)

# Global optimized database instance
db = OptimizedDatabase()