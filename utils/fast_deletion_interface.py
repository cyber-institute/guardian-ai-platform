"""
Fast Deletion Interface for Repository Admin
Optimizes checkbox selection and document loading for large datasets
"""

import streamlit as st
from typing import List, Dict, Any
import time

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_documents_summary():
    """Get summary of documents for fast selection interface"""
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        documents = db_manager.execute_query("""
            SELECT 
                id, 
                title, 
                document_type, 
                created_at::date as date_created,
                CASE 
                    WHEN LENGTH(text_content) > 0 THEN 'Has Content'
                    ELSE 'Empty'
                END as content_status
            FROM documents 
            ORDER BY created_at DESC
            LIMIT 500
        """)
        
        return documents if isinstance(documents, list) else []
        
    except Exception as e:
        st.error(f"Error loading documents: {e}")
        return []

def render_fast_deletion_interface():
    """Render optimized deletion interface with minimal UI updates"""
    
    st.markdown("#### Individual Document Deletion")
    
    # Get documents once
    all_documents = get_documents_summary()
    
    if not all_documents:
        st.info("No documents found in database")
        return
    
    # Show document count
    st.info(f"Found {len(all_documents)} documents")
    
    # Quick filters to reduce selection set
    col1, col2 = st.columns(2)
    
    with col1:
        # Filter by document type
        doc_types = list(set([doc.get('document_type', 'Unknown') for doc in all_documents]))
        selected_type = st.selectbox("Filter by Type:", ["All"] + doc_types, key="type_filter")
    
    with col2:
        # Filter by content status
        content_filter = st.selectbox("Filter by Content:", ["All", "Has Content", "Empty"], key="content_filter")
    
    # Apply filters
    filtered_docs = all_documents
    if selected_type != "All":
        filtered_docs = [doc for doc in filtered_docs if doc.get('document_type') == selected_type]
    if content_filter != "All":
        filtered_docs = [doc for doc in filtered_docs if doc.get('content_status') == content_filter]
    
    st.info(f"Showing {len(filtered_docs)} documents after filtering")
    
    if not filtered_docs:
        st.warning("No documents match the current filters")
        return
    
    # Batch selection options
    st.markdown("**Quick Selection:**")
    col1, col2, col3 = st.columns(3)
    
    selected_docs = []
    
    with col1:
        if st.button("Select First 10", key="select_10"):
            selected_docs = [doc['id'] for doc in filtered_docs[:10]]
            st.session_state['bulk_selected'] = selected_docs
    
    with col2:
        if st.button("Select First 20", key="select_20"):
            selected_docs = [doc['id'] for doc in filtered_docs[:20]]
            st.session_state['bulk_selected'] = selected_docs
    
    with col3:
        if st.button("Clear Selection", key="clear_selection"):
            st.session_state['bulk_selected'] = []
            selected_docs = []
    
    # Get current selection
    if 'bulk_selected' not in st.session_state:
        st.session_state['bulk_selected'] = []
    
    selected_docs = st.session_state.get('bulk_selected', [])
    
    # Show selected count
    if selected_docs:
        st.success(f"Selected {len(selected_docs)} documents for deletion")
    
    # Individual document selection with pagination
    st.markdown("**Individual Selection:**")
    
    # Pagination
    docs_per_page = 20
    total_pages = (len(filtered_docs) + docs_per_page - 1) // docs_per_page
    
    if total_pages > 1:
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1, key="doc_page")
        start_idx = (page - 1) * docs_per_page
        end_idx = start_idx + docs_per_page
        page_docs = filtered_docs[start_idx:end_idx]
        st.info(f"Page {page} of {total_pages}")
    else:
        page_docs = filtered_docs
    
    # Document selection checkboxes
    for doc in page_docs:
        doc_id = doc['id']
        title = doc.get('title', 'Untitled')[:60] + "..." if len(doc.get('title', '')) > 60 else doc.get('title', 'Untitled')
        doc_type = doc.get('document_type', 'Unknown')
        date_created = doc.get('date_created', 'Unknown')
        
        # Simple checkbox without heavy session state
        is_selected = doc_id in selected_docs
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.checkbox("", key=f"doc_select_{doc_id}", value=is_selected):
                if doc_id not in st.session_state['bulk_selected']:
                    st.session_state['bulk_selected'].append(doc_id)
            else:
                if doc_id in st.session_state['bulk_selected']:
                    st.session_state['bulk_selected'].remove(doc_id)
        
        with col2:
            st.markdown(f"**{title}** | {doc_type} | {date_created}")
    
    # Deletion actions
    current_selected = st.session_state.get('bulk_selected', [])
    
    if current_selected:
        st.markdown("---")
        st.warning(f"Ready to delete {len(current_selected)} documents")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Delete Selected Documents", type="primary", key="confirm_bulk_delete"):
                # Perform deletion
                with st.spinner("Deleting documents..."):
                    from utils.optimized_deletions_fixed import batch_delete_documents
                    result = batch_delete_documents(current_selected)
                
                if result['success']:
                    st.success(f"Successfully deleted {result['deleted_count']} documents in {result.get('execution_time', 0):.2f} seconds")
                    st.session_state['bulk_selected'] = []
                    st.cache_data.clear()  # Clear cache to show updated counts
                    st.rerun()
                else:
                    st.error(f"Deletion failed: {'; '.join(result['errors'])}")
        
        with col2:
            if st.button("❌ Cancel", key="cancel_bulk_delete"):
                st.session_state['bulk_selected'] = []
                st.rerun()
    
    else:
        st.info("Select documents using the checkboxes to enable deletion")

def render_optimized_document_management():
    """Render optimized document management interface"""
    
    st.markdown("### Document Ingestion & Upload Management")
    
    from components.document_uploader import render_document_uploader, render_bulk_upload
    from utils.admin_performance_cache import render_optimized_system_metrics
    
    # Document upload interface
    st.markdown("#### Single Document Upload")
    render_document_uploader()
    
    st.markdown("---")
    
    # Bulk upload interface
    st.markdown("#### Bulk Document Upload")
    render_bulk_upload()
    
    st.markdown("---")
    
    # Quick bulk deletion with criteria
    with st.expander("⚡ Quick Bulk Deletion", expanded=False):
        st.markdown("**Delete multiple documents by criteria (faster than individual selection)**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Get document types for filtering
            try:
                from utils.admin_performance_cache import get_document_types
                doc_types_data = get_document_types()
                doc_types = [row['document_type'] for row in doc_types_data if row.get('document_type')]
            except:
                doc_types = []
            
            bulk_doc_type = st.selectbox("Delete by Document Type", ["None"] + doc_types, key="bulk_type")
            
        with col2:
            bulk_before_date = st.date_input("Delete documents created before", key="bulk_date")
        
        delete_empty = st.checkbox("Delete documents with empty content", key="bulk_empty")
        
        if st.button("🗑️ Execute Bulk Deletion", type="secondary", key="bulk_delete_btn"):
            criteria = {}
            if bulk_doc_type != "None":
                criteria['document_type'] = bulk_doc_type
            if bulk_before_date:
                criteria['before_date'] = bulk_before_date
            if delete_empty:
                criteria['content_empty'] = True
            
            if criteria:
                with st.spinner("Executing bulk deletion..."):
                    from utils.optimized_deletions_fixed import bulk_delete_by_criteria
                    result = bulk_delete_by_criteria(criteria)
                
                if result['success']:
                    st.success(f"Bulk deletion completed: {result['deleted_count']} documents deleted")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Bulk deletion failed: {'; '.join(result['errors'])}")
            else:
                st.warning("Please select at least one deletion criterion")
    
    st.markdown("---")
    
    # Fast deletion interface
    render_fast_deletion_interface()
    
    st.markdown("---")
    
    # System metrics
    render_optimized_system_metrics()