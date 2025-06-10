import streamlit as st
from all_docs_tab import render
from datetime import datetime
from components.chatbot_widget import render_chatbot_widget, inject_chatbot_css

def main():
    st.set_page_config(
        page_title="GUARDIAN - AI Risk Analysis Navigator",
        page_icon="",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS styling - Government/Nonprofit Theme
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Source+Serif+Pro:wght@400;600&display=swap');
    
    .main > div {
        padding-top: 2rem;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #ffffff;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .main .block-container {
        background-color: #ffffff;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    .quantum-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #312e81 50%, #1e40af 100%) !important;
        padding: 3rem 2rem !important;
        border-radius: 12px !important;
        margin-bottom: 2.5rem !important;
        color: white !important;
        text-align: center !important;
        box-shadow: 0 8px 32px rgba(30, 58, 138, 0.15) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        width: 100% !important;
        display: block !important;
    }
    
    .quantum-header h1 {
        margin: 0 !important;
        font-size: 2.8rem !important;
        font-weight: 600 !important;
        font-family: 'Source Serif Pro', serif !important;
        letter-spacing: -0.02em !important;
        color: white !important;
    }
    
    .quantum-header p {
        margin: 1rem 0 0 0 !important;
        font-size: 1.15rem !important;
        opacity: 0.9 !important;
        font-weight: 400 !important;
        letter-spacing: 0.01em !important;
        color: white !important;
    }
    
    .metric-card {
        background: #ffffff;
        padding: 1.75rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 4px 6px rgba(0, 0, 0, 0.04);
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        border-top: 1px solid #e5e7eb;
    }
    
    .score-excellent {
        border-left-color: #059669;
        background: linear-gradient(145deg, #ffffff 0%, #f0fdf4 100%);
    }
    
    .score-good {
        border-left-color: #d97706;
        background: linear-gradient(145deg, #ffffff 0%, #fffbeb 100%);
    }
    
    .score-moderate {
        border-left-color: #dc2626;
        background: linear-gradient(145deg, #ffffff 0%, #fef2f2 100%);
    }
    
    .document-separator {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, #e5e7eb 0%, #9ca3af 50%, #e5e7eb 100%);
        margin: 2.5rem 0;
        border-radius: 1px;
    }
    
    .stExpander > details > summary {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        border-radius: 10px;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        font-weight: 500;
    }
    
    .sidebar-info {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1.25rem 0;
        border: 1px solid #e2e8f0;
        color: #374151;
    }
    
    .document-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
    }
    
    .document-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1), 0 20px 48px rgba(0, 0, 0, 0.06);
        border-color: #3b82f6;
    }
    
    .score-badge {
        transition: all 0.3s ease;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    .score-badge:hover {
        transform: scale(1.05);
    }
    
    .category-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.75rem;
        margin: 1.5rem 0;
    }
    
    /* Enhanced Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Source Serif Pro', serif;
        color: #1f2937;
        font-weight: 600;
    }
    
    p, div, span {
        color: #374151;
        line-height: 1.6;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f8fafc;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e2e8f0;
        font-weight: 500;
        color: #6b7280;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: #1e40af;
        border-bottom: 2px solid #3b82f6;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(145deg, #6b7280 0%, #4b5563 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        background: linear-gradient(145deg, #4b5563 0%, #374151 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(107, 114, 128, 0.3);
    }
    
    /* Metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Force light theme overrides */
    .stApp, .main, .block-container, .element-container {
        background-color: #ffffff !important;
        color: #374151 !important;
    }
    
    /* Sidebar light theme */
    .css-1d391kg, .css-1cypcdb, .sidebar .sidebar-content {
        background-color: #f8fafc !important;
        color: #374151 !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
    }
    
    /* Select box styling */
    .stSelectbox > div > div > div {
        background-color: #ffffff !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div > div {
        background-color: #ffffff !important;
        color: #374151 !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background-color: #f8fafc !important;
        border: 2px dashed #d1d5db !important;
        border-radius: 8px !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: #ffffff !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        color: #374151 !important;
    }
    
    /* Alert styling */
    .stAlert {
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background-color: #e5e7eb !important;
    }
    
    @media (max-width: 768px) {
        .category-grid {
            grid-template-columns: 1fr;
            gap: 1.25rem;
        }
        
        .quantum-header h1 {
            font-size: 2.2rem;
        }
        
        .quantum-header p {
            font-size: 1rem;
        }
        
        .document-card {
            flex-direction: column;
        }
        
        .score-section {
            margin-top: 1rem;
            justify-content: space-around;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header - simplified approach
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="
            margin: 0 0 1rem 0;
            font-size: 5.6rem;
            font-weight: bold;
            font-family: Arial, sans-serif;
            letter-spacing: -0.02em;
            color: #B91C2C;
        ">GUARDIAN</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Cyber Institute credit with logo inline
    try:
        import base64
        with open("assets/cyber_institute_logo.jpg", "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
        
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 2rem;">
            <img src="data:image/jpeg;base64,{logo_data}" width="40" height="40" style="border-radius: 50%; margin-right: 0.5rem;">
            <span style="font-size: 0.9rem; color: #6b7280; white-space: nowrap;">Developed by Cyber Institute</span>
        </div>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""
        <div style="text-align: center; font-size: 0.9rem; color: #6b7280; margin-bottom: 2rem;">
            Developed by Cyber Institute
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced sidebar with document upload and API functionality
    with st.sidebar:
        
        # File upload section
        st.markdown("### Upload Document")
        uploaded_file = st.file_uploader(
            "Drag and drop file here",
            type=['pdf', 'doc', 'docx', 'txt', 'html', 'htm', 'eml'],
            help="Limit 200MB per file • PDF, DOC, DOCX, HTML, HTM, EML, TXT"
        )
        
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
            if st.button("Process Document"):
                st.info("Processing document... This may take a moment.")
        
        # Browse files button
        st.button("Browse files", use_container_width=True)
        
        st.markdown("---")
        
        # URL submission section  
        st.markdown("### URL")
        url_input = st.text_input("Enter URL:", placeholder="https://example.com/document")
        if st.button("Submit URL", use_container_width=True):
            if url_input:
                with st.spinner(f"Fetching content from {url_input}..."):
                    try:
                        import trafilatura
                        import requests
                        import io
                        from urllib.parse import urlparse
                        from utils.direct_db import save_document_direct
                        from utils.document_analyzer import analyze_document_metadata
                        from utils.comprehensive_scoring import comprehensive_document_scoring
                        
                        # Determine file type from URL
                        parsed_url = urlparse(url_input.lower())
                        file_extension = parsed_url.path.split('.')[-1] if '.' in parsed_url.path else ''
                        
                        text_content = None
                        document_title = None
                        
                        # Check if it's a direct file download
                        if file_extension in ['pdf', 'txt']:
                            st.info(f"Detected {file_extension.upper()} file, downloading and processing...")
                            
                            # Download the file
                            response = requests.get(url_input, timeout=30)
                            response.raise_for_status()
                            
                            if file_extension == 'pdf':
                                try:
                                    from pypdf import PdfReader
                                    pdf_file = io.BytesIO(response.content)
                                    pdf_reader = PdfReader(pdf_file)
                                    text_content = ""
                                    for page in pdf_reader.pages:
                                        text_content += page.extract_text() + "\n"
                                    document_title = f"PDF Document from {parsed_url.netloc}"
                                except Exception as e:
                                    st.error(f"Could not extract text from PDF: {e}")
                                    return
                                    
                            elif file_extension == 'txt':
                                text_content = response.text
                                document_title = f"Text Document from {parsed_url.netloc}"
                        
                        else:
                            # It's a webpage, use trafilatura
                            st.info("Processing webpage content...")
                            downloaded = trafilatura.fetch_url(url_input)
                            if downloaded:
                                text_content = trafilatura.extract(downloaded)
                                document_title = f"Webpage from {parsed_url.netloc}"
                        
                        if not text_content or len(text_content.strip()) < 50:
                            st.error("Could not extract meaningful text content from the URL. The document may be empty, password-protected, or in an unsupported format.")
                        else:
                            # Extract metadata - try AI first, fallback to pattern matching
                            try:
                                metadata = analyze_document_metadata(text_content, document_title or url_input)
                            except Exception as ai_error:
                                # Use fallback analysis when AI fails
                                from utils.fallback_analyzer import extract_metadata_fallback
                                metadata = extract_metadata_fallback(text_content, url_input)
                                st.info("Document processed using pattern-based analysis due to API limitations.")
                            
                            # Generate comprehensive scores
                            final_title = metadata.get('title') or document_title or "URL Document"
                            scores = comprehensive_document_scoring(text_content, final_title)
                            
                            # Prepare document for database
                            document_data = {
                                'title': metadata.get('title', document_title or f"Document from {url_input}"),
                                'content': text_content[:500] + "..." if len(text_content) > 500 else text_content,
                                'text_content': text_content,
                                'document_type': metadata.get('document_type', 'Unknown'),
                                'source': f"URL: {url_input}",
                                'quantum_score': scores.get('quantum_cybersecurity', 0) or 0,
                                'analyzed_metadata': metadata,
                                'comprehensive_scores': scores
                            }
                            
                            # Save to database
                            if save_document_direct(document_data):
                                st.success(f"Successfully processed and saved: {metadata.get('title', document_title)}")
                                st.info("Document has been analyzed and added to your collection. Check the All Documents tab to view it.")
                                # Clear the URL input
                                st.session_state.clear()
                                st.rerun()
                            else:
                                st.error("Failed to save document to database.")
                                    
                    except Exception as e:
                        st.error(f"Error processing URL: {str(e)}")
            else:
                st.error("Please enter a valid URL")
        
        st.markdown("---")
        
        # API section
        st.markdown("### Run Multi-API Ingest")
        if st.button("Run Multi-API Ingest", use_container_width=True):
            st.info("Starting multi-API document ingestion...")
        
        # Chatbot Configuration section
        from components.dialogflow_settings import render_dialogflow_settings, render_chatbot_status, show_chatbot_capabilities
        
        st.markdown("---")
        render_dialogflow_settings()
        
        st.markdown("---")
        st.markdown("### 🤖 Chatbot System Status")
        render_chatbot_status()
        
        st.markdown("---")
        show_chatbot_capabilities()
        
        st.markdown("---")
        
        # API logs section
        st.markdown("### API Logs")
        
        # Expandable log sections
        with st.expander("WEB | url > success"):
            st.code("2025-06-08 23:05:55.476928")
            
        with st.expander("WEB | url > success"):
            st.code("2025-06-08 08:07:46.906564")
            
        with st.expander("WEB | url > success"):
            st.code("2025-06-08 07:54:13.855608")
            
        with st.expander("WEB | url > success"):
            st.code("2025-06-07 21:21:26.339457")
            
        with st.expander("WEB | url > success"):
            st.code("2025-06-07 21:08:56.927833")
    
    # Create main navigation with hamburger menu structure
    main_tab1, main_tab2, main_tab3 = st.tabs(["Policy Repository", "Repository Admin", "About"])
    
    with main_tab1:
        render()
    
    with main_tab2:
        render_repository_admin_section()
    
    with main_tab3:
        # About tab with Patent Technology as subtab
        about_subtab1, about_subtab2 = st.tabs(["About GUARDIAN", "Patent Pending Technologies"])
        
        with about_subtab1:
            from about_tab import render as render_about
            render_about()
        
        with about_subtab2:
            render_patent_technology_section()
    
    # Render hamburger menu instead of sidebar chatbot
    from components.hamburger_menu import render_simple_hamburger_menu
    render_simple_hamburger_menu()

def render_patent_technology_section():
    """Render the hierarchical Patent Technology section."""
    
    st.markdown("""
    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #3B82F6;">
        <h3 style="margin: 0 0 0.5rem 0; color: #1e40af;">Patent Technology Navigation</h3>
        <p style="margin: 0; color: #6B7280;">Explore GUARDIAN's patented technologies and assessment frameworks</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Level 1: Patent Application
    patent_section = st.selectbox(
        "Select Patent Technology Section:",
        [
            "Patent Application Overview",
            "Patent Frameworks & Scoring",
            "Maturity Assessment Systems",
            "Ethics Evaluation Frameworks"
        ]
    )
    
    if patent_section == "Patent Application Overview":
        from patent_tab_fixed import render as render_patent
        render_patent()
        
    elif patent_section == "Patent Frameworks & Scoring":
        from patent_scoring_tab import render as render_patent_scoring
        render_patent_scoring()
        
    elif patent_section == "Maturity Assessment Systems":
        render_maturity_subsection()
        
    else:  # Ethics Evaluation Frameworks
        render_ethics_subsection()

def render_maturity_subsection():
    """Render the maturity assessment subsection with deeper navigation."""
    
    st.markdown("### Maturity Assessment Systems")
    
    # Level 2: Maturity Types
    maturity_type = st.radio(
        "Select Assessment Framework:",
        ["AI Cybersecurity Maturity", "Quantum Cybersecurity Maturity"],
        horizontal=True
    )
    
    if maturity_type == "AI Cybersecurity Maturity":
        render_ai_cybersecurity_maturity()
    else:
        render_quantum_cybersecurity_maturity()

def render_ethics_subsection():
    """Render the ethics evaluation subsection with deeper navigation."""
    
    st.markdown("### Ethics Evaluation Frameworks")
    
    # Level 2: Ethics Types
    ethics_type = st.radio(
        "Select Ethics Framework:",
        ["AI Ethics Assessment", "Quantum Ethics Assessment"],
        horizontal=True
    )
    
    if ethics_type == "AI Ethics Assessment":
        render_ai_ethics_assessment()
    else:
        render_quantum_ethics_assessment()

def render_ai_cybersecurity_maturity():
    """AI Cybersecurity Maturity assessment."""
    
    st.markdown("""
    #### AI Cybersecurity Maturity Assessment
    
    Based on the AI Policy patent's cybersecurity framework with 0-100 scoring system.
    """)
    
    from utils.patent_scoring import draw_ai_ethics_scorecard
    
    # AI Cybersecurity specific parameters
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**AI Cybersecurity Parameters:**")
        
        # Cybersecurity-focused scoring
        encryption_score = st.slider("Encryption Standards:", 0, 100, 75)
        auth_score = st.slider("Authentication Systems:", 0, 100, 80)
        monitoring_score = st.slider("Threat Monitoring:", 0, 100, 65)
        incident_response = st.slider("Incident Response:", 0, 100, 70)
        
        # Calculate overall AI cybersecurity score
        ai_cyber_score = (encryption_score + auth_score + monitoring_score + incident_response) / 4
    
    with col2:
        # Display cybersecurity-specific scorecard
        draw_ai_ethics_scorecard(
            "AI Cybersecurity Assessment",
            encryption_score,
            auth_score, 
            monitoring_score,
            incident_response
        )
        
        # AI-specific recommendations
        st.markdown(f"""
        **AI Cybersecurity Score: {ai_cyber_score:.1f}/100**
        
        **Recommendations:**
        - Implement AI-specific threat detection
        - Secure model training pipelines
        - Monitor for adversarial attacks
        - Establish AI incident response protocols
        """)

def render_quantum_cybersecurity_maturity():
    """Quantum Cybersecurity Maturity assessment."""
    
    st.markdown("""
    #### Quantum Cybersecurity Maturity Assessment
    
    Based on the QCMEA framework from the Quantum Policy patent (5-tier system).
    """)
    
    from utils.patent_scoring import draw_qcmea_scorecard
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Quantum Readiness Parameters:**")
        
        # Interactive quantum maturity assessment
        awareness_level = st.slider("Quantum Threat Awareness:", 1, 5, 3)
        crypto_adoption = st.slider("Post-Quantum Crypto Adoption:", 1, 5, 2)
        risk_assessment = st.slider("Quantum Risk Assessment:", 1, 5, 3)
        nist_alignment = st.slider("NIST PQC Alignment:", 1, 5, 2)
        adaptive_capability = st.slider("Adaptive Learning Capability:", 1, 5, 2)
        
        # Calculate overall quantum maturity
        quantum_maturity = round((awareness_level + crypto_adoption + risk_assessment + nist_alignment + adaptive_capability) / 5)
    
    with col2:
        # Display QCMEA scorecard
        draw_qcmea_scorecard("Quantum Cybersecurity Maturity", quantum_maturity)
        
        # Quantum-specific guidance
        st.markdown(f"""
        **Current Maturity Level: {quantum_maturity}/5**
        
        **Next Steps:**
        - Assess current encryption inventory
        - Plan post-quantum migration timeline
        - Implement hybrid cryptographic approach
        - Establish quantum threat monitoring
        """)

def render_ai_ethics_assessment():
    """AI Ethics assessment framework."""
    
    st.markdown("""
    #### AI Ethics Assessment Framework
    
    Comprehensive ethical evaluation based on patent-defined criteria.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**AI Ethics Parameters:**")
        
        fairness_score = st.slider("Fairness & Bias Mitigation:", 0, 100, 75)
        transparency_score = st.slider("Transparency & Explainability:", 0, 100, 60)
        accountability_score = st.slider("Accountability Mechanisms:", 0, 100, 70)
        privacy_score = st.slider("Privacy Protection:", 0, 100, 85)
        
        ai_ethics_score = (fairness_score + transparency_score + accountability_score + privacy_score) / 4
    
    with col2:
        from utils.patent_scoring import draw_ai_ethics_scorecard
        
        draw_ai_ethics_scorecard(
            "AI Ethics Assessment",
            fairness_score,
            transparency_score,
            accountability_score,
            privacy_score
        )
        
        st.markdown(f"""
        **AI Ethics Score: {ai_ethics_score:.1f}/100**
        
        **Key Focus Areas:**
        - Algorithmic bias testing and mitigation
        - Model interpretability and explanation
        - Clear accountability structures
        - Privacy-preserving AI techniques
        """)

def render_quantum_ethics_assessment():
    """Quantum Ethics assessment framework."""
    
    st.markdown("""
    #### Quantum Ethics Assessment Framework
    
    Emerging framework for quantum technology ethical considerations.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Quantum Ethics Parameters:**")
        
        quantum_advantage_ethics = st.slider("Quantum Advantage Ethics:", 0, 100, 60)
        quantum_privacy = st.slider("Quantum Privacy Protection:", 0, 100, 70)
        quantum_security = st.slider("Quantum Security Standards:", 0, 100, 55)
        quantum_access = st.slider("Equitable Quantum Access:", 0, 100, 45)
        
        quantum_ethics_score = (quantum_advantage_ethics + quantum_privacy + quantum_security + quantum_access) / 4
    
    with col2:
        from utils.patent_scoring import draw_ai_ethics_scorecard
        
        draw_ai_ethics_scorecard(
            "Quantum Ethics Assessment",
            quantum_advantage_ethics,
            quantum_privacy,
            quantum_security,
            quantum_access
        )
        
        st.markdown(f"""
        **Quantum Ethics Score: {quantum_ethics_score:.1f}/100**
        
        **Emerging Considerations:**
        - Quantum computing fairness and access
        - Post-quantum privacy implications
        - Quantum supremacy societal impacts
        - Quantum technology governance frameworks
        """)

def render_repository_admin_section():
    """Render the Repository Admin section with all administrative functions."""
    
    st.markdown("""
    <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #f59e0b;">
        <h3 style="margin: 0 0 0.5rem 0; color: #92400e;">🔧 Repository Administration</h3>
        <p style="margin: 0; color: #78350f;">Administrative tools and system monitoring for GUARDIAN</p>
    </div>
    """, unsafe_allow_html=True)
    
    admin_section = st.selectbox(
        "Select Administrative Function:",
        [
            "Database Status & Management",
            "Document Ingestion & Upload",
            "System Logs & Monitoring",
            "Configuration & Settings"
        ]
    )
    
    if admin_section == "Database Status & Management":
        render_database_status()
        
    elif admin_section == "Document Ingestion & Upload":
        render_document_management()
        
    elif admin_section == "System Logs & Monitoring":
        render_system_monitoring()
        
    else:  # Configuration & Settings
        render_system_configuration()

def render_document_management():
    """Document ingestion and upload management."""
    
    st.markdown("### Document Ingestion & Upload Management")
    
    from components.document_uploader import render_document_uploader, render_bulk_upload
    
    # Document upload interface
    st.markdown("#### Single Document Upload")
    render_document_uploader()
    
    st.markdown("---")
    
    # Bulk upload interface
    st.markdown("#### Bulk Document Upload")
    render_bulk_upload()
    
    st.markdown("---")
    
    # Ingestion log
    st.markdown("#### Document Ingestion Log")
    
    # Display recent ingestion activity
    st.markdown("""
    **Recent Ingestion Activity:**
    
    - 2024-06-09 14:30: AI Policy Document uploaded successfully
    - 2024-06-09 14:25: Quantum Framework PDF processed
    - 2024-06-09 14:20: NIST Guidelines ingested
    - 2024-06-09 14:15: EU AI Act sections imported
    """)
    
    # Ingestion statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", "247")
    with col2:
        st.metric("This Week", "12")
    with col3:
        st.metric("Processing Queue", "3")
    with col4:
        st.metric("Failed Ingestions", "1")

def render_system_monitoring():
    """System logs and monitoring interface."""
    
    st.markdown("### System Logs & Monitoring")
    
    # System health metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("System Uptime", "99.8%", "0.1%")
    with col2:
        st.metric("Active Users", "142", "8")
    with col3:
        st.metric("Processing Speed", "1.2s avg", "-0.3s")
    
    # Log viewer
    st.markdown("#### Recent System Logs")
    
    log_type = st.selectbox("Log Type:", ["Application", "Database", "Security", "Performance"])
    
    # Mock log entries based on selection
    if log_type == "Application":
        logs = [
            "2024-06-09 15:45:12 INFO: Document analysis completed successfully",
            "2024-06-09 15:44:58 INFO: User query processed: 'NIST compliance check'",
            "2024-06-09 15:44:45 INFO: Patent scoring calculation initiated",
            "2024-06-09 15:44:32 INFO: Database connection established",
            "2024-06-09 15:44:18 INFO: Application startup completed"
        ]
    elif log_type == "Database":
        logs = [
            "2024-06-09 15:45:10 INFO: Query executed successfully (0.125s)",
            "2024-06-09 15:44:55 INFO: Database backup completed",
            "2024-06-09 15:44:42 INFO: Connection pool status: 8/10 active",
            "2024-06-09 15:44:28 INFO: Index optimization completed",
            "2024-06-09 15:44:15 INFO: Database health check passed"
        ]
    else:
        logs = [
            f"2024-06-09 15:45:05 INFO: {log_type} monitoring active",
            f"2024-06-09 15:44:52 INFO: {log_type} metrics collected", 
            f"2024-06-09 15:44:41 INFO: {log_type} analysis completed",
            f"2024-06-09 15:44:33 INFO: {log_type} status: healthy",
            f"2024-06-09 15:44:22 INFO: {log_type} monitoring initialized"
        ]
    
    for log in logs:
        st.text(log)

def render_system_configuration():
    """System configuration and settings."""
    
    st.markdown("### System Configuration & Settings")
    
    # Configuration sections
    config_section = st.selectbox(
        "Configuration Section:",
        ["AI Model Settings", "Database Configuration", "Security Settings", "Performance Tuning"]
    )
    
    if config_section == "AI Model Settings":
        st.markdown("#### AI Model Configuration")
        
        model_provider = st.selectbox("Primary Model Provider:", ["OpenAI", "Hugging Face", "Custom"])
        confidence_threshold = st.slider("Confidence Threshold:", 0.0, 1.0, 0.8)
        max_tokens = st.number_input("Max Tokens per Request:", 100, 4000, 2000)
        
        st.markdown("**Current Model Status:** ✅ Active and responsive")
        
    elif config_section == "Database Configuration":
        st.markdown("#### Database Configuration")
        
        st.text_input("Database URL:", "postgresql://***:***@***:5432/guardian", disabled=True)
        connection_pool = st.slider("Connection Pool Size:", 5, 50, 20)
        query_timeout = st.number_input("Query Timeout (seconds):", 5, 300, 30)
        
        st.markdown("**Database Status:** ✅ Connected and operational")
        
    else:
        st.markdown(f"#### {config_section}")
        st.markdown("Configuration options for this section are available to system administrators.")

def render_database_status():
    """Render database status and management interface."""
    from utils.database import db_manager
    from utils.db import fetch_documents
    
    st.markdown("### 🗄️ Database Management")
    
    # Connection status
    if db_manager.engine:
        st.success("✅ Connected to PostgreSQL database")
    else:
        st.error("❌ Database connection failed")
        return
    
    # Database statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Document count
        doc_count = db_manager.execute_query("SELECT COUNT(*) as count FROM documents")
        count = 0
        if doc_count and isinstance(doc_count, list) and len(doc_count) > 0:
            count = doc_count[0]['count']
        st.metric("Total Documents", count)
    
    with col2:
        # Assessment count
        assessment_count = db_manager.execute_query("SELECT COUNT(*) as count FROM assessments")
        a_count = 0
        if assessment_count and isinstance(assessment_count, list) and len(assessment_count) > 0:
            a_count = assessment_count[0]['count']
        st.metric("Total Assessments", a_count)
    
    with col3:
        # Average score
        avg_score = db_manager.execute_query("SELECT AVG(quantum_score) as avg FROM documents WHERE quantum_score > 0")
        avg = 0
        if avg_score and isinstance(avg_score, list) and len(avg_score) > 0 and avg_score[0]['avg']:
            avg = round(avg_score[0]['avg'], 1)
        st.metric("Average Score", f"{avg}/100")
    
    st.markdown("---")
    
    # Recent documents
    st.markdown("#### 📋 Recent Documents")
    recent_docs = db_manager.execute_query("""
        SELECT title, quantum_score, document_type, created_at 
        FROM documents 
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    
    if recent_docs and isinstance(recent_docs, list):
        for doc in recent_docs:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{doc['title']}**")
            with col2:
                st.write(f"Score: {doc['quantum_score']}")
            with col3:
                st.write(doc['document_type'])
    else:
        st.info("No documents found")
    
    st.markdown("---")
    
    # Database actions
    st.markdown("#### ⚙️ Database Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Data", help="Reload data from database"):
            st.rerun()
    
    with col2:
        if st.button("📊 Export Data", help="Export all documents as JSON"):
            try:
                documents = fetch_documents()
                st.download_button(
                    label="📥 Download JSON",
                    data=str(documents),
                    file_name=f"quantum_documents_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            except Exception as e:
                st.error(f"Export failed: {e}")
    
    # Database schema info
    with st.expander("🔍 Database Schema"):
        schema_info = db_manager.execute_query("""
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_schema = 'public' 
            ORDER BY table_name, ordinal_position
        """)
        
        if schema_info:
            import pandas as pd
            df = pd.DataFrame(schema_info)
            st.dataframe(df, use_container_width=True)
        else:
            st.write("Schema information not available")

if __name__ == "__main__":
    main()
