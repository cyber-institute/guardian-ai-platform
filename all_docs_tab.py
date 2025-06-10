import streamlit as st
import re
from utils.db import fetch_documents
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf
from utils.comprehensive_scoring import comprehensive_document_scoring, format_score_display, get_score_badge_color
from utils.document_metadata_extractor import extract_document_metadata
from utils.content_cleaner import clean_document_content
from utils.clean_preview_generator import generate_clean_preview, extract_clean_metadata
from utils.simple_updater import update_document_metadata
from components.chatbot_widget import create_tooltip, render_help_tooltip

def get_comprehensive_badge(score, framework):
    """Create badge for comprehensive scoring system with intelligent tooltips."""
    
    # Define tooltip explanations for each framework
    tooltips = {
        'ai_cybersecurity': 'AI Cybersecurity Maturity (0-100): Evaluates security preparedness for AI systems including encryption standards, authentication mechanisms, threat monitoring, and incident response capabilities.',
        'quantum_cybersecurity': 'Quantum Cybersecurity Maturity (1-5 QCMEA): Assesses quantum threat preparedness from basic awareness (1) to dynamic adaptability (5) using patent-based framework.',
        'ai_ethics': 'AI Ethics (0-100): Measures responsible AI practices including fairness, transparency, accountability, and privacy protection mechanisms.',
        'quantum_ethics': 'Quantum Ethics (0-100): Evaluates ethical considerations in quantum computing including equitable access, privacy implications, and responsible implementation.'
    }
    
    if score is None:
        return "N/A"
    
    display_score = format_score_display(score, framework)
    return f"{display_score}"

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
    
    # Enhanced refresh button with display style controls
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Refresh Analysis", help="Update all documents with improved metadata extraction"):
            with st.spinner("Updating all documents with improved analysis..."):
                try:
                    updated_count = update_document_metadata()
                    if updated_count > 0:
                        st.success(f"Updated {updated_count} documents with improved metadata")
                    else:
                        st.info("All documents are already up to date")
                    
                    # Clear session state to force refresh of displayed data
                    st.session_state.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error updating documents: {e}")
    
    with col2:
        # Display mode selection moved up here
        display_mode = st.session_state.get("display_mode", "cards")
        display_mode = st.selectbox(
            "", 
            ["cards", "compact", "table", "grid", "minimal"],
            index=["cards", "compact", "table", "grid", "minimal"].index(display_mode),
            format_func=lambda x: {
                "cards": "Card View",
                "compact": "Compact Cards", 
                "table": "Table View",
                "grid": "Grid Layout",
                "minimal": "Minimal List"
            }[x],
            label_visibility="collapsed"
        )
        st.session_state["display_mode"] = display_mode
    
    try:
        # Clear any potential caching to ensure fresh data
        if 'documents_cache' in st.session_state:
            del st.session_state['documents_cache']
        
        all_docs = fetch_documents()
        if not all_docs:
            st.info("No documents found in the database. Please upload some documents first.")
            return
            
        # Clean all documents and force fresh metadata analysis
        all_docs = [clean_document_content(doc) for doc in all_docs]
        # Force regeneration of all metadata with enhanced cleaning
        for doc in all_docs:
            doc.pop('analyzed_metadata', None)  # Remove any cached metadata
                
    except Exception as e:
        st.error(f"Error fetching documents: {e}")
        return

    # Extract filter options from documents
    doc_types = sorted(set(doc.get("document_type", "Unknown") for doc in all_docs))
    organizations = sorted(set(doc.get("organization", "Unknown")[:30] for doc in all_docs if doc.get("organization")))
    
    # Extract years from dates
    years = set()
    for doc in all_docs:
        date_str = doc.get("date", "")
        if date_str:
            try:
                # Try to extract year from various date formats
                import re
                year_match = re.search(r'\b(19|20)\d{2}\b', str(date_str))
                if year_match:
                    years.add(year_match.group())
            except:
                pass
    years = sorted(list(years), reverse=True)
    
    # Define regions based on common organizations/sources
    def detect_region(org_name):
        org_lower = org_name.lower()
        if any(term in org_lower for term in ['nist', 'dhs', 'usa', 'united states', 'us ', 'federal', 'dod', 'nasa']):
            return 'US'
        elif any(term in org_lower for term in ['eu', 'european', 'gdpr', 'enisa', 'europa']):
            return 'EU'
        elif any(term in org_lower for term in ['uk', 'britain', 'british', 'ncsc']):
            return 'UK'
        elif any(term in org_lower for term in ['iso', 'itu', 'oecd', 'un ', 'united nations']):
            return 'International'
        elif any(term in org_lower for term in ['china', 'japan', 'korea', 'singapore', 'asia']):
            return 'Asia'
        elif any(term in org_lower for term in ['canada', 'australia', 'new zealand']):
            return 'Other'
        return 'Unknown'
    
    regions = sorted(set(detect_region(org) for org in organizations if org != "Unknown"))

    # Initialize filters in session state
    if "filters" not in st.session_state:
        st.session_state["filters"] = {
            "selected_types": [],
            "selected_orgs": [],
            "selected_years": [],
            "selected_regions": []
        }

    # Compact filter controls with dropdown-style multiselect
    
    # Create compact filter row
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns([2, 2, 1.5, 1.5, 1])
    
    with filter_col1:
        st.session_state["filters"]["selected_types"] = st.multiselect(
            "Document Type", 
            doc_types,
            default=st.session_state["filters"]["selected_types"],
            key="type_multiselect"
        )
    
    with filter_col2:
        # Show top organizations only to avoid clutter
        top_orgs = organizations[:12] if len(organizations) > 12 else organizations
        st.session_state["filters"]["selected_orgs"] = st.multiselect(
            "Author/Organization", 
            top_orgs,
            default=st.session_state["filters"]["selected_orgs"],
            key="org_multiselect",
            format_func=lambda x: x[:25] + "..." if len(x) > 25 else x
        )
    
    with filter_col3:
        st.session_state["filters"]["selected_years"] = st.multiselect(
            "Year", 
            years,
            default=st.session_state["filters"]["selected_years"],
            key="year_multiselect"
        )
    
    with filter_col4:
        st.session_state["filters"]["selected_regions"] = st.multiselect(
            "Region", 
            regions,
            default=st.session_state["filters"]["selected_regions"],
            key="region_multiselect"
        )
    
    with filter_col5:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        if st.button("🗑️ Clear", key="clear_filters", help="Reset all filters"):
            st.session_state["filters"] = {
                "selected_types": [],
                "selected_orgs": [],
                "selected_years": [],
                "selected_regions": []
            }
            st.rerun()
        
        # Show active filter count
        active_filters = (len(st.session_state["filters"]["selected_types"]) + 
                         len(st.session_state["filters"]["selected_orgs"]) + 
                         len(st.session_state["filters"]["selected_years"]) + 
                         len(st.session_state["filters"]["selected_regions"]))
        
        if active_filters > 0:
            st.markdown(f"<small style='color: #059669; font-size: 0.8rem;'>✓ {active_filters} active</small>", unsafe_allow_html=True)

    # Apply filters
    f = st.session_state["filters"]
    docs = all_docs
    
    # Filter by document type
    if f["selected_types"]:
        docs = [d for d in docs if d.get("document_type", "Unknown") in f["selected_types"]]
    
    # Filter by organization
    if f["selected_orgs"]:
        docs = [d for d in docs if d.get("organization", "Unknown") in f["selected_orgs"]]
    
    # Filter by year
    if f["selected_years"]:
        docs = [d for d in docs if any(year in str(d.get("date", "")) for year in f["selected_years"])]
    
    # Filter by region
    if f["selected_regions"]:
        docs = [d for d in docs if detect_region(d.get("organization", "Unknown")) in f["selected_regions"]]

    # Get display mode from session state (set in top controls)
    display_mode = st.session_state.get("display_mode", "cards")

    # Pagination
    per_page = 10
    page = st.session_state.get("doc_page", 0)
    total_pages = max(1, len(docs) // per_page + (1 if len(docs) % per_page else 0))

    if len(docs) > per_page:
        col1, col2, col3, col4, col5 = st.columns((1, 0.3, 2, 0.3, 1))
        with col2:
            if st.button("◀", key="prev_page", help="Previous page") and page > 0:
                st.session_state["doc_page"] = page - 1
                st.rerun()
        with col3:
            st.markdown(f"<div style='text-align: center; padding-top: 0.3rem;'>Page {page + 1} of {total_pages}</div>", unsafe_allow_html=True)
        with col4:
            if st.button("▶", key="next_page", help="Next page") and page < total_pages - 1:
                st.session_state["doc_page"] = page + 1
                st.rerun()

    start = page * per_page
    end = start + per_page
    page_docs = docs[start:end]



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
            content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
            
            # Use database metadata with HTML cleaning
            title = doc.get('title', 'Untitled Document') or 'Untitled Document'
            author_org = doc.get('author_organization', 'Unknown') or 'Unknown'
            
            # Clean date field of HTML artifacts
            raw_date = doc.get('publish_date', '') or ''
            if raw_date and raw_date != 'Unknown':
                # Remove HTML tags and artifacts
                clean_date = re.sub(r'<[^>]*>', '', str(raw_date))
                clean_date = re.sub(r'</[^>]*>', '', clean_date)
                clean_date = clean_date.strip()
                pub_date = clean_date if clean_date and len(clean_date) > 2 else 'Date not available'
            else:
                pub_date = 'Date not available'
            
            doc_type = doc.get('document_type', 'Unknown') or 'Unknown'
            
            # Calculate comprehensive scores
            scores = comprehensive_document_scoring(content, str(title))
            
            st.markdown(f"""
                <div style='border:1px solid #e0e0e0;padding:12px;border-radius:8px;margin:4px;
                background:linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                box-shadow:0 1px 3px rgba(0,0,0,0.1);height:220px;overflow:hidden'>
                    <div style='font-weight:bold;font-size:13px;margin-bottom:4px'>{title[:35]}{'...' if len(title) > 35 else ''}</div>
                    <div style='font-size:10px;color:#666;margin-bottom:6px'>{doc_type} • {author_org}</div>
                    <div style='font-size:9px;line-height:1.3;margin-bottom:6px'>
                        <div>AI Cybersecurity Maturity: {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity')}</div>
                        <div>Quantum Cybersecurity Maturity: {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity')}</div>
                        <div>AI Ethics: {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics')}</div>
                        <div>Quantum Ethics: {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics')}</div>
                    </div>
                    <div style='font-size:9px;color:#888'>{pub_date}</div>
                </div>
            """, unsafe_allow_html=True)

def render_grid_view(docs):
    """Render documents in grid layout."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
            
            # Use database metadata with HTML cleaning
            title = doc.get('title', 'Untitled Document') or 'Untitled Document'
            author_org = doc.get('author_organization', 'Unknown') or 'Unknown'
            
            # Clean date field of HTML artifacts
            raw_date = doc.get('publish_date', '') or ''
            if raw_date and raw_date != 'Unknown':
                # Remove HTML tags and artifacts
                clean_date = re.sub(r'<[^>]*>', '', str(raw_date))
                clean_date = re.sub(r'</[^>]*>', '', clean_date)
                clean_date = clean_date.strip()
                pub_date = clean_date if clean_date and len(clean_date) > 2 else 'Date not available'
            else:
                pub_date = 'Date not available'
            
            doc_type = doc.get('document_type', 'Unknown') or 'Unknown'
            content_preview = doc.get('content_preview', 'No preview available') or 'No preview available'
            
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
        content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
        
        # Use database metadata directly (already corrected)
        title = doc.get('title', 'Untitled Document') or 'Untitled Document'
        author_org = doc.get('author_organization', 'Unknown') or 'Unknown'
        pub_date = doc.get('publish_date') or 'N/A'
        doc_type = doc.get('document_type', 'Unknown') or 'Unknown'
        
        scores = comprehensive_document_scoring(content, str(title))
        
        table_data.append({
            'Title': title[:45],
            'Author/Org': author_org[:25],
            'Type': doc_type,
            'AI Cybersecurity Maturity': format_score_display(scores['ai_cybersecurity'], 'ai_cybersecurity'),
            'Quantum Cybersecurity Maturity': format_score_display(scores['quantum_cybersecurity'], 'quantum_cybersecurity'),
            'AI Ethics': format_score_display(scores['ai_ethics'], 'ai_ethics'),
            'Q Ethics': format_score_display(scores['quantum_ethics'], 'quantum_ethics'),
            'Date': str(pub_date) if pub_date else 'N/A'
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_minimal_list(docs):
    """Render documents in minimal list format."""
    for idx, doc in enumerate(docs):
        content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
        
        # Use database metadata with HTML cleaning
        title = doc.get('title', 'Untitled Document') or 'Untitled Document'
        author_org = doc.get('author_organization', 'Unknown') or 'Unknown'
        
        # Clean date field of HTML artifacts
        raw_date = doc.get('publish_date', '') or ''
        if raw_date and raw_date != 'Unknown':
            # Remove HTML tags and artifacts
            clean_date = re.sub(r'<[^>]*>', '', str(raw_date))
            clean_date = re.sub(r'</[^>]*>', '', clean_date)
            clean_date = clean_date.strip()
            pub_date = clean_date if clean_date and len(clean_date) > 2 else 'Date not available'
        else:
            pub_date = 'Date not available'
        
        doc_type = doc.get('document_type', 'Unknown') or 'Unknown'
        content_preview = doc.get('content_preview', 'No preview available') or 'No preview available'
        
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
                # Clean the raw content for display
                clean_content = re.sub(r'<[^>]+>', '', content)  # Remove HTML tags
                clean_content = re.sub(r"style='[^']*'", '', clean_content)  # Remove style attributes
                clean_content = re.sub(r'\s+', ' ', clean_content).strip()  # Normalize whitespace
                st.write(clean_content[:500] + "..." if len(clean_content) > 500 else clean_content)

def render_card_view(docs):
    """Render documents in full card format."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            # Get raw content for scoring
            raw_content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
            
            # Use database metadata with HTML cleaning
            title = doc.get('title', 'Untitled Document') or 'Untitled Document'
            author_org = doc.get('author_organization', 'Unknown') or 'Unknown'
            
            # Clean date field of HTML artifacts
            raw_date = doc.get('publish_date', '') or ''
            if raw_date and raw_date != 'Unknown':
                # Remove HTML tags and artifacts
                clean_date = re.sub(r'<[^>]*>', '', str(raw_date))
                clean_date = re.sub(r'</[^>]*>', '', clean_date)
                clean_date = clean_date.strip()
                pub_date = clean_date if clean_date and len(clean_date) > 2 else 'Date not available'
            else:
                pub_date = 'Date not available'
            
            doc_type = doc.get('document_type', 'Unknown') or 'Unknown'
            content_preview = doc.get('content_preview', 'No preview available') or 'No preview available'
            
            # Display metadata card (no scoring involved)
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
                </div>
            """, unsafe_allow_html=True)
            
            # ISOLATED STEP 3: Calculate scores separately (after metadata display)
            try:
                scores = comprehensive_document_scoring(raw_content, str(title))
                
                # Display scores in completely separate section
                st.markdown(f"""
                    <div style='margin:8px;padding:8px;background:#f8f9fa;border-radius:6px'>
                        <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px'>
                            <div><strong>AI Cybersecurity Maturity:</strong> {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity')}</div>
                            <div><strong>Quantum Cybersecurity Maturity:</strong> {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity')}</div>
                            <div><strong>AI Ethics:</strong> {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics')}</div>
                            <div><strong>Quantum Ethics:</strong> {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics')}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Scoring error: {e}")
            
            # ISOLATED STEP 4: Display clean content preview (completely separate from scoring)
            with st.expander("Intelligent Content Preview"):
                # Emergency bypass: Generate completely clean text directly from raw content
                bypass_content = re.sub(r'<[^>]*>', '', raw_content)  # Remove all tags
                bypass_content = re.sub(r'</[^>]*>', '', bypass_content)  # Remove closing tags
                bypass_content = re.sub(r'[<>/]', '', bypass_content)  # Remove brackets/slashes
                bypass_content = re.sub(r'&[a-zA-Z0-9#]+;?', ' ', bypass_content)  # Remove entities
                bypass_content = re.sub(r'\bdiv\b|\bspan\b', '', bypass_content, flags=re.IGNORECASE)  # Remove div/span words
                bypass_content = re.sub(r'\s+', ' ', bypass_content).strip()  # Normalize spaces
                
                # Extract first meaningful sentences directly
                sentences = bypass_content.split('.')[:3]
                clean_sentences = []
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 20 and any(c.isalpha() for c in sentence):
                        clean_sentences.append(sentence)
                
                if clean_sentences:
                    final_text = '. '.join(clean_sentences) + '.'
                    if len(final_text) > 200:
                        final_text = final_text[:197] + '...'
                    st.text(final_text)  # Use st.text() instead of st.write() to avoid HTML processing
                else:
                    st.text("Content preview not available")