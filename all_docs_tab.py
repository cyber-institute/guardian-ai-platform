import streamlit as st
import re
from utils.db import fetch_documents

# Performance optimization: Cache document fetching
@st.cache_data(ttl=180)  # Cache for 3 minutes
def fetch_documents_cached():
    """Cached version of document fetching to improve performance"""
    return fetch_documents()
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf
from utils.comprehensive_scoring import comprehensive_document_scoring, format_score_display, get_score_badge_color

# Performance optimization: Cache scoring calculations
@st.cache_data(ttl=600)  # Cache for 10 minutes
def comprehensive_document_scoring_cached(content, title):
    """Cached version of comprehensive scoring to improve performance"""
    return comprehensive_document_scoring(content, title)
# Performance caching will be handled directly in functions
from utils.document_metadata_extractor import extract_document_metadata
from utils.multi_llm_metadata_extractor import extract_clean_metadata
from utils.html_artifact_interceptor import clean_documents, clean_field
from utils.content_cleaner import clean_document_content
from utils.clean_preview_generator import generate_clean_preview, extract_clean_metadata
from utils.simple_updater import update_document_metadata
from components.chatbot_widget import create_tooltip, render_help_tooltip
from utils.thumbnail_generator import get_thumbnail_html
from components.recommendation_widget import render_document_recommendations, render_recommendation_sidebar

def ultra_clean_metadata(field_value):
    """Remove all HTML artifacts from metadata fields using enhanced interceptor"""
    return clean_field(field_value)

def clean_date_safely(doc):
    """Safely clean date field to prevent None value issues causing </div> artifacts"""
    raw_date = doc.get('publish_date')
    
    # Handle None, empty, or invalid values first
    if raw_date is None or raw_date == '' or str(raw_date).lower() in ['none', 'null', 'unknown']:
        return 'Date not available'
    
    # Only process valid date values
    try:
        cleaned_date = ultra_clean_metadata(str(raw_date))
        if cleaned_date and cleaned_date != 'Unknown' and len(cleaned_date.strip()) >= 4:
            # Format date properly if it looks like a date
            date_str = cleaned_date.strip()
            if len(date_str) == 10 and date_str.count('-') == 2:
                return date_str  # Already in YYYY-MM-DD format
            elif len(date_str) >= 4:
                return date_str
            else:
                return 'Date not available'
        else:
            return 'Date not available'
    except:
        return 'Date not available'

def get_comprehensive_badge(score, framework, doc_content="", doc_title=""):
    """Create badge for comprehensive scoring system with intelligent topic detection."""
    
    if score is None or score == 0:
        # Determine if framework is applicable based on content
        content_lower = (doc_content + " " + doc_title).lower()
        
        # Check if document discusses relevant topics
        if 'ai' in framework:
            ai_keywords = ['artificial intelligence', 'machine learning', 'ai ', ' ai', 'neural network', 'algorithm']
            is_ai_related = any(keyword in content_lower for keyword in ai_keywords)
            if not is_ai_related:
                return "<span style='color:#6c757d;font-size:9px'>N/A</span>"
        
        if 'quantum' in framework:
            quantum_keywords = ['quantum', 'post-quantum', 'quantum-safe', 'qkd', 'quantum computing']
            is_quantum_related = any(keyword in content_lower for keyword in quantum_keywords)
            if not is_quantum_related:
                return "<span style='color:#6c757d;font-size:9px'>N/A</span>"
        
        return "0"
    
    # Get clean score display and remove any HTML artifacts
    display_score = format_score_display(score, framework)
    
    # Ultra-clean any HTML that might have leaked through
    clean_score = ultra_clean_metadata(str(display_score))
    
    return clean_score

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

def is_probably_ai(content):
    """Check if content is probably AI-related."""
    if not content:
        return False
    
    content_lower = content.lower()
    ai_keywords = [
        'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
        'ai ', ' ai', 'ml ', ' ml', 'algorithm', 'data science', 'nlp',
        'natural language processing', 'computer vision', 'reinforcement learning',
        'supervised learning', 'unsupervised learning', 'neural', 'deep neural',
        'artificial neural', 'model training', 'data mining', 'predictive analytics'
    ]
    
    return any(keyword in content_lower for keyword in ai_keywords)

def get_document_topic(doc):
    """Determine if document is AI, Quantum, or Both based on content."""
    # Check content sources
    content_sources = [
        doc.get('title', ''),
        doc.get('content', ''),
        doc.get('abstract', ''),
        doc.get('description', ''),
        doc.get('document_type', ''),
        doc.get('organization', '')
    ]
    
    full_content = ' '.join(str(source) for source in content_sources if source)
    
    is_ai = is_probably_ai(full_content)
    is_quantum = is_probably_quantum(full_content)
    
    if is_ai and is_quantum:
        return "Both"
    elif is_quantum:
        return "Quantum"
    elif is_ai:
        return "AI"
    else:
        return "Both"  # Show documents that don't clearly fit either category

def render():
    

    
    try:
        # Force refresh documents - clear all caching mechanisms
        if 'documents_cache' in st.session_state:
            del st.session_state['documents_cache']
        if 'all_docs' in st.session_state:
            del st.session_state['all_docs']
        if 'cached_docs' in st.session_state:
            del st.session_state['cached_docs']
        

        
        # Fetch fresh documents directly from database with comprehensive HTML cleaning
        raw_docs = fetch_documents_cached()
        if not raw_docs:
            st.info("No documents found in the database. Please upload some documents first.")
            return
            
        # Apply comprehensive metadata cleaning to eliminate all HTML artifacts
        from utils.metadata_cleaner import clean_document_list
        all_docs = clean_document_list(raw_docs)
        
        # Clean all documents and force fresh metadata analysis
        all_docs = [clean_document_content(doc) for doc in all_docs]
        # Force regeneration of all metadata with enhanced cleaning
        for doc in all_docs:
            doc.pop('analyzed_metadata', None)  # Remove any cached metadata
                
    except Exception as e:
        st.error(f"Error fetching documents: {e}")
        return

    # Extract filter options from documents using correct field names
    doc_types = sorted(set(doc.get("document_type", "Unknown") for doc in all_docs if doc.get("document_type") and doc.get("document_type") not in ["Unknown", ""]))
    
    # Extract organizations with better handling
    organizations = set()
    for doc in all_docs:
        org = doc.get("author_organization", "")
        if org and org not in ["Unknown", "", "Date not available"]:
            # Truncate long organization names for display
            org_display = org[:40] + "..." if len(org) > 40 else org
            organizations.add(org_display)
    organizations = sorted(list(organizations))
    
    # Extract years from publish_date field
    years = set()
    for doc in all_docs:
        # Try publish_date first, then other date fields
        date_fields = ["publish_date", "date", "created_at", "updated_at"]
        for field in date_fields:
            date_str = doc.get(field, "")
            if date_str and str(date_str) != "Date not available":
                try:
                    # Try to extract year from various date formats
                    import re
                    year_match = re.search(r'\b(19|20)\d{2}\b', str(date_str))
                    if year_match:
                        years.add(year_match.group())
                        break  # Found a year, stop looking in other fields
                except:
                    pass
    years = sorted(list(years), reverse=True)
    
    # Extract regions from detected_region field with fallback to pattern-based detection
    regions = set()
    for doc in all_docs:
        # First try to use the AI-detected region
        detected_region = doc.get("detected_region", "")
        if detected_region and detected_region not in ["Unknown", "", "None"]:
            regions.add(detected_region)
        else:
            # Fallback to pattern-based detection for documents without AI analysis
            org = doc.get("author_organization", "")
            if org and org not in ["Unknown", "", "Date not available"]:
                org_lower = org.lower()
                if any(term in org_lower for term in ['nist', 'dhs', 'usa', 'united states', 'us ', 'federal', 'dod', 'nasa']):
                    regions.add('US')
                elif any(term in org_lower for term in ['eu', 'european', 'gdpr', 'enisa', 'europa']):
                    regions.add('EU')
                elif any(term in org_lower for term in ['uk', 'britain', 'british', 'ncsc']):
                    regions.add('UK')
                elif any(term in org_lower for term in ['iso', 'itu', 'oecd', 'un ', 'united nations']):
                    regions.add('International')
                elif any(term in org_lower for term in ['china', 'japan', 'korea', 'singapore', 'asia']):
                    regions.add('Asia')
                elif any(term in org_lower for term in ['canada', 'australia', 'new zealand']):
                    regions.add('Other')
    
    regions = sorted(list(regions))
    
    # Debug output for troubleshooting empty filters
    if len(organizations) == 0 or len(years) == 0 or len(regions) == 0:
        st.write("**Debug: Filter extraction status:**")
        st.write(f"- Found {len(doc_types)} document types: {doc_types[:5]}")
        st.write(f"- Found {len(organizations)} organizations: {organizations[:5]}")
        st.write(f"- Found {len(years)} years: {years[:5]}")
        st.write(f"- Found {len(regions)} regions: {regions}")
        
        # Sample document inspection
        if all_docs:
            sample_doc = all_docs[0]
            st.write("**Sample document fields:**")
            for key in ["author_organization", "publish_date", "document_type"]:
                st.write(f"- {key}: `{sample_doc.get(key, 'NOT FOUND')}`")

    # Initialize filters in session state
    if "filters" not in st.session_state:
        st.session_state["filters"] = {
            "selected_types": [],
            "selected_orgs": [],
            "selected_years": [],
            "selected_regions": [],
            "topic_filter": "Both"
        }

    # Compact filter controls with inline topic and view mode
    
    # Topic filter and View Mode on same row
    topic_col, spacer_col, view_col = st.columns([2, 2, 3])
    
    with topic_col:
        topic_filter = st.radio(
            "**Topic Filter:**",
            ["AI", "Quantum", "Both"],
            index=["AI", "Quantum", "Both"].index(st.session_state["filters"]["topic_filter"]),
            horizontal=True,
            key="topic_filter_radio"
        )
        st.session_state["filters"]["topic_filter"] = topic_filter
    
    with view_col:
        # Display mode selection with radio buttons (right-justified)
        st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
        display_mode = st.session_state.get("display_mode", "cards")
        display_mode = st.radio(
            "**View Mode:**",
            ["cards", "compact", "table", "grid", "minimal"],
            index=["cards", "compact", "table", "grid", "minimal"].index(display_mode),
            format_func=lambda x: {
                "cards": "Cards",
                "compact": "Compact", 
                "table": "Table",
                "grid": "Grid",
                "minimal": "Minimal"
            }[x],
            horizontal=True,
            key="display_mode_radio"
        )
        st.session_state["display_mode"] = display_mode
        st.markdown('</div>', unsafe_allow_html=True)
    

    
    st.markdown("---")  # Separator line
    
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
                "selected_regions": [],
                "topic_filter": "Both"
            }
            st.rerun()
        
        # Show active filter count
        active_filters = (len(st.session_state["filters"]["selected_types"]) + 
                         len(st.session_state["filters"]["selected_orgs"]) + 
                         len(st.session_state["filters"]["selected_years"]) + 
                         len(st.session_state["filters"]["selected_regions"]) +
                         (1 if st.session_state["filters"]["topic_filter"] != "Both" else 0))
        
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
    
    # Filter by region using AI-detected regions with fallback
    if f["selected_regions"]:
        def get_document_region(doc):
            # First try AI-detected region
            detected_region = doc.get("detected_region", "")
            if detected_region and detected_region not in ["Unknown", "", "None"]:
                return detected_region
            
            # Fallback to pattern-based detection
            org = doc.get("author_organization", "") or doc.get("organization", "")
            if org and org not in ["Unknown", "", "Date not available"]:
                org_lower = org.lower()
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
        
        docs = [d for d in docs if get_document_region(d) in f["selected_regions"]]
    
    # Filter by topic (AI/Quantum/Both)
    topic_filter = f.get("topic_filter", "Both")
    if topic_filter != "Both":
        if topic_filter == "AI":
            docs = [d for d in docs if get_document_topic(d) in ["AI", "Both"]]
        elif topic_filter == "Quantum":
            docs = [d for d in docs if get_document_topic(d) in ["Quantum", "Both"]]

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
    
    # Document Upload and URL Input Section
    st.markdown("---")
    st.markdown("### Add New Documents")
    
    upload_col1, upload_col2 = st.columns(2)
    
    with upload_col1:
        st.markdown("#### 📄 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt', 'docx'],
            help="Upload PDF, TXT, or DOCX files for analysis",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Import enhanced policy uploader
            from components.enhanced_policy_uploader import process_uploaded_file
            
            if st.button("🚀 Process Upload", type="primary", use_container_width=True):
                with st.spinner("Processing uploaded document..."):
                    try:
                        result = process_uploaded_file(uploaded_file)
                        if result:
                            st.success("Document processed successfully!")
                            st.info("Refresh the page to see the new document in your collection")
                        else:
                            st.error("Failed to process document")
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")
    
    with upload_col2:
        st.markdown("#### 🌐 Add from URL")
        url_input = st.text_input(
            "Enter document URL",
            placeholder="https://example.com/document.pdf",
            help="Enter a URL to a document for analysis",
            label_visibility="collapsed"
        )
        
        if url_input:
            # Import URL processing functionality
            from utils.fast_admin_loader import process_url_content
            
            if st.button("🔗 Process URL", type="primary", use_container_width=True):
                with st.spinner("Processing URL content..."):
                    try:
                        # Use the enhanced URL processing from admin loader
                        import requests
                        import trafilatura
                        from utils.patent_scoring_engine import comprehensive_document_scoring
                        from utils.database import get_db_connection
                        import uuid
                        
                        # Fetch and process URL content
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                        }
                        response = requests.get(url_input, headers=headers, timeout=30)
                        response.raise_for_status()
                        
                        # Extract content
                        content = trafilatura.extract(response.text, include_comments=False, include_tables=True)
                        
                        if content and len(content.strip()) > 100:
                            # Generate document ID and basic metadata
                            doc_id = str(uuid.uuid4())
                            title = url_input.split('/')[-1] or "URL Document"
                            
                            # Score the document
                            scores = comprehensive_document_scoring(content, title)
                            
                            # Save to database
                            conn = get_db_connection()
                            cursor = conn.cursor()
                            
                            cursor.execute("""
                                INSERT INTO documents (
                                    id, title, content, source_url, document_type,
                                    ai_cybersecurity_score, quantum_cybersecurity_score,
                                    ai_ethics_score, quantum_ethics_score,
                                    upload_date
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                            """, (
                                doc_id, title, content, url_input, "URL Document",
                                scores.get('ai_cybersecurity', 0),
                                scores.get('quantum_cybersecurity', 0), 
                                scores.get('ai_ethics', 0),
                                scores.get('quantum_ethics', 0)
                            ))
                            
                            conn.commit()
                            cursor.close()
                            conn.close()
                            
                            st.success("URL content processed successfully!")
                            st.info("Refresh the page to see the new document in your collection")
                        else:
                            st.error("Could not extract sufficient content from URL")
                            
                    except Exception as e:
                        st.error(f"Error processing URL: {str(e)}")
                        st.info("Please verify the URL is accessible and contains readable content")
    
    # Policy Analyzer Modal Button
    st.markdown("---")
    st.markdown("### Advanced Analysis")
    
    analyze_col1, analyze_col2 = st.columns([1, 2])
    
    with analyze_col1:
        if st.button("📋 Open Policy Analyzer", type="secondary", use_container_width=True):
            st.session_state.show_policy_analyzer = True
            st.rerun()
    
    with analyze_col2:
        st.markdown("*Comprehensive policy analysis with gap detection and recommendations*")
    
    # Policy Analyzer Modal
    if st.session_state.get('show_policy_analyzer', False):
        render_policy_analyzer_modal()

def render_policy_analyzer_modal():
    """Render the Policy Analyzer in a modal-style container"""
    
    # Create a visually distinct modal-style container
    st.markdown("""
    <style>
    .policy-modal {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
        position: relative;
    }
    .modal-header {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 12px;
        margin: -2rem -2rem 2rem -2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Modal container with custom styling
    with st.container():
        st.markdown('<div class="policy-modal">', unsafe_allow_html=True)
        
        # Header with close button
        header_col1, header_col2 = st.columns([4, 1])
        
        with header_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); 
                        color: white; padding: 1rem 2rem; border-radius: 12px; margin-bottom: 2rem;">
                <h2 style="margin: 0; color: white;">📋 Policy Analyzer</h2>
                <p style="margin: 0.5rem 0 0 0; color: #bfdbfe; font-size: 0.9rem;">
                    Comprehensive policy analysis with gap detection and recommendations
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with header_col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            if st.button("✕ Close", key="close_modal", type="secondary", use_container_width=True):
                st.session_state.show_policy_analyzer = False
                st.rerun()
        
        # Policy Analyzer content in the modal
        with st.container():
            from components.enhanced_policy_uploader import render_enhanced_policy_uploader
            render_enhanced_policy_uploader()
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_compact_cards(docs):
    """Render documents in compact card format."""
    cols = st.columns(3)
    for i, doc in enumerate(docs):
        with cols[i % 3]:
            content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
            
            # Use database metadata with comprehensive HTML cleaning
            title = ultra_clean_metadata(doc.get('title', 'Untitled Document'))
            author_org = ultra_clean_metadata(doc.get('author_organization', 'Unknown'))
            
            # Clean date field safely to prevent </div> artifacts
            pub_date = clean_date_safely(doc)
            
            doc_type = ultra_clean_metadata(doc.get('document_type', 'Unknown'))
            
            # Use simple placeholder thumbnail for performance
            thumbnail_html = f'<div style="width:60px;height:75px;background:#f0f0f0;border:1px solid #ddd;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:10px;color:#666;">Doc</div>'
            
            # Use actual database scores instead of recalculating
            scores = {
                'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
                'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
                'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
                'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
            }
            
            # Properly escape all HTML content for compact cards
            import html
            
            safe_title = html.escape(title)
            safe_doc_type = html.escape(doc_type)
            safe_author_org = html.escape(author_org)
            safe_pub_date = html.escape(pub_date)
            
            st.markdown(f"""
                <div style='border:1px solid #e0e0e0;padding:12px;border-radius:8px;margin:4px;
                background:linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                box-shadow:0 1px 3px rgba(0,0,0,0.1);height:240px;overflow:hidden'>
                    <div style='display:flex;align-items:flex-start;gap:8px;margin-bottom:6px'>
                        <div style='flex-shrink:0'>
                            {thumbnail_html.replace('width:120px;height:150px', 'width:60px;height:75px')}
                        </div>
                        <div style='flex:1;min-width:0'>
                            <div style='font-weight:bold;font-size:12px;margin-bottom:4px;line-height:1.2'>{safe_title[:32]}{'...' if len(safe_title) > 32 else ''}</div>
                            <div style='font-size:9px;color:#666;margin-bottom:6px'>{safe_doc_type} • {safe_author_org[:15]}{'...' if len(safe_author_org) > 15 else ''}</div>
                        </div>
                    </div>
                    <div style='font-size:8px;line-height:1.3;margin-bottom:6px'>
                        <div>AI Cyber: {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity', content, title)}</div>
                        <div>Q Cyber: {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity', content, title)}</div>
                        <div>AI Ethics: {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics', content, title)}</div>
                        <div>Q Ethics: {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics', content, title)}</div>
                    </div>
                    <div style='font-size:8px;color:#888'>{safe_pub_date if safe_pub_date != 'Date not available' else 'Date not available'}</div>
                </div>
            """, unsafe_allow_html=True)

def render_grid_view(docs):
    """Render documents in grid layout."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
            
            # Use database metadata with comprehensive HTML cleaning
            title = ultra_clean_metadata(doc.get('title', 'Untitled Document'))
            author_org = ultra_clean_metadata(doc.get('author_organization', 'Unknown'))
            
            # Clean date field safely to prevent </div> artifacts
            pub_date = clean_date_safely(doc)
            
            doc_type = ultra_clean_metadata(doc.get('document_type', 'Unknown'))
            content_preview = ultra_clean_metadata(doc.get('content_preview', 'No preview available') or 'No preview available')
            
            # Use actual database scores instead of recalculating
            scores = {
                'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
                'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
                'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
                'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
            }
            
            # Properly escape all HTML content for grid view
            import html
            
            safe_title = html.escape(title)
            safe_doc_type = html.escape(doc_type)
            safe_author_org = html.escape(author_org)
            safe_pub_date = html.escape(pub_date)
            safe_content_preview = html.escape(content_preview)
            
            st.markdown(f"""
                <div style='border:2px solid #f0f0f0;padding:12px;border-radius:8px;margin:6px;
                background:white;box-shadow:0 2px 4px rgba(0,0,0,0.08);
                border-left:4px solid #3B82F6'>
                    <h4 style='margin:0 0 6px 0;font-size:15px'>{safe_title[:40]}{'...' if len(safe_title) > 40 else ''}</h4>
                    <div style='font-size:10px;color:#666;margin-bottom:8px'>{safe_doc_type} • {safe_author_org} • {safe_pub_date}</div>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:8px;font-size:10px'>
                        <div>AI Cyber: {get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity', content, title)}</div>
                        <div>Q Cyber: {get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity', content, title)}</div>
                        <div>AI Ethics: {get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics', content, title)}</div>
                        <div>Q Ethics: {get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics', content, title)}</div>
                    </div>
                    <p style='font-size:11px;color:#666;margin:0'>{safe_content_preview[:120]}{'...' if len(safe_content_preview) > 120 else ''}</p>
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
        
        # Use actual database scores instead of recalculating
        scores = {
            'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
            'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
            'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
            'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
        }
        
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
        
        # Use actual database scores instead of recalculating
        scores = {
            'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
            'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
            'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
            'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
        }
        
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"**{title}**")
            topic = ultra_clean_metadata(doc.get('topic', 'General'))
            st.caption(f"{topic} • {doc_type} • {author_org} • {pub_date}")
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
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
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
        
        with col2:
            # Quick report generation
            has_scores = any([scores[key] > 0 for key in scores.keys()])
            if has_scores:
                if st.button("📊 Quick Report", key=f"quick_report_{idx}"):
                    from components.risk_report_interface import RiskReportInterface
                    interface = RiskReportInterface()
                    interface._generate_quick_report(doc)
            else:
                st.caption("Risk scoring required")
        
        with col3:
            if has_scores:
                if st.button("📧 Email Report", key=f"email_report_{idx}"):
                    st.info("Email functionality available in Risk Reports section")

def render_card_view(docs):
    """Render documents in full card format."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            # Get raw content for scoring
            raw_content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
            
            # Use database metadata with comprehensive HTML cleaning
            title = ultra_clean_metadata(doc.get('title', 'Untitled Document'))
            author_org = ultra_clean_metadata(doc.get('author_organization', 'Unknown'))
            
            # Clean date field safely to prevent </div> artifacts
            pub_date = clean_date_safely(doc)
            
            doc_type = ultra_clean_metadata(doc.get('document_type', 'Unknown'))
            content_preview = ultra_clean_metadata(doc.get('content_preview', 'No preview available') or 'No preview available')
            
            # Display metadata card without thumbnail (Card View)
            import html
            
            # Properly escape all HTML content
            safe_title = html.escape(title)
            safe_doc_type = html.escape(doc_type)
            safe_author_org = html.escape(author_org)
            safe_pub_date = html.escape(pub_date)
            safe_topic = html.escape(ultra_clean_metadata(doc.get('topic', 'General')))
            
            st.markdown(f"""
                <div style='border:1px solid #ddd;padding:20px;border-radius:12px;margin:8px;
                background:white;box-shadow:0 4px 6px rgba(0,0,0,0.1);
                transition:transform 0.2s ease;border-left:5px solid #3B82F6'>
                    <h3 style='margin:0 0 12px 0;color:#333;line-height:1.3'>{safe_title}</h3>
                    <div style='margin-bottom:10px;display:flex;gap:8px;flex-wrap:wrap'>
                        <span style='background:#e8f5e8;padding:4px 10px;border-radius:12px;font-size:12px;color:#2e7d32'>{safe_topic}</span>
                        <span style='background:#f0f0f0;padding:4px 10px;border-radius:12px;font-size:12px'>{safe_doc_type}</span>
                        <span style='background:#e0f2fe;padding:4px 10px;border-radius:12px;font-size:12px;color:#0277bd'>{safe_author_org}</span>
                        {f"<span style='background:#f3e5f5;padding:4px 10px;border-radius:12px;font-size:12px;color:#7b1fa2'>{safe_pub_date}</span>" if pub_date and pub_date != 'Date not available' else "<span style='background:#ffeaa7;padding:4px 10px;border-radius:12px;font-size:12px;color:#636e72'>Date not available</span>"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # ISOLATED STEP 3: Calculate scores separately (after metadata display)
            try:
                scores = comprehensive_document_scoring_cached(raw_content, str(title))
                
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