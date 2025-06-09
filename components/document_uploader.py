import streamlit as st
from utils.db import save_document
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf
import datetime

def render_document_uploader():
    """Render the document upload interface."""
    
    st.markdown("### 📄 Add New Document")
    
    with st.form("document_upload_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Document Title*", placeholder="e.g., Quantum Security Assessment")
            document_type = st.selectbox(
                "Document Type",
                ["strategy", "assessment", "framework", "policy", "implementation", "research"]
            )
        
        with col2:
            source = st.selectbox(
                "Source",
                ["internal", "external", "vendor", "regulatory", "research"]
            )
            auto_analyze = st.checkbox("Auto-analyze with AI", value=True)
        
        content = st.text_area(
            "Document Content*",
            placeholder="Paste the full text content of your document here...",
            height=200
        )
        
        summary = st.text_input(
            "Brief Summary",
            placeholder="One-line summary of the document"
        )
        
        submitted = st.form_submit_button("Add Document", type="primary")
        
        if submitted:
            if not title or not content:
                st.error("Please provide both title and content.")
                return
            
            with st.spinner("Processing document..."):
                # Prepare document data
                document_data = {
                    'title': title,
                    'content': summary if summary else content[:200] + "...",
                    'text': content,
                    'document_type': document_type,
                    'source': source,
                    'quantum_q': 0  # Will be updated by AI analysis if enabled
                }
                
                # Perform AI analysis if requested
                if auto_analyze:
                    try:
                        ai_result = evaluate_quantum_maturity_hf(content)
                        document_data['quantum_q'] = ai_result.get('patent_score', 0)
                        
                        st.success(f"Document analyzed! Quantum maturity score: {ai_result.get('patent_score', 0):.1f}/100")
                        
                        # Show quick analysis preview
                        if ai_result.get('narrative'):
                            st.info("Key findings: " + ", ".join(ai_result['narrative'][:2]))
                            
                    except Exception as e:
                        st.warning(f"AI analysis failed, document saved without score: {e}")
                
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
    """Render bulk document upload interface."""
    
    st.markdown("### 📚 Bulk Document Upload")
    
    uploaded_files = st.file_uploader(
        "Upload multiple documents",
        type=['txt', 'md', 'csv'],
        accept_multiple_files=True,
        help="Upload text files, markdown files, or CSV files containing document data"
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
                    # Read file content
                    content = uploaded_file.read().decode('utf-8')
                    
                    # Prepare document
                    document_data = {
                        'title': uploaded_file.name.replace('.txt', '').replace('.md', ''),
                        'content': content[:200] + "..." if len(content) > 200 else content,
                        'text': content,
                        'document_type': 'uploaded',
                        'source': 'file_upload',
                        'quantum_q': 0
                    }
                    
                    # AI analysis
                    try:
                        ai_result = evaluate_quantum_maturity_hf(content)
                        document_data['quantum_q'] = ai_result.get('patent_score', 0)
                    except:
                        pass  # Continue without AI analysis if it fails
                    
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