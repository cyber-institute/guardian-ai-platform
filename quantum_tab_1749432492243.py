import streamlit as st
from utils.db import fetch_documents
from utils.score_utils import draw_scorecard, get_score_analysis, get_deep_diagnostics
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf

def render():
    documents = fetch_documents()
    
    # Summary metrics at the top
    if documents:
        avg_score = sum(doc.get("quantum_q", 0) for doc in documents) / len(documents)
        high_score = max(doc.get("quantum_q", 0) for doc in documents)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Documents Analyzed", len(documents))
        with col2:
            st.metric("Average Score", f"{avg_score:.1f}")
        with col3:
            st.metric("Highest Score", f"{high_score:.1f}")
        
        st.markdown("<hr class='document-separator'>", unsafe_allow_html=True)
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

        # Document card styling
        score_class = "score-excellent" if score >= 75 else "score-good" if score >= 50 else "score-moderate"
        
        st.markdown(f"""
        <div class="metric-card {score_class}">
            <h3 style="margin-top: 0; color: #1f2937;">{doc.get("title", "Untitled Document")}</h3>
            <p style="color: #6b7280; margin-bottom: 0;">Quantum Maturity Assessment</p>
        </div>
        """, unsafe_allow_html=True)

        if score > 0:
            # Create two columns for better layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                draw_scorecard("Quantum Maturity", score)
            
            with col2:
                st.markdown("#### Key Focus Areas")
                st.markdown("""
                - **Post-Quantum Cryptography**
                - **Risk Assessment** 
                - **Implementation Planning**
                - **Standards Compliance**
                """)
            
            st.markdown("---")
            st.markdown("### 📈 Analysis Summary")
            st.markdown(get_score_analysis(score, "quantum readiness"))

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

        st.markdown("—" * 15)