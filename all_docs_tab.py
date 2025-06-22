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

@st.cache_data(ttl=300)
def fetch_documents_cached():
    """Cached version of document fetching with memory optimization"""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, title, content, text_content, 
                   ai_cybersecurity_score, quantum_cybersecurity_score, 
                   ai_ethics_score, quantum_ethics_score,
                   source, organization, document_type, publication_date,
                   author_organization, detected_region, quantum_score, topic
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

@st.cache_data(ttl=180)
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

def show_detailed_scoring_explanation(content, title, score, framework_type, unique_id):
    """Show detailed scoring explanation in a modal dialog"""
    
    # Analysis of content for specific factors
    content_lower = (content + " " + title).lower()
    
    if framework_type == 'ai_cybersecurity':
        factors = {
            'security frameworks': ['security framework', 'cybersecurity framework', 'security model'],
            'threat assessment': ['threat', 'risk assessment', 'vulnerability', 'attack'],
            'data protection': ['data protection', 'privacy', 'encryption', 'secure data'],
            'model security': ['model security', 'ai model protection', 'adversarial', 'poisoning'],
            'governance': ['governance', 'oversight', 'compliance', 'audit']
        }
        
        performance_levels = {
            80: ("Excellent", "#2e7d32", "Comprehensive AI cybersecurity practices with robust security measures"),
            60: ("Good", "#f57c00", "Solid AI cybersecurity foundation with room for enhancement"), 
            40: ("Moderate", "#ed6c02", "Basic AI cybersecurity but lacks comprehensive coverage"),
            20: ("Limited", "#d32f2f", "Minimal AI cybersecurity guidance"),
            0: ("Insufficient", "#d32f2f", "Lacks adequate AI cybersecurity considerations")
        }
        
        improvements = [
            "Implement comprehensive AI threat modeling",
            "Establish robust model validation procedures", 
            "Develop AI-specific incident response plans",
            "Create continuous monitoring frameworks",
            "Enhance data governance for AI systems"
        ]
        
        title_text = "AI Cybersecurity Maturity Assessment"
        
    elif framework_type == 'quantum_cybersecurity':
        factors = {
            'post-quantum cryptography': ['post-quantum', 'quantum-safe', 'quantum-resistant'],
            'quantum key distribution': ['qkd', 'quantum key', 'quantum communication'],
            'quantum threat assessment': ['quantum threat', 'quantum attack', 'quantum computing threat'],
            'cryptographic agility': ['crypto agility', 'algorithm agility', 'cryptographic transition'],
            'quantum readiness': ['quantum readiness', 'quantum preparedness', 'quantum migration']
        }
        
        performance_levels = {
            80: ("Tier 5 - Advanced", "#1976d2", "Advanced quantum cybersecurity readiness with comprehensive post-quantum strategies"),
            60: ("Tier 4 - Proficient", "#1976d2", "Strong quantum cybersecurity foundation with active post-quantum planning"),
            40: ("Tier 3 - Developing", "#f57c00", "Basic quantum awareness with initial post-quantum considerations"),
            20: ("Tier 2 - Emerging", "#ed6c02", "Limited quantum cybersecurity awareness and preparation"),
            0: ("Tier 1 - Baseline", "#d32f2f", "Minimal quantum cybersecurity considerations")
        }
        
        improvements = [
            "Develop post-quantum cryptography migration plan",
            "Implement quantum threat assessment procedures",
            "Establish cryptographic agility frameworks", 
            "Create quantum risk management policies",
            "Plan for NIST post-quantum standards adoption"
        ]
        
        title_text = "Quantum Cybersecurity Maturity Assessment"
        
    elif framework_type == 'ai_ethics':
        factors = {
            'bias mitigation': ['bias', 'fairness', 'discrimination', 'bias mitigation'],
            'transparency': ['transparency', 'explainable', 'interpretable', 'explainability'],
            'accountability': ['accountability', 'responsibility', 'oversight', 'audit'],
            'privacy protection': ['privacy', 'data protection', 'personal data', 'consent'],
            'human oversight': ['human oversight', 'human control', 'human-in-the-loop']
        }
        
        performance_levels = {
            80: ("Exemplary", "#2e7d32", "Comprehensive AI ethics framework with strong emphasis on responsible AI"),
            60: ("Proficient", "#f57c00", "Good AI ethics foundation with most key principles addressed"),
            40: ("Developing", "#ed6c02", "Basic AI ethics considerations with room for significant improvement"),
            20: ("Emerging", "#d32f2f", "Limited AI ethics awareness and implementation"),
            0: ("Insufficient", "#d32f2f", "Inadequate attention to AI ethics principles")
        }
        
        improvements = [
            "Implement comprehensive bias testing procedures",
            "Develop explainable AI capabilities",
            "Establish ethical review boards",
            "Create stakeholder engagement processes",
            "Enhance privacy-preserving techniques"
        ]
        
        title_text = "AI Ethics Assessment"
        
    elif framework_type == 'quantum_ethics':
        factors = {
            'quantum advantage equity': ['quantum advantage', 'quantum supremacy', 'equitable access'],
            'quantum privacy': ['quantum privacy', 'quantum encryption', 'quantum security'],
            'quantum governance': ['quantum governance', 'quantum regulation', 'quantum policy'],
            'societal impact': ['societal impact', 'social implications', 'public benefit'],
            'quantum responsibility': ['quantum responsibility', 'responsible quantum', 'ethical quantum']
        }
        
        performance_levels = {
            80: ("Advanced", "#2e7d32", "Sophisticated understanding of quantum ethics with comprehensive societal considerations"),
            60: ("Developed", "#f57c00", "Good quantum ethics awareness with attention to key societal considerations"),
            40: ("Emerging", "#ed6c02", "Basic quantum ethics considerations with limited depth"),
            20: ("Initial", "#d32f2f", "Minimal quantum ethics awareness"),
            0: ("Absent", "#d32f2f", "No significant quantum ethics considerations identified")
        }
        
        improvements = [
            "Develop quantum equity frameworks",
            "Address quantum digital divide concerns",
            "Create quantum ethics guidelines",
            "Establish quantum governance structures", 
            "Promote quantum literacy initiatives"
        ]
        
        title_text = "Quantum Ethics Assessment"
    
    else:
        return
    
    # Find matching factors
    factors_found = []
    for factor, keywords in factors.items():
        if any(keyword in content_lower for keyword in keywords):
            factors_found.append(factor)
    
    # Determine performance level
    performance = "N/A"
    color = "#9e9e9e"
    interpretation = "Not applicable for this document type"
    
    if score == 'N/A':
        if framework_type == 'ai_cybersecurity':
            interpretation = "This document does not focus on AI-specific cybersecurity. For a high score, documents should address AI threat modeling, model security, AI governance, and AI-specific incident response procedures."
        elif framework_type == 'quantum_cybersecurity':
            interpretation = "This document does not address quantum cybersecurity concerns. For a high score, documents should cover post-quantum cryptography, quantum key distribution, quantum threat assessment, and NIST post-quantum standards."
        elif framework_type == 'ai_ethics':
            interpretation = "This document does not focus on AI ethics. For a high score, documents should address bias mitigation, algorithmic transparency, accountability frameworks, and responsible AI development practices."
        elif framework_type == 'quantum_ethics':
            interpretation = "This document does not address quantum ethics. For a high score, documents should cover quantum equity, societal impacts of quantum technology, quantum governance, and responsible quantum development."
    elif isinstance(score, (int, float)):
        for threshold, (perf, col, interp) in sorted(performance_levels.items(), reverse=True):
            if score >= threshold:
                performance = perf
                color = col
                interpretation = interp
                break
    
    # Display compact explanation content (no nested expander)
    st.markdown(f"**{title_text} - Score: {score} ({performance})**")
    st.markdown(f"""
    <div style="background: {color}; color: white; padding: 8px; border-radius: 4px; margin: 4px 0;">
        <strong>Assessment:</strong> {interpretation}
    </div>
    """, unsafe_allow_html=True)
    
    if factors_found:
        st.markdown("**Key factors identified:**")
        for factor in factors_found[:3]:  # Show only top 3
            st.markdown(f"• {factor.title()}")
    
    if isinstance(score, (int, float)) and score > 0:
        st.markdown("**Areas for improvement:**")
        for improvement in improvements[:3]:  # Show only top 3
            st.markdown(f"• {improvement}")

def extract_document_metadata(content):
    """Extract metadata from document content using enhanced interceptor system"""
    if not content:
        return {}
    
    content_str = str(content)[:3000] if content else ""
    
    # Basic metadata extraction
    metadata = {
        'length': len(content_str),
        'has_tables': 'table' in content_str.lower(),
        'has_figures': any(term in content_str.lower() for term in ['figure', 'chart', 'graph']),
        'language': 'english',  # Default assumption
        'document_type': 'policy'
    }
    
    return metadata

def extract_clean_metadata(content):
    """Extract clean metadata using enhanced system"""
    return extract_document_metadata(content)

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
    """Remove all HTML artifacts from metadata fields"""
    if not field_value:
        return "Not specified"
    
    cleaned = str(field_value)
    
    # Remove common HTML artifacts
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
    """Safely clean date field"""
    try:
        date_field = doc[11] if len(doc) > 11 else None
        if date_field and str(date_field) != 'None':
            return ultra_clean_metadata(date_field)
    except:
        pass
    return "Not specified"

def get_document_topic(doc):
    """Determine document topic based on content"""
    title = str(doc[1] or "").lower()
    content_preview = str(doc[2] or "")[:500].lower() if doc[2] else ""
    
    # Check for AI indicators
    ai_terms = ['artificial intelligence', 'ai ', 'machine learning', 'neural network', 'deep learning']
    has_ai = any(term in title or term in content_preview for term in ai_terms)
    
    # Check for Quantum indicators  
    quantum_terms = ['quantum', 'post-quantum', 'qkd', 'quantum computing']
    has_quantum = any(term in title or term in content_preview for term in quantum_terms)
    
    # Check for Cybersecurity indicators
    cyber_terms = ['cybersecurity', 'cyber security', 'information security', 'security framework']
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
    """Render the All Documents tab with card layout matching screenshot"""
    
    # Apply compact CSS
    apply_ultra_compact_css()
    
    st.markdown("## 📚 **Policy Repository**")
    
    # Repository overview section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; margin: 10px 0; color: white;">
        <h4 style="margin: 0 0 8px 0; color: white;">🔍 Repository Overview</h4>
        <p style="margin: 0; font-size: 14px; line-height: 1.4;">
            Comprehensive policy document analysis using GUARDIAN's multi-LLM ensemble system. 
            Documents are scored across four frameworks: AI Cybersecurity, Quantum Cybersecurity, AI Ethics, and Quantum Ethics.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch documents
    docs = fetch_documents_cached()
    
    if not docs:
        st.warning("No documents found in the repository.")
        return
    
    st.success(f"📊 **{len(docs)} documents** in repository")
    
    # Create layout for documents exactly as shown in screenshot
    for i, doc in enumerate(docs):
        unique_id = f"doc_{doc[0]}_{i}"
        
        # Create card with blue border exactly as shown
        st.markdown(f"""
        <div style="background: white; border: 2px solid #4285f4; border-radius: 8px; padding: 15px; margin: 10px 0;">
            <h3 style="margin: 0 0 8px 0; color: #4285f4; font-size: 16px; font-weight: 600;">
                {ultra_clean_metadata(doc[1])} 🔗
            </h3>
            <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                <span style="background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {get_document_topic(doc)}
                </span>
                <span style="background: #007bff; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {ultra_clean_metadata(doc[10])}
                </span>
                <span style="background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {ultra_clean_metadata(doc[9])}
                </span>
                <span style="background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 11px;">
                    {clean_date_safely(doc)}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Create 2x2 scoring grid exactly as shown in screenshot
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # AI Cybersecurity Score with colored dot
            ai_cyber_score = doc[4] if doc[4] is not None else 'N/A'
            ai_cyber_display = str(ai_cyber_score).replace('/100', '') if ai_cyber_score != 'N/A' else 'N/A'
            
            # Color based on score
            if ai_cyber_score == 'N/A':
                color = "#6c757d"
            elif isinstance(ai_cyber_score, (int, float)) and ai_cyber_score >= 75:
                color = "#dc3545"  # Red for high scores as shown
            else:
                color = "#fd7e14"  # Orange
            
            ai_cyber_expanded = st.selectbox(
                f"● AI Cybersecurity: {ai_cyber_display}",
                ["▼"],
                key=f"ai_cyber_{unique_id}",
                index=0
            )
            
            # AI Ethics Score
            ai_ethics_score = doc[6] if doc[6] is not None else 'N/A'
            ai_ethics_display = str(ai_ethics_score).replace('/100', '') if ai_ethics_score != 'N/A' else 'N/A'
            
            ai_ethics_expanded = st.selectbox(
                f"● AI Ethics: {ai_ethics_display}",
                ["▼"],
                key=f"ai_ethics_{unique_id}",
                index=0
            )
        
        with col2:
            # Quantum Cybersecurity Score
            q_cyber_score = doc[5] if doc[5] is not None else 'N/A'
            q_cyber_display = str(q_cyber_score).replace('/100', '') if q_cyber_score != 'N/A' else 'N/A'
            
            # Green for good quantum scores as shown
            if q_cyber_score != 'N/A' and isinstance(q_cyber_score, (int, float)) and q_cyber_score >= 4:
                color = "#28a745"
            else:
                color = "#6c757d"
            
            q_cyber_expanded = st.selectbox(
                f"● Quantum Cybersecurity: {q_cyber_display}",
                ["▼"],
                key=f"q_cyber_{unique_id}",
                index=0
            )
            
            # Quantum Ethics Score
            q_ethics_score = doc[7] if doc[7] is not None else 'N/A'
            q_ethics_display = str(q_ethics_score).replace('/100', '') if q_ethics_score != 'N/A' else 'N/A'
            
            q_ethics_expanded = st.selectbox(
                f"● Quantum Ethics: {q_ethics_display}",
                ["▼"],
                key=f"q_ethics_{unique_id}",
                index=0
            )
        
        # Show expandable analysis sections when dropdown is selected
        if ai_cyber_expanded:
            with st.expander("🔒 AI Cybersecurity Analysis", expanded=True):
                analysis = analyze_ai_cybersecurity_content(doc[2], ai_cyber_score)
                st.markdown(f"**Score: {ai_cyber_display}**")
                st.write(analysis)
        
        if q_cyber_expanded:
            with st.expander("⚡ Quantum Cybersecurity Analysis", expanded=True):
                analysis = analyze_quantum_cybersecurity_content(doc[2], q_cyber_score)
                st.markdown(f"**Score: {q_cyber_display}**")
                st.write(analysis)
        
        if ai_ethics_expanded:
            with st.expander("🤖 AI Ethics Analysis", expanded=True):
                analysis = analyze_ai_ethics_content(doc[2], ai_ethics_score)
                st.markdown(f"**Score: {ai_ethics_display}**")
                st.write(analysis)
        
        if q_ethics_expanded:
            with st.expander("⚡ Quantum Ethics Analysis", expanded=True):
                analysis = analyze_quantum_ethics_content(doc[2], q_ethics_score)
                st.markdown(f"**Score: {q_ethics_display}**")
                st.write(analysis)
        
        # Add spacing between cards
        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    render()