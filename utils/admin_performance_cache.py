"""
Performance Caching for Repository Admin Section
Optimizes database queries and UI loading for administrative functions
"""

import streamlit as st
from typing import Dict, List, Any
from datetime import datetime, timedelta

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_system_metrics():
    """Cached system metrics for admin dashboard"""
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        metrics = {}
        
        # Document counts
        total_docs = db_manager.execute_query("SELECT COUNT(*) as count FROM documents")
        metrics['total_documents'] = total_docs[0]['count'] if total_docs and isinstance(total_docs, list) else 0
        
        # Today's documents
        today_docs = db_manager.execute_query("""
            SELECT COUNT(*) as count FROM documents 
            WHERE created_at >= CURRENT_DATE
        """)
        metrics['today_documents'] = today_docs[0]['count'] if today_docs and isinstance(today_docs, list) else 0
        
        # This week's documents
        week_docs = db_manager.execute_query("""
            SELECT COUNT(*) as count FROM documents 
            WHERE created_at >= NOW() - INTERVAL '7 days'
        """)
        metrics['week_documents'] = week_docs[0]['count'] if week_docs and isinstance(week_docs, list) else 0
        
        # Scored documents
        scored_docs = db_manager.execute_query("""
            SELECT COUNT(*) as count FROM documents 
            WHERE ai_cybersecurity_score IS NOT NULL 
            OR quantum_cybersecurity_score IS NOT NULL 
            OR ai_ethics_score IS NOT NULL 
            OR quantum_ethics_score IS NOT NULL
        """)
        metrics['scored_documents'] = scored_docs[0]['count'] if scored_docs and isinstance(scored_docs, list) else 0
        
        return metrics
        
    except Exception as e:
        return {
            'total_documents': 0,
            'today_documents': 0,
            'week_documents': 0,
            'scored_documents': 0,
            'error': str(e)
        }

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_database_stats():
    """Cached database statistics"""
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        # Table statistics
        table_stats = db_manager.execute_query("""
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_rows
            FROM pg_stat_user_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        
        return table_stats if isinstance(table_stats, list) else []
        
    except Exception as e:
        return []

@st.cache_data(ttl=180)  # Cache for 3 minutes
def get_recent_activity(limit=10):
    """Cached recent system activity"""
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        recent_docs = db_manager.execute_query(f"""
            SELECT 
                id,
                title, 
                created_at, 
                document_type, 
                source,
                ai_cybersecurity_score,
                ai_ethics_score
            FROM documents 
            ORDER BY created_at DESC 
            LIMIT {limit}
        """)
        
        return recent_docs if isinstance(recent_docs, list) else []
        
    except Exception as e:
        return []

@st.cache_data(ttl=900)  # Cache for 15 minutes
def get_document_types():
    """Cached list of document types for admin filtering"""
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        
        doc_types = db_manager.execute_query("""
            SELECT DISTINCT document_type, COUNT(*) as count
            FROM documents 
            WHERE document_type IS NOT NULL AND document_type != ''
            GROUP BY document_type
            ORDER BY count DESC
        """)
        
        return doc_types if isinstance(doc_types, list) else []
        
    except Exception as e:
        return []

def render_optimized_system_metrics():
    """Render system metrics with caching"""
    metrics = get_system_metrics()
    
    if 'error' in metrics:
        st.error(f"Database connection issue: {metrics['error']}")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", metrics['total_documents'])
    
    with col2:
        st.metric("Today", metrics['today_documents'])
    
    with col3:
        st.metric("This Week", metrics['week_documents'])
    
    with col4:
        st.metric("Scored Documents", metrics['scored_documents'])

def render_optimized_database_status():
    """Render database status with caching"""
    st.markdown("### Database Status & Performance")
    
    # Connection test
    try:
        from utils.database import DatabaseManager
        db_manager = DatabaseManager()
        test_query = db_manager.execute_query("SELECT 1 as test")
        if test_query:
            st.success("✅ Database Connection: Healthy")
        else:
            st.error("❌ Database Connection: Failed")
    except Exception as e:
        st.error(f"❌ Database Connection Error: {str(e)}")
    
    # System metrics
    render_optimized_system_metrics()
    
    st.markdown("---")
    
    # Table statistics
    with st.expander("📊 Database Table Statistics", expanded=False):
        table_stats = get_database_stats()
        
        if table_stats:
            for table in table_stats:
                st.markdown(f"**{table['tablename']}**")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Live Rows", table['live_rows'])
                with col2:
                    st.metric("Inserts", table['inserts'])
                with col3:
                    st.metric("Updates", table['updates'])
                with col4:
                    st.metric("Deletes", table['deletes'])
                st.markdown("---")
        else:
            st.info("No table statistics available")

def render_optimized_recent_activity():
    """Render recent activity with caching"""
    st.markdown("### Recent System Activity")
    
    activity = get_recent_activity(15)
    
    if activity:
        for doc in activity:
            timestamp = doc['created_at'].strftime("%Y-%m-%d %H:%M:%S") if doc.get('created_at') else "Unknown"
            title = doc.get('title', 'Untitled')[:50] + "..." if len(doc.get('title', '')) > 50 else doc.get('title', 'Untitled')
            doc_type = doc.get('document_type', 'Unknown')
            
            # Score indicator
            has_scores = any([
                doc.get('ai_cybersecurity_score'),
                doc.get('ai_ethics_score')
            ])
            score_indicator = "🎯 Scored" if has_scores else "⏳ Pending"
            
            st.markdown(f"**{timestamp}** | {title} | {doc_type} | {score_indicator}")
    else:
        st.info("No recent activity found")

def clear_admin_caches():
    """Clear all admin-related caches"""
    try:
        get_system_metrics.clear()
        get_database_stats.clear()
        get_recent_activity.clear()
        get_document_types.clear()
        return True
    except:
        return False