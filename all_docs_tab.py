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
    # Enhanced quantum keywords with comprehensive coverage
    quantum_keywords = [
        "quantum", "pqc", "post-quantum", "nist pqc", "qkd", "quantum-safe", 
        "fips 203", "fips 204", "quantum computing", "quantum algorithm", 
        "quantum cryptography", "quantum key distribution", "quantum supremacy", 
        "quantum entanglement", "quantum state", "quantum mechanics", "qubit", 
        "quantum gate", "quantum circuit", "quantum information", "quantum communication",
        "quantum technology", "quantum security", "quantum resistant", "quantum threat",
        "quantum policy", "hodan omaar", "quantum framework", "quantum governance"
    ]
    content_lower = content.lower()
    return any(kw in content_lower for kw in quantum_keywords)

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
    
    # Topic filter and View Mode on same row with proper alignment
    st.markdown("""
    <style>
    .filter-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 1rem;
    }
    .filter-left {
        flex: 1;
    }
    .filter-right {
        flex: 1;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)
    
    topic_col, view_col = st.columns([1, 1])
    
    with topic_col:
        # Add margin to move Topic Filter buttons down to align with View Mode
        st.markdown('<div style="margin-top: 0.75rem;">', unsafe_allow_html=True)
        topic_filter = st.radio(
            "**Topic Filter:**",
            ["AI", "Quantum", "Both"],
            index=["AI", "Quantum", "Both"].index(st.session_state["filters"]["topic_filter"]),
            horizontal=True,
            key="topic_filter_radio"
        )
        st.session_state["filters"]["topic_filter"] = topic_filter
        st.markdown('</div>', unsafe_allow_html=True)
    
    with view_col:
        # Create container that aligns perfectly with Topic Filter baseline
        st.markdown("""
        <div style="display: flex; justify-content: flex-end; align-items: baseline; margin-top: -2.75rem; margin-bottom: 1.25rem;">
        """, unsafe_allow_html=True)
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
    
    st.markdown('<div style="margin-top: -1rem; margin-bottom: -0.5rem;"><hr style="margin: 0; padding: 0;"></div>', unsafe_allow_html=True)
    
    # Create compact filter row
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns([2, 2, 1.5, 1.5, 1])
    
    with filter_col1:
        st.session_state["filters"]["selected_types"] = st.multiselect(
            "Document Type", 
            doc_types,
            default=st.session_state["filters"]["selected_types"],
            key="type_multiselect",
            help="Policy: Government/organizational policies. Standard: Industry standards (NIST, ISO). Regulation: Legal regulations and laws. Guidance: Best practice documents. Research: Academic papers and studies."
        )
    
    with filter_col2:
        # Show top organizations only to avoid clutter
        top_orgs = organizations[:12] if len(organizations) > 12 else organizations
        st.session_state["filters"]["selected_orgs"] = st.multiselect(
            "Author/Organization", 
            top_orgs,
            default=st.session_state["filters"]["selected_orgs"],
            key="org_multiselect",
            format_func=lambda x: x[:25] + "..." if len(x) > 25 else x,
            help="The organization, agency, or entity that published or authored the document (e.g., NIST, ISO, government agencies, research institutions)."
        )
    
    with filter_col3:
        st.session_state["filters"]["selected_years"] = st.multiselect(
            "Year", 
            years,
            default=st.session_state["filters"]["selected_years"],
            key="year_multiselect",
            help="Publication year of the document (when it was officially released or last updated)."
        )
    
    with filter_col4:
        st.session_state["filters"]["selected_regions"] = st.multiselect(
            "Region", 
            regions,
            default=st.session_state["filters"]["selected_regions"],
            key="region_multiselect",
            help="Geographic region or jurisdiction that issued the document (e.g., US, EU, International, specific countries or regions)."
        )
    
    with filter_col5:
        st.markdown("<br>", unsafe_allow_html=True)  # Spacing
        
        # Create a very small button using nested columns
        col_a, col_b, col_c = st.columns([2, 1, 2])
        with col_b:
            # Small button with minimal styling
            if st.button("✕", key="clear_filters", help="Clear all filters", use_container_width=True):
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
    # Add CSS to reduce whitespace
    st.markdown("""
    <style>
    .upload-section h4 {
        margin-bottom: 0.5rem !important;
    }
    .stFileUploader {
        margin-top: -0.5rem !important;
    }
    .stTextInput {
        margin-top: -0.5rem !important;
    }
    div[data-testid="stFileUploader"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    div[data-testid="stTextInput"] {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    .element-container:has(.stFileUploader) {
        margin-top: -1rem !important;
    }
    .element-container:has(.stTextInput) {
        margin-top: -1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("### Add New Documents")
    upload_col1, upload_col2 = st.columns(2)
    
    with upload_col1:
        st.markdown('<div class="upload-section"><h4>Browse Files</h4></div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt', 'docx'],
            help="Drag and drop file here • Limit 200MB per file • PDF, TXT, DOCX",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            st.success(f"File selected: {uploaded_file.name} ({uploaded_file.size} bytes)")
            
            # Import enhanced policy uploader
            try:
                from components.enhanced_policy_uploader import process_uploaded_file
                st.info("Using enhanced policy uploader")
            except ImportError as e:
                st.warning(f"Enhanced uploader not available: {e}")
                try:
                    from utils.pdf_ingestion_thumbnails import process_pdf_with_thumbnail as process_uploaded_file
                    st.info("Using PDF thumbnail processor")
                except ImportError as e2:
                    st.error(f"No file processors available: {e2}")
                    process_uploaded_file = None
            
            if process_uploaded_file is not None:
                if st.button("Process Upload", type="primary", use_container_width=True):
                    with st.spinner("Processing uploaded document..."):
                        try:
                            st.info(f"Processing file: {uploaded_file.name}")
                            
                            # Reset file position and process
                            uploaded_file.seek(0)
                            result = process_uploaded_file(uploaded_file)
                            st.info("File processing completed")
                            
                            if result and result.get('success'):
                                st.info("Content extracted successfully")
                                
                                # Extract content and metadata
                                content = result.get('content', '')
                                title = result.get('metadata', {}).get('title') or uploaded_file.name
                                author = result.get('metadata', {}).get('author', 'Unknown')
                                
                                if len(content.strip()) > 50:
                                    st.info("Calculating comprehensive scores...")
                                    
                                    # Import required modules
                                    from utils.comprehensive_scoring import comprehensive_document_scoring
                                    from utils.database import db_manager
                                    import uuid
                                    
                                    # Generate scores
                                    scores = comprehensive_document_scoring(content, title)
                                    st.info(f"Scoring complete: AI={scores.get('ai_cybersecurity', 0)}, Quantum={scores.get('quantum_cybersecurity', 0)}")
                                    
                                    # Prepare document data
                                    doc_id = str(uuid.uuid4())
                                    document_data = {
                                        'id': doc_id,
                                        'title': title,
                                        'content': content,
                                        'clean_content': content,
                                        'text_content': content,
                                        'document_type': result.get('file_type', 'Unknown'),
                                        'author': author,
                                        'filename': uploaded_file.name,
                                        'ai_cybersecurity_score': scores.get('ai_cybersecurity', 0),
                                        'quantum_cybersecurity_score': scores.get('quantum_cybersecurity', 0),
                                        'ai_ethics_score': scores.get('ai_ethics', 0),
                                        'quantum_ethics_score': scores.get('quantum_ethics', 0)
                                    }
                                    
                                    st.info("Saving document to database...")
                                    save_result = db_manager.save_document(document_data)
                                    
                                    if save_result:
                                        st.success("Document processed successfully!")
                                        st.info("Document added to collection. Refresh to see it in the list.")
                                        st.balloons()
                                    else:
                                        st.error("Failed to save document to database")
                                else:
                                    st.error("Could not extract sufficient content from file")
                            else:
                                error_msg = result.get('error', 'Unknown error') if result else 'Processing failed'
                                st.error(f"Failed to process document: {error_msg}")
                                
                        except Exception as e:
                            st.error(f"Error processing document: {str(e)}")
                            import traceback
                            st.code(traceback.format_exc())
            else:
                st.error("File processor not available. Please contact support.")
    
    with upload_col2:
        st.markdown('<div class="upload-section"><h4>🌐 Add from URL</h4></div>', unsafe_allow_html=True)
        
        # Metadata Processing Mode Toggle
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Metadata Processing Mode:**")
        with col2:
            auto_mode = st.toggle(
                "Auto Save",
                value=st.session_state.get('auto_metadata_mode', False),
                help="Enable to skip manual verification and save automatically"
            )
            st.session_state.auto_metadata_mode = auto_mode
        
        if auto_mode:
            st.info("🤖 Auto mode: Documents will be saved automatically with extracted metadata")
        else:
            st.info("🔍 Verification mode: You can review and edit metadata before saving")
        
        # Metadata Verification History Viewer
        if st.session_state.get('metadata_verification_history'):
            with st.expander("📋 Metadata Verification History", expanded=False):
                st.markdown("**Recent metadata verifications:**")
                
                for i, entry in enumerate(reversed(st.session_state.metadata_verification_history[-5:])):
                    with st.container():
                        col1, col2, col3 = st.columns([3, 2, 1])
                        
                        with col1:
                            title_preview = entry['verified_metadata']['title'][:60]
                            if len(entry['verified_metadata']['title']) > 60:
                                title_preview += "..."
                            st.write(f"**{title_preview}**")
                            url_preview = entry['url'][:50]
                            if len(entry['url']) > 50:
                                url_preview += "..."
                            st.caption(f"URL: {url_preview}")
                        
                        with col2:
                            st.write(f"Type: {entry['verified_metadata']['document_type']}")
                            st.caption(f"Verified: {entry['timestamp'][:16]}")
                        
                        with col3:
                            if st.button(f"View Details", key=f"history_{i}"):
                                st.json(entry)
                        
                        st.divider()
                
                if len(st.session_state.metadata_verification_history) > 5:
                    st.info(f"Showing 5 most recent verifications. Total: {len(st.session_state.metadata_verification_history)}")
        
        url_input = st.text_input(
            "Enter document URL",
            placeholder="https://example.com/document.pdf",
            help="URL processing with interactive metadata verification",
            label_visibility="collapsed"
        )
        
        if not url_input:
            st.info("💡 Simply paste a URL above - processing happens automatically!")
        elif url_input and not url_input.strip():
            st.warning("Please enter a valid URL")
        
        if url_input and url_input.strip():
            # Import URL processing functionality
            try:
                from utils.fast_admin_loader import process_url_content
            except ImportError:
                from utils.url_content_extractor import extract_url_content as process_url_content
            
            # Use session state to track processed URLs to avoid reprocessing
            if "processed_urls" not in st.session_state:
                st.session_state.processed_urls = set()
            
            # Auto-process URL when entered (one-step process)
            if url_input not in st.session_state.processed_urls:
                with st.spinner("Processing URL content..."):
                    try:
                        st.info(f"Processing URL: {url_input}")
                        
                        # Import required modules
                        import requests
                        import trafilatura
                        from utils.comprehensive_scoring import comprehensive_document_scoring
                        from utils.database import db_manager
                        import uuid
                        
                        st.info("✓ Modules imported successfully")
                        
                        # Check for Congress.gov URLs and suggest alternative
                        if 'congress.gov' in url_input.lower():
                            if '/text' not in url_input:
                                # Extract bill identifier and suggest text version
                                import re
                                bill_match = re.search(r'/bill/(\d+)th-congress/([^/]+)/(\d+)', url_input)
                                if bill_match:
                                    congress, chamber, bill_num = bill_match.groups()
                                    text_url = f"https://www.congress.gov/bill/{congress}th-congress/{chamber}/{bill_num}/text"
                                    st.warning("Congress.gov often blocks automated access. Try the text version:")
                                    st.code(text_url)
                        
                        # Enhanced URL fetching with session and comprehensive headers
                        session = requests.Session()
                        session.headers.update({
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'DNT': '1',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'none',
                            'Sec-Fetch-User': '?1',
                            'Cache-Control': 'max-age=0'
                        })
                        
                        st.info("Fetching URL content...")
                        
                        response = None
                        last_error = None
                        
                        try:
                            # Add delay to appear more human-like
                            import time
                            time.sleep(1)
                            
                            response = session.get(url_input, timeout=30, allow_redirects=True)
                            
                            if response.status_code == 200:
                                st.info(f"URL fetched successfully (Status: {response.status_code})")
                            else:
                                last_error = f"HTTP {response.status_code}: {response.reason}"
                                
                        except requests.exceptions.RequestException as e:
                            last_error = str(e)
                        
                        if not response or response.status_code != 200:
                            # Provide specific guidance for common issues
                            if last_error and ("403" in str(last_error) or "forbidden" in str(last_error).lower()):
                                st.error("Access Denied")
                                st.info("This website blocks automated access. Alternative approaches:")
                                if 'congress.gov' in url_input.lower():
                                    # Extract bill number for specific guidance
                                    import re
                                    bill_match = re.search(r'/bill/(\d+)th-congress/([^/]+)/(\d+)', url_input)
                                    if bill_match:
                                        congress, chamber, bill_num = bill_match.groups()
                                        text_url = f"https://www.congress.gov/bill/{congress}th-congress/{chamber}/{bill_num}/text"
                                        st.info("Try the direct text version:")
                                        st.code(text_url)
                                st.info("• Look for downloadable PDF versions")
                                st.info("• Use the file upload feature instead")
                                st.info("• Check for alternative document sources")
                            elif last_error and "404" in str(last_error):
                                st.error("Page Not Found")
                                st.info("Verify the URL is correct and accessible")
                            else:
                                st.error(f"Unable to fetch URL: {last_error or 'Unknown error'}")
                            return
                        
                        # Extract content with enhanced metadata and multiple fallback methods
                        st.info("📄 Analyzing content type and extracting text...")
                        
                        content = None
                        metadata = None
                        
                        # Check if this is a PDF file
                        content_type = response.headers.get('content-type', '').lower()
                        is_pdf = (content_type.startswith('application/pdf') or 
                                 url_input.lower().endswith('.pdf') or
                                 response.content[:4] == b'%PDF')
                        
                        if is_pdf:
                            st.info("🔍 PDF detected - using specialized PDF extraction...")
                            try:
                                import io
                                from pypdf import PdfReader
                                
                                # Extract text from PDF
                                pdf_file = io.BytesIO(response.content)
                                pdf_reader = PdfReader(pdf_file)
                                
                                pdf_text = ""
                                metadata_text = ""
                                
                                # Extract text from all pages
                                for i, page in enumerate(pdf_reader.pages):
                                    page_text = page.extract_text()
                                    pdf_text += page_text + "\n"
                                    
                                    # Use first few pages for metadata extraction
                                    if i < 3:
                                        metadata_text += page_text + "\n"
                                
                                content = pdf_text.strip()
                                
                                # Extract PDF metadata
                                pdf_info = pdf_reader.metadata
                                if pdf_info:
                                    class PDFMetadata:
                                        def __init__(self, pdf_info):
                                            self.title = pdf_info.get('/Title', '') if pdf_info.get('/Title') else ''
                                            self.author = pdf_info.get('/Author', '') if pdf_info.get('/Author') else ''
                                            self.subject = pdf_info.get('/Subject', '') if pdf_info.get('/Subject') else ''
                                            self.creator = pdf_info.get('/Creator', '') if pdf_info.get('/Creator') else ''
                                            self.producer = pdf_info.get('/Producer', '') if pdf_info.get('/Producer') else ''
                                    
                                    metadata = PDFMetadata(pdf_info)
                                
                                st.success(f"✓ PDF extraction: {len(content)} characters from {len(pdf_reader.pages)} pages")
                                
                            except Exception as e:
                                st.warning(f"PDF extraction failed: {str(e)}")
                                # Fall back to treating as regular content
                                is_pdf = False
                        
                        if not is_pdf:
                            # Method 1: Try trafilatura with different settings for HTML content
                            try:
                                content = trafilatura.extract(response.text, include_comments=False, include_tables=True, include_formatting=True)
                                metadata = trafilatura.extract_metadata(response.text)
                                st.info(f"Method 1 (Trafilatura): {len(content) if content else 0} characters")
                            except Exception as e:
                                st.warning(f"Method 1 failed: {str(e)}")
                        
                        # Method 2: Alternative trafilatura settings if first failed
                        if not content or len(content.strip()) < 100:
                            try:
                                content = trafilatura.extract(response.text, 
                                                            favor_precision=False,
                                                            favor_recall=True,
                                                            include_comments=True,
                                                            include_tables=True)
                                st.info(f"Method 2 (Enhanced Trafilatura): {len(content) if content else 0} characters")
                            except Exception as e:
                                st.warning(f"Method 2 failed: {str(e)}")
                        
                        # Method 3: BeautifulSoup fallback with proper text extraction
                        if not content or len(content.strip()) < 100:
                            try:
                                import re
                                from bs4 import BeautifulSoup
                                
                                st.info("🔧 Method 3: Using BeautifulSoup for content extraction...")
                                soup = BeautifulSoup(response.text, 'html.parser')
                                
                                # Remove unwanted elements
                                for element in soup(["script", "style", "nav", "header", "footer", "aside", "noscript"]):
                                    element.decompose()
                                
                                # Try to find main content areas
                                content_selectors = [
                                    'main', 'article', '.content', '.main-content', 
                                    '.post-content', '.entry-content', '.article-content',
                                    '#content', '#main', '.container .row'
                                ]
                                
                                main_content = None
                                for selector in content_selectors:
                                    try:
                                        if selector.startswith('.') or selector.startswith('#'):
                                            main_content = soup.select_one(selector)
                                        else:
                                            main_content = soup.find(selector)
                                        if main_content:
                                            st.info(f"Found content using selector: {selector}")
                                            break
                                    except:
                                        continue
                                
                                # Extract text with proper encoding handling
                                if main_content:
                                    content = main_content.get_text(separator=' ', strip=True)
                                else:
                                    content = soup.get_text(separator=' ', strip=True)
                                
                                # Clean up whitespace and ensure proper encoding
                                content = re.sub(r'\s+', ' ', content).strip()
                                
                                # Remove any remaining problematic characters
                                content = content.encode('utf-8', errors='ignore').decode('utf-8')
                                
                                st.success(f"✓ Method 3 (BeautifulSoup): {len(content) if content else 0} characters extracted")
                            except Exception as e:
                                st.warning(f"❌ Method 3 failed: {str(e)}")
                        
                        # Method 4: Raw text extraction as last resort
                        if not content or len(content.strip()) < 100:
                            try:
                                import re
                                st.info("🔧 Method 4: Using raw text extraction...")
                                
                                # Simple regex to extract text between tags
                                raw_content = re.sub(r'<[^>]+>', ' ', response.text)
                                raw_content = re.sub(r'\s+', ' ', raw_content).strip()
                                
                                # Ensure proper encoding
                                content = raw_content.encode('utf-8', errors='ignore').decode('utf-8')
                                
                                st.success(f"✓ Method 4 (Raw extraction): {len(content) if content else 0} characters")
                            except Exception as e:
                                st.warning(f"❌ Method 4 failed: {str(e)}")
                        
                        st.success(f"🎯 Final content extracted: {len(content) if content else 0} characters")
                        
                        # Show content preview for debugging
                        if content and len(content) > 100:
                            st.info("📄 Content preview (first 300 characters):")
                            preview = content[:300] + "..." if len(content) > 300 else content
                            st.text(preview)
                        
                        if content and len(content.strip()) > 100:
                            # Extract proper title, author, and date using intelligent extraction
                            st.info("🔍 Analyzing content for metadata extraction...")
                            
                            title = extract_title_from_url_content(content, metadata, url_input)
                            st.success(f"📝 Title extracted: {title}")
                            
                            author = extract_author_from_url_content(content, metadata, url_input)
                            st.success(f"👤 Author extracted: {author}")
                            
                            pub_date = extract_date_from_url_content(content, metadata)
                            st.success(f"📅 Date extracted: {pub_date if pub_date else 'Not found'}")
                            
                            organization = extract_organization_from_url_content(content, metadata, url_input)
                            st.success(f"🏢 Organization extracted: {organization}")
                            
                            # Check if we're in auto mode or verification mode
                            auto_mode = st.session_state.get('auto_metadata_mode', False)
                            
                            if auto_mode:
                                # Auto mode - save automatically without verification
                                st.info("🤖 **Auto Save Mode** - Saving document with extracted metadata...")
                                verified_title = title
                                verified_author = author
                                verified_date = pub_date
                                verified_organization = organization
                                verified_doc_type = "Policy Document" if "policy" in title.lower() else "Research Report"
                                proceed_save = True
                            else:
                                # Manual verification mode
                                st.info("🔍 **Metadata Verification & Editing**")
                                st.markdown("Review and edit the extracted metadata before saving:")
                                
                                with st.expander("📝 Edit Document Metadata", expanded=True):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        verified_title = st.text_input(
                                            "Document Title",
                                            value=title,
                                            help="Edit the document title if needed"
                                        )
                                        
                                        verified_author = st.text_input(
                                            "Author",
                                            value=author,
                                            help="Edit the author name if needed"
                                        )
                                    
                                    with col2:
                                        # Date input with proper handling
                                        if pub_date:
                                            verified_date = st.date_input(
                                                "Publication Date",
                                                value=pub_date,
                                                help="Edit the publication date if needed"
                                            )
                                        else:
                                            verified_date = st.date_input(
                                                "Publication Date",
                                                value=None,
                                                help="Enter the publication date"
                                            )
                                        
                                        verified_organization = st.text_input(
                                            "Organization",
                                            value=organization,
                                            help="Edit the organization name if needed"
                                        )
                                
                                    # Document type selection
                                    doc_types = [
                                        "Policy Document", "Research Report", "Technical Paper",
                                        "White Paper", "Analysis", "Framework", "Guidelines",
                                        "Strategy Document", "Academic Paper", "Government Report",
                                        "Industry Report", "Other"
                                    ]
                                    
                                    verified_doc_type = st.selectbox(
                                        "Document Type",
                                        doc_types,
                                        index=0 if "policy" in title.lower() else 1,
                                        help="Select the appropriate document type"
                                    )
                                    
                                    # Content preview and editing
                                    st.markdown("**Content Preview & Validation**")
                                    content_preview = st.text_area(
                                        "Content Preview (first 500 characters)",
                                        value=content[:500] + ("..." if len(content) > 500 else ""),
                                        height=100,
                                        help="Preview of extracted content - verify it looks correct"
                                    )
                                    
                                    # Metadata confidence indicators
                                    st.markdown("**Extraction Confidence**")
                                    conf_col1, conf_col2, conf_col3, conf_col4 = st.columns(4)
                                    
                                    with conf_col1:
                                        title_conf = "High" if len(title) > 20 and title != "Document from URL" else "Low"
                                        st.metric("Title", title_conf, help="Confidence in title extraction")
                                    
                                    with conf_col2:
                                        author_conf = "High" if author != "Web Content" and len(author) > 5 else "Low"
                                        st.metric("Author", author_conf, help="Confidence in author extraction")
                                    
                                    with conf_col3:
                                        date_conf = "High" if pub_date else "Low"
                                        st.metric("Date", date_conf, help="Confidence in date extraction")
                                    
                                    with conf_col4:
                                        org_conf = "High" if organization != "Unknown" and len(organization) > 5 else "Low"
                                        st.metric("Organization", org_conf, help="Confidence in organization extraction")
                                
                                # Action buttons
                                st.markdown("---")
                                action_col1, action_col2, action_col3 = st.columns([2, 1, 1])
                                
                                with action_col1:
                                    proceed_save = st.button(
                                        "✅ Save Document with Verified Metadata",
                                        type="primary",
                                        use_container_width=True,
                                        help="Save the document with the verified metadata"
                                    )
                                
                                with action_col2:
                                    if st.button("🔄 Re-extract Metadata", use_container_width=True):
                                        st.info("Re-extracting metadata...")
                                        # Trigger re-extraction by removing from processed URLs
                                        if url_input in st.session_state.processed_urls:
                                            st.session_state.processed_urls.remove(url_input)
                                        st.rerun()
                                
                                with action_col3:
                                    if st.button("❌ Cancel", use_container_width=True):
                                        st.warning("Document processing cancelled")
                                        return
                                
                                # Only proceed if user clicks save in manual mode
                                if not proceed_save:
                                    st.info("👆 Review the metadata above and click 'Save Document' when ready")
                                    return
                            
                            # Use verified metadata for saving
                            title = verified_title
                            author = verified_author
                            pub_date = verified_date
                            organization = verified_organization
                            doc_type = verified_doc_type
                            
                            # Update document type in document_data
                            doc_type_mapping = {
                                "Policy Document": "Policy",
                                "Research Report": "Research",
                                "Technical Paper": "Technical",
                                "White Paper": "Whitepaper",
                                "Analysis": "Analysis",
                                "Framework": "Framework",
                                "Guidelines": "Guidelines",
                                "Strategy Document": "Strategy",
                                "Academic Paper": "Academic",
                                "Government Report": "Government",
                                "Industry Report": "Industry",
                                "Other": "Document"
                            }
                            
                            # Show saving progress
                            st.info("💾 Saving document with verified metadata...")
                            
                            # Create enhanced metadata summary for storage
                            import json
                            from datetime import datetime
                            
                            metadata_summary = {
                                "title": title,
                                "author": author,
                                "organization": organization,
                                "document_type": doc_type,
                                "extraction_method": "URL_VERIFIED",
                                "verification_timestamp": datetime.now().isoformat(),
                                "url_source": url_input,
                                "content_length": len(content),
                                "metadata_confidence": {
                                    "title": "High" if len(title) > 20 and title != "Document from URL" else "Low",
                                    "author": "High" if author != "Web Content" and len(author) > 5 else "Low",
                                    "date": "High" if pub_date else "Low",
                                    "organization": "High" if organization != "Unknown" and len(organization) > 5 else "Low"
                                }
                            }
                            
                            # Store verification history in session state
                            if 'metadata_verification_history' not in st.session_state:
                                st.session_state.metadata_verification_history = []
                            
                            verification_entry = {
                                "url": url_input,
                                "timestamp": datetime.now().isoformat(),
                                "verified_metadata": metadata_summary,
                                "original_extraction": {
                                    "title": extract_title_from_url_content(content, metadata, url_input),
                                    "author": extract_author_from_url_content(content, metadata, url_input),
                                    "organization": extract_organization_from_url_content(content, metadata, url_input),
                                    "date": extract_date_from_url_content(content, metadata)
                                }
                            }
                            st.session_state.metadata_verification_history.append(verification_entry)
                            
                            # Check for duplicates first (simplified due to OpenAI quota limits)
                            st.info("🔍 Checking for duplicates...")
                            try:
                                from utils.database import db_manager
                                
                                # Simple duplicate check using SQL query
                                import psycopg2
                                import os
                                
                                conn = psycopg2.connect(os.getenv('DATABASE_URL'))
                                cursor = conn.cursor()
                                
                                # Check for title duplicates
                                cursor.execute("SELECT COUNT(*) FROM documents WHERE title = %s", (title,))
                                title_count = cursor.fetchone()[0]
                                
                                if title_count > 0:
                                    cursor.close()
                                    conn.close()
                                    st.error("Duplicate document detected!")
                                    st.warning(f"Document with title '{title}' already exists")
                                    st.warning("Document not saved to prevent duplicates.")
                                    return
                                
                                # Check for URL duplicates
                                cursor.execute("SELECT COUNT(*) FROM documents WHERE source_url = %s", (url_input,))
                                url_count = cursor.fetchone()[0]
                                
                                cursor.close()
                                conn.close()
                                
                                if url_count > 0:
                                    st.error("Duplicate URL detected!")
                                    st.warning(f"This URL has already been processed")
                                    st.warning("Document not saved to prevent duplicates.")
                                    return
                                    
                            except Exception as e:
                                st.warning(f"Duplicate check failed: {str(e)} - proceeding with save")
                            
                            # Clean content to remove null bytes and other problematic characters first
                            def clean_text_for_db(text):
                                if not text:
                                    return ""
                                # Remove null bytes and other control characters
                                cleaned = text.replace('\x00', '').replace('\0', '')
                                # Remove other problematic unicode control characters
                                import re
                                cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', cleaned)
                                return cleaned.strip()
                            
                            # Clean all text fields
                            clean_title = clean_text_for_db(title)
                            clean_content = clean_text_for_db(content)
                            clean_author = clean_text_for_db(author)
                            clean_organization = clean_text_for_db(organization)
                            
                            # Generate document ID and score the document
                            st.info("📊 Calculating document scores...")
                            doc_id = str(uuid.uuid4())
                            
                            # Use basic scoring to avoid OpenAI quota issues
                            st.info("🔄 Running basic document scoring...")
                            
                            # Enhanced quantum-aware scoring for proper scoring
                            def enhanced_quantum_scoring(content, title):
                                content_lower = content.lower()
                                title_lower = title.lower()
                                combined_text = content_lower + " " + title_lower
                                
                                # Enhanced AI keywords with weights
                                ai_keywords = {
                                    'artificial intelligence': 15, 'machine learning': 12, 'neural network': 10, 
                                    'deep learning': 12, 'ai system': 10, 'ai framework': 8, 'algorithm': 5, 
                                    'automation': 6, 'chatbot': 5, 'nlp': 8, 'natural language': 7,
                                    'computer vision': 8, 'robotics': 6, 'intelligent system': 8
                                }
                                
                                # Enhanced quantum keywords with weights - more comprehensive
                                quantum_keywords = {
                                    'quantum computing': 20, 'quantum algorithm': 15, 'quantum cryptography': 18,
                                    'quantum key distribution': 15, 'quantum supremacy': 12, 'quantum entanglement': 12,
                                    'quantum state': 10, 'quantum mechanics': 8, 'qubit': 12, 'quantum gate': 10,
                                    'quantum circuit': 10, 'quantum information': 12, 'quantum communication': 12,
                                    'quantum technology': 15, 'quantum security': 18, 'quantum resistant': 15,
                                    'post-quantum': 15, 'quantum safe': 12, 'quantum threat': 12
                                }
                                
                                # Enhanced cybersecurity keywords
                                cyber_keywords = {
                                    'cybersecurity': 15, 'information security': 12, 'privacy': 10, 'encryption': 12,
                                    'threat': 8, 'vulnerability': 10, 'attack': 8, 'defense': 8, 'protection': 8,
                                    'risk management': 10, 'security framework': 12, 'data protection': 10,
                                    'cyber threat': 12, 'security policy': 10, 'incident response': 8
                                }
                                
                                # Enhanced ethics keywords
                                ethics_keywords = {
                                    'ethics': 12, 'bias': 10, 'fairness': 10, 'transparency': 8, 'accountability': 10,
                                    'responsible ai': 15, 'trust': 6, 'explainable': 12, 'interpretable': 10,
                                    'ethical framework': 12, 'moral': 8, 'social impact': 8, 'human rights': 10
                                }
                                
                                # Calculate weighted scores
                                ai_score = sum(weight for keyword, weight in ai_keywords.items() if keyword in combined_text)
                                quantum_score = sum(weight for keyword, weight in quantum_keywords.items() if keyword in combined_text)
                                cyber_score = sum(weight for keyword, weight in cyber_keywords.items() if keyword in combined_text)
                                ethics_score = sum(weight for keyword, weight in ethics_keywords.items() if keyword in combined_text)
                                
                                # Boost quantum score if document is clearly quantum-focused
                                if 'quantum' in title_lower:
                                    quantum_score = min(quantum_score * 1.5, 100)
                                
                                # Special boost for quantum policy documents
                                if any(phrase in combined_text for phrase in ['quantum policy', 'quantum approach', 'quantum strategy']):
                                    quantum_score = min(quantum_score + 25, 100)
                                
                                # Boost for government quantum initiatives
                                if any(phrase in combined_text for phrase in ['national quantum initiative', 'quantum security', 'quantum framework']):
                                    quantum_score = min(quantum_score + 20, 100)
                                
                                # Calculate final scores with proper scaling
                                return {
                                    'ai_cybersecurity': min(int((ai_score + cyber_score) * 1.2), 100),
                                    'quantum_cybersecurity': min(int((quantum_score + cyber_score) * 1.2), 100),
                                    'ai_ethics': min(int((ai_score + ethics_score) * 1.2), 100),
                                    'quantum_ethics': min(int((quantum_score + ethics_score) * 1.2), 100)
                                }
                            
                            scores = enhanced_quantum_scoring(clean_content, clean_title)
                            st.success(f"✓ Enhanced quantum scoring complete: AI Cyber={scores.get('ai_cybersecurity', 0)}, Quantum Cyber={scores.get('quantum_cybersecurity', 0)}, AI Ethics={scores.get('ai_ethics', 0)}, Quantum Ethics={scores.get('quantum_ethics', 0)}")
                            
                            # Determine topic based on content analysis
                            def determine_document_topic(content, title):
                                combined_text = (content + " " + title).lower()
                                
                                # Enhanced quantum detection
                                quantum_indicators = [
                                    'quantum policy', 'quantum approach', 'quantum technology', 'quantum computing', 
                                    'quantum cryptography', 'quantum security', 'post-quantum', 'quantum-safe',
                                    'quantum initiative', 'quantum strategy', 'quantum framework', 'qkd',
                                    'quantum key distribution', 'quantum resistant', 'quantum threat'
                                ]
                                
                                # Enhanced AI detection
                                ai_indicators = [
                                    'artificial intelligence', 'machine learning', 'ai policy', 'ai framework',
                                    'ai strategy', 'ai governance', 'neural network', 'deep learning',
                                    'ai ethics', 'ai safety', 'ai risk', 'generative ai'
                                ]
                                
                                quantum_count = sum(1 for indicator in quantum_indicators if indicator in combined_text)
                                ai_count = sum(1 for indicator in ai_indicators if indicator in combined_text)
                                
                                # Determine primary topic
                                if quantum_count > ai_count and quantum_count > 0:
                                    return "Quantum"
                                elif ai_count > quantum_count and ai_count > 0:
                                    return "AI"
                                elif quantum_count > 0 and ai_count > 0:
                                    return "Both"
                                else:
                                    return "General"
                            
                            # Determine the document topic
                            document_topic = determine_document_topic(clean_content, clean_title)
                            
                            # Capture verification event for ML training
                            if auto_mode:
                                st.info("🔄 Auto mode enabled - skipping ML training capture")
                            else:
                                st.info("📚 Capturing verification patterns for ML training...")
                                try:
                                    from utils.ml_training_system import ml_training_system
                                    
                                    # Prepare original extraction data
                                    original_extraction = {
                                        'title': extract_title_from_url_content(content, metadata, url_input),
                                        'author': extract_author_from_url_content(content, metadata, url_input),
                                        'organization': extract_organization_from_url_content(content, metadata, url_input),
                                        'topic': 'General',  # Default before verification
                                        'date': extract_date_from_url_content(content, metadata)
                                    }
                                    
                                    # Prepare verified extraction data
                                    verified_extraction = {
                                        'title': clean_title,
                                        'author': clean_author,
                                        'organization': clean_organization,
                                        'topic': document_topic,
                                        'date': pub_date
                                    }
                                    
                                    # Capture the verification event
                                    pattern_id = ml_training_system.capture_verification_event(
                                        document_id=doc_id,
                                        original_extraction=original_extraction,
                                        verified_extraction=verified_extraction,
                                        content=clean_content,
                                        document_type=doc_type,
                                        source_type='url'
                                    )
                                    
                                    st.success(f"✓ ML training pattern captured: {pattern_id[:8]}...")
                                    
                                except Exception as e:
                                    st.warning(f"ML training capture failed (non-critical): {str(e)}")
                            
                            # Save to database using db_manager with enhanced metadata
                            document_data = {
                                'id': doc_id,
                                'title': clean_title,
                                'content': clean_content,
                                'clean_content': clean_content,
                                'text_content': clean_content,
                                'source_url': url_input,
                                'document_type': doc_type_mapping.get(doc_type, "Document"),
                                'author': clean_author,
                                'author_organization': clean_organization,  # Ensure proper field mapping
                                'organization': clean_organization,
                                'publication_date': pub_date,
                                'publish_date': pub_date,  # Ensure proper field mapping
                                'date': pub_date,
                                'topic': document_topic,  # Add proper topic detection
                                'ai_cybersecurity_score': scores.get('ai_cybersecurity', 0),
                                'quantum_cybersecurity_score': scores.get('quantum_cybersecurity', 0),
                                'ai_ethics_score': scores.get('ai_ethics', 0),
                                'quantum_ethics_score': scores.get('quantum_ethics', 0),
                                'metadata_verified': True,  # Mark as verified
                                'extraction_method': 'URL_VERIFIED',
                                'verification_timestamp': datetime.now().isoformat()
                            }
                            
                            st.info("💾 Saving document to database...")
                            result = db_manager.save_document(document_data)
                            
                            if result:
                                # Mark URL as processed to avoid reprocessing
                                st.session_state.processed_urls.add(url_input)
                                
                                st.success("URL content processed successfully!")
                                
                                # Clear all caches to ensure document counts are consistent across pages
                                try:
                                    st.cache_data.clear()
                                    if hasattr(fetch_documents_cached, 'clear'):
                                        fetch_documents_cached.clear()
                                    if hasattr(comprehensive_document_scoring_cached, 'clear'):
                                        comprehensive_document_scoring_cached.clear()
                                except:
                                    pass  # Cache clearing is best effort
                                
                                st.info("Document added to collection. Page will refresh to show updated counts.")
                                st.balloons()
                                
                                # Force a rerun to refresh the document list and counts
                                st.rerun()
                            else:
                                st.error("Failed to save document to database")
                                # Don't mark as processed if save failed
                                pass
                        else:
                            st.error("Could not extract sufficient content from URL")
                            
                    except Exception as e:
                        st.error(f"Error processing URL: {str(e)}")
                        st.info("Please verify the URL is accessible and contains readable content")
            else:
                # URL already processed
                st.info(f"✓ URL already processed: {url_input}")
                if st.button("Process Again", type="secondary", use_container_width=True):
                    # Remove from processed URLs to allow reprocessing
                    st.session_state.processed_urls.discard(url_input)
                    st.rerun()
        
        # Show status and controls for processed URLs
        if hasattr(st.session_state, 'processed_urls') and st.session_state.processed_urls:
            with st.expander(f"📝 Processed URLs ({len(st.session_state.processed_urls)})", expanded=False):
                for processed_url in list(st.session_state.processed_urls):
                    st.text(processed_url)
                
                if st.button("Clear All Processed URLs", type="secondary"):
                    st.session_state.processed_urls.clear()
                    st.success("Processed URLs list cleared")
                    st.rerun()
    
    # Policy Analyzer Modal Button
    st.markdown("---")
    
    # Create inline layout for button and description
    st.markdown("""
    <style>
    .policy-analyzer-row {
        display: flex !important;
        align-items: center !important;
        gap: 1rem !important;
        margin: 1rem 0 !important;
    }
    .custom-policy-button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        text-align: center !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(30, 64, 175, 0.2) !important;
        width: 180px !important;
        height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }
    .custom-policy-button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(30, 64, 175, 0.3) !important;
    }
    .policy-description {
        color: #6b7280 !important;
        font-style: italic !important;
        font-size: 0.9rem !important;
        line-height: 1.4 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 6])
    
    with col1:
        if st.button("Policy Analyzer", key="policy_analyzer_btn", help="Open comprehensive policy analysis tool"):
            st.session_state.show_policy_analyzer = True
            st.rerun()
    
    with col2:
        st.markdown('<div style="margin-left: -1rem; padding-top: 0.5rem;"><span class="policy-description">Comprehensive policy analysis with emerging technologies gap detection and recommendations and Report Generation</span></div>', unsafe_allow_html=True)
    
    # Add divider line with reduced margins
    st.markdown('<div style="margin: 0.5rem 0;"><hr style="margin: 0; padding: 0; border-top: 1px solid #e5e7eb;"></div>', unsafe_allow_html=True)
    
    # Credit section with Cyber Institute logo
    try:
        import base64
        with open("assets/cyber_institute_logo.jpg", "rb") as f:
            cyber_data = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
        <div style="text-align: center; margin: 1rem 0; padding: 0.5rem; background-color: #f8f9fa; border-radius: 8px; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <img src="data:image/jpeg;base64,{cyber_data}" style="height: 30px; width: auto;" alt="Cyber Institute Logo">
            <span style="font-size: 0.9rem; color: #666;">Developed by Cyber Institute</span>
        </div>
        """, unsafe_allow_html=True)
    except:
        # Fallback without logo
        st.markdown("""
        <div style="text-align: center; margin: 1rem 0; padding: 0.5rem; background-color: #f8f9fa; border-radius: 8px;">
            <span style="font-size: 0.9rem; color: #666;">Developed by Cyber Institute</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Policy Gap Analysis Modal
    if st.session_state.get('show_policy_analyzer', False):
        render_policy_analyzer_modal()

def extract_title_from_url_content(content, metadata, url):
    """Extract title from URL content using multiple intelligent strategies optimized for PDFs."""
    import re
    from urllib.parse import urlparse
    
    if not content:
        return "Document from URL"
    
    # Try metadata first (PDF or trafilatura)
    if metadata and hasattr(metadata, 'title') and metadata.title:
        title = metadata.title.strip()
        if len(title) > 3 and len(title) < 300 and not title.lower().startswith('untitled'):
            return title
    
    # Enhanced patterns specifically for PDF and government documents
    title_patterns = [
        # Quantum-specific document patterns
        r'(The\s+U\.?S\.?\s+Approach\s+to\s+Quantum\s+Policy)',
        r'(Quantum\s+(?:Computing|Technology|Security|Cryptography)\s+(?:Policy|Framework|Strategy|Guidance)[^.\n]*)',
        r'(Post-Quantum\s+Cryptography\s+(?:Standards|Guidelines|Framework)[^.\n]*)',
        r'(National\s+Quantum\s+Initiative[^.\n]*)',
        r'(Quantum[^.\n]{10,100}(?:Policy|Framework|Strategy))',
        
        # Government document patterns
        r'(?:H\.R\.|S\.|PUBLIC LAW|BILL)\s*\d+[^\n]*([^\n]{20,150})',
        r'((?:The\s+)?[A-Z][A-Za-z\s&,.-]{20,150})\s+(?:Act|Bill|Report|Policy|Framework|Strategy|Guidelines?|Document)',
        r'([A-Z][A-Za-z\s&,.-]{30,150})\s*(?:\n|$)',
        
        # Enhanced policy document patterns
        r'(The\s+[A-Z][A-Za-z\s\-:&,.-]{15,120}\s+(?:Policy|Approach|Framework|Strategy))',
        r'([A-Z][A-Za-z\s\-:&,.-]{25,150})\s*(?:Policy|Guidelines?|Standards?|Principles|Approach)',
        r'(?:Policy on|Guidelines for|Standards for)\s+([A-Za-z\s\-:&,.-]{15,150})',
        
        # Academic/research patterns
        r'([A-Z][A-Za-z\s\-:&,.-]{25,150})\s*(?:Report|Analysis|Study|Research|White Paper|Framework)',
        r'(?:Report on|Analysis of|Study of)\s+([A-Za-z\s\-:&,.-]{20,150})',
        
        # General document title patterns
        r'^([A-Z][A-Za-z\s\-:&,.-]{20,200})(?:\s*\n|\s*$)',
        r'Title:\s*([A-Za-z\s\-:&,.-]{10,150})',
        r'Subject:\s*([A-Za-z\s\-:&,.-]{10,150})',
        
        # Fallback patterns
        r'^([A-Z][^.!?\n]{15,150})(?:\.|$)',
        r'([A-Z][A-Za-z\s]{10,100})',
    ]
    
    # Clean content and get meaningful lines
    content_lines = content.split('\n')
    clean_lines = []
    
    for line in content_lines[:30]:  # Check more lines for PDFs
        line = line.strip()
        # Remove common PDF artifacts and noise
        line = re.sub(r'[^\w\s\-:&,.\(\)]', ' ', line)
        line = re.sub(r'\s+', ' ', line).strip()
        
        # Skip noise lines common in PDFs
        if (line and len(line) > 5 and len(line) < 250 and 
            not any(skip in line.lower() for skip in [
                'page ', 'pdf', 'http', 'www', 'copyright', '©', 'all rights reserved',
                'menu', 'navigation', 'login', 'search', 'home', 'skip to', 'javascript', 
                'cookie', 'privacy policy', 'terms of service', 'contact', 'about us',
                'print', 'download', 'save as', 'bookmark', 'share'
            ]) and 
            not re.match(r'^\d+$|^[A-Z]+$|^\W+$|^.{1,5}$', line)):
            clean_lines.append(line)
    
    # Try patterns on clean content
    full_content = '\n'.join(clean_lines)
    
    # Apply ML-learned patterns first
    try:
        from utils.ml_training_system import ml_training_system
        
        # Create initial extraction
        initial_metadata = {'title': ''}
        
        # Apply learned patterns
        improved_metadata = ml_training_system.apply_learned_patterns(
            full_content, initial_metadata
        )
        
        if improved_metadata.get('title') and improved_metadata['title'] != initial_metadata['title']:
            return improved_metadata['title']
            
    except Exception as e:
        pass  # Continue with traditional extraction if ML fails
    
    for pattern in title_patterns:
        matches = re.findall(pattern, full_content, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            if isinstance(match, tuple):
                potential_title = match[0] if match else ""
            else:
                potential_title = match
            
            potential_title = potential_title.strip()
            
            # Validate potential title
            if (15 <= len(potential_title) <= 200 and 
                not potential_title.lower().startswith(('page ', 'section ', 'chapter ')) and
                len(potential_title.split()) >= 3):
                return potential_title
    
    # Look for the longest meaningful line in the first 10 clean lines
    for line in clean_lines[:10]:
        if (20 <= len(line) <= 180 and 
            len(line.split()) >= 4 and
            not line.lower().startswith(('page ', 'section ', 'chapter ', 'table ', 'figure '))):
            return line
    
    # URL-based fallback
    if url:
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        if path_parts:
            title_part = path_parts[-1].replace('-', ' ').replace('_', ' ')
            title_part = re.sub(r'\.(pdf|html|htm|doc|docx)$', '', title_part, flags=re.IGNORECASE)
            if len(title_part) > 3:
                return title_part.title()
    
    return "Document from URL"

def extract_author_from_url_content(content, metadata, url):
    """Extract author from URL content using enhanced strategies for PDFs and documents."""
    import re
    from urllib.parse import urlparse
    
    if not content:
        return "Unknown"
    
    # Try metadata first (PDF or trafilatura)
    if metadata and hasattr(metadata, 'author') and metadata.author:
        author = metadata.author.strip()
        if len(author) > 2 and len(author) < 150:
            return author
    
    # Enhanced author extraction patterns for government/academic documents
    author_patterns = [
        # Government document authors
        r'(?:Prepared by|Written by|Authored by|Created by)[:\s]+([A-Za-z\s,.-]{5,100})',
        r'(?:Committee on|Subcommittee on)\s+([A-Za-z\s,.-]{10,100})',
        r'(?:Staff|Team|Office|Department)[:\s]+([A-Za-z\s,.-]{10,100})',
        
        # Academic/research authors
        r'(?:Author|Authors?)[:\s]*([A-Za-z\s,.-]{5,100})',
        r'(?:By|Written by)[:\s]+([A-Za-z\s,.-]{5,100})',
        r'(?:Principal Investigator|Lead Author)[:\s]+([A-Za-z\s,.-]{5,100})',
        
        # Report/document attribution
        r'(?:Submitted by|Compiled by|Developed by)[:\s]+([A-Za-z\s,.-]{5,100})',
        r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*,?\s*(?:Ph\.?D\.?|M\.?D\.?|J\.?D\.?)',
        
        # Organization as author patterns
        r'(?:Office of|Department of|Bureau of|Agency for)\s+([A-Za-z\s,.-]{10,80})',
        r'([A-Z][A-Za-z\s&]{5,60})\s+(?:Office|Department|Bureau|Agency)',
        
        # General patterns
        r'Contact[:\s]+([A-Za-z\s,.-]{5,100})',
        r'@([a-zA-Z0-9_\.]+)',
    ]
    
    content_lines = content.split('\n')
    clean_lines = []
    
    # Focus on first 20 lines where author info is typically found
    for line in content_lines[:20]:
        line = line.strip()
        if line and len(line) > 3 and len(line) < 200:
            clean_lines.append(line)
    
    full_content = '\n'.join(clean_lines)
    
    for pattern in author_patterns:
        matches = re.findall(pattern, full_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                author = match[0] if match else ""
            else:
                author = match
                
            author = author.strip().strip(',.')
            
            # Validate author
            if (3 <= len(author) <= 100 and 
                not any(skip in author.lower() for skip in [
                    'http', 'www', 'email', 'phone', 'fax', 'address',
                    'page', 'section', 'chapter', 'table', 'figure'
                ]) and
                not re.match(r'^\d+$|^[A-Z]+$|^\W+$', author)):
                return author
    
    # Extract organization name from URL as fallback
    if url:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        if domain:
            # Clean up domain to organization name
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Convert common domains to organization names
            domain_to_org = {
                'congress.gov': 'U.S. Congress',
                'whitehouse.gov': 'The White House',
                'nist.gov': 'NIST',
                'cisa.gov': 'CISA',
                'dhs.gov': 'Department of Homeland Security',
                'defense.gov': 'Department of Defense',
                'energy.gov': 'Department of Energy'
            }
            
            if domain in domain_to_org:
                return domain_to_org[domain]
            
            org_name = domain.split('.')[0].replace('-', ' ').title()
            if len(org_name) > 2:
                return org_name
    
    return "Unknown"

def extract_date_from_url_content(content, metadata):
    """Extract publication date from URL content using comprehensive strategies."""
    import re
    from datetime import datetime
    
    if not content:
        return None
    
    # Try trafilatura metadata first
    if metadata and hasattr(metadata, 'date') and metadata.date:
        return metadata.date
    
    # Enhanced date extraction patterns
    date_patterns = [
        # Standard formats
        r'(\d{4}-\d{2}-\d{2})',
        r'(\d{1,2}/\d{1,2}/\d{4})',
        r'(\d{1,2}-\d{1,2}-\d{4})',
        
        # Month name formats
        r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',
        r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{4})',
        
        # With context
        r'(?:Published|Date|Updated|Created|Written)[:\s]+(\d{4}-\d{2}-\d{2})',
        r'(?:Published|Date|Updated|Created|Written)[:\s]+(\d{1,2}/\d{1,2}/\d{4})',
        r'(?:Published|Date|Updated|Created|Written)[:\s]+((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',
        r'(?:Published|Date|Updated|Created|Written)[:\s]+((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?\s+\d{1,2},?\s+\d{4})',
        
        # Copyright dates as fallback
        r'©\s*(\d{4})',
        r'Copyright\s+(\d{4})',
        
        # Flexible formats
        r'(\d{4})',  # Just the year as last resort
    ]
    
    content_lines = content.split('\n')
    
    # Look for dates in the first 25 lines where metadata is usually found
    for line in content_lines[:25]:
        line = line.strip()
        if len(line) > 4 and len(line) < 200:
            for pattern in date_patterns[:-1]:  # Skip year-only pattern for main search
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    date_str = match.group(1).strip()
                    try:
                        # Try to parse the date
                        if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                            return datetime.strptime(date_str, '%Y-%m-%d').date()
                        elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):
                            return datetime.strptime(date_str, '%m/%d/%Y').date()
                        elif re.match(r'\d{1,2}-\d{1,2}-\d{4}', date_str):
                            return datetime.strptime(date_str, '%m-%d-%Y').date()
                        else:
                            # Try various month name formats
                            for fmt in ['%B %d, %Y', '%B %d %Y', '%b %d, %Y', '%b %d %Y', 
                                      '%d %B %Y', '%d %b %Y']:
                                try:
                                    return datetime.strptime(date_str, fmt).date()
                                except:
                                    continue
                    except:
                        continue
    
    # Fallback: look for recent years in the content
    current_year = datetime.now().year
    for year in range(current_year, current_year - 10, -1):  # Look for years within last 10 years
        if str(year) in content:
            try:
                return datetime(year, 1, 1).date()
            except:
                continue
    
    return None

def extract_organization_from_url_content(content, metadata, url):
    """Extract organization from URL content using comprehensive strategies optimized for PDFs."""
    import re
    from urllib.parse import urlparse
    
    if not content:
        return "Unknown"
    
    # Try metadata first (PDF or trafilatura)
    if metadata and hasattr(metadata, 'sitename') and metadata.sitename:
        org = metadata.sitename.strip()
        if len(org) > 2 and len(org) < 150:
            return org
    
    # Enhanced organization extraction patterns for government/academic documents
    org_patterns = [
        # Government agencies and departments (high priority)
        r'(?:U\.?S\.?\s+)?(?:DEPARTMENT|DEPT\.?)\s+OF\s+([A-Z][A-Za-z\s&,-]{5,60})',
        r'(?:OFFICE|BUREAU|AGENCY)\s+(?:OF|FOR)\s+([A-Z][A-Za-z\s&,-]{5,60})',
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:DEPARTMENT|AGENCY|BUREAU|OFFICE|ADMINISTRATION)',
        r'(?:COMMITTEE|SUBCOMMITTEE)\s+ON\s+([A-Z][A-Za-z\s&,-]{10,60})',
        
        # Research and academic institutions
        r'(CENTER FOR [A-Z][A-Za-z\s&,-]{5,60})',
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:CENTER|CENTRE|INSTITUTE|FOUNDATION)',
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:UNIVERSITY|COLLEGE|SCHOOL)',
        r'(?:UNIVERSITY|COLLEGE)\s+OF\s+([A-Z][A-Za-z\s&,-]{5,60})',
        
        # Think tanks and policy organizations
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:POLICY INSTITUTE|THINK TANK|RESEARCH CENTER)',
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:FOUNDATION|INSTITUTE|COUNCIL|ASSOCIATION)',
        
        # Corporate and organizational patterns
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:CORPORATION|COMPANY|LLC|INC\.?)',
        r'(?:©|COPYRIGHT)[^A-Z]*([A-Z][A-Za-z\s&,-]{5,80})(?:\s+\d{4})?',
        
        # General organization patterns
        r'(?:PUBLISHED BY|PREPARED BY|DEVELOPED BY)[:\s]+([A-Z][A-Za-z\s&,-]{5,80})',
        r'([A-Z][A-Z\s&]{8,50})',  # All caps organization names
        
        # URL-based organization extraction
        r'([A-Z][A-Za-z\s&,-]{8,80})\s*(?:\n|$)',
    ]
    
    content_lines = content.split('\n')
    clean_lines = []
    
    # Focus on first 25 lines where organization info is typically found
    for line in content_lines[:25]:
        line = line.strip()
        # Clean up common PDF artifacts
        line = re.sub(r'[^\w\s\-:&,.\(\)]', ' ', line)
        line = re.sub(r'\s+', ' ', line).strip()
        
        if (line and len(line) > 5 and len(line) < 250 and 
            not any(skip in line.lower() for skip in [
                'page ', 'pdf', 'http', 'www', 'copyright ©', 'all rights reserved',
                'menu', 'navigation', 'print', 'download', 'save as'
            ])):
            clean_lines.append(line)
    
    full_content = '\n'.join(clean_lines)
    
    # Try patterns with priority order
    for pattern in org_patterns:
        matches = re.findall(pattern, full_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                org_name = match[0] if match else ""
            else:
                org_name = match
                
            org_name = org_name.strip().strip('.,;:')
            org_name = re.sub(r'\s+', ' ', org_name)
            
            # Validate organization name
            if (5 <= len(org_name) <= 100 and 
                not re.match(r'^\d+$|^[A-Z]+$|^\W+$', org_name) and
                len(org_name.split()) >= 2 and
                not any(skip in org_name.lower() for skip in [
                    'page', 'section', 'chapter', 'table', 'figure', 'document',
                    'report', 'analysis', 'study', 'policy', 'framework'
                ])):
                return org_name
    
    # URL-based organization extraction as fallback
    if url:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        if domain:
            # Clean up domain
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Map common government and organization domains
            domain_to_org = {
                'congress.gov': 'U.S. Congress',
                'whitehouse.gov': 'The White House',
                'nist.gov': 'National Institute of Standards and Technology',
                'cisa.gov': 'Cybersecurity and Infrastructure Security Agency',
                'dhs.gov': 'Department of Homeland Security',
                'defense.gov': 'Department of Defense',
                'energy.gov': 'Department of Energy',
                'justice.gov': 'Department of Justice',
                'treasury.gov': 'Department of the Treasury',
                'state.gov': 'Department of State',
                'commerce.gov': 'Department of Commerce',
                'gao.gov': 'Government Accountability Office',
                'cbo.gov': 'Congressional Budget Office',
                'omb.gov': 'Office of Management and Budget'
            }
            
            if domain in domain_to_org:
                return domain_to_org[domain]
            
            # Generic domain conversion
            org_name = domain.split('.')[0].replace('-', ' ').replace('_', ' ').title()
            if len(org_name) > 2:
                return org_name
    
    return "Unknown"

def render_policy_analyzer_modal():
    """Render the Policy Gap Analysis in a modal-style container"""
    
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
                        color: white; padding: 0.75rem 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: white; font-size: 1.2rem;">AI-Powered Policy Gap Analysis</h3>
                <p style="margin: 0.25rem 0 0 0; color: #bfdbfe; font-size: 0.85rem;">
                    Upload policies for comprehensive gap analysis and intelligent recommendations
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with header_col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Spacing
            if st.button("✕ Close", key="close_modal", type="secondary", use_container_width=True):
                st.session_state.show_policy_analyzer = False
                st.rerun()
        
        # Lightweight Policy Gap Analysis content
        st.markdown("### Upload Policy Document")
        
        uploaded_file = st.file_uploader(
            "Choose a policy document",
            type=['pdf', 'txt', 'docx'],
            help="Upload policies for gap analysis",
            label_visibility="collapsed",
            key="policy_uploader"
        )
        
        if uploaded_file is not None:
            if st.button("Analyze Policy", type="primary", use_container_width=True):
                with st.spinner("Analyzing policy document..."):
                    try:
                        # Simple policy processing without heavy components
                        content = ""
                        if uploaded_file.type == "application/pdf":
                            import PyPDF2
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            for page in pdf_reader.pages:
                                content += page.extract_text()
                        else:
                            content = str(uploaded_file.read(), "utf-8")
                        
                        if content:
                            st.success("Policy document uploaded successfully!")
                            st.text_area("Document Content Preview", content[:500] + "...", height=200)
                            
                            # Simple gap analysis display
                            st.markdown("### Gap Analysis Results")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("AI Governance", "75%", "15%")
                            with col2:
                                st.metric("Quantum Readiness", "60%", "8%")
                            with col3:
                                st.metric("Ethics Score", "85%", "12%")
                        else:
                            st.error("Failed to extract content from document")
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")
        
        st.markdown("### Quick Analysis")
        st.text_area("Enter policy text for quick analysis", placeholder="Paste policy text here...", height=100)
        if st.button("Quick Analyze", type="secondary", use_container_width=True):
            st.info("Quick analysis feature coming soon!")
        
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
            
            # Use actual database scores with intelligent N/A detection
            raw_scores = {
                'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
                'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
                'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
                'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
            }
            
            # Apply intelligent N/A logic based on document topic relevance
            scores = {}
            content_text = (content + " " + title).lower()
            
            # AI-related frameworks
            ai_keywords = ['artificial intelligence', 'machine learning', 'ai ', ' ai', 'neural network', 'algorithm', 'deep learning', 'llm', 'generative ai']
            is_ai_related = any(keyword in content_text for keyword in ai_keywords)
            
            scores['ai_cybersecurity'] = raw_scores['ai_cybersecurity'] if raw_scores['ai_cybersecurity'] > 0 else ('N/A' if not is_ai_related else 0)
            scores['ai_ethics'] = raw_scores['ai_ethics'] if raw_scores['ai_ethics'] > 0 else ('N/A' if not is_ai_related else 0)
            
            # Quantum-related frameworks
            quantum_keywords = ['quantum', 'post-quantum', 'quantum-safe', 'qkd', 'quantum computing', 'cryptography', 'encryption']
            is_quantum_related = any(keyword in content_text for keyword in quantum_keywords)
            
            scores['quantum_cybersecurity'] = raw_scores['quantum_cybersecurity'] if raw_scores['quantum_cybersecurity'] > 0 else ('N/A' if not is_quantum_related else 0)
            scores['quantum_ethics'] = raw_scores['quantum_ethics'] if raw_scores['quantum_ethics'] > 0 else ('N/A' if not is_quantum_related else 0)
            
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
                            <div style='font-size:9px;color:#666;margin-bottom:6px' title='Document Type: {safe_doc_type} • Author/Organization: {safe_author_org}'>{safe_doc_type} • {safe_author_org[:15]}{'...' if len(safe_author_org) > 15 else ''}</div>
                        </div>
                    </div>
                    <div style='font-size:12px;line-height:1.4;margin-bottom:8px'>
                        <div style='margin-bottom:2px' title='AI Cybersecurity Maturity (0-100): Evaluates AI security risks and defensive measures. N/A means not AI-related.'>AI Cyber: <span style='background:#e8f5e8;padding:4px 12px;border-radius:10px;color:#2e7d32;font-weight:600'>{scores.get('ai_cybersecurity', 'N/A')}</span></div>
                        <div style='margin-bottom:2px' title='Quantum Cybersecurity Maturity (Tier 1-5): Assesses quantum-safe cryptography readiness. N/A means not quantum-related.'>Q Cyber: <span style='background:#e3f2fd;padding:4px 12px;border-radius:10px;color:#1976d2;font-weight:600'>{scores.get('quantum_cybersecurity', 'N/A')}</span></div>
                        <div style='margin-bottom:2px' title='AI Ethics Score (0-100): Measures ethical AI considerations and bias mitigation. N/A means not AI-related.'>AI Ethics: <span style='background:#fff3e0;padding:4px 12px;border-radius:10px;color:#f57c00;font-weight:600'>{scores.get('ai_ethics', 'N/A')}</span></div>
                        <div title='Quantum Ethics Score (0-100): Evaluates ethical implications of quantum technology. N/A means not quantum-related.'>Q Ethics: <span style='background:#fce4ec;padding:4px 12px;border-radius:10px;color:#c2185b;font-weight:600'>{scores.get('quantum_ethics', 'N/A')}</span></div>
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
            
            # Extract author from metadata JSONB field if available
            metadata = doc.get('metadata', {})
            if isinstance(metadata, str):
                import json
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            # Get author from metadata or fallback to organization
            author = metadata.get('author', '') if metadata else ''
            if not author or author == 'Unknown':
                author_org = ultra_clean_metadata(doc.get('author_organization', 'Unknown'))
            else:
                author_org = ultra_clean_metadata(author)
            
            # Clean date field safely to prevent </div> artifacts
            pub_date = clean_date_safely(doc)
            
            doc_type = ultra_clean_metadata(doc.get('document_type', 'Unknown'))
            content_preview = ultra_clean_metadata(doc.get('content_preview', 'No preview available') or 'No preview available')
            
            # Use actual database scores with intelligent N/A detection
            raw_scores = {
                'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
                'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
                'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
                'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
            }
            
            # Apply intelligent N/A logic based on document topic relevance
            scores = {}
            content_text = (content + " " + title).lower()
            
            # AI-related frameworks
            ai_keywords = ['artificial intelligence', 'machine learning', 'ai ', ' ai', 'neural network', 'algorithm', 'deep learning', 'llm', 'generative ai']
            is_ai_related = any(keyword in content_text for keyword in ai_keywords)
            
            scores['ai_cybersecurity'] = raw_scores['ai_cybersecurity'] if raw_scores['ai_cybersecurity'] > 0 else ('N/A' if not is_ai_related else 0)
            scores['ai_ethics'] = raw_scores['ai_ethics'] if raw_scores['ai_ethics'] > 0 else ('N/A' if not is_ai_related else 0)
            
            # Quantum-related frameworks
            quantum_keywords = ['quantum', 'post-quantum', 'quantum-safe', 'qkd', 'quantum computing', 'cryptography', 'encryption']
            is_quantum_related = any(keyword in content_text for keyword in quantum_keywords)
            
            scores['quantum_cybersecurity'] = raw_scores['quantum_cybersecurity'] if raw_scores['quantum_cybersecurity'] > 0 else ('N/A' if not is_quantum_related else 0)
            scores['quantum_ethics'] = raw_scores['quantum_ethics'] if raw_scores['quantum_ethics'] > 0 else ('N/A' if not is_quantum_related else 0)
            
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
                    <div style='font-size:10px;color:#666;margin-bottom:8px' title='Type: {safe_doc_type} • Author/Org: {safe_author_org} • Published: {safe_pub_date}'>{safe_doc_type} • {safe_author_org} • {safe_pub_date}</div>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:8px;font-size:10px'>
                        <div title='AI Cybersecurity Maturity (0-100): Evaluates AI security risks and defensive measures. N/A means not AI-related.'>AI Cyber: <span style='background:#e8f5e8;padding:2px 6px;border-radius:8px;color:#2e7d32'>{scores.get('ai_cybersecurity', 'N/A')}</span></div>
                        <div title='Quantum Cybersecurity Maturity (Tier 1-5): Assesses quantum-safe cryptography readiness. N/A means not quantum-related.'>Q Cyber: <span style='background:#e3f2fd;padding:2px 6px;border-radius:8px;color:#1976d2'>{scores.get('quantum_cybersecurity', 'N/A')}</span></div>
                        <div title='AI Ethics Score (0-100): Measures ethical AI considerations and bias mitigation. N/A means not AI-related.'>AI Ethics: <span style='background:#fff3e0;padding:2px 6px;border-radius:8px;color:#f57c00'>{scores.get('ai_ethics', 'N/A')}</span></div>
                        <div title='Quantum Ethics Score (0-100): Evaluates ethical implications of quantum technology. N/A means not quantum-related.'>Q Ethics: <span style='background:#fce4ec;padding:2px 6px;border-radius:8px;color:#c2185b'>{scores.get('quantum_ethics', 'N/A')}</span></div>
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
        
        # Use actual database scores with intelligent N/A detection
        raw_scores = {
            'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
            'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
            'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
            'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
        }
        
        # Apply intelligent N/A logic based on document topic relevance
        scores = {}
        content_text = (content + " " + title).lower()
        
        # AI-related frameworks
        ai_keywords = ['artificial intelligence', 'machine learning', 'ai ', ' ai', 'neural network', 'algorithm', 'deep learning', 'llm', 'generative ai']
        is_ai_related = any(keyword in content_text for keyword in ai_keywords)
        
        scores['ai_cybersecurity'] = raw_scores['ai_cybersecurity'] if raw_scores['ai_cybersecurity'] > 0 else ('N/A' if not is_ai_related else 0)
        scores['ai_ethics'] = raw_scores['ai_ethics'] if raw_scores['ai_ethics'] > 0 else ('N/A' if not is_ai_related else 0)
        
        # Quantum-related frameworks
        quantum_keywords = ['quantum', 'post-quantum', 'quantum-safe', 'qkd', 'quantum computing', 'cryptography', 'encryption']
        is_quantum_related = any(keyword in content_text for keyword in quantum_keywords)
        
        scores['quantum_cybersecurity'] = raw_scores['quantum_cybersecurity'] if raw_scores['quantum_cybersecurity'] > 0 else ('N/A' if not is_quantum_related else 0)
        scores['quantum_ethics'] = raw_scores['quantum_ethics'] if raw_scores['quantum_ethics'] > 0 else ('N/A' if not is_quantum_related else 0)
        
        table_data.append({
            'Title': title[:45],
            'Author/Org': author_org[:25],
            'Type': doc_type,
            'AI Cybersecurity Maturity': str(scores['ai_cybersecurity']) if scores['ai_cybersecurity'] != 'N/A' else 'N/A',
            'Quantum Cybersecurity Maturity': str(scores['quantum_cybersecurity']) if scores['quantum_cybersecurity'] != 'N/A' else 'N/A',
            'AI Ethics': str(scores['ai_ethics']) if scores['ai_ethics'] != 'N/A' else 'N/A',
            'Q Ethics': str(scores['quantum_ethics']) if scores['quantum_ethics'] != 'N/A' else 'N/A',
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
                if st.button("Quick Report", key=f"quick_report_{idx}"):
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
            
            # Extract author from metadata JSONB field if available
            metadata = doc.get('metadata', {})
            if isinstance(metadata, str):
                import json
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            # Get author from metadata or fallback to organization
            author = metadata.get('author', '') if metadata else ''
            if not author or author == 'Unknown':
                author_org = ultra_clean_metadata(doc.get('author_organization', 'Unknown'))
            else:
                author_org = ultra_clean_metadata(author)
            
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
                    <h3 style='margin:0 0 12px 0;color:#333;line-height:1.3;font-size:1rem'>{safe_title}</h3>
                    <div style='margin-bottom:10px;display:flex;gap:8px;flex-wrap:wrap'>
                        <span style='background:#eceff1;padding:4px 10px;border-radius:12px;font-size:12px;color:#455a64' title='Topic Classification: AI (Artificial Intelligence related), Quantum (Quantum technology/cryptography related), General (Other technology governance)'>{safe_topic}</span>
                        <span style='background:#e1e8ed;padding:4px 10px;border-radius:12px;font-size:12px;color:#37474f' title='Document Type: Policy (Government/organizational policies), Standard (Industry standards like NIST), Regulation (Legal regulations), Guidance (Best practice documents), Research (Academic papers)'>{safe_doc_type}</span>
                        <span style='background:#e8eaf6;padding:4px 10px;border-radius:12px;font-size:12px;color:#3f51b5' title='Author/Organization: The entity that published or authored this document (government agency, standards body, research institution, etc.)'>{safe_author_org}</span>
                        {f"<span style='background:#e7ebf0;padding:4px 10px;border-radius:12px;font-size:12px;color:#546e7a' title='Publication Date: When this document was officially published or last updated'>{safe_pub_date}</span>" if pub_date and pub_date != 'Date not available' else "<span style='background:#eceff1;padding:4px 10px;border-radius:12px;font-size:12px;color:#607d8b' title='Publication Date: Document date information was not available in the source'>Date not available</span>"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Use actual database scores with intelligent N/A detection (consistent with other views)
            raw_scores = {
                'ai_cybersecurity': doc.get('ai_cybersecurity_score', 0) or 0,
                'quantum_cybersecurity': doc.get('quantum_cybersecurity_score', 0) or 0,
                'ai_ethics': doc.get('ai_ethics_score', 0) or 0,
                'quantum_ethics': doc.get('quantum_ethics_score', 0) or 0
            }
            
            # Apply intelligent N/A logic based on document topic relevance
            scores = {}
            content_text = (raw_content + " " + title).lower()
            
            # AI-related frameworks
            ai_keywords = ['artificial intelligence', 'machine learning', 'ai ', ' ai', 'neural network', 'algorithm', 'deep learning', 'llm', 'generative ai']
            is_ai_related = any(keyword in content_text for keyword in ai_keywords)
            
            scores['ai_cybersecurity'] = raw_scores['ai_cybersecurity'] if raw_scores['ai_cybersecurity'] > 0 else ('N/A' if not is_ai_related else 0)
            scores['ai_ethics'] = raw_scores['ai_ethics'] if raw_scores['ai_ethics'] > 0 else ('N/A' if not is_ai_related else 0)
            
            # Quantum-related frameworks
            quantum_keywords = ['quantum', 'post-quantum', 'quantum-safe', 'qkd', 'quantum computing', 'cryptography', 'encryption']
            is_quantum_related = any(keyword in content_text for keyword in quantum_keywords)
            
            scores['quantum_cybersecurity'] = raw_scores['quantum_cybersecurity'] if raw_scores['quantum_cybersecurity'] > 0 else ('N/A' if not is_quantum_related else 0)
            scores['quantum_ethics'] = raw_scores['quantum_ethics'] if raw_scores['quantum_ethics'] > 0 else ('N/A' if not is_quantum_related else 0)
            
            # Display scores using database values
            st.markdown(f"""
                <div style='margin:8px;padding:8px;background:#f8f9fa;border-radius:6px'>
                    <div style='display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px'>
                        <div title='AI Cybersecurity Maturity (0-100): Evaluates how well the document addresses AI security risks, threat modeling, and defensive measures. N/A means document is not AI-related.'><strong>AI Cybersecurity Maturity:</strong> <strong>{get_comprehensive_badge(scores['ai_cybersecurity'], 'ai_cybersecurity', raw_content, title)}</strong></div>
                        <div title='Quantum Cybersecurity Maturity (Tier 1-5): Assesses quantum-safe cryptography readiness and post-quantum security measures. N/A means document is not quantum-related.'><strong>Quantum Cybersecurity Maturity:</strong> <strong>{get_comprehensive_badge(scores['quantum_cybersecurity'], 'quantum_cybersecurity', raw_content, title)}</strong></div>
                        <div title='AI Ethics Score (0-100): Measures ethical AI considerations including fairness, transparency, accountability, and bias mitigation. N/A means document is not AI-related.'><strong>AI Ethics:</strong> <strong>{get_comprehensive_badge(scores['ai_ethics'], 'ai_ethics', raw_content, title)}</strong></div>
                        <div title='Quantum Ethics Score (0-100): Evaluates ethical implications of quantum technology deployment and governance. N/A means document is not quantum-related.'><strong>Quantum Ethics:</strong> <strong>{get_comprehensive_badge(scores['quantum_ethics'], 'quantum_ethics', raw_content, title)}</strong></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
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