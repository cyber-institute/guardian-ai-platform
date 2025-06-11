import streamlit as st
from utils.db import save_document
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf
import datetime

def render_document_uploader():
    """Render the document upload interface with PDF support and thumbnail extraction."""
    
    st.markdown("### 📄 Add New Document")
    
    # Content input options
    input_method = st.radio(
        "Content Input Method:",
        ["Manual Entry", "PDF Upload", "URL Extraction"],
        horizontal=True
    )
    
    uploaded_file = None
    url_content = None
    
    if input_method == "PDF Upload":
        uploaded_file = st.file_uploader(
            "Upload PDF Document",
            type=['pdf'],
            help="Upload a PDF file to automatically extract content and generate thumbnail"
        )
    elif input_method == "URL Extraction":
        url_input = st.text_input(
            "Enter URL to extract content:",
            placeholder="https://example.com/document",
            help="Enter a web URL to automatically extract content and metadata"
        )
        
        if url_input and st.button("Extract from URL", type="secondary"):
            with st.spinner("Extracting content from URL..."):
                from utils.url_content_extractor import extract_url_content
                url_result = extract_url_content(url_input)
                
                if url_result['success']:
                    url_content = url_result
                    st.success(f"Successfully extracted content from: {url_result['organization']}")
                    st.info(f"Title: {url_result['title'][:100]}...")
                else:
                    st.error(f"Failed to extract content: {url_result['error']}")
                    url_content = None
    
    with st.form("document_upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Pre-populate from URL extraction if available
            if url_content:
                title = st.text_input("Document Title*", value=url_content['title'], placeholder="e.g., Quantum Security Assessment")
                organization = st.text_input("Author/Organization", value=url_content['organization'])
            else:
                title = st.text_input("Document Title*", placeholder="e.g., Quantum Security Assessment")
                organization = st.text_input("Author/Organization", placeholder="e.g., NIST, NASA, EU Agency")
            
            from utils.document_classifier import DOCUMENT_TYPES
            document_type = st.selectbox(
                "Document Type",
                list(DOCUMENT_TYPES.keys())
            )
        
        with col2:
            source = st.selectbox(
                "Source",
                ["internal", "external", "vendor", "regulatory", "research"]
            )
            if url_content:
                url_field = st.text_input("Source URL", value=url_content['url'])
            else:
                url_field = st.text_input("Source URL (Optional)", placeholder="https://example.com/document")
            auto_analyze = st.checkbox("Auto-analyze with AI", value=True)
        
        # Content input - auto-populate based on input method
        content_placeholder = "Paste the full text content of your document here..."
        content_value = ""
        
        if uploaded_file:
            content_placeholder = "Content will be automatically extracted from uploaded PDF..."
        elif url_content:
            content_placeholder = "Content extracted from URL - you can edit if needed"
            content_value = url_content['text_content'][:8000] + "..." if len(url_content['text_content']) > 8000 else url_content['text_content']
            
        content = st.text_area(
            "Document Content*",
            value=content_value,
            placeholder=content_placeholder,
            height=200
        )
        
        summary = st.text_input(
            "Brief Summary",
            placeholder="One-line summary of the document"
        )
        
        submitted = st.form_submit_button("Add Document", type="primary")
        
        if submitted:
            # Handle PDF upload with thumbnail extraction
            pdf_content = None
            pdf_thumbnail_extracted = False
            
            if uploaded_file:
                with st.spinner("Processing PDF and extracting thumbnail..."):
                    from utils.pdf_ingestion_thumbnails import process_uploaded_pdf_with_thumbnail
                    import time
                    
                    # Generate temporary doc_id for processing
                    temp_doc_id = int(time.time() * 1000) % 1000000
                    
                    pdf_result = process_uploaded_pdf_with_thumbnail(uploaded_file, temp_doc_id)
                    
                    if pdf_result['text_content']:
                        pdf_content = pdf_result['text_content']
                        pdf_thumbnail_extracted = pdf_result['thumbnail_data'] is not None
                        
                        # Extract region detection results
                        region_data = pdf_result.get('region_metadata', {})
                        detected_region = region_data.get('detected_region', 'Unknown')
                        region_confidence = region_data.get('region_confidence', 0.0)
                        
                        if pdf_thumbnail_extracted:
                            st.success(f"PDF processed successfully! Thumbnail extracted and region detected: {detected_region} (confidence: {region_confidence:.1%})")
                        else:
                            st.warning("PDF processed but thumbnail extraction failed. Using fallback thumbnail.")
                        
                        # Auto-fill title if not provided
                        if not title and 'filename' in pdf_result:
                            title = pdf_result['filename'].replace('.pdf', '').replace('_', ' ').title()
            
            # Use PDF content if available, otherwise require manual content input
            final_content = pdf_content if pdf_content else content
            
            if not title or not final_content:
                st.error("Please provide both title and content (or upload a PDF file).")
                return
            
            with st.spinner("Processing document..."):
                # Enhanced metadata extraction for all ingestion methods
                try:
                    from utils.enhanced_metadata_extractor import extract_enhanced_metadata
                    from utils.duplicate_detector import check_document_duplicates
                    
                    # Check for duplicates first
                    duplicate_result = check_document_duplicates(
                        title=title,
                        content=final_content,
                        url=url_field if url_field else "",
                        filename=uploaded_file.name if uploaded_file else ""
                    )
                    
                    if duplicate_result["is_duplicate"]:
                        st.error(f"🚫 Duplicate document detected!")
                        st.warning(f"Confidence: {duplicate_result['confidence']:.1%} - {duplicate_result['match_type']}")
                        for match in duplicate_result["matches"][:2]:
                            st.info(f"Similar to: {match['title']} (ID: {match['id']}) - {match['reason']}")
                        return
                    
                    # Extract comprehensive metadata using multi-LLM intelligence
                    enhanced_metadata = extract_enhanced_metadata(
                        title=title,
                        content=final_content,
                        url=url_field if url_field else "",
                        filename=uploaded_file.name if uploaded_file else ""
                    )
                    
                    # Use enhanced metadata with form overrides
                    final_title = title if title != enhanced_metadata.get('title', 'Unknown') else enhanced_metadata.get('title', title)
                    final_organization = organization if organization else enhanced_metadata.get('organization', 'Unknown')
                    final_author = enhanced_metadata.get('author', 'Unknown')
                    final_pub_date = enhanced_metadata.get('publication_date', 'Unknown')
                    final_description = summary if summary else enhanced_metadata.get('description', 'Unknown')
                    final_doc_type = document_type if document_type != 'Unknown' else enhanced_metadata.get('document_type', document_type)
                    
                    st.info(f"📋 Enhanced metadata extracted - Organization: {final_organization}, Type: {final_doc_type}")
                    
                except Exception as e:
                    st.warning(f"Enhanced metadata extraction failed: {e}. Using form data.")
                    final_title = title
                    final_organization = organization if organization else "Unknown"
                    final_author = "Unknown"
                    final_pub_date = "Unknown"
                    final_description = summary if summary else "Unknown"
                    final_doc_type = document_type
                
                # Prepare document data with enhanced metadata
                document_data = {
                    'title': final_title,
                    'content': final_description if final_description != 'Unknown' else final_content[:200] + "...",
                    'text': final_content,
                    'document_type': final_doc_type,
                    'source': source,
                    'author_organization': final_organization,
                    'author': final_author,
                    'publication_date': final_pub_date,
                    'quantum_q': 0,  # Will be updated by AI analysis if enabled
                    'has_thumbnail': pdf_thumbnail_extracted
                }
                
                # Apply comprehensive patent-based scoring
                if auto_analyze:
                    try:
                        from utils.patent_scoring_engine import ComprehensivePatentScoringEngine
                        
                        # Initialize scoring engine
                        scoring_engine = ComprehensivePatentScoringEngine()
                        
                        # Apply comprehensive scoring to document content
                        scores = scoring_engine.assess_document_comprehensive(final_content, title)
                        
                        # Update document data with all four framework scores
                        document_data.update({
                            'ai_cybersecurity_score': scores['ai_cybersecurity_score'],
                            'quantum_cybersecurity_score': scores['quantum_cybersecurity_score'],
                            'ai_ethics_score': scores['ai_ethics_score'],
                            'quantum_ethics_score': scores['quantum_ethics_score'],
                            'quantum_q': scores['quantum_cybersecurity_score'] * 20  # Legacy compatibility
                        })
                        
                        # Enhanced region detection for all input methods
                        try:
                            from utils.enhanced_region_detector import enhanced_region_detection
                            
                            # Use organization from form or extracted data
                            org_for_detection = organization if organization else "Unknown"
                            url_for_detection = url_field if url_field else ""
                            
                            region_result = enhanced_region_detection(
                                title=title,
                                content=final_content[:2000],  # First 2000 chars for analysis
                                organization=org_for_detection,
                                url=url_for_detection
                            )
                            
                            document_data.update({
                                'detected_region': region_result.get('region', 'Unknown'),
                                'region_confidence': region_result.get('confidence', 0.0),
                                'region_reasoning': region_result.get('reasoning', 'Enhanced multi-LLM detection'),
                                'author_organization': org_for_detection
                            })
                            
                            if region_result.get('confidence', 0) > 0.5:
                                st.info(f"🌍 Region detected: {region_result['region']} (confidence: {region_result['confidence']:.1%})")
                                
                        except Exception as e:
                            print(f"Region detection failed: {e}")
                            document_data.update({
                                'detected_region': 'Unknown',
                                'region_confidence': 0.0,
                                'region_reasoning': 'Detection failed',
                                'author_organization': organization if organization else "Unknown"
                            })
                        
                        st.success("Document analyzed with comprehensive patent-based scoring!")
                        
                        # Show scoring results
                        score_col1, score_col2, score_col3, score_col4 = st.columns(4)
                        
                        with score_col1:
                            st.metric("AI Cybersecurity", f"{scores['ai_cybersecurity_score']}/100")
                        with score_col2:
                            st.metric("Quantum QCMEA", f"{scores['quantum_cybersecurity_score']}/5")
                        with score_col3:
                            st.metric("AI Ethics", f"{scores['ai_ethics_score']}/100")
                        with score_col4:
                            st.metric("Quantum Ethics", f"{scores['quantum_ethics_score']}/100")
                            
                    except Exception as e:
                        st.warning(f"Patent scoring failed, applying fallback analysis: {e}")
                        try:
                            ai_result = evaluate_quantum_maturity_hf(final_content)
                            document_data['quantum_q'] = ai_result.get('patent_score', 0)
                        except:
                            document_data['quantum_q'] = 0
                
                # Save to database
                try:
                    success = save_document(document_data)
                    if success:
                        st.success("Document successfully added to the database!")
                        st.balloons()
                        # Clear form by rerunning
                        st.rerun()
                    else:
                        st.error("Failed to save document to database.")
                except Exception as e:
                    st.error(f"Database error: {e}")

def render_bulk_upload():
    """Render bulk document upload interface with PDF support."""
    
    st.markdown("### 📚 Bulk Document Upload")
    
    uploaded_files = st.file_uploader(
        "Upload multiple documents",
        type=['txt', 'md', 'csv', 'pdf'],
        accept_multiple_files=True,
        help="Upload text files, markdown files, CSV files, or PDF documents with automatic thumbnail extraction"
    )
    
    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} files")
        
        if st.button("Process All Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            successful_uploads = 0
            total_files = len(uploaded_files)
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                
                try:
                    # Handle PDF files with thumbnail extraction
                    if uploaded_file.name.lower().endswith('.pdf'):
                        from utils.pdf_ingestion_thumbnails import process_uploaded_pdf_with_thumbnail
                        import time
                        
                        # Generate doc_id for PDF processing
                        doc_id = int(time.time() * 1000) % 1000000 + i
                        
                        pdf_result = process_uploaded_pdf_with_thumbnail(uploaded_file, doc_id)
                        content = pdf_result['text_content']
                        file_title = uploaded_file.name.replace('.pdf', '').replace('_', ' ').title()
                        has_thumbnail = pdf_result['thumbnail_data'] is not None
                        
                    else:
                        # Handle text files
                        content = uploaded_file.read().decode('utf-8')
                        file_title = uploaded_file.name.replace('.txt', '').replace('.md', '').replace('.csv', '')
                        has_thumbnail = False
                    
                    # Check for duplicates
                    from utils.duplicate_detector import check_document_duplicates
                    from utils.enhanced_metadata_extractor import extract_enhanced_metadata
                    
                    duplicate_result = check_document_duplicates(
                        title=file_title,
                        content=content,
                        filename=uploaded_file.name
                    )
                    
                    if duplicate_result["is_duplicate"]:
                        st.warning(f"⚠️ Skipping duplicate: {file_title} (confidence: {duplicate_result['confidence']:.1%})")
                        continue
                    
                    # Extract enhanced metadata
                    try:
                        enhanced_metadata = extract_enhanced_metadata(
                            title=file_title,
                            content=content,
                            filename=uploaded_file.name
                        )
                        
                        final_title = enhanced_metadata.get('title', file_title)
                        final_organization = enhanced_metadata.get('organization', 'Unknown')
                        final_author = enhanced_metadata.get('author', 'Unknown')
                        final_pub_date = enhanced_metadata.get('publication_date', 'Unknown')
                        final_description = enhanced_metadata.get('description', 'Unknown')
                        final_doc_type = enhanced_metadata.get('document_type', 'Unknown')
                        
                    except Exception as e:
                        print(f"Enhanced metadata extraction failed for {file_title}: {e}")
                        final_title = file_title
                        final_organization = "Unknown"
                        final_author = "Unknown"
                        final_pub_date = "Unknown"
                        final_description = "Unknown"
                        
                        # Fallback to basic detection
                        from utils.document_classifier import detect_document_type
                        final_doc_type = detect_document_type(file_title, content)
                    
                    # Prepare document with enhanced metadata
                    document_data = {
                        'title': final_title,
                        'content': final_description if final_description != 'Unknown' else content[:200] + "..." if len(content) > 200 else content,
                        'text': content,
                        'document_type': final_doc_type,
                        'source': 'file_upload',
                        'author_organization': final_organization,
                        'author': final_author,
                        'publication_date': final_pub_date,
                        'quantum_q': 0,
                        'has_thumbnail': has_thumbnail
                    }
                    
                    # Apply comprehensive patent-based scoring
                    try:
                        from utils.patent_scoring_engine import ComprehensivePatentScoringEngine
                        
                        scoring_engine = ComprehensivePatentScoringEngine()
                        scores = scoring_engine.assess_document_comprehensive(content, file_title)
                        
                        # Update document with all four framework scores
                        document_data.update({
                            'ai_cybersecurity_score': scores['ai_cybersecurity_score'],
                            'quantum_cybersecurity_score': scores['quantum_cybersecurity_score'],
                            'ai_ethics_score': scores['ai_ethics_score'],
                            'quantum_ethics_score': scores['quantum_ethics_score'],
                            'quantum_q': scores['quantum_cybersecurity_score'] * 20
                        })
                    except Exception as e:
                        # Fallback to legacy scoring if patent scoring fails
                        try:
                            ai_result = evaluate_quantum_maturity_hf(content)
                            document_data['quantum_q'] = ai_result.get('patent_score', 0)
                        except:
                            document_data['quantum_q'] = 0
                    
                    # Save to database
                    if save_document(document_data):
                        successful_uploads += 1
                        
                except Exception as e:
                    st.error(f"Failed to process {uploaded_file.name}: {e}")
                
                # Update progress
                progress_bar.progress((i + 1) / total_files)
            
            status_text.text("Upload complete!")
            st.success(f"Successfully uploaded {successful_uploads} out of {total_files} documents.")
            
            if successful_uploads > 0:
                st.balloons()