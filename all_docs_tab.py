"""
All Documents Tab for GUARDIAN - Enhanced with Multi-LLM Scoring
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
    from utils.ui_protection import protect_ui_elements
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
        # Scope detection with fallback
        try:
            content_str = str(content) if content else ""
            # Simple scope detection fallback
            out_of_scope_terms = ['children', 'fairy tale', 'recipe', 'cooking', 'religious text', 'bible', 'quran', 'torah']
            if any(term in content_str.lower() for term in out_of_scope_terms):
                return "This document appears to be outside the scope of cybersecurity, AI, or quantum technology policy. AI Cybersecurity scoring is not applicable for this content type."
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
        # Scope detection with fallback
        try:
            content_str = str(content) if content else ""
            # Simple scope detection fallback
            out_of_scope_terms = ['children', 'fairy tale', 'recipe', 'cooking', 'religious text', 'bible', 'quran', 'torah']
            if any(term in content_str.lower() for term in out_of_scope_terms):
                return "This document appears to be outside the scope of cybersecurity, AI, or quantum technology policy. Quantum Cybersecurity scoring is not applicable for this content type."
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
        # Scope detection with fallback
        try:
            content_str = str(content) if content else ""
            # Simple scope detection fallback
            out_of_scope_terms = ['children', 'fairy tale', 'recipe', 'cooking', 'religious text', 'bible', 'quran', 'torah']
            if any(term in content_str.lower() for term in out_of_scope_terms):
                return "This document appears to be outside the scope of cybersecurity, AI, or quantum technology policy. AI Ethics scoring is not applicable for this content type."
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
        # Scope detection with fallback
        try:
            content_str = str(content) if content else ""
            # Simple scope detection fallback
            out_of_scope_terms = ['children', 'fairy tale', 'recipe', 'cooking', 'religious text', 'bible', 'quran', 'torah']
            if any(term in content_str.lower() for term in out_of_scope_terms):
                return "This document appears to be outside the scope of cybersecurity, AI, or quantum technology policy. Quantum Ethics scoring is not applicable for this content type."
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

try:
    from utils.direct_db import get_db_connection
except ImportError:
    def get_db_connection():
        return psycopg2.connect(os.getenv('DATABASE_URL'))

def calculate_database_averages():
    """Calculate dynamic averages from database for NORM comparison"""
    try:
        # Use the cached document fetching function
        docs = fetch_documents_cached()
        if not docs:
            return {
                'ai_cybersecurity': 50,
                'quantum_cybersecurity': 40,
                'ai_ethics': 45,
                'quantum_ethics': 35,
                'comprehensive': 42
            }
        
        # Calculate averages from non-null scores
        totals = {'ai_cybersecurity': [], 'quantum_cybersecurity': [], 'ai_ethics': [], 'quantum_ethics': [], 'comprehensive': []}
        
        for doc in docs:
            if doc[4] is not None and doc[4] != 'N/A':  # ai_cybersecurity_score
                try:
                    totals['ai_cybersecurity'].append(float(str(doc[4]).replace('/100', '')))
                except:
                    pass
            if doc[5] is not None and doc[5] != 'N/A':  # quantum_cybersecurity_score
                try:
                    totals['quantum_cybersecurity'].append(float(str(doc[5]).replace('/100', '')))
                except:
                    pass
            if doc[6] is not None and doc[6] != 'N/A':  # ai_ethics_score
                try:
                    totals['ai_ethics'].append(float(str(doc[6]).replace('/100', '')))
                except:
                    pass
            if doc[7] is not None and doc[7] != 'N/A':  # quantum_ethics_score
                try:
                    totals['quantum_ethics'].append(float(str(doc[7]).replace('/100', '')))
                except:
                    pass
            if doc[15] is not None and doc[15] != 'N/A':  # comprehensive_score
                try:
                    totals['comprehensive'].append(float(str(doc[15]).replace('/100', '')))
                except:
                    pass
        
        # Calculate averages
        averages = {}
        for key, values in totals.items():
            if values:
                averages[key] = sum(values) / len(values)
            else:
                # Default fallback values if no data
                defaults = {'ai_cybersecurity': 50, 'quantum_cybersecurity': 40, 'ai_ethics': 45, 'quantum_ethics': 35, 'comprehensive': 42}
                averages[key] = defaults[key]
        
        return averages
        
    except Exception as e:
        # Return fallback averages if calculation fails
        return {
            'ai_cybersecurity': 50,
            'quantum_cybersecurity': 40,
            'ai_ethics': 45,
            'quantum_ethics': 35,
            'comprehensive': 42
        }

def generate_norm_analysis(score_type, current_score, averages):
    """Generate dynamic NORM analysis comparing to database averages"""
    try:
        current_num = float(str(current_score).replace('/100', ''))
        avg_score = averages.get(score_type, 50)
        
        # Calculate percentile difference
        diff = current_num - avg_score
        
        if diff > 15:
            comparison = f"significantly above average ({avg_score:.1f})"
            performance = "exceptional"
        elif diff > 5:
            comparison = f"above average ({avg_score:.1f})"
            performance = "strong"
        elif diff > -5:
            comparison = f"near average ({avg_score:.1f})"
            performance = "typical"
        elif diff > -15:
            comparison = f"below average ({avg_score:.1f})"
            performance = "developing"
        else:
            comparison = f"significantly below average ({avg_score:.1f})"
            performance = "needs improvement"
        
        return f"This document's {score_type.replace('_', ' ').title()} score is {comparison}, indicating {performance} performance in the repository."
        
    except:
        return f"This document shows {score_type.replace('_', ' ').title()} characteristics."

def show_score_explanation(framework_type, score, content="", title=""):
    """Show detailed scoring explanation in a modal dialog"""
    
    # Calculate database averages for NORM analysis
    averages = calculate_database_averages()
    
    # Generate NORM analysis
    norm_analysis = generate_norm_analysis(framework_type, score, averages)
    
    # Create modal dialog using Streamlit
    with st.expander(f"📊 {framework_type.replace('_', ' ').title()} Framework Analysis", expanded=False):
        
        # Add NORM Analysis header
        st.markdown("### 🎯 **NORM Analysis (Repository Comparison)**")
        st.info(norm_analysis)
        
        # Add detailed analysis based on framework type
        if framework_type == 'ai_cybersecurity':
            analysis = analyze_ai_cybersecurity_content(content, score)
        elif framework_type == 'quantum_cybersecurity':
            analysis = analyze_quantum_cybersecurity_content(content, score)
        elif framework_type == 'ai_ethics':
            analysis = analyze_ai_ethics_content(content, score)
        elif framework_type == 'quantum_ethics':
            analysis = analyze_quantum_ethics_content(content, score)
        else:
            analysis = f"Comprehensive scoring analysis for {framework_type}"
        
        st.markdown("### 📋 **Detailed Assessment**")
        st.markdown(analysis)

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

def get_comprehensive_badge(score, framework, doc_content="", doc_title=""):
    """Create badge for comprehensive scoring system with intelligent topic detection and help tooltips."""
    
    # Handle None or 'N/A' scores
    if score is None or score == 'N/A' or str(score).strip() == '':
        return f"""
        <div style="display: inline-block; margin: 2px;">
            <span style="background: linear-gradient(135deg, #6c757d, #495057); color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1); cursor: help;" 
                  title="This framework does not apply to this document type">
                {framework.replace('_', ' ').title()}: N/A
            </span>
        </div>
        """
    
    try:
        # Extract numeric score
        score_num = float(str(score).replace('/100', ''))
        
        # Determine color and description based on score
        if score_num >= 80:
            color = "linear-gradient(135deg, #28a745, #20c997)"
            desc = "Excellent"
        elif score_num >= 65:
            color = "linear-gradient(135deg, #17a2b8, #6f42c1)"
            desc = "Good"
        elif score_num >= 50:
            color = "linear-gradient(135deg, #ffc107, #fd7e14)"
            desc = "Fair"
        elif score_num >= 35:
            color = "linear-gradient(135deg, #fd7e14, #dc3545)"
            desc = "Developing"
        else:
            color = "linear-gradient(135deg, #dc3545, #6f42c1)"
            desc = "Needs Improvement"
        
        # Create clickable badge with help tooltip
        badge_html = f"""
        <div style="display: inline-block; margin: 2px;">
            <span style="background: {color}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1); cursor: help;" 
                  title="Click for detailed {framework.replace('_', ' ').title()} analysis. Score: {score_num}/100 ({desc})">
                {framework.replace('_', ' ').title()}: {score_num:.0f}/100
            </span>
        </div>
        """
        
        return badge_html
        
    except (ValueError, TypeError):
        # Handle invalid score format
        return f"""
        <div style="display: inline-block; margin: 2px;">
            <span style="background: linear-gradient(135deg, #6c757d, #495057); color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; box-shadow: 0 2px 4px rgba(0,0,0,0.1); cursor: help;" 
                  title="Invalid score format for {framework.replace('_', ' ').title()}">
                {framework.replace('_', ' ').title()}: Invalid
            </span>
        </div>
        """

def get_badge(score):
    """Legacy badge function for backward compatibility."""
    return get_comprehensive_badge(score, "legacy")

def render():
    """Render the All Documents tab with comprehensive document repository and contextual help tooltips."""
    
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
    
    # Create layout columns for controls
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        view_mode = st.selectbox(
            "View Mode",
            ["Cards", "Table", "Grid", "Compact", "Minimal"],
            index=0
        )
    
    with col2:
        sort_by = st.selectbox(
            "Sort By",
            ["Recent", "AI Cyber Score", "Quantum Cyber Score", "AI Ethics Score", "Quantum Ethics Score", "Title"],
            index=0
        )
    
    with col3:
        filter_topic = st.selectbox(
            "Filter by Topic",
            ["All", "AI", "Quantum", "Cybersecurity", "Both"],
            index=0
        )
    
    # Apply filtering and sorting
    filtered_docs = docs.copy()
    
    # Topic filtering
    if filter_topic != "All":
        if filter_topic == "AI":
            filtered_docs = [doc for doc in filtered_docs if get_document_topic(doc) in ["AI", "Both"]]
        elif filter_topic == "Quantum":
            filtered_docs = [doc for doc in filtered_docs if get_document_topic(doc) in ["Quantum", "Both"]]
        elif filter_topic == "Cybersecurity":
            filtered_docs = [doc for doc in filtered_docs if get_document_topic(doc) == "Cybersecurity"]
        elif filter_topic == "Both":
            filtered_docs = [doc for doc in filtered_docs if get_document_topic(doc) == "Both"]
    
    # Sorting
    if sort_by == "AI Cyber Score":
        filtered_docs = sorted(filtered_docs, key=lambda x: float(str(x[4] or 0).replace('/100', '')), reverse=True)
    elif sort_by == "Quantum Cyber Score":
        filtered_docs = sorted(filtered_docs, key=lambda x: float(str(x[5] or 0).replace('/100', '')), reverse=True)
    elif sort_by == "AI Ethics Score":
        filtered_docs = sorted(filtered_docs, key=lambda x: float(str(x[6] or 0).replace('/100', '')), reverse=True)
    elif sort_by == "Quantum Ethics Score":
        filtered_docs = sorted(filtered_docs, key=lambda x: float(str(x[7] or 0).replace('/100', '')), reverse=True)
    elif sort_by == "Title":
        filtered_docs = sorted(filtered_docs, key=lambda x: str(x[1] or "").lower())
    # Default is "Recent" which maintains the original order (ORDER BY id DESC)
    
    st.info(f"Showing {len(filtered_docs)} documents")
    
    # Render documents based on view mode
    if view_mode == "Cards":
        render_card_view(filtered_docs)
    elif view_mode == "Table":
        render_table_view(filtered_docs)
    elif view_mode == "Grid":
        render_grid_view(filtered_docs)
    elif view_mode == "Compact":
        render_compact_cards(filtered_docs)
    elif view_mode == "Minimal":
        render_minimal_list(filtered_docs)

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

def render_card_view(docs):
    """Render documents in full card format."""
    
    for i, doc in enumerate(docs):
        with st.container():
            # Create card with enhanced styling
            card_html = f"""
            <div style="background: white; border: 1px solid #e0e0e0; border-radius: 12px; padding: 20px; margin: 15px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); transition: all 0.3s ease;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <h3 style="margin: 0; color: #2c3e50; font-size: 18px; font-weight: 600; line-height: 1.3;">
                        {ultra_clean_metadata(doc[1])}
                    </h3>
                    <span style="background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 4px 8px; border-radius: 8px; font-size: 12px; font-weight: 500;">
                        {get_document_topic(doc)}
                    </span>
                </div>
                
                <div style="margin: 12px 0; color: #7f8c8d; font-size: 14px;">
                    <strong>Organization:</strong> {ultra_clean_metadata(doc[9])} | 
                    <strong>Date:</strong> {clean_date_safely(doc)} |
                    <strong>Region:</strong> {ultra_clean_metadata(doc[13])}
                </div>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Add scoring badges
            col1, col2 = st.columns([3, 1])
            
            with col1:
                badges_html = ""
                badges_html += get_comprehensive_badge(doc[4], "ai_cybersecurity", doc[2], doc[1])
                badges_html += get_comprehensive_badge(doc[5], "quantum_cybersecurity", doc[2], doc[1])
                badges_html += get_comprehensive_badge(doc[6], "ai_ethics", doc[2], doc[1])
                badges_html += get_comprehensive_badge(doc[7], "quantum_ethics", doc[2], doc[1])
                
                st.markdown(badges_html, unsafe_allow_html=True)
            
            with col2:
                if st.button(f"📄 View Details", key=f"details_{doc[0]}"):
                    st.session_state[f'show_details_{doc[0]}'] = not st.session_state.get(f'show_details_{doc[0]}', False)
            
            # Show expandable details
            if st.session_state.get(f'show_details_{doc[0]}', False):
                with st.expander("📋 Document Details", expanded=True):
                    st.markdown(f"**URL:** {ultra_clean_metadata(doc[8])}")
                    st.markdown(f"**Author:** {ultra_clean_metadata(doc[12])}")
                    st.markdown(f"**Document Type:** {ultra_clean_metadata(doc[10])}")
                    
                    if doc[2]:  # content preview
                        preview = str(doc[2])[:300] + "..." if len(str(doc[2])) > 300 else str(doc[2])
                        st.markdown(f"**Content Preview:** {preview}")
            
            # Add click handlers for scoring analysis
            for framework, score in [
                ("ai_cybersecurity", doc[4]),
                ("quantum_cybersecurity", doc[5]), 
                ("ai_ethics", doc[6]),
                ("quantum_ethics", doc[7])
            ]:
                if st.session_state.get(f'show_{framework}_{doc[0]}', False):
                    show_score_explanation(framework, score, doc[2], doc[1])

def render_minimal_list(docs):
    """Render documents in minimal list format."""
    for doc in docs:
        col1, col2, col3 = st.columns([4, 2, 1])
        
        with col1:
            st.markdown(f"**{ultra_clean_metadata(doc[1])}**")
            st.caption(f"{ultra_clean_metadata(doc[9])} • {clean_date_safely(doc)}")
        
        with col2:
            badges_html = ""
            badges_html += get_comprehensive_badge(doc[4], "ai_cybersecurity")
            badges_html += get_comprehensive_badge(doc[6], "ai_ethics")
            st.markdown(badges_html, unsafe_allow_html=True)
        
        with col3:
            topic_color = {
                "AI": "#3498db", "Quantum": "#9b59b6", 
                "Both": "#e74c3c", "Cybersecurity": "#f39c12", "General": "#95a5a6"
            }
            topic = get_document_topic(doc)
            st.markdown(f'<span style="background: {topic_color.get(topic, "#95a5a6")}; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px;">{topic}</span>', unsafe_allow_html=True)

def render_compact_cards(docs):
    """Render documents in compact card format."""
    for doc in docs:
        st.markdown(f"""
        <div style="background: #f8f9fa; border-left: 4px solid #007bff; padding: 12px; margin: 8px 0; border-radius: 8px;">
            <div style="font-weight: 600; color: #495057; margin-bottom: 4px;">{ultra_clean_metadata(doc[1])}</div>
            <div style="font-size: 12px; color: #6c757d;">{ultra_clean_metadata(doc[9])} • {clean_date_safely(doc)}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Compact badges
        badges_html = ""
        badges_html += get_comprehensive_badge(doc[4], "ai_cybersecurity")
        badges_html += get_comprehensive_badge(doc[5], "quantum_cybersecurity")
        badges_html += get_comprehensive_badge(doc[6], "ai_ethics")  
        badges_html += get_comprehensive_badge(doc[7], "quantum_ethics")
        st.markdown(badges_html, unsafe_allow_html=True)

def render_grid_view(docs):
    """Render documents in grid layout."""
    cols = st.columns(3)
    
    for i, doc in enumerate(docs):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 8px 0; height: 200px; overflow: hidden;">
                <h4 style="margin: 0 0 8px 0; font-size: 14px; line-height: 1.2;">{ultra_clean_metadata(doc[1])[:50]}...</h4>
                <p style="font-size: 12px; color: #6c757d; margin: 4px 0;">{ultra_clean_metadata(doc[9])}</p>
                <p style="font-size: 11px; color: #adb5bd;">{clean_date_safely(doc)}</p>
            </div>
            """, unsafe_allow_html=True)

def render_table_view(docs):
    """Render documents in table format."""
    
    # Create table data
    table_data = []
    for doc in docs:
        table_data.append({
            "Title": ultra_clean_metadata(doc[1])[:50] + "..." if len(ultra_clean_metadata(doc[1])) > 50 else ultra_clean_metadata(doc[1]),
            "Organization": ultra_clean_metadata(doc[9]),
            "Date": clean_date_safely(doc),
            "AI Cyber": str(doc[4]) if doc[4] else "N/A",
            "Q Cyber": str(doc[5]) if doc[5] else "N/A", 
            "AI Ethics": str(doc[6]) if doc[6] else "N/A",
            "Q Ethics": str(doc[7]) if doc[7] else "N/A",
            "Topic": get_document_topic(doc)
        })
    
    # Display as dataframe
    st.dataframe(table_data, use_container_width=True)

# Additional helper functions remain the same...
if __name__ == "__main__":
    render()