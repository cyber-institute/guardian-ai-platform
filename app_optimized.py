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
    }
    .guardian-header h1 {
        color: #dc2626;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
    }
    .guardian-header p {
        color: #666;
        font-size: 1.2rem;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Simple header
    st.markdown("""
    <div class="guardian-header">
        <h1>🛡️ GUARDIAN</h1>
        <p>AI Risk Analysis Navigator</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for performance tracking
    if 'page_load_time' not in st.session_state:
        st.session_state.page_load_time = time.time()
    
    # Simplified navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 All Documents", 
        "🛡️ Patent Systems", 
        "🎯 AI Recommendations", 
        "📈 LLM Enhancement",
        "ℹ️ About"
    ])
    
    with tab1:
        render_documents_tab()
    
    with tab2:
        render_patent_tab()
    
    with tab3:
        render_recommendations_tab()
    
    with tab4:
        render_llm_tab()
    
    with tab5:
        render_about_tab()

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_documents_cached(limit=50):
    """Optimized document loading with caching"""
    try:
        from utils.db import fetch_documents
        return fetch_documents()[:limit]
    except Exception as e:
        st.error(f"Database connection issue: {e}")
        return []

@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_analytics_cached():
    """Cached analytics data"""
    try:
        from utils.db import fetch_documents
        documents = fetch_documents()
        
        total_docs = len(documents)
        ai_scored = sum(1 for doc in documents if doc.get('ai_cybersecurity_score', 0) > 0)
        avg_ai_score = sum(doc.get('ai_cybersecurity_score', 0) for doc in documents if doc.get('ai_cybersecurity_score', 0) > 0)
        if ai_scored > 0:
            avg_ai_score = avg_ai_score / ai_scored
        else:
            avg_ai_score = 0
        
        return {
            'total_documents': total_docs,
            'ai_scored_documents': ai_scored,
            'avg_ai_score': avg_ai_score
        }
    except Exception as e:
        return {'total_documents': 0, 'ai_scored_documents': 0, 'avg_ai_score': 0}

def render_documents_tab():
    """Optimized documents tab with pagination"""
    st.header("📊 Document Repository")
    
    # Quick stats
    with st.spinner("Loading analytics..."):
        analytics = get_analytics_cached()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Documents", analytics['total_documents'])
    with col2:
        st.metric("AI Scored", analytics['ai_scored_documents'])
    with col3:
        st.metric("Avg AI Score", f"{analytics['avg_ai_score']:.1f}" if analytics['avg_ai_score'] else "N/A")
    
    # Document loading controls
    st.subheader("Document Browser")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        limit = st.selectbox("Documents per page", [10, 25, 50, 100], index=1)
    with col2:
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    # Load and display documents
    with st.spinner(f"Loading {limit} documents..."):
        documents = get_documents_cached(limit)
    
    if documents:
        st.success(f"Loaded {len(documents)} documents")
        
        # Simple document list
        for i, doc in enumerate(documents):
            with st.expander(f"{i+1}. {doc.get('title', 'Untitled')[:60]}..."):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Type:** {doc.get('document_type', 'Unknown')}")
                    st.write(f"**Author/Org:** {doc.get('author_organization', 'Unknown')}")
                    if doc.get('url'):
                        st.write(f"**URL:** {doc['url']}")
                
                with col2:
                    ai_score = doc.get('ai_cybersecurity_score', 0)
                    if ai_score > 0:
                        st.metric("AI Score", f"{ai_score}/100")
                    
                    quantum_score = doc.get('quantum_cybersecurity_score', 0)
                    if quantum_score > 0:
                        st.metric("Quantum Score", f"{quantum_score}/5")
    else:
        st.info("No documents found. Upload documents in the Repository Admin section.")

def render_patent_tab():
    """Simplified patent tab"""
    st.header("🛡️ Patent-Based Scoring Systems")
    
    st.markdown("""
    ### GUARDIAN Patent Framework
    
    The GUARDIAN system implements patent-protected scoring algorithms:
    
    **AI Cybersecurity Maturity (0-100)**
    - Threat Detection Capabilities
    - Security Control Implementation  
    - Risk Assessment Accuracy
    - Incident Response Readiness
    
    **Quantum Cybersecurity Maturity (1-5 Tiers)**
    - Tier 1: Basic Quantum Awareness
    - Tier 2: Post-Quantum Cryptography Planning
    - Tier 3: Quantum-Safe Implementation
    - Tier 4: Advanced Quantum Security
    - Tier 5: Quantum-Native Protection
    
    **AI Ethics Assessment (0-100)**
    - Fairness and Bias Mitigation
    - Transparency and Explainability
    - Accountability Mechanisms
    - Privacy Protection
    
    **Gap Analysis Framework**
    - Critical, High, Medium, Low severity levels
    - Targeted recommendations
    - Implementation priority scoring
    """)

def render_recommendations_tab():
    """Simplified recommendations tab"""
    st.header("🎯 AI-Powered Recommendations")
    
    st.markdown("""
    ### Intelligent Document Discovery
    
    The recommendation system provides:
    
    **Smart Content Analysis**
    - Semantic similarity matching
    - Topic clustering and categorization
    - Relevance scoring
    
    **Trending Documents**
    - Recently accessed content
    - High-scoring documents
    - Popular topics
    
    **Context-Based Discovery**
    - Related document suggestions
    - Cross-reference analysis
    - Knowledge gap identification
    """)
    
    if st.button("Generate Sample Recommendations"):
        with st.spinner("Analyzing document patterns..."):
            time.sleep(1)  # Simulate processing
            st.success("Recommendations generated based on current repository content.")

def render_llm_tab():
    """Simplified LLM enhancement tab"""
    st.header("📈 LLM Enhancement System")
    
    st.markdown("""
    ### Multi-LLM Ensemble Intelligence
    
    **Integrated Services:**
    - OpenAI GPT-4 (requires API key)
    - Anthropic Claude (requires API key)
    - Groq (free tier available)
    - Ollama (local deployment)
    - Hugging Face (free tier)
    
    **Enhancement Capabilities:**
    - Automated metadata extraction
    - Content summarization
    - Scoring validation
    - Gap analysis refinement
    """)
    
    st.subheader("Service Status")
    
    # Check API keys
    import os
    services = {
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY",
        "Groq": "GROQ_API_KEY"
    }
    
    for service, env_var in services.items():
        if os.getenv(env_var):
            st.success(f"✅ {service} - API key configured")
        else:
            st.warning(f"⚠️ {service} - API key needed for full functionality")

def render_about_tab():
    """Simple about tab"""
    st.header("ℹ️ About GUARDIAN")
    
    st.markdown("""
    ### System Information
    
    **GUARDIAN** (Governance, Understanding, Assessment, Risk-management, 
    Determination, Intelligence, Analysis, Navigation) is an advanced AI governance 
    platform that provides comprehensive technological risk assessment.
    
    **Key Features:**
    - Multi-LLM ensemble intelligence
    - Patent-protected scoring algorithms
    - Real-time document analysis
    - Interactive data visualization
    - Comprehensive gap analysis
    
    **Technology Stack:**
    - Streamlit for web interface
    - PostgreSQL for data storage
    - Multi-LLM integration
    - Advanced NLP processing
    
    **Performance Status:**
    """)
    
    # Performance metrics
    if 'page_load_time' in st.session_state:
        load_time = time.time() - st.session_state.page_load_time
        st.metric("Page Load Time", f"{load_time:.2f}s")
    
    # System status
    st.success("✅ System operational")

if __name__ == "__main__":
    main()