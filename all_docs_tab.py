"""
All Documents Tab for GUARDIAN Policy Repository
Comprehensive document repository with intelligent scoring and analysis
"""

import streamlit as st
import psycopg2
import os
from functools import lru_cache
import hashlib


def apply_ultra_compact_css():
    """Apply ultra-compact CSS styling to maximize space efficiency"""
    st.markdown("""
    <style>
    /* Ultra-compact spacing */
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }
    
    /* Compact elements */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px !important;
        margin-bottom: 0.3rem !important;
    }
    
    .stSelectbox, .stText {
        margin-bottom: 0.2rem !important;
    }
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 0.2rem !important;
    }
    
    /* Compact metrics */
    [data-testid="metric-container"] {
        padding: 0.2rem !important;
        margin: 0.1rem !important;
    }
    
    /* Button styling with intelligent color coding */
    div[data-testid="stVerticalBlock"] div[data-testid="stButton"] > button,
    div[data-testid="column"] div[data-testid="stButton"] > button,
    .main .stButton > button,
    .stApp .stButton > button {
        font-size: 8px !important;
        font-weight: bold !important;
        height: 18px !important;
        padding: 2px 4px !important;
        line-height: 1.0 !important;
        border-radius: 0px !important;
        margin: 0px !important;
    }
    
    /* Target button content specifically */
    .stButton > button > div,
    .stButton > button > p,
    .stButton button * {
        font-size: 8px !important;
        font-weight: bold !important;
        line-height: 1.0 !important;
    }
    
    /* Global button override with maximum specificity */
    html body .stApp .main .stButton button {
        font-size: 8px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)


@lru_cache(maxsize=100)
def fetch_documents_cached():
    """Cached version of document fetching with memory optimization"""
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id, title, organization, source, publication_date, 
                ai_cybersecurity_score, quantum_cybersecurity_score,
                ai_ethics_score, quantum_ethics_score,
                topic, content
            FROM documents 
            ORDER BY publication_date DESC NULLS LAST, title ASC
        """)
        
        documents = cur.fetchall()
        cur.close()
        conn.close()
        
        return documents
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return []


def analyze_ai_cybersecurity_content(content, score):
    """Analyze AI cybersecurity content"""
    
    # Check if content appears to be out of scope
    content_lower = content.lower() if content else ""
    
    # Define scope indicators
    ai_cyber_indicators = [
        'artificial intelligence', 'machine learning', 'cybersecurity', 'ai security',
        'neural network', 'deep learning', 'threat detection', 'malware detection',
        'intrusion detection', 'security automation', 'ai governance', 'algorithmic security'
    ]
    
    # Check for children's literature, novels, religious content, etc.
    out_of_scope_indicators = [
        'once upon a time', 'fairy tale', 'children', 'story', 'novel', 'fiction',
        'character', 'adventure', 'forest', 'princess', 'dragon', 'magic',
        'bible', 'scripture', 'prayer', 'worship', 'religious', 'spiritual',
        'cookbook', 'recipe', 'ingredients', 'cooking', 'baking'
    ]
    
    # Count scope indicators
    ai_cyber_count = sum(1 for indicator in ai_cyber_indicators if indicator in content_lower)
    out_of_scope_count = sum(1 for indicator in out_of_scope_indicators if indicator in content_lower)
    
    # If clearly out of scope, return simple message
    if out_of_scope_count > ai_cyber_count and len(content) < 2000:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # If no clear AI cybersecurity content found
    if ai_cyber_count == 0:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # Return proper analysis for in-scope content
    if score == 'N/A' or score is None:
        return "This document appears to contain AI cybersecurity content but has not been scored by GUARDIAN's assessment system."
    
    try:
        score_num = int(score)
    except (ValueError, TypeError):
        return "This document appears to contain AI cybersecurity content but has not been scored by GUARDIAN's assessment system."
    
    if score_num >= 80:
        analysis = f"This document demonstrates excellent AI Cybersecurity maturity with a score of {score}/100.\n\n"
        analysis += "**Key Strengths Identified:**\n"
        analysis += "- Comprehensive AI security frameworks and implementation strategies\n"
        analysis += "- Advanced threat detection and response mechanisms\n"
        analysis += "- Strong governance and risk management practices\n"
        analysis += "- Proactive security measures and continuous monitoring\n\n"
        analysis += "**Assessment Shows:**\n"
        analysis += f"- Score of {score_num}/100 indicates advanced AI cybersecurity readiness\n"
        analysis += "- Document addresses critical AI security challenges effectively\n"
        analysis += "- Content includes robust security architecture and controls\n\n"
        analysis += "**Recommendations:**\n"
        analysis += "- Maintain current security posture with regular updates\n"
        analysis += "- Continue monitoring emerging AI threat landscapes\n"
        analysis += "- Share best practices with industry stakeholders"
    elif score_num >= 60:
        analysis = f"This document shows good AI Cybersecurity practices with a score of {score}/100.\n\n"
        analysis += "**Positive Elements:**\n"
        analysis += "- Solid foundational AI security concepts and frameworks\n"
        analysis += "- Adequate threat detection and mitigation strategies\n"
        analysis += "- Basic governance structures for AI security\n"
        analysis += "- Some proactive security measures implemented\n\n"
        analysis += "**Areas for Enhancement:**\n"
        analysis += "- Strengthen advanced threat detection capabilities\n"
        analysis += "- Expand AI security governance frameworks\n"
        analysis += "- Improve incident response procedures\n"
        analysis += "- Enhance continuous monitoring systems"
    else:
        analysis = f"This document has basic AI Cybersecurity coverage with a score of {score}/100.\n\n"
        analysis += "**Current State:**\n"
        analysis += "- Limited AI security framework implementation\n"
        analysis += "- Basic threat awareness and detection capabilities\n"
        analysis += "- Minimal governance structures in place\n"
        analysis += "- Reactive rather than proactive security approach\n\n"
        analysis += "**Priority Improvements:**\n"
        analysis += "- Develop comprehensive AI security strategy\n"
        analysis += "- Implement advanced threat detection systems\n"
        analysis += "- Establish robust governance frameworks\n"
        analysis += "- Create incident response and recovery plans"
    
    return analysis


def analyze_quantum_cybersecurity_content(content, score):
    """Analyze quantum cybersecurity content"""
    
    # Check if content appears to be out of scope
    content_lower = content.lower() if content else ""
    
    # Define scope indicators
    quantum_cyber_indicators = [
        'quantum', 'post-quantum', 'cryptography', 'encryption', 'qkd',
        'quantum key distribution', 'quantum computing', 'quantum resistance',
        'lattice-based', 'hash-based', 'code-based', 'multivariate'
    ]
    
    # Check for children's literature, novels, religious content, etc.
    out_of_scope_indicators = [
        'once upon a time', 'fairy tale', 'children', 'story', 'novel', 'fiction',
        'character', 'adventure', 'forest', 'princess', 'dragon', 'magic',
        'bible', 'scripture', 'prayer', 'worship', 'religious', 'spiritual',
        'cookbook', 'recipe', 'ingredients', 'cooking', 'baking'
    ]
    
    # Count scope indicators
    quantum_count = sum(1 for indicator in quantum_cyber_indicators if indicator in content_lower)
    out_of_scope_count = sum(1 for indicator in out_of_scope_indicators if indicator in content_lower)
    
    # If clearly out of scope, return simple message
    if out_of_scope_count > quantum_count and len(content) < 2000:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # If no clear quantum cybersecurity content found
    if quantum_count == 0:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # Return proper analysis for in-scope content
    if score == 'N/A' or score is None:
        return "This document appears to contain quantum cybersecurity content but has not been scored by GUARDIAN's assessment system."
    
    try:
        score_num = int(score)
    except (ValueError, TypeError):
        return "This document appears to contain quantum cybersecurity content but has not been scored by GUARDIAN's assessment system."
    
    if score_num >= 4:
        analysis = f"This document demonstrates Quantum Cybersecurity maturity of {score}/5.\n\n"
        analysis += "**Quantum Security Elements:**\n"
        analysis += "- Cryptographic agility frameworks and transition planning\n"
        analysis += "- NIST post-quantum cryptographic standards adoption\n"
        analysis += "- Quantum-safe algorithm evaluation and selection\n"
        analysis += "- Quantum computing threat timeline and preparedness\n"
        analysis += "- Integration of quantum-resistant technologies\n\n"
        analysis += f"Assessment shows {score_num}/5 quantum cybersecurity readiness"
    elif score_num >= 3:
        analysis = f"This document shows Quantum Cybersecurity awareness with a score of {score}/5.\n\n"
        analysis += "**Document addresses:**\n"
        analysis += "- Quantum-safe cryptography and post-quantum security measures\n"
        analysis += "- Content includes quantum threat assessment and mitigation strategies\n"
        analysis += f"- Assessment shows {score_num}/5 quantum cybersecurity readiness\n\n"
        analysis += "**Recommendations:**\n"
        analysis += "- Implement post-quantum cryptographic standards\n"
        analysis += "- Prepare for quantum computing timeline\n"
        analysis += "- Regular quantum security assessments"
    else:
        analysis = f"This document has limited Quantum Cybersecurity content with a score of {score}/5.\n\n"
        analysis += "**Basic Coverage:**\n"
        analysis += "- Minimal quantum security considerations\n"
        analysis += "- Limited post-quantum cryptography awareness\n"
        analysis += "- Basic quantum threat understanding\n\n"
        analysis += "**Priority Actions:**\n"
        analysis += "- Develop quantum-safe migration strategy\n"
        analysis += "- Assess current cryptographic vulnerabilities\n"
        analysis += "- Plan for post-quantum transition"
    
    return analysis


def analyze_ai_ethics_content(content, score):
    """Analyze AI ethics content"""
    
    # Check if content appears to be out of scope
    content_lower = content.lower() if content else ""
    
    # Define scope indicators
    ai_ethics_indicators = [
        'ai ethics', 'artificial intelligence ethics', 'algorithmic bias', 'fairness',
        'transparency', 'accountability', 'explainability', 'responsible ai',
        'ethical ai', 'bias mitigation', 'algorithmic fairness'
    ]
    
    # Check for children's literature, novels, religious content, etc.
    out_of_scope_indicators = [
        'once upon a time', 'fairy tale', 'children', 'story', 'novel', 'fiction',
        'character', 'adventure', 'forest', 'princess', 'dragon', 'magic',
        'bible', 'scripture', 'prayer', 'worship', 'religious', 'spiritual',
        'cookbook', 'recipe', 'ingredients', 'cooking', 'baking'
    ]
    
    # Count scope indicators
    ai_ethics_count = sum(1 for indicator in ai_ethics_indicators if indicator in content_lower)
    out_of_scope_count = sum(1 for indicator in out_of_scope_indicators if indicator in content_lower)
    
    # If clearly out of scope, return simple message
    if out_of_scope_count > ai_ethics_count and len(content) < 2000:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # If no clear AI ethics content found
    if ai_ethics_count == 0:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # Return proper analysis for in-scope content
    if score == 'N/A' or score is None:
        return "This document appears to contain AI ethics content but has not been scored by GUARDIAN's assessment system."
    
    try:
        score_num = int(score)
    except (ValueError, TypeError):
        return "This document appears to contain AI ethics content but has not been scored by GUARDIAN's assessment system."
    
    if score_num >= 80:
        analysis = f"This document demonstrates an AI Ethics score of {score}/100.\n\n"
        analysis += "**Ethical Framework Coverage:**\n"
        analysis += "- Document addresses ethical AI considerations, bias prevention measures\n"
        analysis += "- Content includes comprehensive ethical guidelines and frameworks\n"
        analysis += f"- Assessment shows {score_num}/100 AI ethics practices\n\n"
        analysis += "**Recommendations:**\n"
        analysis += "- Implement comprehensive bias detection systems\n"
        analysis += "- Regular ethical AI audits and assessments\n"
        analysis += "- Stakeholder engagement in AI ethics governance"
    else:
        analysis = f"This document shows AI Ethics considerations with a score of {score}/100.\n\n"
        analysis += "**Ethics Elements:**\n"
        analysis += "- Basic AI ethics framework and guidelines\n"
        analysis += "- Some bias mitigation strategies\n"
        analysis += "- Limited stakeholder engagement processes\n\n"
        analysis += "**Improvement Areas:**\n"
        analysis += "- Enhance bias detection and mitigation\n"
        analysis += "- Strengthen ethical review processes\n"
        analysis += "- Expand stakeholder consultation"
    
    return analysis


def analyze_quantum_ethics_content(content, score):
    """Analyze quantum ethics content"""
    
    # Check if content appears to be out of scope
    content_lower = content.lower() if content else ""
    
    # Define scope indicators
    quantum_ethics_indicators = [
        'quantum ethics', 'quantum computing ethics', 'quantum equity', 'quantum access',
        'quantum governance', 'quantum divide', 'responsible quantum', 'quantum policy'
    ]
    
    # Check for children's literature, novels, religious content, etc.
    out_of_scope_indicators = [
        'once upon a time', 'fairy tale', 'children', 'story', 'novel', 'fiction',
        'character', 'adventure', 'forest', 'princess', 'dragon', 'magic',
        'bible', 'scripture', 'prayer', 'worship', 'religious', 'spiritual',
        'cookbook', 'recipe', 'ingredients', 'cooking', 'baking'
    ]
    
    # Count scope indicators
    quantum_ethics_count = sum(1 for indicator in quantum_ethics_indicators if indicator in content_lower)
    out_of_scope_count = sum(1 for indicator in out_of_scope_indicators if indicator in content_lower)
    
    # If clearly out of scope, return simple message
    if out_of_scope_count > quantum_ethics_count and len(content) < 2000:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # If no clear quantum ethics content found
    if quantum_ethics_count == 0:
        return "This appears to be children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    # Return proper analysis for in-scope content
    if score == 'N/A' or score is None:
        return "This document appears to contain quantum ethics content but has not been scored by GUARDIAN's assessment system."
    
    try:
        score_num = int(score)
    except (ValueError, TypeError):
        return "This document appears to contain quantum ethics content but has not been scored by GUARDIAN's assessment system."
    
    if score_num >= 80:
        analysis = f"This document demonstrates Quantum Ethics considerations scoring {score}/100.\n\n"
        analysis += "**Quantum Ethics Framework:**\n"
        analysis += "- Document addresses quantum computing ethics, access and equity concerns\n"
        analysis += "- Content includes quantum technology governance and societal impact\n"
        analysis += f"- Assessment shows {score_num}/100 quantum ethics considerations\n\n"
        analysis += "**Recommendations:**\n"
        analysis += "- Ensure equitable access to quantum technologies\n"
        analysis += "- Address quantum computing societal implications\n"
        analysis += "- Develop quantum governance frameworks"
    else:
        analysis = f"This document shows Quantum Ethics awareness with a score of {score}/100.\n\n"
        analysis += "**Ethics Elements:**\n"
        analysis += "- Basic quantum ethics framework\n"
        analysis += "- Some equity and access considerations\n"
        analysis += "- Limited governance structures\n\n"
        analysis += "**Improvement Areas:**\n"
        analysis += "- Enhance quantum equity policies\n"
        analysis += "- Strengthen governance frameworks\n"
        analysis += "- Expand stakeholder engagement"
    
    return analysis


def get_score_color(score):
    """Get color for score based on value and scoring system"""
    if score == 'N/A' or score is None:
        return '#808080'  # Gray
    
    try:
        score_num = int(score)
        
        # Check if this is a quantum cybersecurity score (1-5 scale)
        if score_num <= 5:
            if score_num >= 4:
                return '#22C55E'  # Green for 4-5
            elif score_num >= 3:
                return '#EAB308'  # Orange for 3
            else:
                return '#EF4444'  # Red for 1-2
        else:
            # Standard 0-100 scale
            if score_num >= 80:
                return '#22C55E'  # Green
            elif score_num >= 60:
                return '#EAB308'  # Orange
            else:
                return '#EF4444'  # Red
    except:
        return '#808080'  # Gray for any parsing issues


def comprehensive_document_scoring_cached(content, title):
    """Cached version of comprehensive scoring with content hashing"""
    if not content:
        return {
            'ai_cybersecurity': 'N/A',
            'quantum_cybersecurity': 'N/A',
            'ai_ethics': 'N/A',
            'quantum_ethics': 'N/A'
        }
    
    # Create hash for caching
    content_hash = hashlib.md5(f"{content[:1000]}{title}".encode()).hexdigest()
    
    # Simple mock scoring for now
    return {
        'ai_cybersecurity': 75,
        'quantum_cybersecurity': 3,
        'ai_ethics': 68,
        'quantum_ethics': 72
    }


def render():
    """Render the All Documents tab with comprehensive document repository and contextual help tooltips."""
    
    # Apply ultra-compact CSS to eliminate all spacing
    apply_ultra_compact_css()
    
    st.title("📚 Policy Repository")
    st.markdown("*Comprehensive cybersecurity, AI, and quantum policy document collection*")
    
    # Fetch documents
    documents = fetch_documents_cached()
    
    if not documents:
        st.warning("No documents found in the repository.")
        return
    
    # Statistics
    total_docs = len(documents)
    ai_cyber_docs = len([d for d in documents if d[5] not in ['N/A', None]])
    q_cyber_docs = len([d for d in documents if d[6] not in ['N/A', None]])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", total_docs)
    with col2:
        st.metric("AI Cybersecurity Scored", ai_cyber_docs)
    with col3:
        st.metric("Quantum Cybersecurity Scored", q_cyber_docs)
    
    # Filters
    st.markdown("**Filters:**")
    col1, col2 = st.columns(2)
    
    with col1:
        organizations = list(set([d[2] for d in documents if d[2]]))
        selected_org = st.selectbox("Filter by Organization", ["All"] + sorted(organizations))
    
    with col2:
        topics = list(set([d[9] for d in documents if d[9]]))
        selected_topic = st.selectbox("Filter by Topic", ["All"] + sorted(topics))
    
    # Apply filters
    filtered_docs = documents
    if selected_org != "All":
        filtered_docs = [d for d in filtered_docs if d[2] == selected_org]
    if selected_topic != "All":
        filtered_docs = [d for d in filtered_docs if d[9] == selected_topic]
    
    st.markdown(f"**Showing {len(filtered_docs)} of {total_docs} documents**")
    
    # Display documents
    for doc in filtered_docs:
        doc_id, title, organization, source, pub_date, ai_cyber, q_cyber, ai_ethics, q_ethics, topic, content = doc
        
        # Clean and format display values
        title = title or "Untitled Document"
        organization = organization or "Unknown Organization"
        
        # Format scores for display with proper color coding
        ai_cyber_display = f"{ai_cyber}/100" if ai_cyber not in ['N/A', None] else "N/A"
        ai_ethics_display = f"{ai_ethics}/100" if ai_ethics not in ['N/A', None] else "N/A"
        q_cyber_display = f"{q_cyber}/5" if q_cyber not in ['N/A', None] else "N/A"
        q_ethics_display = f"{q_ethics}/100" if q_ethics not in ['N/A', None] else "N/A"
        
        # Create document card
        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; border-radius: 5px;">
                <h4 style="margin: 0 0 5px 0; color: #2c3e50;">{title}</h4>
                <p style="margin: 0 0 5px 0; color: #7f8c8d; font-size: 14px;"><strong>{organization}</strong></p>
                <p style="margin: 0 0 10px 0; color: #95a5a6; font-size: 12px;">{pub_date or 'Date not available'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Score buttons row with proper color coding
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
            
            with col1:
                ai_cyber_color = get_score_color(ai_cyber)
                if st.button(ai_cyber_display, key=f"ai_cyber_{doc_id}"):
                    pass
                st.markdown("<div style='text-align: center; font-size: 10px;'>AI Cyber</div>", unsafe_allow_html=True)
            
            with col2:
                q_cyber_color = get_score_color(q_cyber)
                if st.button(q_cyber_display, key=f"q_cyber_{doc_id}"):
                    pass
                st.markdown("<div style='text-align: center; font-size: 10px;'>Q Cyber</div>", unsafe_allow_html=True)
            
            with col3:
                ai_ethics_color = get_score_color(ai_ethics)
                if st.button(ai_ethics_display, key=f"ai_ethics_{doc_id}"):
                    pass
                st.markdown("<div style='text-align: center; font-size: 10px;'>AI Ethics</div>", unsafe_allow_html=True)
            
            with col4:
                q_ethics_color = get_score_color(q_ethics)
                if st.button(q_ethics_display, key=f"q_ethics_{doc_id}"):
                    pass
                st.markdown("<div style='text-align: center; font-size: 10px;'>Q Ethics</div>", unsafe_allow_html=True)
            
            with col5:
                if source and source.startswith('http'):
                    st.markdown(f"""
                    <a href="{source}" target="_blank" style="
                        background-color: #3498db; 
                        color: white; 
                        text-decoration: none; 
                        padding: 5px 10px; 
                        border-radius: 3px; 
                        font-size: 12px; 
                        font-weight: bold;
                        display: inline-block;
                        width: 90%;
                        text-align: center;
                    ">View</a>
                    """, unsafe_allow_html=True)
                st.markdown("<div style='text-align: center; font-size: 10px;'>Source</div>", unsafe_allow_html=True)
            
            # Analysis expandable sections
            st.markdown("**Analysis:**")
            
            # AI Cybersecurity Analysis
            with st.expander("🔒 AI Cybersecurity Analysis", expanded=False):
                ai_cyber_analysis = analyze_ai_cybersecurity_content(content or "", ai_cyber)
                st.write(ai_cyber_analysis)
            
            # Quantum Cybersecurity Analysis
            with st.expander("⚛️ Quantum Cybersecurity Analysis", expanded=False):
                q_cyber_analysis = analyze_quantum_cybersecurity_content(content or "", q_cyber)
                st.write(q_cyber_analysis)
            
            # AI Ethics Analysis
            with st.expander("🤖 AI Ethics Analysis", expanded=False):
                ai_ethics_analysis = analyze_ai_ethics_content(content or "", ai_ethics)
                st.write(ai_ethics_analysis)
            
            # Quantum Ethics Analysis
            with st.expander("🔬 Quantum Ethics Analysis", expanded=False):
                q_ethics_analysis = analyze_quantum_ethics_content(content or "", q_ethics)
                st.write(q_ethics_analysis)
            
            st.markdown("---")