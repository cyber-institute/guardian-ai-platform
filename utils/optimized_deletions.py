"""
Optimized Bulk Deletion Operations for GUARDIAN
Implements batch deletions and efficient database operations
"""

import streamlit as st
from typing import List, Dict, Any
import time

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_documents_for_deletion():
    """Cached retrieval of documents for deletion interface"""
    try:
        from utils.database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, document_type, created_at, source, 
                   COALESCE(CHAR_LENGTH(text_content), 0) as content_length
            FROM documents 
            ORDER BY created_at DESC
            LIMIT 1000
        """)
        
        documents = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(doc) for doc in documents]
        
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        return []

def batch_delete_documents(document_ids: List[int]) -> Dict[str, Any]:
    """
    Optimized batch deletion of documents
    Returns: {'success': bool, 'deleted_count': int, 'errors': List[str]}
    """
    if not document_ids:
        return {'success': False, 'deleted_count': 0, 'errors': ['No documents selected']}
    
    start_time = time.time()
    deleted_count = 0
    errors = []
    
    try:
        from utils.database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Start transaction for atomic operation
        conn.autocommit = False
        
        # Create parameterized query for batch deletion
        if len(document_ids) == 1:
            # Single document deletion
            cursor.execute("DELETE FROM documents WHERE id = %s", (document_ids[0],))
        else:
            # Batch deletion using IN clause
            placeholders = ','.join(['%s'] * len(document_ids))
            query = f"DELETE FROM documents WHERE id IN ({placeholders})"
            cursor.execute(query, document_ids)
        
        deleted_count = cursor.rowcount
        
        # Commit the transaction
        conn.commit()
        cursor.close()
        conn.close()
        
        # Clear caches
        st.cache_data.clear()
        
        execution_time = time.time() - start_time
        
        return {
            'success': True,
            'deleted_count': deleted_count,
            'errors': [],
            'execution_time': execution_time
        }
        
    except Exception as e:
        errors.append(f"Database error: {str(e)}")
        try:
            if 'conn' in locals():
                conn.rollback()
                conn.close()
        except:
            pass
        
        return {
            'success': False,
            'deleted_count': 0,
            'errors': errors,
            'execution_time': time.time() - start_time
        }

def bulk_delete_by_criteria(criteria: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete documents based on criteria (type, date range, etc.)
    More efficient than individual selections for large datasets
    """
    try:
        from utils.database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build WHERE clause based on criteria
        where_clauses = []
        params = []
        
        if criteria.get('document_type'):
            where_clauses.append("document_type = %s")
            params.append(criteria['document_type'])
        
        if criteria.get('before_date'):
            where_clauses.append("created_at < %s")
            params.append(criteria['before_date'])
        
        if criteria.get('content_empty'):
            where_clauses.append("(text_content IS NULL OR text_content = '')")
        
        if not where_clauses:
            return {'success': False, 'deleted_count': 0, 'errors': ['No criteria specified']}
        
        # Start transaction
        conn.autocommit = False
        
        # Execute deletion
        where_clause = " AND ".join(where_clauses)
        query = f"DELETE FROM documents WHERE {where_clause}"
        
        cursor.execute(query, params)
        deleted_count = cursor.rowcount
        
        conn.commit()
        cursor.close()
        conn.close()
        
        # Clear caches
        st.cache_data.clear()
        
        return {
            'success': True,
            'deleted_count': deleted_count,
            'errors': []
        }
        
    except Exception as e:
        try:
            if 'conn' in locals():
                conn.rollback()
                conn.close()
        except:
            pass
        
        return {
            'success': False,
            'deleted_count': 0,
            'errors': [f"Bulk deletion error: {str(e)}"]
        }

def get_deletion_preview(document_ids: List[int]) -> List[Dict[str, Any]]:
    """Get preview of documents to be deleted"""
    if not document_ids:
        return []
    
    try:
        from utils.database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        placeholders = ','.join(['%s'] * len(document_ids))
        query = f"""
            SELECT id, title, document_type, created_at
            FROM documents 
            WHERE id IN ({placeholders})
            ORDER BY created_at DESC
        """
        
        cursor.execute(query, document_ids)
        documents = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return [dict(doc) for doc in documents]
        
    except Exception as e:
        st.error(f"Error loading deletion preview: {e}")
        return []