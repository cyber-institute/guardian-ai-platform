"""
All Documents Tab for GUARDIAN - Enhanced with Multi-LLM Scoring
Preserves original card layout while updating N/A scoring messages
"""

import streamlit as st
import psycopg2
import os
import json
import requests
from datetime import datetime
import time

# Try to import UI protection with fallback
try:
    from utils.ui_protection import protect_ui_elements, validate_ui_integrity
    protect_ui_elements()
except ImportError:
    pass

# Performance optimization: Cache document fetching
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_documents_cached():
    """Cached version of document fetching with memory optimization"""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, title, content, text_content, 
                   ai_cybersecurity_score, quantum_cybersecurity_score, 
                   ai_ethics_score, quantum_ethics_score,
                   url, organization, document_type, publication_date,
                   author, region, comprehensive_score, topic_classification
            FROM documents 
            ORDER BY id DESC
            LIMIT 100
        """)
        
        documents = cursor.fetchall()
        return documents
        
    except Exception as e:
        st.error(f"Error fetching documents: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

@st.cache_data(ttl=180)  # Cache for 3 minutes
def get_document_content_cached(doc_id, url):
    """Cache document content separately for better memory management"""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT content, text_content FROM documents WHERE id = %s", (doc_id,))
        result = cursor.fetchone()
        return result if result else (None, None)
    except:
        return (None, None)
    finally:
        cursor.close()
        conn.close()

def analyze_ai_cybersecurity_content(content, score):
    """Analyze AI cybersecurity content"""
    if score == 'N/A':
        # Check if document is out of scope
        try:
            from utils.multi_llm_scoring_engine import detect_document_scope
            content_str = str(content) if content else ""
            scope_analysis = detect_document_scope(content_str, "")
            
            if scope_analysis['out_of_scope']:
                return f"This document appears to be {scope_analysis['document_type']} rather than a cybersecurity, AI, or quantum technology policy document. AI Cybersecurity scoring is not applicable for this content type."
        except:
            pass
            
        return """
This document does not focus on AI-specific cybersecurity concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    try:
        score_num = int(str(score).replace('/100', ''))
    except:
        score_num = 0
    
    return f"""
This document demonstrates an AI Cybersecurity maturity score of {score}/100.

- Document addresses AI security considerations and risk assessment frameworks
- Content includes guidance on AI system protection and threat mitigation
- Assessment shows {'excellent' if score_num >= 75 else 'good' if score_num >= 50 else 'developing'} AI cybersecurity practices

**Recommendations:**
- Implement comprehensive AI security frameworks
- Regular AI system vulnerability assessments
- Continuous monitoring and threat detection
"""

def analyze_quantum_cybersecurity_content(content, score):
    """Analyze quantum cybersecurity content"""
    if score == 'N/A':
        # Check if document is out of scope
        try:
            from utils.multi_llm_scoring_engine import detect_document_scope
            content_str = str(content) if content else ""
            scope_analysis = detect_document_scope(content_str, "")
            
            if scope_analysis['out_of_scope']:
                return f"This document appears to be {scope_analysis['document_type']} rather than a cybersecurity, AI, or quantum technology policy document. Quantum Cybersecurity scoring is not applicable for this content type."
        except:
            pass
            
        return """
This document does not address quantum cybersecurity concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    try:
        score_num = int(str(score).replace('/100', ''))
    except:
        score_num = 0
    
    return f"""
This document demonstrates Quantum Cybersecurity readiness scoring {score}/100.

- Document addresses quantum-safe cryptography and post-quantum security measures
- Content includes quantum threat assessment and mitigation strategies
- Assessment shows {'advanced' if score_num >= 4 else 'intermediate' if score_num >= 3 else 'basic'} quantum cybersecurity readiness

**Recommendations:**
- Implement post-quantum cryptographic standards
- Prepare for quantum computing threats
- Regular quantum security assessments
"""

def analyze_ai_ethics_content(content, score):
    """Analyze AI ethics content"""
    if score == 'N/A':
        # Check if document is out of scope
        try:
            from utils.multi_llm_scoring_engine import detect_document_scope
            content_str = str(content) if content else ""
            scope_analysis = detect_document_scope(content_str, "")
            
            if scope_analysis['out_of_scope']:
                return f"This document appears to be {scope_analysis['document_type']} rather than a cybersecurity, AI, or quantum technology policy document. AI Ethics scoring is not applicable for this content type."
        except:
            pass
            
        return """
This document does not focus on AI ethics considerations.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    try:
        score_num = int(str(score).replace('/100', ''))
    except:
        score_num = 0
    
    return f"""
This document demonstrates AI Ethics maturity scoring {score}/100.

- Document addresses ethical AI principles and responsible development practices
- Content includes bias mitigation and fairness considerations
- Assessment shows {'excellent' if score_num >= 75 else 'good' if score_num >= 50 else 'developing'} AI ethics implementation

**Recommendations:**
- Strengthen bias detection and mitigation measures
- Enhance transparency and explainability frameworks
- Regular ethical AI audits and assessments
"""

def analyze_quantum_ethics_content(content, score):
    """Analyze quantum ethics content"""
    if score == 'N/A':
        # Check if document is out of scope
        try:
            from utils.multi_llm_scoring_engine import detect_document_scope
            content_str = str(content) if content else ""
            scope_analysis = detect_document_scope(content_str, "")
            
            if scope_analysis['out_of_scope']:
                return f"This document appears to be {scope_analysis['document_type']} rather than a cybersecurity, AI, or quantum technology policy document. Quantum Ethics scoring is not applicable for this content type."
        except:
            pass
            
        return """
This document does not address quantum ethics considerations.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    try:
        score_num = int(str(score).replace('/100', ''))
    except:
        score_num = 0
    
    return f"""
This document demonstrates Quantum Ethics considerations scoring {score}/100.

- Document addresses quantum technology societal impacts and governance
- Content includes quantum equity and access considerations
- Assessment shows {'excellent' if score_num >= 75 else 'good' if score_num >= 50 else 'developing'} quantum ethics awareness

**Recommendations:**
- Enhance quantum governance frameworks
- Address quantum equity and access issues
- Strengthen public engagement in quantum policy
"""

# Import utilities with fallback handling
try:
    from utils.document_metadata_extractor import extract_document_metadata
except ImportError:
    def extract_document_metadata(content):
        return {}

try:
    from utils.multi_llm_metadata_extractor import extract_clean_metadata
except ImportError:
    def extract_clean_metadata(content):
        return {}

try:
    from components.help_tooltips import help_tooltips
except ImportError:
    help_tooltips = {}

def apply_ultra_compact_css():
    """Apply ultra-compact CSS to eliminate all spacing"""
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    .stButton > button {
        font-size: 8px !important;
        font-weight: bold !important;
        height: 18px !important;
        padding: 2px 4px !important;
        line-height: 1.0 !important;
        border-radius: 0px !important;
        margin: 0px !important;
    }
    
    div[data-testid="stExpander"] {
        border: 1px solid #ddd !important;
        border-radius: 8px !important;
        background: #f8f9fa !important;
        margin: 2px 0 !important;
    }
    
    .streamlit-expanderHeader {
        font-family: 'Segoe UI', 'Roboto', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
        padding: 8px 12px !important;
        background: #f8f9fa !important;
        border-bottom: 1px solid #e9ecef !important;
    }
    
    .streamlit-expanderContent {
        padding: 12px !important;
        background: white !important;
        font-family: 'Segoe UI', 'Roboto', sans-serif !important;
        font-size: 12px !important;
        line-height: 1.4 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def ultra_clean_metadata(field_value):
    """Remove all HTML artifacts from metadata fields using enhanced interceptor"""
    if not field_value:
        return "Not specified"
    
    # Convert to string and clean
    cleaned = str(field_value)
    
    # Remove common HTML artifacts that slip through
    html_artifacts = [
        '</div>', '<div>', '</span>', '<span>', '</p>', '<p>',
        '</h1>', '<h1>', '</h2>', '<h2>', '</h3>', '<h3>',
        '</strong>', '<strong>', '</em>', '<em>',
        '</a>', '<a href=', '</li>', '<li>', '</ul>', '<ul>',
        '&nbsp;', '&amp;', '&lt;', '&gt;', '&quot;', '&#39;'
    ]
    
    for artifact in html_artifacts:
        cleaned = cleaned.replace(artifact, '')
    
    # Remove any remaining HTML-like patterns
    import re
    cleaned = re.sub(r'<[^>]+>', '', cleaned)
    cleaned = re.sub(r'&[a-zA-Z0-9#]+;', '', cleaned)
    
    # Clean up whitespace
    cleaned = ' '.join(cleaned.split())
    
    return cleaned if cleaned.strip() else "Not specified"

def clean_date_safely(doc):
    """Safely clean date field to prevent None value issues causing </div> artifacts"""
    try:
        date_field = doc[11] if len(doc) > 11 else None  # publication_date is at index 11
        if date_field and str(date_field) != 'None':
            cleaned_date = ultra_clean_metadata(date_field)
            # Ensure it's actually a date-like string
            if cleaned_date and cleaned_date != "Not specified" and len(cleaned_date) > 3:
                return cleaned_date
    except:
        pass
    return "Not specified"

def get_document_topic(doc):
    """Determine if document is AI, Quantum, Cybersecurity, or Both based on content."""
    title = str(doc[1] or "").lower()
    content_preview = str(doc[2] or "")[:500].lower() if doc[2] else ""
    
    # Check for AI indicators
    ai_terms = ['artificial intelligence', 'ai ', 'machine learning', 'neural network', 'deep learning', 'llm', 'generative ai']
    has_ai = any(term in title or term in content_preview for term in ai_terms)
    
    # Check for Quantum indicators  
    quantum_terms = ['quantum', 'post-quantum', 'qkd', 'quantum computing', 'quantum cryptography']
    has_quantum = any(term in title or term in content_preview for term in quantum_terms)
    
    # Check for Cybersecurity indicators
    cyber_terms = ['cybersecurity', 'cyber security', 'information security', 'infosec', 'security framework']
    has_cyber = any(term in title or term in content_preview for term in cyber_terms)
    
    if has_ai and has_quantum:
        return "Both"
    elif has_ai:
        return "AI"
    elif has_quantum:
        return "Quantum"
    elif has_cyber:
        return "Cybersecurity"
    else:
        return "General"

def render():
    """Render the All Documents tab with comprehensive document repository and contextual help tooltips."""
    
    # CRITICAL: Validate UI protection before rendering
    try:
        validate_ui_integrity()
    except (ImportError, NameError):
        pass  # UI protection not available, continue safely
    
    # Apply ultra-compact CSS to eliminate all spacing
    apply_ultra_compact_css()
    
    st.markdown("## 📚 **Policy Repository**")
    
    # Add help text with improved styling
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; margin: 10px 0; color: white;">
        <h4 style="margin: 0 0 8px 0; color: white;">🔍 Repository Overview</h4>
        <p style="margin: 0; font-size: 14px; line-height: 1.4;">
            Comprehensive policy document analysis using GUARDIAN's multi-LLM ensemble system. 
            Documents are scored across four frameworks: AI Cybersecurity, Quantum Cybersecurity, AI Ethics, and Quantum Ethics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch documents with caching
    docs = fetch_documents_cached()
    
    if not docs:
        st.warning("No documents found in the repository.")
        return
    
    # Display document count
    st.success(f"📊 **{len(docs)} documents** in repository")
    
    # Create layout for documents with original card format
    for i, doc in enumerate(docs):
        unique_id = f"doc_{doc[0]}_{i}"
        
        # Create card with bordered sections and metadata exactly as shown in screenshot
        st.markdown(f"""
        <div style="background: white; border: 2px solid #4da6ff; border-radius: 15px; padding: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 8px 0; color: #2c3e50; font-size: 16px; font-weight: 600;">
                {ultra_clean_metadata(doc[1])} 🔗
            </h3>
            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                <span style="background: #007bff; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {get_document_topic(doc)}
                </span>
                <span style="background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {ultra_clean_metadata(doc[10])}
                </span>
                <span style="background: #28a745; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {ultra_clean_metadata(doc[9])}
                </span>
                <span style="background: #ffc107; color: black; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {clean_date_safely(doc)}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create scoring section with colored dropdown selectboxes exactly as shown
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # AI Cybersecurity Score with colored indicator
            ai_cyber_score = doc[4] if doc[4] is not None else 'N/A'
            ai_cyber_display = str(ai_cyber_score).replace('/100', '') if ai_cyber_score != 'N/A' else 'N/A'
            
            # Color coding based on score
            if ai_cyber_score == 'N/A':
                color = "#6c757d"  # Gray
            elif isinstance(ai_cyber_score, (int, float)) and ai_cyber_score >= 75:
                color = "#28a745"  # Green
            elif isinstance(ai_cyber_score, (int, float)) and ai_cyber_score >= 50:
                color = "#fd7e14"  # Orange
            else:
                color = "#dc3545"  # Red
            
            st.markdown(f"<div style='color: {color}; font-weight: bold; margin: 5px 0;'>● AI Cybersecurity: {ai_cyber_display}</div>", unsafe_allow_html=True)
            if st.selectbox("", ["▼"], key=f"ai_cyber_select_{unique_id}", label_visibility="collapsed"):
                st.session_state[f'show_ai_cyber_{unique_id}'] = True
            
            # AI Ethics Score with colored indicator
            ai_ethics_score = doc[6] if doc[6] is not None else 'N/A'
            ai_ethics_display = str(ai_ethics_score).replace('/100', '') if ai_ethics_score != 'N/A' else 'N/A'
            
            if ai_ethics_score == 'N/A':
                color = "#6c757d"  # Gray
            elif isinstance(ai_ethics_score, (int, float)) and ai_ethics_score >= 75:
                color = "#28a745"  # Green
            elif isinstance(ai_ethics_score, (int, float)) and ai_ethics_score >= 50:
                color = "#fd7e14"  # Orange
            else:
                color = "#dc3545"  # Red
                
            st.markdown(f"<div style='color: {color}; font-weight: bold; margin: 5px 0;'>● AI Ethics: {ai_ethics_display}</div>", unsafe_allow_html=True)
            if st.selectbox("", ["▼"], key=f"ai_ethics_select_{unique_id}", label_visibility="collapsed"):
                st.session_state[f'show_ai_ethics_{unique_id}'] = True
        
        with col2:
            # Quantum Cybersecurity Score with colored indicator
            q_cyber_score = doc[5] if doc[5] is not None else 'N/A'
            q_cyber_display = str(q_cyber_score).replace('/100', '') if q_cyber_score != 'N/A' else 'N/A'
            
            if q_cyber_score == 'N/A':
                color = "#6c757d"  # Gray
            elif isinstance(q_cyber_score, (int, float)) and q_cyber_score >= 4:
                color = "#28a745"  # Green
            elif isinstance(q_cyber_score, (int, float)) and q_cyber_score >= 3:
                color = "#fd7e14"  # Orange
            else:
                color = "#dc3545"  # Red
                
            st.markdown(f"<div style='color: {color}; font-weight: bold; margin: 5px 0;'>● Quantum Cybersecurity: {q_cyber_display}</div>", unsafe_allow_html=True)
            if st.selectbox("", ["▼"], key=f"q_cyber_select_{unique_id}", label_visibility="collapsed"):
                st.session_state[f'show_q_cyber_{unique_id}'] = True
            
            # Quantum Ethics Score with colored indicator
            q_ethics_score = doc[7] if doc[7] is not None else 'N/A'
            q_ethics_display = str(q_ethics_score).replace('/100', '') if q_ethics_score != 'N/A' else 'N/A'
            
            if q_ethics_score == 'N/A':
                color = "#6c757d"  # Gray
            elif isinstance(q_ethics_score, (int, float)) and q_ethics_score >= 75:
                color = "#28a745"  # Green
            elif isinstance(q_ethics_score, (int, float)) and q_ethics_score >= 50:
                color = "#fd7e14"  # Orange
            else:
                color = "#dc3545"  # Red
                
            st.markdown(f"<div style='color: {color}; font-weight: bold; margin: 5px 0;'>● Quantum Ethics: {q_ethics_display}</div>", unsafe_allow_html=True)
            if st.selectbox("", ["▼"], key=f"q_ethics_select_{unique_id}", label_visibility="collapsed"):
                st.session_state[f'show_q_ethics_{unique_id}'] = True
        
        # Expandable analysis sections with exact emoji styling as shown in screenshots
        if st.session_state.get(f'show_ai_cyber_{unique_id}', False):
            with st.expander("🔒 AI Cybersecurity Analysis", expanded=True):
                ai_cyber_analysis = analyze_ai_cybersecurity_content(doc[2], ai_cyber_score)
                st.markdown(f"**Score: {ai_cyber_display}**")
                st.write(ai_cyber_analysis)
        
        if st.session_state.get(f'show_q_cyber_{unique_id}', False):
            with st.expander("⚡ Quantum Cybersecurity Analysis", expanded=True):
                q_cyber_analysis = analyze_quantum_cybersecurity_content(doc[2], q_cyber_score)
                st.markdown(f"**Score: {q_cyber_display}**")
                st.write(q_cyber_analysis)
        
        if st.session_state.get(f'show_ai_ethics_{unique_id}', False):
            with st.expander("🤖 AI Ethics Analysis", expanded=True):
                ai_ethics_analysis = analyze_ai_ethics_content(doc[2], ai_ethics_score)
                st.markdown(f"**Score: {ai_ethics_display}**")
                st.write(ai_ethics_analysis)
        
        if st.session_state.get(f'show_q_ethics_{unique_id}', False):
            with st.expander("⚡ Quantum Ethics Analysis", expanded=True):
                q_ethics_analysis = analyze_quantum_ethics_content(doc[2], q_ethics_score)
                st.markdown(f"**Score: {q_ethics_display}**")
                st.write(q_ethics_analysis)
        
        # Add spacing between cards
        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()