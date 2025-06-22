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
        
        # Create card layout
        with st.container():
            st.markdown(f"""
            <div style='border:1px solid #007bff;padding:20px;border-radius:12px;margin:8px;
                        background:linear-gradient(135deg, #f8f9ff 0%, #e3f2fd 100%);
                        box-shadow:0 4px 12px rgba(0,123,255,0.15);'>
                <h3 style='color:#1976d2;margin:0 0 12px 0;font-family:"Segoe UI",sans-serif;
                          font-size:18px;font-weight:600;'>{title}</h3>
                <p style='color:#666;margin:4px 0;font-size:14px;'>
                    <strong>Organization:</strong> {organization}<br>
                    <strong>Date:</strong> {upload_date}<br>
                    <strong>Type:</strong> {metadata.get('document_type', 'Policy Document')}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Scoring section
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button(f"AI Cyber: {scores['ai_cybersecurity']}", key=f"ai_cyber_{doc_id}"):
                    with st.expander("🤖 AI Cybersecurity Analysis", expanded=True):
                        analysis = analyze_ai_cybersecurity_content(content, scores['ai_cybersecurity'])
                        st.markdown(analysis)
            
            with col2:
                if st.button(f"Q Cyber: {scores['quantum_cybersecurity']}", key=f"q_cyber_{doc_id}"):
                    with st.expander("🔐 Quantum Cybersecurity Analysis", expanded=True):
                        analysis = analyze_quantum_cybersecurity_content(content, scores['quantum_cybersecurity'])
                        st.markdown(analysis)
            
            with col3:
                if st.button(f"AI Ethics: {scores['ai_ethics']}", key=f"ai_ethics_{doc_id}"):
                    with st.expander("⚖️ AI Ethics Analysis", expanded=True):
                        analysis = analyze_ai_ethics_content(content, scores['ai_ethics'])
                        st.markdown(analysis)
            
            with col4:
                if st.button(f"Q Ethics: {scores['quantum_ethics']}", key=f"q_ethics_{doc_id}"):
                    with st.expander("🌟 Quantum Ethics Analysis", expanded=True):
                        analysis = analyze_quantum_ethics_content(content, scores['quantum_ethics'])
                        st.markdown(analysis)

def render():
    """Render the All Documents tab"""
    st.markdown("## 📚 **Policy Repository**")
    
    docs = fetch_documents_cached()
    if not docs:
        st.warning("No documents found.")
        return
    
    st.success(f"📊 **{len(docs)} documents** in repository")
    
    # Display documents with card view
    render_card_view(docs)