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
    
    # Create the exact filter layout from the reference
    col_filter, col_view = st.columns([1, 2])
    
    with col_filter:
        st.markdown("**Topic Filter:**")
        topic_ai = st.checkbox("AI", value=False)
        topic_quantum = st.checkbox("Quantum", value=False) 
        topic_both = st.checkbox("Both", value=True)
    
    with col_view:
        st.markdown("**View Mode:**")
        view_col1, view_col2, view_col3, view_col4, view_col5 = st.columns(5)
        with view_col1:
            cards_selected = st.radio("", ["Cards"], index=0, key="cards_radio")
        with view_col2:
            compact_selected = st.checkbox("Compact", value=False)
        with view_col3:
            table_selected = st.checkbox("Table", value=False)
        with view_col4:
            grid_selected = st.checkbox("Grid", value=False) 
        with view_col5:
            minimal_selected = st.checkbox("Minimal", value=False)
    
    # Filter dropdowns
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
    with filter_col1:
        st.selectbox("Document Type", ["Choose an option"], key="doc_type_filter")
    with filter_col2:
        st.selectbox("Author/Organization", ["Choose an option"], key="author_filter")  
    with filter_col3:
        st.selectbox("Year", ["Choose an option"], key="year_filter")
    with filter_col4:
        st.selectbox("Region", ["Choose an option"], key="region_filter")
    
    # Add navigation arrows and pagination
    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
    with nav_col1:
        st.markdown("◀")
    with nav_col2:
        st.markdown("**Page 1 of 4**")
    with nav_col3:
        st.markdown("▶")
    
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
        
        # Create colored scoring dropdowns matching the reference exactly
        scoring_col1, scoring_col2, scoring_col3, scoring_col4 = st.columns(4)
        
        def get_analysis_text(framework, score):
            if score == "N/A":
                return f"""
This document does not address {framework} concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
            return f"{framework} analysis for score: {score}"
        
        # Create dropdown styling to match reference colors
        with scoring_col1:
            st.selectbox(f"🔧 AI Cybersecurity: {doc['scores']['ai_cyber']}", 
                        [doc['scores']['ai_cyber']], 
                        key=f"ai_cyber_{doc['title'][:10]}")
            if st.button("View Analysis", key=f"ai_cyber_btn_{doc['title'][:10]}"):
                st.info(get_analysis_text("AI cybersecurity", doc['scores']['ai_cyber']))
        
        with scoring_col2:
            st.selectbox(f"🔐 Quantum Cybersecurity: {doc['scores']['quantum_cyber']}", 
                        [doc['scores']['quantum_cyber']], 
                        key=f"q_cyber_{doc['title'][:10]}")
            if st.button("View Analysis", key=f"q_cyber_btn_{doc['title'][:10]}"):
                st.info(get_analysis_text("quantum cybersecurity", doc['scores']['quantum_cyber']))
        
        with scoring_col3:
            st.selectbox(f"⚖️ AI Ethics: {doc['scores']['ai_ethics']}", 
                        [doc['scores']['ai_ethics']], 
                        key=f"ai_ethics_{doc['title'][:10]}")
            if st.button("View Analysis", key=f"ai_ethics_btn_{doc['title'][:10]}"):
                st.info(get_analysis_text("AI ethics", doc['scores']['ai_ethics']))
        
        with scoring_col4:
            st.selectbox(f"🌟 Quantum Ethics: {doc['scores']['quantum_ethics']}", 
                        [doc['scores']['quantum_ethics']], 
                        key=f"q_ethics_{doc['title'][:10]}")
            if st.button("View Analysis", key=f"q_ethics_btn_{doc['title'][:10]}"):
                st.info(get_analysis_text("quantum ethics", doc['scores']['quantum_ethics']))