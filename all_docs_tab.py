import streamlit as st
from utils.db import fetch_documents
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf
from utils.comprehensive_scoring import comprehensive_document_scoring, format_score_display, get_score_badge_color
from utils.document_metadata_extractor import extract_document_metadata

def get_comprehensive_badge(score, framework):
    """Create badge for comprehensive scoring system."""
    if score is None:
        return f"<span style='background: #9CA3AF;color:white;padding:4px 8px;border-radius:6px;font-weight:500;font-family:Inter,sans-serif;'>N/A</span>"
    
    color = get_score_badge_color(score, framework)
    display_score = format_score_display(score, framework)
    
    return f"<span style='background: {color};color:white;padding:4px 8px;border-radius:6px;font-weight:600;font-family:Inter,sans-serif;box-shadow:0 2px 4px rgba(0,0,0,0.1)'>{display_score}</span>"

def get_badge(score):
    """Legacy badge function for backward compatibility."""
    if score >= 80:
        return f"<span style='background: linear-gradient(135deg, #059669 0%, #10b981 100%);color:white;padding:4px 12px;border-radius:8px;font-weight:600;font-family:Inter,sans-serif;box-shadow:0 2px 4px rgba(5,150,105,0.2)'>{score}</span>"
    elif score >= 50:
        return f"<span style='background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);color:white;padding:4px 12px;border-radius:8px;font-weight:600;font-family:Inter,sans-serif;box-shadow:0 2px 4px rgba(217,119,6,0.2)'>{score}</span>"
    else:
        return f"<span style='background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);color:white;padding:4px 12px;border-radius:8px;font-weight:600;font-family:Inter,sans-serif;box-shadow:0 2px 4px rgba(220,38,38,0.2)'>{score}</span>"

def is_probably_quantum(content):
    if not content:
        return False
    keywords = ["quantum", "pqc", "post-quantum", "nist pqc", "qkd", "quantum-safe", "fips 203", "fips 204"]
    return any(kw in content.lower() for kw in keywords)

def render():
    st.markdown("<h2 style='text-align:center;'>All Uploaded Documents</h2>", unsafe_allow_html=True)
    
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
            "Document Type", 
            available_types, 
            index=available_types.index(current_selection)
        )
    
    with col2:
        st.markdown("""
        <style>
        .clear-filters-btn {
            background: linear-gradient(145deg, #ef4444 0%, #dc2626 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
            font-size: 0.875rem;
            margin-top: 1.5rem;
            width: 100%;
        }
        .clear-filters-btn:hover {
            background: linear-gradient(145deg, #dc2626 0%, #b91c1c 100%);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear Filters", key="clear_filters", help="Reset all filters to default values"):
            st.session_state["filters"] = {
                "doc_type": "All",
                "source_multi": []
            }
            st.rerun()
    
    with col3:
        st.session_state["filters"]["source_multi"] = st.multiselect(
            "Filter by Source", 
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
            "Display Style", 
            ["cards", "compact", "table", "grid", "minimal"],
            index=["cards", "compact", "table", "grid", "minimal"].index(display_mode),
            format_func=lambda x: {
                "cards": "Card View",
                "compact": "Compact Cards", 
                "table": "Table View",
                "grid": "Grid Layout",
                "minimal": "Minimal List"
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
            if st.button("Previous") and page > 0:
                st.session_state["doc_page"] = page - 1
                st.rerun()
        with col2:
            st.write(f"Page {page + 1} of {total_pages}")
        with col3:
            if st.button("Next") and page < total_pages - 1:
                st.session_state["doc_page"] = page + 1
                st.rerun()

    start = page * per_page
    end = start + per_page
    page_docs = docs[start:end]

    # Help section
    with st.expander("What do these scores mean?"):
        st.markdown("""
        **Quantum Maturity Scores**
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
    st.markdown("### Collection Summary")
    
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
    cols = st.columns(3)
    for i, doc in enumerate(docs):
        with cols[i % 3]:
            content = doc.get('content', '') or doc.get('text_content', '')
            
            # Get or generate intelligent metadata
            if not doc.get('analyzed_metadata'):
                metadata = extract_document_metadata(content, doc.get('title', ''))
                doc['analyzed_metadata'] = metadata
            else:
                metadata = doc['analyzed_metadata']
            
            title = metadata.get('title', 'Untitled Document') or 'Untitled Document'
            author_org = metadata.get('author_organization', 'Unknown') or 'Unknown'
            pub_date = metadata.get('publish_date') or 'No date'
            doc_type = metadata.get('document_type', 'Unknown') or 'Unknown'
            
            # Calculate comprehensive scores
            scores = comprehensive_document_scoring(content, str(title))
            
            st.markdown(f"""
                <div style='border:1px solid #e0e0e0;padding:12px;border-radius:8px;margin:4px;
                background:linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                box-shadow:0 1px 3px rgba(0,0,0,0.1);height:220px;overflow:hidden'>
                    <div style='font-weight:bold;font-size:13px;margin-bottom:4px'>{title[:35]}{'...' if len(title) > 35 else ''}</div>
                    <div style='font-size:10px;color:#666;margin-bottom:6px'>{doc_type} • {author_org}</div>
                    <div style='font-size:9px;line-height:1.3;margin-bottom:6px'>
                        <div>AI Cyber: {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity')}</div>
                        <div>Q Cyber: {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity')}</div>
                        <div>AI Ethics: {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics')}</div>
                        <div>Q Ethics: {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics')}</div>
                    </div>
                    <div style='font-size:9px;color:#888'>{pub_date}</div>
                </div>
            """, unsafe_allow_html=True)

def render_grid_view(docs):
    """Render documents in grid layout."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            content = doc.get('content', '') or doc.get('text_content', '')
            
            # Get or generate intelligent metadata
            if not doc.get('analyzed_metadata'):
                metadata = extract_document_metadata(content, doc.get('title', ''))
                doc['analyzed_metadata'] = metadata
            else:
                metadata = doc['analyzed_metadata']
            
            title = metadata.get('title', 'Untitled Document') or 'Untitled Document'
            author_org = metadata.get('author_organization', 'Unknown') or 'Unknown'
            pub_date = metadata.get('publish_date') or 'No date'
            doc_type = metadata.get('document_type', 'Unknown') or 'Unknown'
            content_preview = metadata.get('content_preview', 'No preview available') or 'No preview available'
            
            # Calculate comprehensive scores
            scores = comprehensive_document_scoring(content, str(title))
            
            st.markdown(f"""
                <div style='border:2px solid #f0f0f0;padding:12px;border-radius:8px;margin:6px;
                background:white;box-shadow:0 2px 4px rgba(0,0,0,0.08);
                border-left:4px solid #3B82F6'>
                    <h4 style='margin:0 0 6px 0;font-size:15px'>{title[:40]}{'...' if len(title) > 40 else ''}</h4>
                    <div style='font-size:10px;color:#666;margin-bottom:8px'>{doc_type} • {author_org} • {pub_date}</div>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:8px;font-size:10px'>
                        <div>AI Cyber: {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity')}</div>
                        <div>Q Cyber: {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity')}</div>
                        <div>AI Ethics: {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics')}</div>
                        <div>Q Ethics: {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics')}</div>
                    </div>
                    <p style='font-size:11px;color:#666;margin:0'>{content_preview[:120]}{'...' if len(content_preview) > 120 else ''}</p>
                </div>
            """, unsafe_allow_html=True)

def render_table_view(docs):
    """Render documents in table format."""
    import pandas as pd
    
    table_data = []
    for doc in docs:
        content = doc.get('content', '') or doc.get('text_content', '')
        
        # Get or generate intelligent metadata
        if not doc.get('analyzed_metadata'):
            metadata = extract_document_metadata(content, doc.get('title', ''))
            doc['analyzed_metadata'] = metadata
        else:
            metadata = doc['analyzed_metadata']
        
        title = metadata.get('title', 'Untitled Document') or 'Untitled Document'
        author_org = metadata.get('author_organization', 'Unknown') or 'Unknown'
        pub_date = metadata.get('publish_date') or 'N/A'
        doc_type = metadata.get('document_type', 'Unknown') or 'Unknown'
        
        scores = comprehensive_document_scoring(content, str(title))
        
        table_data.append({
            'Title': title[:45],
            'Author/Org': author_org[:25],
            'Type': doc_type,
            'AI Cyber': format_score_display(scores['ai_cybersecurity'], 'ai_cybersecurity'),
            'Q Cyber': format_score_display(scores['quantum_cybersecurity'], 'quantum_cybersecurity'),
            'AI Ethics': format_score_display(scores['ai_ethics'], 'ai_ethics'),
            'Q Ethics': format_score_display(scores['quantum_ethics'], 'quantum_ethics'),
            'Date': pub_date
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_minimal_list(docs):
    """Render documents in minimal list format."""
    for idx, doc in enumerate(docs):
        content = doc.get('content', '') or doc.get('text_content', '')
        
        # Get or generate intelligent metadata
        if not doc.get('analyzed_metadata'):
            metadata = extract_document_metadata(content, doc.get('title', ''))
            doc['analyzed_metadata'] = metadata
        else:
            metadata = doc['analyzed_metadata']
        
        title = metadata.get('title', 'Untitled Document') or 'Untitled Document'
        author_org = metadata.get('author_organization', 'Unknown') or 'Unknown'
        pub_date = metadata.get('publish_date') or 'No date'
        doc_type = metadata.get('document_type', 'Unknown') or 'Unknown'
        content_preview = metadata.get('content_preview', 'No preview available') or 'No preview available'
        
        # Calculate comprehensive scores
        scores = comprehensive_document_scoring(content, str(title))
        
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**{title}**")
            st.caption(f"{doc_type} • {author_org} • {pub_date}")
        with col2:
            # Display all four scores in compact format
            st.markdown(f"""
            <div style='display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end'>
                <small>AI Cyber:</small> {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity')}
                <small>Q Cyber:</small> {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity')}
                <small>AI Ethics:</small> {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics')}
                <small>Q Ethics:</small> {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics')}
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("View Details", key=f"view_{idx}"):
            with st.expander("Document Details", expanded=True):
                st.write("**Intelligent Preview:**")
                st.write(content_preview)
                st.write("**Raw Content:**")
                st.write(content[:500] + "..." if len(content) > 500 else content)

def render_card_view(docs):
    """Render documents in full card format."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            content = doc.get('content', '') or doc.get('text_content', '')
            
            # Get or generate intelligent metadata
            if not doc.get('analyzed_metadata'):
                metadata = extract_document_metadata(content, doc.get('title', ''))
                doc['analyzed_metadata'] = metadata
            else:
                metadata = doc['analyzed_metadata']
            
            title = metadata.get('title', 'Untitled Document') or 'Untitled Document'
            author_org = metadata.get('author_organization', 'Unknown') or 'Unknown'
            pub_date = metadata.get('publish_date', 'Unknown') or 'Unknown'
            doc_type = metadata.get('document_type', 'Unknown') or 'Unknown'
            content_preview = metadata.get('content_preview', 'No preview available') or 'No preview available'
            
            # Calculate comprehensive scores
            scores = comprehensive_document_scoring(content, str(title))
            
            st.markdown(f"""
                <div style='border:1px solid #ddd;padding:16px;border-radius:12px;margin:8px;
                background:white;box-shadow:0 4px 6px rgba(0,0,0,0.1);
                transition:transform 0.2s ease;border-left:5px solid #3B82F6'>
                    <h3 style='margin:0 0 8px 0;color:#333'>{title}</h3>
                    <div style='margin-bottom:10px;display:flex;gap:8px;flex-wrap:wrap'>
                        <span style='background:#f0f0f0;padding:2px 8px;border-radius:12px;font-size:12px'>{doc_type}</span>
                        <span style='background:#e0f2fe;padding:2px 8px;border-radius:12px;font-size:12px;color:#0277bd'>{author_org}</span>
                        {f"<span style='background:#f3e5f5;padding:2px 8px;border-radius:12px;font-size:12px;color:#7b1fa2'>{pub_date}</span>" if pub_date and pub_date != 'Unknown' else ""}
                    </div>
                    <div style='margin-bottom:12px'>
                        <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px'>
                            <div><strong>AI Cybersecurity:</strong> {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity')}</div>
                            <div><strong>Quantum Cybersecurity:</strong> {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity')}</div>
                            <div><strong>AI Ethics:</strong> {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics')}</div>
                            <div><strong>Quantum Ethics:</strong> {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics')}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Intelligent Content Preview"):
                st.write(content_preview)