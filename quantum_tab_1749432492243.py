import streamlit as st
from utils.db import fetch_documents
from utils.score_utils import draw_scorecard, get_score_analysis, get_deep_diagnostics
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf

def render():
    documents = fetch_documents()
    
    # Enhanced summary metrics at the top
    if documents:
        # Calculate comprehensive scores
        total_docs = len(documents)
        quantum_scores = [doc.get("quantum_q", 0) for doc in documents]
        avg_quantum = sum(quantum_scores) / total_docs if quantum_scores else 0
        
        # Calculate cyber and ethics averages based on document content
        cyber_scores = []
        ethics_scores = []
        
        for doc in documents:
            text_lower = doc.get("text", "").lower()
            base_score = doc.get("quantum_q", 0)
            
            # Cyber score calculation
            cyber_boost = 20 if any(word in text_lower for word in ['security', 'threat', 'vulnerability', 'attack', 'defense']) else 0
            cyber_scores.append(min(100, base_score + cyber_boost))
            
            # Ethics score calculation
            ethics_boost = 15 if any(word in text_lower for word in ['privacy', 'ethics', 'governance', 'responsible']) else 0
            ethics_scores.append(min(100, base_score + ethics_boost))
        
        avg_cyber = sum(cyber_scores) / total_docs if cyber_scores else 0
        avg_ethics = sum(ethics_scores) / total_docs if ethics_scores else 0
        
        # Display metrics in a compact card layout
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 2rem;
            color: white;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="text-align: center; flex: 1;">
                    <div style="font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;">{total_docs}</div>
                    <div style="font-size: 0.9rem; opacity: 0.9;">Documents Analyzed</div>
                </div>
                
                <div style="text-align: center; flex: 1;">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span style="font-size: 1.5rem;">🔐</span>
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700;">{avg_quantum:.0f}</div>
                            <div style="font-size: 0.8rem; opacity: 0.9;">Quantum Avg</div>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; flex: 1;">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span style="font-size: 1.5rem;">🛡️</span>
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700;">{avg_cyber:.0f}</div>
                            <div style="font-size: 0.8rem; opacity: 0.9;">Cyber Avg</div>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: center; flex: 1;">
                    <div style="display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                        <span style="font-size: 1.5rem;">⚖️</span>
                        <div>
                            <div style="font-size: 1.8rem; font-weight: 700;">{avg_ethics:.0f}</div>
                            <div style="font-size: 0.8rem; opacity: 0.9;">Ethics Avg</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No documents found for analysis")

    for doc in documents:
        base_score = doc.get("quantum_q", 0)

        text_blob = doc.get("text") or doc.get("content")
        if text_blob:
            hf_result = evaluate_quantum_maturity_hf(text_blob)
            score = hf_result["patent_score"]
            label = hf_result["label"]
            narrative = hf_result["narrative"]
            raw_conf = hf_result["raw"]
            traits = hf_result.get("traits", {})
        else:
            score = base_score
            label = "Stored"
            narrative = []
            raw_conf = {}
            traits = {}

        # Extract better title from document content
        def extract_document_title(text, fallback_title):
            if not text:
                return fallback_title
            
            # Look for title patterns in first few lines
            lines = text.strip().split('\n')[:5]
            for line in lines:
                line = line.strip()
                if len(line) > 10 and len(line) < 100:
                    # Check if it looks like a title (no periods, proper length)
                    if not line.endswith('.') and any(word.istitle() for word in line.split()):
                        return line
            
            # Fallback to first sentence
            sentences = text.split('.')[:1]
            if sentences and len(sentences[0]) > 10 and len(sentences[0]) < 120:
                return sentences[0].strip()
            
            return fallback_title
        
        document_title = extract_document_title(doc.get("text", ""), doc.get("title", "Untitled Document"))
        
        # Generate multiple scores for different categories
        def generate_category_scores(base_score, text_content):
            text_lower = text_content.lower() if text_content else ""
            
            # Ethics score - based on privacy, governance keywords
            ethics_boost = 0
            if any(word in text_lower for word in ['privacy', 'ethics', 'governance', 'responsible']):
                ethics_boost = 15
            ethics_score = min(100, base_score + ethics_boost)
            
            # Cyber score - based on security, threat keywords
            cyber_boost = 0
            if any(word in text_lower for word in ['security', 'threat', 'vulnerability', 'attack', 'defense']):
                cyber_boost = 20
            cyber_score = min(100, base_score + cyber_boost)
            
            # Quantum score - the base score
            quantum_score = base_score
            
            return {
                'quantum': quantum_score,
                'cyber': cyber_score,
                'ethics': ethics_score
            }
        
        category_scores = generate_category_scores(score, doc.get("text", ""))
        
        # Enhanced compact card design with animations
        st.markdown(f"""
        <div class="document-card" style="
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 5px solid {'#22c55e' if score >= 75 else '#f59e0b' if score >= 50 else '#ef4444'};
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div style="flex: 1; margin-right: 1rem; min-width: 250px;">
                    <h3 style="
                        margin: 0 0 0.8rem 0; 
                        color: #111827; 
                        font-size: 1.2rem;
                        line-height: 1.4;
                        font-weight: 700;
                        letter-spacing: -0.02em;
                    ">{document_title}</h3>
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="
                            background: {'#dcfce7' if score >= 75 else '#fef3c7' if score >= 50 else '#fee2e2'};
                            color: {'#166534' if score >= 75 else '#92400e' if score >= 50 else '#991b1b'};
                            padding: 0.25rem 0.5rem;
                            border-radius: 6px;
                            font-size: 0.75rem;
                            font-weight: 600;
                        ">{doc.get('document_type', 'document').title()}</span>
                        <span style="color: #9ca3af; font-size: 0.8rem;">{doc.get('source', 'unknown').title()}</span>
                    </div>
                </div>
                
                <div class="score-section" style="display: flex; gap: 1.2rem; align-items: center;">
                    <div class="score-badge" style="
                        text-align: center;
                        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
                        border-radius: 12px;
                        padding: 0.8rem 0.6rem;
                        border: 1px solid #bae6fd;
                        min-width: 60px;
                    ">
                        <div style="font-size: 1.4rem; margin-bottom: 0.2rem;">🔐</div>
                        <div style="font-size: 0.65rem; color: #0369a1; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Quantum</div>
                        <div style="font-size: 1.1rem; color: {'#22c55e' if category_scores['quantum'] >= 75 else '#f59e0b' if category_scores['quantum'] >= 50 else '#ef4444'}; font-weight: 800; margin-top: 0.2rem;">
                            {category_scores['quantum']:.0f}
                        </div>
                    </div>
                    
                    <div class="score-badge" style="
                        text-align: center;
                        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
                        border-radius: 12px;
                        padding: 0.8rem 0.6rem;
                        border: 1px solid #bbf7d0;
                        min-width: 60px;
                    ">
                        <div style="font-size: 1.4rem; margin-bottom: 0.2rem;">🛡️</div>
                        <div style="font-size: 0.65rem; color: #166534; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Cyber</div>
                        <div style="font-size: 1.1rem; color: {'#22c55e' if category_scores['cyber'] >= 75 else '#f59e0b' if category_scores['cyber'] >= 50 else '#ef4444'}; font-weight: 800; margin-top: 0.2rem;">
                            {category_scores['cyber']:.0f}
                        </div>
                    </div>
                    
                    <div class="score-badge" style="
                        text-align: center;
                        background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
                        border-radius: 12px;
                        padding: 0.8rem 0.6rem;
                        border: 1px solid #fed7aa;
                        min-width: 60px;
                    ">
                        <div style="font-size: 1.4rem; margin-bottom: 0.2rem;">⚖️</div>
                        <div style="font-size: 0.65rem; color: #92400e; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">Ethics</div>
                        <div style="font-size: 1.1rem; color: {'#22c55e' if category_scores['ethics'] >= 75 else '#f59e0b' if category_scores['ethics'] >= 50 else '#ef4444'}; font-weight: 800; margin-top: 0.2rem;">
                            {category_scores['ethics']:.0f}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if score > 0:
            # Interactive expandable analysis section
            with st.expander("📊 Detailed Analysis & Insights", expanded=False):
                
                # Create three columns for category analysis
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("#### 🔐 Quantum Security")
                    draw_scorecard("Quantum Score", category_scores['quantum'])
                    st.markdown(get_score_analysis(category_scores['quantum'], "quantum security"))
                
                with col2:
                    st.markdown("#### 🛡️ Cyber Defense")
                    draw_scorecard("Cyber Score", category_scores['cyber'])
                    st.markdown(get_score_analysis(category_scores['cyber'], "cyber security"))
                
                with col3:
                    st.markdown("#### ⚖️ Ethics & Governance")
                    draw_scorecard("Ethics Score", category_scores['ethics'])
                    st.markdown(get_score_analysis(category_scores['ethics'], "ethics compliance"))
                
                st.markdown("---")
                
                # Document insights
                text_content = doc.get("text", "")
                if text_content:
                    st.markdown("#### 🔍 Document Insights")
                    
                    # Key metrics about the document
                    word_count = len(text_content.split())
                    char_count = len(text_content)
                    
                    insight_col1, insight_col2, insight_col3 = st.columns(3)
                    with insight_col1:
                        st.metric("Word Count", f"{word_count:,}")
                    with insight_col2:
                        st.metric("Characters", f"{char_count:,}")
                    with insight_col3:
                        coverage_score = min(100, (word_count / 500) * 100) if word_count > 0 else 0
                        st.metric("Coverage", f"{coverage_score:.0f}%")
                    
                    # Quick content preview
                    preview_text = text_content[:300] + "..." if len(text_content) > 300 else text_content
                    st.markdown("**Content Preview:**")
                    st.markdown(f"_{preview_text}_")

            with st.expander("🔍 Detailed AI Analysis", expanded=False):
                # Create tabs for better organization
                tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Confidence Scores", "Maturity Traits", "Recommendations"])
                
                with tab1:
                    st.markdown("**Analysis Method:** Advanced text classification using zero-shot learning")
                    if narrative:
                        st.markdown("**Key Findings:**")
                        for item in narrative:
                            st.markdown(f"• {item}")
                    else:
                        st.info("Analysis based on keyword matching and document structure")
                
                with tab2:
                    st.markdown("**Raw Confidence Scores**")
                    if raw_conf:
                        for label, conf in raw_conf.items():
                            try:
                                score_value = float(conf)
                                st.progress(score_value, text=f"{label}: {score_value:.2f}")
                            except (ValueError, TypeError):
                                st.text(f"{label}: {conf}")
                    else:
                        st.info("No detailed confidence scores available")
                
                with tab3:
                    st.markdown("**Implementation Readiness Indicators**")
                    
                    trait_col1, trait_col2 = st.columns(2)
                    with trait_col1:
                        plan_status = "✅ Present" if traits.get('implementation_plan') else "❌ Missing"
                        st.markdown(f"**Implementation Plan:** {plan_status}")
                        
                        standards_status = "✅ Present" if traits.get('standards_reference') else "❌ Missing"
                        st.markdown(f"**Standards Reference:** {standards_status}")
                    
                    with trait_col2:
                        roadmap_status = "✅ Present" if traits.get('roadmap_timeline') else "❌ Missing"
                        st.markdown(f"**Roadmap/Timeline:** {roadmap_status}")
                        
                        # Overall readiness indicator
                        trait_count = sum(1 for v in traits.values() if v)
                        readiness_pct = (trait_count / len(traits)) * 100 if traits else 0
                        st.metric("Implementation Readiness", f"{readiness_pct:.0f}%")
                
                with tab4:
                    st.markdown("**Improvement Recommendations**")
                    
                    recommendations = []
                    if not traits.get("implementation_plan"):
                        recommendations.append("Develop a comprehensive implementation plan for quantum-safe cryptography")
                    if not traits.get("standards_reference"):
                        recommendations.append("Include references to industry standards (NIST PQC, FIPS 203/204)")
                    if not traits.get("roadmap_timeline"):
                        recommendations.append("Create a detailed migration roadmap with specific timelines")
                    
                    if recommendations:
                        for i, rec in enumerate(recommendations, 1):
                            st.markdown(f"{i}. {rec}")
                    else:
                        st.success("Document demonstrates strong quantum maturity indicators")
                    
                    # Add weighting explanation
                    st.markdown("---")
                    st.markdown("**Scoring Methodology**")
                    st.markdown("""
                    - **Awareness indicators:** 0.8x weight
                    - **Readiness indicators:** 1.2x weight  
                    - **Implementation controls:** 1.5x weight
                    """)
                    
                    st.markdown(get_deep_diagnostics(score, "quantum readiness"))
        else:
            st.markdown("**Quantum Score:** N/A")
            st.markdown("_This document does not appear to contain any quantum-related content._")

        st.markdown("<hr class='document-separator'>", unsafe_allow_html=True)