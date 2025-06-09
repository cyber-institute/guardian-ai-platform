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

    # Display mode selection
    display_mode = st.session_state.get("display_mode", "cards")
    col1, col2 = st.columns([3, 1])
    with col1:
        display_mode = st.selectbox(
            "🎨 Display Style", 
            ["cards", "compact", "table", "grid", "minimal"],
            index=["cards", "compact", "table", "grid", "minimal"].index(display_mode),
            format_func=lambda x: {
                "cards": "🎴 Card View",
                "compact": "📦 Compact Cards", 
                "table": "📊 Table View",
                "grid": "⬜ Grid Layout",
                "minimal": "📄 Minimal List"
            }[x]
        )
    st.session_state["display_mode"] = display_mode

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

    # Document display based on selected mode
    if not page_docs:
        st.info("No documents match the current filters.")
        return

    # Render documents based on display mode
    if display_mode == "table":
        render_table_view(page_docs)
    elif display_mode == "compact":
        render_compact_cards(page_docs)
    elif display_mode == "grid":
        render_grid_view(page_docs)
    elif display_mode == "minimal":
        render_minimal_list(page_docs)
    else:  # cards
        render_card_view(page_docs)

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

def render_compact_cards(docs):
    """Render documents in compact card format."""
    cols = st.columns(4)
    for i, doc in enumerate(docs):
        with cols[i % 4]:
            title = doc.get('title', 'Untitled Document')
            doc_type = doc.get('document_type', 'Unknown')
            quantum_score = doc.get("quantum_score", 0)
            
            st.markdown(f"""
                <div style='border:1px solid #e0e0e0;padding:8px;border-radius:6px;margin:4px;
                background:linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                box-shadow:0 1px 3px rgba(0,0,0,0.1);height:140px;overflow:hidden'>
                    <div style='font-weight:bold;font-size:14px;margin-bottom:4px'>{title[:35]}{'...' if len(title) > 35 else ''}</div>
                    <div style='font-size:11px;color:#666;margin-bottom:6px'>{doc_type}</div>
                    <div style='margin-bottom:6px'>
                        Quantum Score: {get_badge(int(quantum_score))}
                    </div>
                    <div style='font-size:10px;color:#888'>
                        {str(doc.get('created_at', ''))[:10] if doc.get('created_at') else 'No date'}
                    </div>
                </div>
            """, unsafe_allow_html=True)

def render_grid_view(docs):
    """Render documents in grid layout."""
    cols = st.columns(3)
    for i, doc in enumerate(docs):
        with cols[i % 3]:
            title = doc.get('title', 'Untitled Document')
            quantum_score = doc.get("quantum_score", 0)
            content = doc.get('content', '')[:100]
            
            st.markdown(f"""
                <div style='border:2px solid #f0f0f0;padding:12px;border-radius:8px;margin:6px;
                background:white;box-shadow:0 2px 4px rgba(0,0,0,0.08);
                border-left:4px solid {"#2eb875" if quantum_score >= 80 else "#ff6b27" if quantum_score >= 50 else "#dc3545"}'>
                    <h4 style='margin:0 0 8px 0;font-size:16px'>{title[:40]}{'...' if len(title) > 40 else ''}</h4>
                    <div style='margin-bottom:8px'>{get_badge(int(quantum_score))}</div>
                    <p style='font-size:12px;color:#666;margin:0'>{content}{'...' if len(content) >= 100 else ''}</p>
                </div>
            """, unsafe_allow_html=True)

def render_table_view(docs):
    """Render documents in table format."""
    import pandas as pd
    
    table_data = []
    for doc in docs:
        table_data.append({
            'Title': doc.get('title', 'Untitled')[:50],
            'Type': doc.get('document_type', 'Unknown'),
            'Quantum Score': int(doc.get('quantum_score', 0)),
            'Date': str(doc.get('created_at', ''))[:10] if doc.get('created_at') else 'N/A',
            'Source': doc.get('source', 'Unknown')[:30] if doc.get('source') else 'N/A'
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_minimal_list(docs):
    """Render documents in minimal list format."""
    for idx, doc in enumerate(docs):
        title = doc.get('title', 'Untitled Document')
        quantum_score = doc.get("quantum_score", 0)
        doc_type = doc.get('document_type', 'Unknown')
        
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.markdown(f"**{title}**")
            st.caption(f"{doc_type} • {str(doc.get('created_at', ''))[:10] if doc.get('created_at') else 'No date'}")
        with col2:
            st.markdown(get_badge(int(quantum_score)), unsafe_allow_html=True)
        with col3:
            if st.button("View", key=f"view_{idx}"):
                with st.expander("Document Details", expanded=True):
                    st.write(doc.get('content', 'No content')[:500])

def render_card_view(docs):
    """Render documents in full card format."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            title = doc.get('title', 'Untitled Document')
            doc_type = doc.get('document_type', 'Unknown')
            quantum_score = doc.get("quantum_score", 0)
            content = doc.get('content', '')
            
            st.markdown(f"""
                <div style='border:1px solid #ddd;padding:16px;border-radius:12px;margin:8px;
                background:white;box-shadow:0 4px 6px rgba(0,0,0,0.1);
                transition:transform 0.2s ease;border-left:5px solid {"#2eb875" if quantum_score >= 80 else "#ff6b27" if quantum_score >= 50 else "#dc3545"}'>
                    <h3 style='margin:0 0 8px 0;color:#333'>{title}</h3>
                    <div style='margin-bottom:10px'>
                        <span style='background:#f0f0f0;padding:2px 8px;border-radius:12px;font-size:12px'>{doc_type}</span>
                    </div>
                    <div style='margin-bottom:12px'>
                        Quantum Maturity: {get_badge(int(quantum_score))}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if content:
                with st.expander("📄 Content Preview"):
                    st.write(content[:300] + "..." if len(content) > 300 else content)