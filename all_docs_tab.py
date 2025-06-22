"""
All Documents Tab for GUARDIAN System - Isolated Clean Version
"""
import streamlit as st
import sqlite3

def render():
    """Render the All Documents tab with complete GUARDIAN interface"""
    
    # GUARDIAN Header with Eagle Logo
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <div style='display: inline-block;'>
            <span style='font-size: 48px; color: #dc3545; margin-right: 15px;'>🦅</span>
            <span style='color: #dc3545; font-family: "Arial Black", Arial, sans-serif; font-size: 36px; font-weight: 900; letter-spacing: 2px;'>GUARDIAN</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Policy Repository Header
    st.markdown("## 📚 **Policy Repository**")
    st.markdown("Repository with comprehensive document analysis and risk assessment frameworks.")
    
    # Topic Filter Section
    st.markdown("**Topic Filter:**")
    topic_filter = st.radio("Topic Filter", ["AI", "Quantum", "Both"], index=2, label_visibility="collapsed", horizontal=True)
    
    # View Mode Section
    st.markdown("**View Mode:**")
    view_mode = st.radio("View Mode", ["Cards", "Compact", "Table", "Grid", "Minimal"], index=0, label_visibility="collapsed", horizontal=True)
    
    # Filter Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.selectbox("Document Type", ["Choose an option"])
    with col2:
        st.selectbox("Author/Organization", ["Choose an option"])
    with col3:
        st.selectbox("Year", ["Choose an option"])
    with col4:
        st.selectbox("Region", ["Choose an option"])
    
    # Pagination
    st.markdown("**Page 1 of 4**")
    
    # Sample Documents with Cards
    documents = [
        {
            "title": "Winnie the Pooh",
            "tags": ["General", "Document", "Smithsonian", "2024-02-01"],
            "scores": {"ai_cyber": "N/A", "quantum_cyber": "N/A", "ai_ethics": "N/A", "quantum_ethics": "N/A"}
        },
        {
            "title": "NIST Special Publication 800-63-3: Digital Identity Guidelines",
            "tags": ["Cybersecurity", "Standard", "NIST", "2017-06-01"],
            "scores": {"ai_cyber": "N/A", "quantum_cyber": "N/A", "ai_ethics": "N/A", "quantum_ethics": "N/A"}
        }
    ]
    
    for doc in documents:
        # Create blue-bordered card
        st.markdown(f"""
        <div style='border: 2px solid #007bff; border-radius: 8px; padding: 20px; margin: 15px 0; background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 100%);'>
            <h3 style='color: #1976d2; margin: 0 0 10px 0; font-size: 18px; font-weight: 600;'>{doc["title"]}</h3>
            <div style='margin-bottom: 15px;'>
                {' '.join([f'<span style="background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px;">{tag}</span>' for tag in doc["tags"]])}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Scoring Dropdowns with proper color styling
        col1, col2, col3, col4 = st.columns(4)
        
        def get_analysis_text(framework, score):
            if score == "N/A":
                return f"""
This document does not address {framework} concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
            return f"{framework} analysis for score: {score}"
        
        with col1:
            with st.expander(f"🔧 AI Cybersecurity: {doc['scores']['ai_cyber']}", expanded=False):
                st.markdown(get_analysis_text("AI cybersecurity", doc['scores']['ai_cyber']))
        
        with col2:
            with st.expander(f"🔐 Quantum Cybersecurity: {doc['scores']['quantum_cyber']}", expanded=False):
                st.markdown(get_analysis_text("quantum cybersecurity", doc['scores']['quantum_cyber']))
        
        with col3:
            with st.expander(f"⚖️ AI Ethics: {doc['scores']['ai_ethics']}", expanded=False):
                st.markdown(get_analysis_text("AI ethics", doc['scores']['ai_ethics']))
        
        with col4:
            with st.expander(f"🌟 Quantum Ethics: {doc['scores']['quantum_ethics']}", expanded=False):
                st.markdown(get_analysis_text("quantum ethics", doc['scores']['quantum_ethics']))