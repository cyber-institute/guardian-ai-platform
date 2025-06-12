"""
Optimized Bulk Deletion Operations for GUARDIAN - Fixed Version
Implements batch deletions using the existing DatabaseManager
"""

import streamlit as st
from typing import List, Dict, Any
import time

@st.cache_data(ttl=60)  # Cache for 1 minute
def get_documents_for_deletion():
    """Cached retrieval of documents for deletion interface"""
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        # Use the execute_query method
        documents = db_manager.execute_query("""
            SELECT id, title, document_type, created_at, source, 
                   COALESCE(CHAR_LENGTH(text_content), 0) as content_length
            FROM documents 
            ORDER BY created_at DESC
            LIMIT 1000
        """)
        
        if isinstance(documents, list):
            return documents
        else:
            return []
            
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        return []

def batch_delete_documents(document_ids: List[int]) -> Dict[str, Any]:
    """
    Optimized batch deletion of documents using DatabaseManager
    Returns: {'success': bool, 'deleted_count': int, 'errors': List[str]}
    """
    if not document_ids:
        return {'success': False, 'deleted_count': 0, 'errors': ['No documents selected']}
    
    start_time = time.time()
    errors = []
    
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        deleted_count = 0
        
        # Delete documents one by one using the DatabaseManager
        for doc_id in document_ids:
            try:
                result = db_manager.execute_query(f"DELETE FROM documents WHERE id = {doc_id}")
                if isinstance(result, int) and result > 0:
                    deleted_count += 1
            except Exception as e:
                errors.append(f"Failed to delete document {doc_id}: {str(e)}")
        
        # Clear caches
        st.cache_data.clear()
        
        execution_time = time.time() - start_time
        
        return {
            'success': True,
            'deleted_count': deleted_count,
            'errors': errors,
            'execution_time': execution_time
        }
        
    except Exception as e:
        errors.append(f"Database error: {str(e)}")
        
        return {
            'success': False,
            'deleted_count': 0,
            'errors': errors,
            'execution_time': time.time() - start_time
        }

def bulk_delete_by_criteria(criteria: Dict[str, Any]) -> Dict[str, Any]:
    """
    Delete documents based on criteria using DatabaseManager
    """
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        # Build WHERE clause based on criteria
        where_clauses = []
        
        if criteria.get('document_type'):
            where_clauses.append(f"document_type = '{criteria['document_type']}'")
        
        if criteria.get('before_date'):
            where_clauses.append(f"created_at < '{criteria['before_date']}'")
        
        if criteria.get('content_empty'):
            where_clauses.append("(text_content IS NULL OR text_content = '')")
        
        if not where_clauses:
            return {'success': False, 'deleted_count': 0, 'errors': ['No criteria specified']}
        
        # Execute deletion
        where_clause = " AND ".join(where_clauses)
        query = f"DELETE FROM documents WHERE {where_clause}"
        
        result = db_manager.execute_query(query)
        deleted_count = result if isinstance(result, int) else 0
        
        # Clear caches
        st.cache_data.clear()
        
        return {
            'success': True,
            'deleted_count': deleted_count,
            'errors': []
        }
        
    except Exception as e:
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
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        # Create IN clause for multiple IDs
        ids_str = ','.join(map(str, document_ids))
        query = f"""
            SELECT id, title, document_type, created_at
            FROM documents 
            WHERE id IN ({ids_str})
            ORDER BY created_at DESC
        """
        
        documents = db_manager.execute_query(query)
        
        if isinstance(documents, list):
            return documents
        else:
            return []
        
    except Exception as e:
        st.error(f"Error loading deletion preview: {e}")
        return []