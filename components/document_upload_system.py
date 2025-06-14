"""
Enhanced Document Upload System with Automatic URL Discovery
"""

import streamlit as st
import os
import tempfile
import pypdf
from typing import Optional, Dict
from utils.enhanced_metadata_extractor import extract_enhanced_metadata
from utils.self_healing_url_system import SelfHealingURLSystem
from utils.ml_enhanced_scoring import assess_document_with_ml
import psycopg2
from datetime import datetime

class DocumentUploadSystem:
    """
    Enhanced document upload with automatic metadata extraction and URL discovery
    """
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.txt', '.docx', '.doc']
    
    def render_upload_interface(self):
        """Render the document upload interface"""
        
        st.subheader("📄 Upload Document")
        st.markdown("Upload a document to automatically extract metadata, discover source URLs, and perform AI/Quantum analysis.")
        
        uploaded_file = st.file_uploader(
            "Choose a document file",
            type=['pdf', 'txt', 'docx', 'doc'],
            help="Supported formats: PDF, TXT, DOCX, DOC"
        )
        
        if uploaded_file is not None:
            return self.process_uploaded_file(uploaded_file)
        
        return None
    
    def process_uploaded_file(self, uploaded_file) -> Optional[Dict]:
        """Process the uploaded file with full analysis"""
        
        with st.spinner("Processing uploaded document..."):
            try:
                # Extract text content from file
                content = self._extract_text_from_file(uploaded_file)
                
                if not content:
                    st.error("Could not extract text from the uploaded file.")
                    return None
                
                # Basic file info
                file_info = {
                    'filename': uploaded_file.name,
                    'file_size': len(uploaded_file.getvalue()),
                    'content_length': len(content)
                }
                
                st.success(f"✅ Extracted {len(content)} characters from {uploaded_file.name}")
                
                # Extract enhanced metadata
                with st.spinner("Extracting metadata..."):
                    metadata = extract_enhanced_metadata(content, uploaded_file.name)
                
                # Auto-discover and validate source URL
                with st.spinner("Auto-discovering source URL..."):
                    healer = SelfHealingURLSystem()
                    discovered_url = healer._heal_document_url(
                        metadata['title'], 
                        metadata['author_organization'], 
                        content
                    )
                    
                    # Validate discovered URL
                    if discovered_url:
                        is_valid, status, redirect = healer.validator.validate_url(discovered_url)
                        if not is_valid:
                            discovered_url = None
                
                # Perform ML-enhanced scoring
                with st.spinner("Analyzing document with ML frameworks..."):
                    ml_scores = assess_document_with_ml(content, metadata['title'])
                
                # Display analysis results
                self._display_analysis_results(metadata, discovered_url, ml_scores, file_info)
                
                # Option to save to database
                if st.button("💾 Save Document to Repository", type="primary"):
                    doc_id = self._save_to_database(content, metadata, discovered_url, ml_scores)
                    if doc_id:
                        st.success(f"✅ Document saved to repository with ID: {doc_id}")
                        st.balloons()
                        return {'doc_id': doc_id, 'metadata': metadata}
                
                return {
                    'content': content,
                    'metadata': metadata,
                    'url': discovered_url,
                    'scores': ml_scores,
                    'file_info': file_info
                }
                
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
                return None
    
    def _extract_text_from_file(self, uploaded_file) -> Optional[str]:
        """Extract text content from uploaded file"""
        
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._extract_from_pdf(uploaded_file)
            elif file_extension == '.txt':
                return str(uploaded_file.getvalue(), 'utf-8')
            elif file_extension in ['.docx', '.doc']:
                return self._extract_from_docx(uploaded_file)
            else:
                return None
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            return None
    
    def _extract_from_pdf(self, uploaded_file) -> Optional[str]:
        """Extract text from PDF file"""
        
        try:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Extract text using pypdf
            with open(tmp_file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            # Clean up
            os.unlink(tmp_file_path)
            
            return text.strip()
            
        except Exception as e:
            st.error(f"PDF extraction error: {str(e)}")
            return None
    
    def _extract_from_docx(self, uploaded_file) -> Optional[str]:
        """Extract text from DOCX file"""
        
        try:
            from docx import Document
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Extract text using python-docx
            doc = Document(tmp_file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Clean up
            os.unlink(tmp_file_path)
            
            return text.strip()
            
        except ImportError:
            st.error("python-docx library not available for DOCX processing")
            return None
        except Exception as e:
            st.error(f"DOCX extraction error: {str(e)}")
            return None
    
    def _display_analysis_results(self, metadata: Dict, discovered_url: Optional[str], 
                                ml_scores: Dict, file_info: Dict):
        """Display the analysis results to the user"""
        
        st.subheader("📊 Document Analysis Results")
        
        # Metadata section
        with st.expander("📋 Extracted Metadata", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Title:**", metadata['title'])
                st.write("**Topic:**", metadata['topic'])
                st.write("**Document Type:**", metadata['document_type'])
                st.write("**Organization:**", metadata['author_organization'])
            
            with col2:
                st.write("**Publication Date:**", metadata['publish_date'] or "Not found")
                st.write("**File Size:**", f"{file_info['file_size']:,} bytes")
                st.write("**Content Length:**", f"{file_info['content_length']:,} characters")
        
        # URL Discovery section
        with st.expander("🔗 Source URL Discovery"):
            if discovered_url:
                st.success(f"✅ **Source URL found:** {discovered_url}")
                st.markdown(f"[Open Document]({discovered_url})")
            else:
                st.warning("⚠️ No source URL discovered. Document may be newly uploaded or from a non-standard source.")
                st.info("💡 **Tip:** The system searches for URLs in document content and uses patterns for known organizations (NIST, CISA, NASA, etc.)")
        
        # ML Scoring section
        with st.expander("🤖 AI/Quantum Framework Analysis", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                ai_cyber = ml_scores.get('ai_cybersecurity_score')
                ai_ethics = ml_scores.get('ai_ethics_score')
                
                st.write("**AI Frameworks:**")
                if ai_cyber is not None:
                    st.metric("AI Cybersecurity Maturity", f"{ai_cyber}/100")
                else:
                    st.write("AI Cybersecurity: N/A (not AI-related)")
                
                if ai_ethics is not None:
                    st.metric("AI Ethics Score", f"{ai_ethics}/100")
                else:
                    st.write("AI Ethics: N/A (not AI-related)")
            
            with col2:
                q_cyber = ml_scores.get('quantum_cybersecurity_score')
                q_ethics = ml_scores.get('quantum_ethics_score')
                
                st.write("**Quantum Frameworks:**")
                if q_cyber is not None:
                    st.metric("Quantum Cybersecurity Maturity", f"Tier {q_cyber}/5")
                else:
                    st.write("Quantum Cybersecurity: N/A (not quantum-related)")
                
                if q_ethics is not None:
                    st.metric("Quantum Ethics Score", f"{q_ethics}/100")
                else:
                    st.write("Quantum Ethics: N/A (not quantum-related)")
        
        # Framework Applicability
        framework_applicability = metadata.get('framework_applicability', {})
        if any(framework_applicability.values()):
            with st.expander("⚙️ Framework Applicability Analysis"):
                st.write("**Detected Framework Relevance:**")
                for framework, applies in framework_applicability.items():
                    status = "✅ Applicable" if applies else "❌ Not Applicable"
                    st.write(f"- {framework.replace('_', ' ').title()}: {status}")
    
    def _save_to_database(self, content: str, metadata: Dict, discovered_url: Optional[str], 
                         ml_scores: Dict) -> Optional[int]:
        """Save the document to the database"""
        
        try:
            # Connect to database
            database_url = os.getenv('DATABASE_URL')
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor()
            
            # Insert document
            cursor.execute("""
                INSERT INTO documents (
                    title, content, topic, document_type, author_organization, 
                    publish_date, source, content_preview,
                    ai_cybersecurity_score, quantum_cybersecurity_score,
                    ai_ethics_score, quantum_ethics_score,
                    created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING id
            """, (
                metadata['title'],
                content,
                metadata['topic'],
                metadata['document_type'],
                metadata['author_organization'],
                metadata['publish_date'],
                discovered_url,
                metadata['content_summary'],
                ml_scores.get('ai_cybersecurity_score'),
                ml_scores.get('quantum_cybersecurity_score'),
                ml_scores.get('ai_ethics_score'),
                ml_scores.get('quantum_ethics_score'),
                datetime.now(),
                datetime.now()
            ))
            
            doc_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            
            return doc_id
            
        except Exception as e:
            st.error(f"Database error: {str(e)}")
            return None

# Global instance
upload_system = DocumentUploadSystem()

def render_document_upload():
    """Render the document upload system"""
    return upload_system.render_upload_interface()