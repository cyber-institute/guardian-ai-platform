import streamlit as st
from all_docs_tab import render
from datetime import datetime

def main():
    st.set_page_config(
        page_title="Quantum Maturity Score",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS styling
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    
    .quantum-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .quantum-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .quantum-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .score-excellent {
        border-left-color: #22c55e;
    }
    
    .score-good {
        border-left-color: #f59e0b;
    }
    
    .score-moderate {
        border-left-color: #ef4444;
    }
    
    .document-separator {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    .stExpander > details > summary {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .sidebar-info {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .document-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .document-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .score-badge {
        transition: transform 0.2s ease;
    }
    
    .score-badge:hover {
        transform: scale(1.1);
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 1rem 0;
    }
    
    @media (max-width: 768px) {
        .category-grid {
            grid-template-columns: 1fr;
        }
        
        .document-card {
            flex-direction: column;
        }
        
        .score-section {
            margin-top: 1rem;
            justify-content: space-around;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="quantum-header">
        <h1>🔐 Quantum Maturity Score</h1>
        <p>AI-powered quantum readiness evaluation system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### 📊 Assessment Overview")
        st.markdown("""
        <div class="sidebar-info">
        <strong>Evaluation Criteria:</strong><br>
        • Post-Quantum Cryptography<br>
        • Risk Assessment<br>
        • Implementation Planning<br>
        • Standards Compliance<br>
        • Migration Strategy
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Scoring Scale")
        st.markdown("""
        <div class="sidebar-info">
        <strong>90-100:</strong> Quantum-Ready<br>
        <strong>75-89:</strong> Advanced<br>
        <strong>50-74:</strong> Developing<br>
        <strong>25-49:</strong> Basic<br>
        <strong>0-24:</strong> Initial
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔍 Analysis Features")
        st.markdown("""
        <div class="sidebar-info">
        • AI-powered text analysis<br>
        • Keyword density scoring<br>
        • Maturity trait detection<br>
        • Standards reference checking<br>
        • Implementation gap analysis
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📄 All Documents", "📄 Add Document", "🗄️ Database Status"])
    
    with tab1:
        render()
    
    with tab2:
        from components.document_uploader import render_document_uploader, render_bulk_upload
        render_document_uploader()
        st.markdown("---")
        render_bulk_upload()
    
    with tab3:
        render_database_status()

def render_database_status():
    """Render database status and management interface."""
    from utils.database import db_manager
    from utils.db import fetch_documents
    
    st.markdown("### 🗄️ Database Management")
    
    # Connection status
    if db_manager.engine:
        st.success("✅ Connected to PostgreSQL database")
    else:
        st.error("❌ Database connection failed")
        return
    
    # Database statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Document count
        doc_count = db_manager.execute_query("SELECT COUNT(*) as count FROM documents")
        count = 0
        if doc_count and isinstance(doc_count, list) and len(doc_count) > 0:
            count = doc_count[0]['count']
        st.metric("Total Documents", count)
    
    with col2:
        # Assessment count
        assessment_count = db_manager.execute_query("SELECT COUNT(*) as count FROM assessments")
        a_count = 0
        if assessment_count and isinstance(assessment_count, list) and len(assessment_count) > 0:
            a_count = assessment_count[0]['count']
        st.metric("Total Assessments", a_count)
    
    with col3:
        # Average score
        avg_score = db_manager.execute_query("SELECT AVG(quantum_score) as avg FROM documents WHERE quantum_score > 0")
        avg = 0
        if avg_score and isinstance(avg_score, list) and len(avg_score) > 0 and avg_score[0]['avg']:
            avg = round(avg_score[0]['avg'], 1)
        st.metric("Average Score", f"{avg}/100")
    
    st.markdown("---")
    
    # Recent documents
    st.markdown("#### 📋 Recent Documents")
    recent_docs = db_manager.execute_query("""
        SELECT title, quantum_score, document_type, created_at 
        FROM documents 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    
    if recent_docs and isinstance(recent_docs, list):
        for doc in recent_docs:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{doc['title']}**")
            with col2:
                st.write(f"Score: {doc['quantum_score']}")
            with col3:
                st.write(doc['document_type'])
    else:
        st.info("No documents found")
    
    st.markdown("---")
    
    # Database actions
    st.markdown("#### ⚙️ Database Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Data", help="Reload data from database"):
            st.rerun()
    
    with col2:
        if st.button("📊 Export Data", help="Export all documents as JSON"):
            try:
                documents = fetch_documents()
                st.download_button(
                    label="📥 Download JSON",
                    data=str(documents),
                    file_name=f"quantum_documents_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Export failed: {e}")
    
    # Database schema info
    with st.expander("🔍 Database Schema"):
        schema_info = db_manager.execute_query("""
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            ORDER BY table_name, ordinal_position
        """)
        
        if schema_info:
            import pandas as pd
            df = pd.DataFrame(schema_info)
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Schema information not available")

if __name__ == "__main__":
    main()
