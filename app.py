import streamlit as st
from all_docs_tab import render
from datetime import datetime

def main():
    st.set_page_config(
        page_title="GUARDIAN - AI Risk Analysis Navigator",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS styling - Government/Nonprofit Theme
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Serif+Pro:wght@400;600&display=swap');
    
    .main > div {
        padding-top: 2rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #ffffff;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .main .block-container {
        background-color: #ffffff;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .quantum-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #312e81 50%, #1e40af 100%) !important;
        padding: 3rem 2rem !important;
        border-radius: 12px !important;
        margin-bottom: 2.5rem !important;
        color: white !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(30, 58, 138, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        width: 100% !important;
        display: block !important;
    }
    
    .quantum-header h1 {
        margin: 0 !important;
        font-size: 2.8rem !important;
        font-weight: 600 !important;
        font-family: 'Source Serif Pro', serif !important;
        letter-spacing: -0.02em !important;
        color: white !important;
    }
    
    .quantum-header p {
        margin: 1rem 0 0 0 !important;
        font-size: 1.15rem !important;
        opacity: 0.9 !important;
        font-weight: 400 !important;
        letter-spacing: 0.01em !important;
        color: white !important;
    }
    
    .metric-card {
        background: #ffffff;
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 6px rgba(0, 0, 0, 0.04);
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        border-top: 1px solid #e5e7eb;
    }
    
    .score-excellent {
        border-left-color: #059669;
        background: linear-gradient(145deg, #ffffff 0%, #f0fdf4 100%);
    }
    
    .score-good {
        border-left-color: #d97706;
        background: linear-gradient(145deg, #ffffff 0%, #fffbeb 100%);
    }
    
    .score-moderate {
        border-left-color: #dc2626;
        background: linear-gradient(145deg, #ffffff 0%, #fef2f2 100%);
    }
    
    .document-separator {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, #e5e7eb 0%, #9ca3af 50%, #e5e7eb 100%);
        margin: 2.5rem 0;
        border-radius: 1px;
    }
    
    .stExpander > details > summary {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 10px;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        font-weight: 500;
    }
    
    .sidebar-info {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.25rem 0;
        border: 1px solid #e2e8f0;
        color: #374151;
    }
    
    .document-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
    }
    
    .document-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1), 0 20px 48px rgba(0, 0, 0, 0.06);
        border-color: #3b82f6;
    }
    
    .score-badge {
        transition: all 0.3s ease;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .score-badge:hover {
        transform: scale(1.05);
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.75rem;
        margin: 1.5rem 0;
    }
    
    /* Enhanced Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Source Serif Pro', serif;
        color: #1f2937;
        font-weight: 600;
    }
    
    p, div, span {
        color: #374151;
        line-height: 1.6;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8fafc;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        color: #6b7280;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: #1e40af;
        border-bottom: 2px solid #3b82f6;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(145deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        background: linear-gradient(145deg, #1e40af 0%, #1e3a8a 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Force light theme overrides */
    .stApp, .main, .block-container, .element-container {
        background-color: #ffffff !important;
        color: #374151 !important;
    }
    
    /* Sidebar light theme */
    .css-1d391kg, .css-1cypcdb, .sidebar .sidebar-content {
        background-color: #f8fafc !important;
        color: #374151 !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div > div {
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div > div {
        background-color: #ffffff !important;
        color: #374151 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #f8fafc !important;
        border: 2px dashed #d1d5db !important;
        border-radius: 8px !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #ffffff !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        color: #374151 !important;
    }
    
    /* Alert styling */
    .stAlert {
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background-color: #e5e7eb !important;
    }
    
    @media (max-width: 768px) {
        .category-grid {
            grid-template-columns: 1fr;
            gap: 1.25rem;
        }
        
        .quantum-header h1 {
            font-size: 2.2rem;
        }
        
        .quantum-header p {
            font-size: 1rem;
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
    
    # Main header without background
    st.markdown("""
    <div style="
        padding: 2rem 0 1rem 0;
        margin-bottom: 2rem;
        text-align: center;
        width: 100%;
        display: block;
    ">
        <h1 style="
            margin: 0;
            font-size: 2.8rem;
            font-weight: bold;
            font-family: Arial, sans-serif;
            letter-spacing: -0.02em;
            color: #dc2626;
        ">GUARDIAN</h1>
        <p style="
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
            font-weight: 400;
            letter-spacing: 0.01em;
            color: #6b7280;
            font-style: italic;
        ">(Global Unified AI Risk Discovery & Impact Analysis Navigator)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Cyber Institute credit with logo - centered
    try:
        import base64
        with open("assets/cyber_institute_logo.jpg", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <img src="data:image/jpeg;base64,{logo_data}" width="40" height="40" style="border-radius: 50%; margin-bottom: 0.5rem;">
            <div style="font-size: 0.9rem; color: #6b7280;">
                Developed by Cyber Institute
            </div>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style="text-align: center; font-size: 0.9rem; color: #6b7280; margin-bottom: 1.5rem;">
            Developed by Cyber Institute
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced sidebar with government/nonprofit styling
    with st.sidebar:
        # Government seal-style header
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.2);
        ">
            <h3 style="margin: 0; font-family: 'Source Serif Pro', serif; font-weight: 600;">
                🔐 Risk Assessment Framework
            </h3>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">
                Official Quantum Readiness Evaluation
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Assessment Methodology")
        st.markdown("""
        <div class="sidebar-info">
        <strong>Core Evaluation Areas:</strong><br><br>
        🔒 <strong>Post-Quantum Cryptography</strong><br>
        Assessment of quantum-resistant algorithms<br><br>
        ⚠️ <strong>Risk Assessment</strong><br>
        Vulnerability identification and impact analysis<br><br>
        📋 <strong>Implementation Planning</strong><br>
        Strategy development and roadmap creation<br><br>
        ✅ <strong>Standards Compliance</strong><br>
        NIST, FIPS, and industry standard adherence<br><br>
        🔄 <strong>Migration Strategy</strong><br>
        Transition planning and execution framework
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Maturity Classification")
        st.markdown("""
        <div class="sidebar-info">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 12px; height: 12px; background: #059669; border-radius: 2px; margin-right: 8px;"></div>
            <strong>90-100: Quantum-Ready</strong>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 12px; height: 12px; background: #10b981; border-radius: 2px; margin-right: 8px;"></div>
            <strong>75-89: Advanced</strong>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 12px; height: 12px; background: #d97706; border-radius: 2px; margin-right: 8px;"></div>
            <strong>50-74: Developing</strong>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <div style="width: 12px; height: 12px; background: #f59e0b; border-radius: 2px; margin-right: 8px;"></div>
            <strong>25-49: Basic</strong>
        </div>
        <div style="display: flex; align-items: center;">
            <div style="width: 12px; height: 12px; background: #dc2626; border-radius: 2px; margin-right: 8px;"></div>
            <strong>0-24: Initial</strong>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Technical Capabilities")
        st.markdown("""
        <div class="sidebar-info">
        <strong>Analysis Engine:</strong><br><br>
        • Intelligent text processing<br>
        • Quantum keyword detection<br>
        • Compliance verification<br>
        • Maturity trait identification<br>
        • Gap analysis reporting<br>
        • Standards cross-referencing<br><br>
        <em>Powered by advanced natural language processing and domain-specific evaluation algorithms.</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Add contact/support section
        st.markdown("### Support Resources")
        st.markdown("""
        <div class="sidebar-info">
        <strong>Need Assistance?</strong><br><br>
        📚 Documentation available<br>
        🎯 Training materials provided<br>
        📞 Technical support accessible<br>
        🔄 Regular updates included<br><br>
        <small><em>This tool supports federal agencies and organizations in preparing for the post-quantum cryptography transition.</em></small>
        </div>
        """, unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["All Documents", "Quantum Maturity", "Add Document", "Database Status"])
    
    with tab1:
        render()
    
    with tab2:
        from quantum_tab_fixed import render as render_quantum
        render_quantum()
    
    with tab3:
        from components.document_uploader import render_document_uploader, render_bulk_upload
        render_document_uploader()
        st.markdown("---")
        render_bulk_upload()
    
    with tab4:
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
