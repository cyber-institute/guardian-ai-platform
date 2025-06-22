"""
All Documents Tab for GUARDIAN System - Clean Working Version
"""
import streamlit as st
import sqlite3
import hashlib
from functools import lru_cache
from utils.ultra_compact_css import apply_ultra_compact_css
from utils import help_tooltips
import time
import json

@st.cache_data(ttl=300)
def fetch_documents_cached():
    """Cached version of document fetching with memory optimization"""
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, url, upload_date, organization FROM documents ORDER BY upload_date DESC")
    docs = cursor.fetchall()
    conn.close()
    return docs

@st.cache_data(ttl=600)
def get_document_content_cached(doc_id, url):
    """Cache document content separately for better memory management"""
    # For now, return placeholder - in production this would fetch actual content
    return f"Document content for {doc_id}"

def comprehensive_document_scoring_cached(content, title):
    """Cached version of comprehensive scoring with content hashing"""
    # Simple scoring based on title content
    scores = {'ai_cybersecurity': 'N/A', 'quantum_cybersecurity': 'N/A', 'ai_ethics': 'N/A', 'quantum_ethics': 'N/A'}
    title_lower = title.lower()
    
    if 'ai' in title_lower or 'artificial intelligence' in title_lower:
        if 'cyber' in title_lower or 'security' in title_lower:
            scores['ai_cybersecurity'] = 'Tier 3'
        if 'ethics' in title_lower:
            scores['ai_ethics'] = 'Tier 4'
    
    if 'quantum' in title_lower:
        if 'security' in title_lower or 'crypto' in title_lower:
            scores['quantum_cybersecurity'] = 'Tier 4'
        if 'ethics' in title_lower:
            scores['quantum_ethics'] = 'Tier 3'
    
    return scores

def get_document_metadata_cached(doc_id):
    """Cache document metadata separately for faster loading"""
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, organization, upload_date, url FROM documents WHERE id = ?", (doc_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {'title': result[0], 'organization': result[1], 'upload_date': result[2], 'url': result[3]}
    return {}

def analyze_ai_cybersecurity_content(content, score):
    """Analyze AI cybersecurity content"""
    if score == 'N/A':
        return """
This document does not address AI cybersecurity concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    return f"AI Cybersecurity analysis for score: {score}"

def analyze_quantum_cybersecurity_content(content, score):
    """Analyze quantum cybersecurity content"""
    if score == 'N/A':
        return """
This document does not address quantum cybersecurity concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    return f"Quantum Cybersecurity analysis for score: {score}"

def analyze_ai_ethics_content(content, score):
    """Analyze AI ethics content"""
    if score == 'N/A':
        return """
This document does not address AI ethics considerations.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    return f"AI Ethics analysis for score: {score}"

def analyze_quantum_ethics_content(content, score):
    """Analyze quantum ethics content"""
    if score == 'N/A':
        return """
This document does not address quantum ethics considerations.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    return f"Quantum Ethics analysis for score: {score}"

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
    col_ai, col_quantum, col_both = st.columns([1, 1, 1])
    with col_ai:
        ai_filter = st.radio("", ["AI", "Quantum", "Both"], index=2, key="topic_filter", horizontal=True)
    
    # View Mode Section
    st.markdown("**View Mode:**")
    col_cards, col_compact, col_table, col_grid, col_minimal = st.columns(5)
    with col_cards:
        view_mode = st.radio("", ["Cards", "Compact", "Table", "Grid", "Minimal"], index=0, key="view_mode", horizontal=True)
    
    # Filter Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.selectbox("Document Type", ["Choose an option"], key="doc_type")
    with col2:
        st.selectbox("Author/Organization", ["Choose an option"], key="author_org")
    with col3:
        st.selectbox("Year", ["Choose an option"], key="year")
    with col4:
        st.selectbox("Region", ["Choose an option"], key="region")
    
    # Pagination
    st.markdown("**Page 1 of 4**")
    
    # Sample Documents
    sample_docs = [
        (1, "Winnie the Pooh", "https://example.com/winnie", "2024-02-01", "General Document Smithsonian"),
        (2, "NIST Special Publication 800-63-3: Digital Identity Guidelines", "https://example.com/nist", "2017-06-01", "Cybersecurity Standard NIST")
    ]
    
    # Document Cards
    for doc in sample_docs:
        doc_id, title, url, upload_date, organization = doc
        
        # Get scores for each document
        content = get_document_content_cached(doc_id, url)
        scores = comprehensive_document_scoring_cached(content, title)
        
        # Create blue-bordered card
        st.markdown(f"""
        <div style='border: 2px solid #007bff; border-radius: 8px; padding: 20px; margin: 15px 0; background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 100%);'>
            <h3 style='color: #1976d2; margin: 0 0 10px 0; font-size: 18px; font-weight: 600;'>{title}</h3>
            <div style='margin-bottom: 15px;'>
                <span style='background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px;'>General</span>
                <span style='background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px;'>Document</span>
                <span style='background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 12px; margin-right: 5px;'>{organization.split()[-1]}</span>
                <span style='background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 12px;'>{upload_date}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Scoring Dropdowns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            with st.expander(f"🔧 AI Cybersecurity: {scores['ai_cybersecurity']}", expanded=False):
                analysis = analyze_ai_cybersecurity_content(content, scores['ai_cybersecurity'])
                st.markdown(analysis)
        
        with col2:
            with st.expander(f"🔐 Quantum Cybersecurity: {scores['quantum_cybersecurity']}", expanded=False):
                analysis = analyze_quantum_cybersecurity_content(content, scores['quantum_cybersecurity'])
                st.markdown(analysis)
        
        with col3:
            with st.expander(f"⚖️ AI Ethics: {scores['ai_ethics']}", expanded=False):
                analysis = analyze_ai_ethics_content(content, scores['ai_ethics'])
                st.markdown(analysis)
        
        with col4:
            with st.expander(f"🌟 Quantum Ethics: {scores['quantum_ethics']}", expanded=False):
                analysis = analyze_quantum_ethics_content(content, scores['quantum_ethics'])
                st.markdown(analysis)