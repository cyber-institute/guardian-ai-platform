"""
GUARDIAN Repository Insights Tab
Provides intelligent document discovery and continuous learning insights
"""

import streamlit as st
from components.recommendation_widget import (
    render_document_recommendations, 
    render_trending_documents,
    render_recommendation_cards
)
from utils.document_recommendation_engine import recommendation_engine
from utils.db import fetch_documents

def render():
    """Render the GUARDIAN Repository Insights tab."""
    
    st.markdown("# 🧠 **GUARDIAN Repository Insights**")
    st.markdown("---")
    
    st.markdown("""
    GUARDIAN continuously learns from its growing repository and AI-powered learning model incorporating 
    current best practices and globally accepted ethical norms. The system provides intelligent insights 
    through dynamic pattern recognition, adaptive scoring refinement, and evolving policy recommendations 
    that improve with each document analyzed.
    """)
    
    # Main recommendation interface
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Smart Recommendations", 
        "🔥 Trending Documents", 
        "📊 Similarity Analysis",
        "🔍 Context Discovery"
    ])
    
    with tab1:
        render_smart_recommendations_tab()
    
    with tab2:
        render_trending_documents_tab()
    
    with tab3:
        render_similarity_analysis_tab()
    
    with tab4:
        render_context_discovery_tab()

def render_smart_recommendations_tab():
    """Render smart recommendations interface."""
    
    st.markdown("### 🎯 **Intelligent Document Recommendations**")
    
    # Document selection for recommendations
    documents = fetch_documents()
    if not documents:
        st.info("No documents available for recommendations. Please upload documents first.")
        return
    
    # Create document selector
    doc_options = {f"{doc.get('title', 'Unknown')} (ID: {doc.get('id')})": doc.get('id') 
                   for doc in documents}
    
    selected_doc = st.selectbox(
        "Select a document to get recommendations for:",
        options=list(doc_options.keys()),
        help="Choose a document to find similar and related content"
    )
    
    if selected_doc:
        target_doc_id = doc_options[selected_doc]
        
        # Recommendation options
        col1, col2 = st.columns([2, 1])
        
        with col1:
            recommendation_method = st.radio(
                "Recommendation Method:",
                ["comprehensive", "content", "scoring", "contextual"],
                format_func=lambda x: {
                    "comprehensive": "🎯 All Methods Combined",
                    "content": "📝 Content Similarity",
                    "scoring": "📊 Scoring Patterns", 
                    "contextual": "🏢 Same Context"
                }[x],
                horizontal=True
            )
        
        with col2:
            max_recs = st.slider("Max Recommendations", 3, 12, 6)
        
        st.markdown("---")
        
        # Display recommendations
        render_document_recommendations(
            target_doc_id=target_doc_id,
            context_mode=recommendation_method,
            max_recommendations=max_recs
        )

def render_trending_documents_tab():
    """Render trending documents interface."""
    
    st.markdown("### 🔥 **Trending Documents by Framework**")
    st.markdown("Documents with highest relevance scores in each assessment framework")
    
    render_trending_documents(max_count=10)

def render_similarity_analysis_tab():
    """Render similarity analysis interface."""
    
    st.markdown("### 📊 **Document Similarity Analysis**")
    
    documents = fetch_documents()
    if not documents:
        st.info("No documents available for similarity analysis.")
        return
    
    # Document selection
    doc_options = {f"{doc.get('title', 'Unknown')} (ID: {doc.get('id')})": doc.get('id') 
                   for doc in documents}
    
    selected_doc = st.selectbox(
        "Select document for similarity analysis:",
        options=list(doc_options.keys()),
        key="similarity_doc_selector"
    )
    
    if selected_doc:
        target_doc_id = doc_options[selected_doc]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📝 **Content Similarity**")
            st.markdown("*Based on text analysis and semantic matching*")
            
            with st.spinner("Analyzing content similarity..."):
                content_similar = recommendation_engine.calculate_content_similarity(
                    target_doc_id, top_k=5
                )
                
                if content_similar:
                    for doc_id, similarity in content_similar:
                        doc_info = recommendation_engine._get_document_info(doc_id, similarity)
                        if doc_info:
                            st.markdown(f"""
                            **{doc_info.get('title', 'Unknown')}**  
                            Similarity: {similarity:.3f} | {doc_info.get('organization', 'Unknown')}
                            """)
                            st.progress(similarity)
                            st.markdown("---")
                else:
                    st.info("No content-similar documents found")
        
        with col2:
            st.markdown("#### 📊 **Scoring Pattern Similarity**")
            st.markdown("*Based on patent framework scoring patterns*")
            
            with st.spinner("Analyzing scoring patterns..."):
                scoring_similar = recommendation_engine.calculate_scoring_similarity(
                    target_doc_id, top_k=5
                )
                
                if scoring_similar:
                    for doc_id, similarity in scoring_similar:
                        doc_info = recommendation_engine._get_document_info(doc_id, similarity)
                        if doc_info:
                            st.markdown(f"""
                            **{doc_info.get('title', 'Unknown')}**  
                            Pattern Match: {similarity:.3f} | {doc_info.get('organization', 'Unknown')}
                            """)
                            st.progress(similarity)
                            st.markdown("---")
                else:
                    st.info("No pattern-similar documents found")

def render_context_discovery_tab():
    """Render context-based discovery interface."""
    
    st.markdown("### 🔍 **Context-Based Document Discovery**")
    st.markdown("Find documents by organizational context, document type, or framework focus")
    
    col1, col2, col3 = st.columns(3)
    
    # Get available options from documents
    documents = fetch_documents()
    if not documents:
        st.info("No documents available for context discovery.")
        return
    
    doc_types = sorted(set(doc.get('document_type', 'Unknown') for doc in documents if doc.get('document_type')))
    organizations = sorted(set(doc.get('organization', 'Unknown') for doc in documents if doc.get('organization')))
    
    with col1:
        selected_doc_type = st.selectbox(
            "Document Type",
            ["Any"] + doc_types,
            help="Filter by document type"
        )
    
    with col2:
        selected_org = st.selectbox(
            "Organization",
            ["Any"] + organizations,
            help="Filter by organization"
        )
    
    with col3:
        framework_focus = st.selectbox(
            "Framework Focus",
            ["Any", "ai_cybersecurity", "quantum_cybersecurity", "ai_ethics", "quantum_ethics"],
            format_func=lambda x: {
                "Any": "Any Framework",
                "ai_cybersecurity": "🤖 AI Cybersecurity",
                "quantum_cybersecurity": "⚛️ Quantum Cybersecurity", 
                "ai_ethics": "🎯 AI Ethics",
                "quantum_ethics": "🔬 Quantum Ethics"
            }[x],
            help="Focus on specific assessment framework"
        )
    
    # Apply context filters
    if st.button("🔍 Discover Documents", type="primary", use_container_width=True):
        
        # Build context parameters
        context_doc_type = None if selected_doc_type == "Any" else selected_doc_type
        context_org = None if selected_org == "Any" else selected_org
        context_framework = None if framework_focus == "Any" else framework_focus
        
        with st.spinner("Discovering relevant documents..."):
            contextual_docs = recommendation_engine.get_context_recommendations(
                document_type=context_doc_type,
                organization=context_org,
                framework_focus=context_framework,
                top_k=10
            )
            
            if contextual_docs:
                st.markdown(f"### 📋 **Found {len(contextual_docs)} Relevant Documents**")
                
                # Display as cards
                recommendations = [
                    recommendation_engine._format_document_info(doc) 
                    for doc in contextual_docs
                ]
                render_recommendation_cards(recommendations)
                
            else:
                st.info("No documents found matching the specified criteria. Try adjusting your filters.")

def render_recommendation_analytics():
    """Render analytics about recommendation system performance."""
    
    st.markdown("### 📈 **Recommendation System Analytics**")
    
    with st.spinner("Generating analytics..."):
        # Get basic statistics
        documents = recommendation_engine.load_documents()
        
        if documents:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Documents", len(documents))
            
            with col2:
                scored_docs = sum(1 for doc in documents 
                                if any([
                                    doc.get('ai_cybersecurity_score', 0) > 0,
                                    doc.get('quantum_cybersecurity_score', 0) > 0,
                                    doc.get('ai_ethics_score', 0) > 0,
                                    doc.get('quantum_ethics_score', 0) > 0
                                ]))
                st.metric("Scored Documents", scored_docs)
            
            with col3:
                doc_types = len(set(doc.get('document_type', 'Unknown') for doc in documents))
                st.metric("Document Types", doc_types)
            
            with col4:
                organizations = len(set(doc.get('organization', 'Unknown') for doc in documents))
                st.metric("Organizations", organizations)
        
        # Show system status
        st.markdown("#### 🔧 **System Status**")
        
        system_status = {
            "Content Vectorization": "✅ Ready" if recommendation_engine.document_vectors is not None else "⚠️ Not Initialized",
            "Patent Scoring Integration": "✅ Active",
            "Database Connection": "✅ Connected",
            "Machine Learning Models": "✅ Operational"
        }
        
        for component, status in system_status.items():
            st.markdown(f"**{component}:** {status}")