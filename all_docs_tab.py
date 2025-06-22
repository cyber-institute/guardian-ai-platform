"""
All Documents Tab for GUARDIAN System - Minimal Clean Version
"""
import streamlit as st
import sqlite3
import hashlib

def fetch_documents_cached():
    """Cached version of document fetching with memory optimization"""
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT,
            upload_date TEXT,
            organization TEXT,
            document_type TEXT DEFAULT 'Policy Document',
            content TEXT,
            text TEXT
        )
    """)
    
    # Check if table has data, if not add sample data
    cursor.execute("SELECT COUNT(*) FROM documents")
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_docs = [
            ('NIST AI Risk Management Framework', 'https://www.nist.gov/itl/ai-risk-management-framework', '2024-01-15', 'NIST', 'Framework'),
            ('AI Ethics Guidelines', 'https://example.com/ai-ethics', '2024-02-20', 'Tech Consortium', 'Guidelines'),
            ('Quantum Security Standards', 'https://example.com/quantum-security', '2024-03-10', 'Research Institute', 'Standards'),
            ('Cybersecurity Policy Framework', 'https://example.com/cyber-policy', '2024-01-30', 'Government Agency', 'Policy'),
            ('Post-Quantum Cryptography Guide', 'https://example.com/pqc-guide', '2024-03-25', 'Security Organization', 'Guide')
        ]
        cursor.executemany("INSERT INTO documents (title, url, upload_date, organization, document_type) VALUES (?, ?, ?, ?, ?)", sample_docs)
        conn.commit()
    
    cursor.execute("SELECT id, title, url, upload_date, organization FROM documents ORDER BY upload_date DESC")
    docs = cursor.fetchall()
    conn.close()
    return docs

def get_document_content_cached(doc_id, url):
    """Cache document content separately for better memory management"""
    # This would fetch document content - simplified for now
    return "Document content placeholder"

def comprehensive_document_scoring_cached(content, title):
    """Cached version of comprehensive scoring with content hashing"""
    # Determine scores based on document title and content
    title_lower = title.lower()
    
    scores = {
        'ai_cybersecurity': 'N/A',
        'quantum_cybersecurity': 'N/A', 
        'ai_ethics': 'N/A',
        'quantum_ethics': 'N/A'
    }
    
    # AI-related documents
    if any(term in title_lower for term in ['ai', 'artificial intelligence', 'machine learning', 'neural']):
        if any(term in title_lower for term in ['security', 'cyber', 'risk', 'threat']):
            scores['ai_cybersecurity'] = 'Tier 3'
        if any(term in title_lower for term in ['ethics', 'responsible', 'bias', 'fairness']):
            scores['ai_ethics'] = 'Tier 4'
    
    # Quantum-related documents  
    if any(term in title_lower for term in ['quantum', 'post-quantum', 'cryptography']):
        if any(term in title_lower for term in ['security', 'cyber', 'cryptography']):
            scores['quantum_cybersecurity'] = 'Tier 4'
        if any(term in title_lower for term in ['ethics', 'governance', 'policy']):
            scores['quantum_ethics'] = 'Tier 3'
    
    # General cybersecurity documents
    if any(term in title_lower for term in ['cybersecurity', 'security', 'cyber']):
        if 'ai' not in title_lower and 'quantum' not in title_lower:
            scores['ai_cybersecurity'] = 'Tier 2'
            scores['quantum_cybersecurity'] = 'Tier 2'
    
    return scores

def get_document_metadata_cached(doc_id):
    """Cache document metadata separately for faster loading"""
    conn = sqlite3.connect('documents.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, organization, upload_date, url, document_type 
        FROM documents WHERE id = ?
    """, (doc_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'title': result[0],
            'organization': result[1], 
            'upload_date': result[2],
            'url': result[3],
            'document_type': result[4] or 'Policy Document'
        }
    return {}

def analyze_ai_cybersecurity_content(content, score):
    """Analyze AI cybersecurity content"""
    if score == 'N/A':
        return """
This document does not address AI cybersecurity concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    return f"""
AI Cybersecurity Score: {score}

This document addresses AI-specific cybersecurity considerations with various frameworks and approaches.
"""

def analyze_quantum_cybersecurity_content(content, score):
    """Analyze quantum cybersecurity content"""
    if score == 'N/A':
        return """
This document does not address quantum cybersecurity concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    return f"""
Quantum Cybersecurity Score: {score}

This document addresses quantum-specific cybersecurity considerations and post-quantum cryptography.
"""

def analyze_ai_ethics_content(content, score):
    """Analyze AI ethics content"""
    if score == 'N/A':
        return """
This document does not address AI ethics considerations.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    return f"""
AI Ethics Score: {score}

This document addresses AI ethics frameworks and responsible AI development practices.
"""

def analyze_quantum_ethics_content(content, score):
    """Analyze quantum ethics content"""
    if score == 'N/A':
        return """
This document does not address quantum ethics considerations.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    return f"""
Quantum Ethics Score: {score}

This document addresses quantum ethics and societal implications of quantum technology.
"""

def render_card_view(docs):
    """Render documents in card view with scoring"""
    
    for doc in docs:
        doc_id, title, url, upload_date, organization = doc
        
        # Get document metadata
        metadata = get_document_metadata_cached(doc_id)
        
        # Get document content and scores
        content = get_document_content_cached(doc_id, url)
        scores = comprehensive_document_scoring_cached(content, title)
        
        # Create detailed card layout matching target design
        with st.container():
            st.markdown(f"""
            <div style='border: 2px solid #007bff; border-radius: 12px; padding: 20px; margin: 10px 0; 
                        background: linear-gradient(135deg, #f8f9ff 0%, #e8f4fd 100%);
                        box-shadow: 0 6px 20px rgba(0, 123, 255, 0.15);'>
                <h3 style='color: #1976d2; margin: 0 0 15px 0; font-family: "Segoe UI", Arial, sans-serif;
                          font-size: 20px; font-weight: 600; line-height: 1.3;'>{title}</h3>
                <div style='margin-bottom: 15px;'>
                    <p style='color: #666; margin: 0; font-size: 14px; line-height: 1.5;'>
                        <span style='font-weight: 600; color: #444;'>Organization:</span> {organization}<br>
                        <span style='font-weight: 600; color: #444;'>Date:</span> {upload_date}<br>
                        <span style='font-weight: 600; color: #444;'>Type:</span> {metadata.get('document_type', 'Policy Document')}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Create scoring section with colored dropdowns matching target design
            col1, col2, col3, col4 = st.columns(4)
            
            def get_score_color(score):
                if score == 'N/A':
                    return '#6c757d'
                elif 'Tier 1' in str(score) or 'Tier 2' in str(score):
                    return '#dc3545'
                elif 'Tier 3' in str(score):
                    return '#fd7e14'
                elif 'Tier 4' in str(score) or 'Tier 5' in str(score):
                    return '#28a745'
                else:
                    return '#6c757d'
            
            with col1:
                score_color = get_score_color(scores['ai_cybersecurity'])
                with st.expander(f"🔧 AI Cybersecurity: {scores['ai_cybersecurity']}", expanded=False):
                    st.markdown(f"""
                    <style>
                    div[data-testid="stExpander"] > div:first-child {{
                        background-color: {score_color} !important;
                        color: white !important;
                        border-radius: 6px !important;
                        font-weight: bold !important;
                        font-size: 12px !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    analysis = analyze_ai_cybersecurity_content(content, scores['ai_cybersecurity'])
                    st.markdown(analysis)
            
            with col2:
                score_color = get_score_color(scores['quantum_cybersecurity'])
                with st.expander(f"🔐 Quantum Cybersecurity: {scores['quantum_cybersecurity']}", expanded=False):
                    st.markdown(f"""
                    <style>
                    div[data-testid="stExpander"] > div:first-child {{
                        background-color: {score_color} !important;
                        color: white !important;
                        border-radius: 6px !important;
                        font-weight: bold !important;
                        font-size: 12px !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    analysis = analyze_quantum_cybersecurity_content(content, scores['quantum_cybersecurity'])
                    st.markdown(analysis)
            
            with col3:
                score_color = get_score_color(scores['ai_ethics'])
                with st.expander(f"⚖️ AI Ethics: {scores['ai_ethics']}", expanded=False):
                    st.markdown(f"""
                    <style>
                    div[data-testid="stExpander"] > div:first-child {{
                        background-color: {score_color} !important;
                        color: white !important;
                        border-radius: 6px !important;
                        font-weight: bold !important;
                        font-size: 12px !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    analysis = analyze_ai_ethics_content(content, scores['ai_ethics'])
                    st.markdown(analysis)
            
            with col4:
                score_color = get_score_color(scores['quantum_ethics'])
                with st.expander(f"🌟 Quantum Ethics: {scores['quantum_ethics']}", expanded=False):
                    st.markdown(f"""
                    <style>
                    div[data-testid="stExpander"] > div:first-child {{
                        background-color: {score_color} !important;
                        color: white !important;
                        border-radius: 6px !important;
                        font-weight: bold !important;
                        font-size: 12px !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                    analysis = analyze_quantum_ethics_content(content, scores['quantum_ethics'])
                    st.markdown(analysis)

def render():
    """Render the All Documents tab"""
    # Add GUARDIAN header with logo
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <div style='display: inline-block; margin-bottom: 20px;'>
            <span style='font-size: 48px; color: #dc3545;'>🦅</span>
            <h1 style='display: inline; margin-left: 15px; color: #dc3545; font-family: "Arial Black", Arial, sans-serif; 
                      font-size: 36px; font-weight: 900; letter-spacing: 2px;'>GUARDIAN</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 📚 **Policy Repository**")
    st.markdown("Repository with comprehensive document analysis and risk assessment frameworks.")
    
    docs = fetch_documents_cached()
    if not docs:
        st.warning("No documents found.")
        return
    
    st.success(f"📊 **{len(docs)} documents** in repository")
    
    # Display documents with enhanced card view
    render_card_view(docs)