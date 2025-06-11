"""
Document Recommendation Widget for GUARDIAN
Provides intelligent document suggestions based on content analysis and scoring patterns
"""

import streamlit as st
from typing import Dict, List, Optional
from utils.document_recommendation_engine import recommendation_engine

def render_document_recommendations(target_doc_id: int = None, 
                                  context_mode: str = "comprehensive",
                                  max_recommendations: int = 6):
    """
    Render document recommendations interface.
    
    Args:
        target_doc_id: ID of document to base recommendations on
        context_mode: Type of recommendations (comprehensive, content, scoring, trending)
        max_recommendations: Maximum number of recommendations to show
    """
    
    if context_mode == "trending":
        return render_trending_documents(max_recommendations)
    
    if target_doc_id is None:
        st.info("Select a document to see related recommendations")
        return
    
    with st.spinner("Generating intelligent recommendations..."):
        try:
            if context_mode == "comprehensive":
                recommendations = recommendation_engine.get_comprehensive_recommendations(
                    target_doc_id, max_recommendations=max_recommendations
                )
                render_comprehensive_recommendations(recommendations)
                
            elif context_mode == "content":
                content_similar = recommendation_engine.calculate_content_similarity(
                    target_doc_id, top_k=max_recommendations
                )
                render_similarity_recommendations(content_similar, "Content Similarity")
                
            elif context_mode == "scoring":
                scoring_similar = recommendation_engine.calculate_scoring_similarity(
                    target_doc_id, top_k=max_recommendations
                )
                render_similarity_recommendations(scoring_similar, "Scoring Pattern Similarity")
                
        except Exception as e:
            st.error(f"Error generating recommendations: {e}")

def render_comprehensive_recommendations(recommendations: Dict[str, List]):
    """Render comprehensive recommendations with multiple categories."""
    
    if not any(recommendations.values()):
        st.info("No similar documents found in the database")
        return
    
    # Combined recommendations (primary)
    if recommendations.get('combined'):
        st.markdown("### 🎯 **Recommended Documents**")
        render_recommendation_cards(recommendations['combined'][:6])
        
        # Show breakdown in expandable sections
        with st.expander("📊 View Recommendation Details", expanded=False):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if recommendations.get('content_similar'):
                    st.markdown("**📝 Content Similar**")
                    render_compact_recommendations(recommendations['content_similar'][:3])
            
            with col2:
                if recommendations.get('scoring_similar'):
                    st.markdown("**📈 Scoring Pattern Similar**")
                    render_compact_recommendations(recommendations['scoring_similar'][:3])
                    
            with col3:
                if recommendations.get('contextual'):
                    st.markdown("**🏢 Same Context**")
                    render_compact_recommendations(recommendations['contextual'][:3])

def render_recommendation_cards(recommendations: List[Dict]):
    """Render recommendations as interactive cards."""
    
    for i in range(0, len(recommendations), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(recommendations):
                render_single_recommendation_card(recommendations[i])
        
        with col2:
            if i + 1 < len(recommendations):
                render_single_recommendation_card(recommendations[i + 1])

def render_single_recommendation_card(doc: Dict):
    """Render a single recommendation card."""
    
    # Get scoring indicators
    scores = []
    if doc.get('ai_cybersecurity_score', 0) > 15:
        scores.append("🤖 AI Cyber")
    if doc.get('quantum_cybersecurity_score', 0) > 1:
        scores.append("⚛️ Quantum")
    if doc.get('ai_ethics_score', 0) > 20:
        scores.append("🎯 AI Ethics")
    if doc.get('quantum_ethics_score', 0) > 15:
        scores.append("🔬 Q-Ethics")
    
    score_badges = " | ".join(scores) if scores else "📄 General"
    
    # Recommendation score indicator
    rec_score = doc.get('recommendation_score')
    confidence = ""
    if rec_score is not None:
        if rec_score > 0.7:
            confidence = "🔥 Highly Relevant"
        elif rec_score > 0.4:
            confidence = "✨ Relevant"
        else:
            confidence = "💡 Related"
    
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 8px 0; background: #f9f9f9;">
            <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 12px; color: #666;">{confidence}</span>
                <span style="font-size: 11px; color: #888;">{doc.get('document_type', 'Document')}</span>
            </div>
            <h4 style="margin: 0 0 8px 0; color: #333;">{doc.get('title', 'Unknown Title')}</h4>
            <div style="font-size: 12px; color: #666; margin-bottom: 8px;">
                📍 {doc.get('organization', 'Unknown Org')} | {score_badges}
            </div>
            <p style="font-size: 13px; color: #555; margin: 0; line-height: 1.4;">
                {doc.get('content_preview', 'No preview available')[:120]}...
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action button
        if st.button(f"View Document", key=f"view_doc_{doc['id']}", use_container_width=True):
            st.session_state['selected_document_id'] = doc['id']
            st.rerun()

def render_compact_recommendations(recommendations: List[Dict]):
    """Render compact recommendation list."""
    
    for doc in recommendations:
        score_text = ""
        if doc.get('recommendation_score') is not None:
            score_text = f" ({doc['recommendation_score']:.2f})"
        
        st.markdown(f"""
        <div style="padding: 8px; margin: 4px 0; border-left: 3px solid #007acc; background: #f0f8ff;">
            <div style="font-weight: bold; font-size: 13px;">{doc.get('title', 'Unknown')}</div>
            <div style="font-size: 11px; color: #666;">{doc.get('organization', 'Unknown')}{score_text}</div>
        </div>
        """, unsafe_allow_html=True)

def render_similarity_recommendations(similarities: List[tuple], category_name: str):
    """Render similarity-based recommendations."""
    
    if not similarities:
        st.info(f"No {category_name.lower()} found")
        return
    
    st.markdown(f"### 📊 {category_name}")
    
    recommendations = []
    for doc_id, similarity_score in similarities:
        doc_info = recommendation_engine._get_document_info(doc_id, similarity_score)
        if doc_info:
            recommendations.append(doc_info)
    
    render_recommendation_cards(recommendations)

def render_trending_documents(max_count: int = 8):
    """Render trending documents across different frameworks."""
    
    st.markdown("### 🔥 **Trending Documents**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Cybersecurity", "⚛️ Quantum Cyber", "🎯 AI Ethics", "🔬 Quantum Ethics"])
    
    with tab1:
        ai_cyber_trending = recommendation_engine.get_trending_documents(
            framework='ai_cybersecurity', top_k=max_count
        )
        if ai_cyber_trending:
            render_trending_list(ai_cyber_trending, "AI Cybersecurity")
        else:
            st.info("No AI cybersecurity documents with significant scores found")
    
    with tab2:
        quantum_cyber_trending = recommendation_engine.get_trending_documents(
            framework='quantum_cybersecurity', top_k=max_count
        )
        if quantum_cyber_trending:
            render_trending_list(quantum_cyber_trending, "Quantum Cybersecurity")
        else:
            st.info("No quantum cybersecurity documents with significant scores found")
    
    with tab3:
        ai_ethics_trending = recommendation_engine.get_trending_documents(
            framework='ai_ethics', top_k=max_count
        )
        if ai_ethics_trending:
            render_trending_list(ai_ethics_trending, "AI Ethics")
        else:
            st.info("No AI ethics documents with significant scores found")
    
    with tab4:
        quantum_ethics_trending = recommendation_engine.get_trending_documents(
            framework='quantum_ethics', top_k=max_count
        )
        if quantum_ethics_trending:
            render_trending_list(quantum_ethics_trending, "Quantum Ethics")
        else:
            st.info("No quantum ethics documents with significant scores found")

def render_trending_list(trending_docs: List[Dict], framework_name: str):
    """Render trending documents list."""
    
    for i, doc in enumerate(trending_docs[:6], 1):
        with st.container():
            col1, col2 = st.columns([1, 6])
            
            with col1:
                score = doc.get('recommendation_score', 0)
                st.markdown(f"""
                <div style="text-align: center; padding: 8px; background: #e8f4f8; border-radius: 50%; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #2c5aa0;">
                    #{i}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                **{doc.get('title', 'Unknown Title')}**  
                📍 {doc.get('organization', 'Unknown')} | 📊 Score: {score:.1f}  
                📄 {doc.get('document_type', 'Document')} | 📅 {doc.get('date', 'Unknown date')}
                """)
                
                if st.button(f"View Document", key=f"trending_{framework_name}_{doc['id']}", use_container_width=True):
                    st.session_state['selected_document_id'] = doc['id']
                    st.rerun()
            
            st.divider()

def render_recommendation_sidebar(selected_doc_id: Optional[int] = None):
    """Render recommendation widget in sidebar."""
    
    with st.sidebar:
        st.markdown("### 💡 **Smart Recommendations**")
        
        rec_mode = st.selectbox(
            "Recommendation Type",
            ["comprehensive", "content", "scoring", "trending"],
            format_func=lambda x: {
                "comprehensive": "🎯 All Methods",
                "content": "📝 Content Similar",
                "scoring": "📊 Score Pattern",
                "trending": "🔥 Trending"
            }[x]
        )
        
        if rec_mode != "trending" and selected_doc_id:
            st.markdown(f"*Based on Document ID: {selected_doc_id}*")
        
        render_document_recommendations(
            target_doc_id=selected_doc_id,
            context_mode=rec_mode,
            max_recommendations=4
        )