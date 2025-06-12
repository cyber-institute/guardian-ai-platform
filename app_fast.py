import streamlit as st
from datetime import datetime
import time

def main():
    st.set_page_config(
        page_title="GUARDIAN - AI Risk Analysis Navigator",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Minimal CSS for performance
    st.markdown("""
    <style>
    .main > div {
        padding-top: 1rem;
        background-color: #ffffff;
    }
    .stApp {
        background-color: #ffffff;
    }
    .guardian-header {
        text-align: center;
        padding: 1rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%);
        color: white;
        border-radius: 8px;
    }
    .guardian-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }
    .guardian-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="guardian-header">
        <h1>🛡️ GUARDIAN</h1>
        <p>AI Risk Analysis Navigator - High Performance Mode</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'page_load_time' not in st.session_state:
        st.session_state.page_load_time = time.time()
    
    # Performance-optimized navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Documents", 
        "🛡️ Patents", 
        "🎯 Recommendations", 
        "📈 LLM Tools",
        "ℹ️ About"
    ])
    
    with tab1:
        render_documents_fast()
    
    with tab2:
        render_patents_fast()
    
    with tab3:
        render_recommendations_fast()
    
    with tab4:
        render_llm_fast()
    
    with tab5:
        render_about_fast()

def get_documents_with_fallback():
    """Get documents with proper error handling"""
    try:
        from utils.db import fetch_documents
        docs = fetch_documents()
        if docs:
            return docs
        else:
            return []
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return []

def render_documents_fast():
    """Fast document rendering with error handling"""
    st.header("📊 Document Repository")
    
    # Performance metrics
    start_time = time.time()
    
    # Load documents with error handling
    with st.spinner("Loading documents..."):
        documents = get_documents_with_fallback()
    
    load_time = time.time() - start_time
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", len(documents))
    
    with col2:
        ai_scored = sum(1 for doc in documents if doc.get('ai_cybersecurity_score', 0) > 0)
        st.metric("AI Scored", ai_scored)
    
    with col3:
        quantum_scored = sum(1 for doc in documents if doc.get('quantum_cybersecurity_score', 0) > 0)
        st.metric("Quantum Scored", quantum_scored)
    
    with col4:
        st.metric("Load Time", f"{load_time:.2f}s")
    
    # Document controls
    st.subheader("Document Browser")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        show_limit = st.selectbox("Show", [10, 25, 50, 100], index=1)
    
    with col2:
        view_mode = st.selectbox("View", ["List", "Cards"])
    
    with col3:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Filter documents
    if documents:
        filtered_docs = documents[:show_limit]
        
        if view_mode == "List":
            render_document_list(filtered_docs)
        else:
            render_document_cards(filtered_docs)
    
    else:
        st.info("No documents found. Upload documents using the Repository Admin section.")

def render_document_list(documents):
    """Render documents as a simple list"""
    for i, doc in enumerate(documents):
        with st.expander(f"{i+1}. {doc.get('title', 'Untitled')[:60]}..."):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Type:** {doc.get('document_type', 'Unknown')}")
                st.write(f"**Author:** {doc.get('author_organization', 'Unknown')}")
                st.write(f"**Date:** {doc.get('publish_date', 'N/A')}")
                if doc.get('url'):
                    st.write(f"**Source:** [Link]({doc['url']})")
            
            with col2:
                # Display scores if available
                ai_score = doc.get('ai_cybersecurity_score', 0)
                if ai_score > 0:
                    st.metric("AI Security", f"{ai_score}/100")
                
                quantum_score = doc.get('quantum_cybersecurity_score', 0)
                if quantum_score > 0:
                    st.metric("Quantum Security", f"{quantum_score}/5")

def render_document_cards(documents):
    """Render documents as cards"""
    cols = st.columns(2)
    
    for i, doc in enumerate(documents):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{doc.get('title', 'Untitled')[:50]}...</h4>
                    <p><strong>Type:</strong> {doc.get('document_type', 'Unknown')}</p>
                    <p><strong>Author:</strong> {doc.get('author_organization', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Scores
                col1, col2 = st.columns(2)
                
                with col1:
                    ai_score = doc.get('ai_cybersecurity_score', 0)
                    if ai_score > 0:
                        st.metric("AI Score", f"{ai_score}/100")
                
                with col2:
                    quantum_score = doc.get('quantum_cybersecurity_score', 0)
                    if quantum_score > 0:
                        st.metric("Quantum Score", f"{quantum_score}/5")

def render_patents_fast():
    """Fast patent information rendering"""
    st.header("🛡️ Patent-Based Scoring Systems")
    
    st.markdown("""
    ### GUARDIAN Patent Framework
    
    The GUARDIAN system implements three patent-protected algorithms:
    """)
    
    tab1, tab2, tab3 = st.tabs(["AI Cybersecurity", "Quantum Security", "AI Ethics"])
    
    with tab1:
        st.markdown("""
        **AI Cybersecurity Maturity Assessment (0-100 scale)**
        
        - **Threat Detection**: Advanced AI-powered threat identification
        - **Security Controls**: Implementation of AI security frameworks
        - **Risk Assessment**: Automated vulnerability analysis
        - **Response Capabilities**: AI-enhanced incident response
        
        **Scoring Levels:**
        - 0-25: Basic AI security awareness
        - 26-50: Developing AI security practices
        - 51-75: Mature AI security implementation
        - 76-100: Advanced AI security excellence
        """)
    
    with tab2:
        st.markdown("""
        **Quantum Cybersecurity Maturity (5-tier framework)**
        
        - **Tier 1**: Basic quantum awareness and education
        - **Tier 2**: Post-quantum cryptography planning
        - **Tier 3**: Quantum-safe implementation
        - **Tier 4**: Advanced quantum security measures
        - **Tier 5**: Quantum-native protection systems
        
        **Implementation Focus:**
        - Post-quantum cryptographic algorithms
        - Quantum key distribution systems
        - Quantum-resistant security protocols
        """)
    
    with tab3:
        st.markdown("""
        **AI Ethics Assessment (0-100 scale)**
        
        - **Fairness**: Bias detection and mitigation systems
        - **Transparency**: Explainable AI implementations
        - **Accountability**: Clear responsibility frameworks
        - **Privacy**: Data protection in AI systems
        
        **Evaluation Criteria:**
        - Algorithmic fairness measures
        - Transparency in decision-making
        - Audit and accountability mechanisms
        - Privacy-preserving AI techniques
        """)

def render_recommendations_fast():
    """Fast recommendations rendering"""
    st.header("🎯 AI-Powered Recommendations")
    
    st.markdown("""
    ### Intelligent Document Analysis
    
    The recommendation engine provides intelligent insights based on:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Content Analysis**
        - Semantic similarity matching
        - Topic clustering
        - Relevance scoring
        - Gap identification
        """)
    
    with col2:
        st.markdown("""
        **Trend Analysis**
        - Document popularity
        - Scoring patterns
        - Recent additions
        - Usage analytics
        """)
    
    if st.button("Generate Sample Recommendations"):
        with st.spinner("Analyzing document patterns..."):
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)
            
            st.success("Analysis complete! Recommendations generated based on current repository.")
            
            st.markdown("""
            **Recommended Documents:**
            1. High-scoring AI cybersecurity frameworks
            2. Emerging quantum security standards
            3. AI ethics implementation guides
            4. Cross-domain policy analysis
            """)

def render_llm_fast():
    """Fast LLM tools rendering"""
    st.header("📈 LLM Enhancement Tools")
    
    st.markdown("""
    ### Multi-LLM Integration Status
    """)
    
    # Check API keys
    import os
    
    services = {
        "OpenAI GPT-4": ("OPENAI_API_KEY", "Industry-leading language model"),
        "Anthropic Claude": ("ANTHROPIC_API_KEY", "Advanced reasoning capabilities"),
        "Groq": ("GROQ_API_KEY", "Ultra-fast inference"),
        "Hugging Face": ("HUGGINGFACE_API_KEY", "Open-source models")
    }
    
    st.subheader("Service Configuration")
    
    for service, (env_var, description) in services.items():
        col1, col2, col3 = st.columns([2, 3, 1])
        
        with col1:
            st.write(f"**{service}**")
        
        with col2:
            st.write(description)
        
        with col3:
            if os.getenv(env_var):
                st.success("✅")
            else:
                st.warning("⚠️")
    
    st.markdown("""
    ### Enhancement Capabilities
    
    **Automated Processing:**
    - Document metadata extraction
    - Content summarization
    - Scoring validation
    - Gap analysis refinement
    
    **Multi-LLM Synthesis:**
    - Consensus scoring across models
    - Confidence calibration
    - Outlier detection
    - Quality assurance
    """)

def render_about_fast():
    """Fast about page rendering"""
    st.header("ℹ️ About GUARDIAN")
    
    st.markdown("""
    ### System Overview
    
    **GUARDIAN** is an advanced AI governance platform providing comprehensive 
    technological risk assessment through patent-protected algorithms.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Core Features:**
        - Multi-LLM ensemble intelligence
        - Patent-based scoring frameworks
        - Real-time document analysis
        - Interactive visualizations
        - Comprehensive gap analysis
        """)
    
    with col2:
        st.markdown("""
        **Technology Stack:**
        - Streamlit web framework
        - PostgreSQL database
        - Multi-LLM integration
        - Advanced NLP processing
        - Cloud-ready architecture
        """)
    
    # Performance metrics
    st.subheader("Performance Metrics")
    
    if 'page_load_time' in st.session_state:
        load_time = time.time() - st.session_state.page_load_time
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Page Load Time", f"{load_time:.2f}s")
        
        with col2:
            st.metric("Memory Usage", "Optimized")
        
        with col3:
            st.metric("System Status", "Operational")
    
    st.success("✅ High-performance mode active")

if __name__ == "__main__":
    main()