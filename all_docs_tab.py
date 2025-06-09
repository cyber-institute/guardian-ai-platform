import streamlit as st
from utils.db import fetch_documents
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf

def get_badge(score):
    if score >= 80:
        return f"<span style='background-color:#2eb875;color:white;padding:2px 6px;border-radius:6px'>{score}</span>"
    elif score >= 50:
        return f"<span style='background-color:#ff6b27;color:white;padding:2px 6px;border-radius:6px'>{score}</span>"
    else:
        return f"<span style='background-color:#dc3545;color:white;padding:2px 6px;border-radius:6px'>{score}</span>"

def is_probably_quantum(content):
    if not content:
        return False
    keywords = ["quantum", "pqc", "post-quantum", "nist pqc", "qkd", "quantum-safe", "fips 203", "fips 204"]
    return any(kw in content.lower() for kw in keywords)

def render():
    st.markdown("<h2 style='text-align:center;'>📄 All Uploaded Documents</h2>", unsafe_allow_html=True)
    
    try:
        all_docs = fetch_documents()
        if not all_docs:
            st.info("No documents found in the database. Please upload some documents first.")
            return
    except Exception as e:
        st.error(f"Error fetching documents: {e}")
        return

    # Extract document types and years for filtering
    doc_types = sorted(set(doc.get("document_type", "Unknown") for doc in all_docs))
    sources = sorted(set(doc.get("source", "Unknown")[:30] for doc in all_docs if doc.get("source")))

    # Initialize filters in session state
    if "filters" not in st.session_state:
        st.session_state["filters"] = {
            "doc_type": "All",
            "source_multi": []
        }

    # Filter controls
    col1, col2, col3 = st.columns([3, 3, 4])
    with col1:
        available_types = ["All"] + doc_types
        current_selection = st.session_state["filters"]["doc_type"]
        if current_selection not in available_types:
            current_selection = "All"
        st.session_state["filters"]["doc_type"] = st.selectbox(
            "📂 Document Type", 
            available_types, 
            index=available_types.index(current_selection)
        )
    
    with col2:
        if st.button("🔄 Clear Filters"):
            st.session_state["filters"] = {
                "doc_type": "All",
                "source_multi": []
            }
            st.rerun()
    
    with col3:
        st.session_state["filters"]["source_multi"] = st.multiselect(
            "🌍 Filter by Source", 
            sources, 
            default=st.session_state["filters"]["source_multi"]
        )

    # Apply filters
    f = st.session_state["filters"]
    docs = all_docs
    if f["doc_type"] != "All":
        docs = [d for d in docs if d.get("document_type") == f["doc_type"]]
    if f["source_multi"]:
        docs = [d for d in docs if any(d.get("source", "").startswith(s) for s in f["source_multi"])]

    # Display mode toggle
    compact = st.session_state.get("card_mode", False)
    compact_toggle = st.checkbox("📦 Compact Mode", value=compact)
    st.session_state["card_mode"] = compact_toggle

    # Pagination
    per_page = 10
    page = st.session_state.get("doc_page", 0)
    total_pages = max(1, len(docs) // per_page + (1 if len(docs) % per_page else 0))

    if len(docs) > per_page:
        col1, col2, col3 = st.columns((1, 2, 1))
        with col1:
            if st.button("⬅️ Prev") and page > 0:
                st.session_state["doc_page"] = page - 1
                st.rerun()
        with col2:
            st.write(f"Page {page + 1} of {total_pages}")
        with col3:
            if st.button("Next ➡️") and page < total_pages - 1:
                st.session_state["doc_page"] = page + 1
                st.rerun()

    start = page * per_page
    end = start + per_page
    page_docs = docs[start:end]

    # Help section
    with st.expander("📖 What do these scores mean?"):
        st.markdown("""
        **🔐 Quantum Maturity Scores**
        - **Quantum Maturity**: Readiness for quantum threats (e.g., crypto-agility, PQC controls)
        - **Implementation**: Evidence of actual deployment or migration planning
        - **Standards**: Compliance with NIST and other quantum-safe standards
        - **Risk Assessment**: Evaluation of quantum computing threats

        **Scoring Scale:**
        - 80-100: Quantum-Ready (Green)
        - 50-79: Developing (Orange) 
        - 0-49: Initial (Red)
        """)

    # Document display
    if not page_docs:
        st.info("No documents match the current filters.")
        return

    cols = st.columns(4 if compact_toggle else 3)
    for i, doc in enumerate(page_docs):
        with cols[i % len(cols)]:
            with st.container():
                st.markdown("""
                    <div style='border:1px solid #ddd;padding:14px;border-radius:10px;margin:6px;
                    box-shadow:2px 4px rgba(0,0,0,0.05); transition:0.3s'>
                """, unsafe_allow_html=True)

                # Document title and type
                title = doc.get('title', 'Untitled Document')
                doc_type = doc.get('document_type', 'Unknown')
                st.markdown(f"**📜 {title[:60]}**", unsafe_allow_html=True)
                st.markdown(f"<small>{doc_type}</small>", unsafe_allow_html=True)

                # Get quantum maturity score
                text_blob = doc.get("text") or doc.get("content", "")
                stored_score = doc.get("quantum_score", 0)
                
                # Try AI evaluation with fallback
                try:
                    if text_blob and len(text_blob.strip()) > 50:
                        hf_result = evaluate_quantum_maturity_hf(text_blob)
                        quantum_score = hf_result.get("patent_score", stored_score)
                        traits = hf_result.get("traits", {})
                    else:
                        quantum_score = stored_score
                        traits = {}
                except Exception as e:
                    quantum_score = stored_score
                    traits = {}
                    st.caption(f"AI analysis unavailable: {str(e)[:50]}...")

                # Display quantum score
                if is_probably_quantum(text_blob) or quantum_score > 0:
                    st.markdown(f"Quantum Maturity: {get_badge(int(quantum_score))}", unsafe_allow_html=True)
                else:
                    st.markdown(f"Quantum Maturity: <span style='color:#888'>N/A</span>", unsafe_allow_html=True)

                # Content preview
                if not compact_toggle:
                    with st.expander("📖 Content Preview"):
                        content_preview = doc.get('content', '')[:500]
                        if len(content_preview) >= 500:
                            content_preview += "..."
                        st.text(content_preview if content_preview else "No content available")

                # Quantum analysis details
                if quantum_score > 0:
                    with st.expander("🔍 Quantum Analysis Details"):
                        st.markdown("**Maturity Indicators:**")
                        if traits:
                            st.markdown(f"- Implementation Plan: {'✅' if traits.get('implementation_plan') else '❌'}")
                            st.markdown(f"- Standards Reference: {'✅' if traits.get('standards_reference') else '❌'}")
                            st.markdown(f"- Risk Assessment: {'✅' if traits.get('risk_assessment') else '❌'}")
                            st.markdown(f"- Migration Strategy: {'✅' if traits.get('migration_strategy') else '❌'}")
                        else:
                            st.markdown("- Based on stored score and keyword analysis")
                        
                        st.markdown(f"**Score**: {quantum_score:.1f}/100")
                        if quantum_score >= 80:
                            st.success("Excellent quantum readiness")
                        elif quantum_score >= 60:
                            st.warning("Good quantum awareness")
                        else:
                            st.info("Basic quantum consideration")

                # Source information
                source = doc.get("source", "")
                if source and source.startswith("http"):
                    st.markdown(f"[🌐 View Source]({source})", unsafe_allow_html=True)
                elif source:
                    st.caption(f"Source: {source[:50]}")

                # Document metadata
                created_at = doc.get("created_at")
                if created_at:
                    st.caption(f"Added: {str(created_at)[:10]}")

                st.markdown("</div>", unsafe_allow_html=True)

    # Summary statistics
    st.markdown("---")
    st.markdown("### 📊 Collection Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Documents", len(docs))
    with col2:
        quantum_docs = len([d for d in docs if (d.get("text") or d.get("content", "")) and is_probably_quantum(d.get("text") or d.get("content", ""))])
        st.metric("Quantum-Related", quantum_docs)
    with col3:
        avg_score = sum(d.get("quantum_score", 0) for d in docs) / len(docs) if docs else 0
        st.metric("Avg Score", f"{avg_score:.1f}")
    with col4:
        high_scoring = len([d for d in docs if d.get("quantum_score", 0) >= 75])
        st.metric("High Scoring (75+)", high_scoring)