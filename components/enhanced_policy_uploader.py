"""
Enhanced Policy File Uploader
Handles PDF, DOCX, TXT file uploads with comprehensive metadata extraction
"""

import os
import tempfile
import uuid
from io import BytesIO
import streamlit as st

def process_uploaded_file(uploaded_file, file_type=None):
    """
    Process uploaded file and extract content with metadata.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        file_type: Optional file type override
        
    Returns:
        Dictionary with extracted content and metadata
    """
    try:
        # Read file bytes
        file_bytes = uploaded_file.read()
        filename = uploaded_file.name
        
        # Determine file type
        if not file_type:
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension == '.pdf':
                file_type = 'pdf'
            elif file_extension in ['.docx', '.doc']:
                file_type = 'docx'
            elif file_extension == '.txt':
                file_type = 'txt'
            else:
                file_type = 'unknown'
        
        # Process based on file type
        if file_type == 'pdf':
            return process_pdf_file(file_bytes, filename)
        elif file_type == 'docx':
            return process_docx_file(file_bytes, filename)
        elif file_type == 'txt':
            return process_txt_file(file_bytes, filename)
        else:
            return {
                'success': False,
                'error': f'Unsupported file type: {file_type}',
                'content': '',
                'metadata': {}
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'content': '',
            'metadata': {}
        }

def process_pdf_file(file_bytes, filename):
    """Process PDF file and extract content."""
    try:
        import PyPDF2
        from utils.pdf_ingestion_thumbnails import extract_pdf_thumbnail_during_ingestion
        import hashlib
        
        # Extract text content
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
        text_content = ""
        
        for page in pdf_reader.pages:
            text_content += page.extract_text() + "\n"
        
        # Generate thumbnail
        doc_id = hashlib.md5(file_bytes).hexdigest()[:8]
        thumbnail = extract_pdf_thumbnail_during_ingestion(file_bytes, doc_id, filename)
        
        # Extract metadata from PDF
        metadata = {}
        if pdf_reader.metadata:
            metadata = {
                'title': pdf_reader.metadata.get('/Title', ''),
                'author': pdf_reader.metadata.get('/Author', ''),
                'subject': pdf_reader.metadata.get('/Subject', ''),
                'creator': pdf_reader.metadata.get('/Creator', ''),
                'creation_date': pdf_reader.metadata.get('/CreationDate', ''),
                'modification_date': pdf_reader.metadata.get('/ModDate', '')
            }
        
        return {
            'success': True,
            'content': text_content,
            'text_content': text_content,
            'clean_content': text_content,
            'thumbnail': thumbnail,
            'metadata': metadata,
            'filename': filename,
            'file_type': 'PDF'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'content': '',
            'metadata': {}
        }

def process_docx_file(file_bytes, filename):
    """Process DOCX file and extract content."""
    try:
        from docx import Document
        
        # Load document
        doc = Document(BytesIO(file_bytes))
        
        # Extract text content
        text_content = ""
        for paragraph in doc.paragraphs:
            text_content += paragraph.text + "\n"
        
        # Extract metadata
        metadata = {
            'title': doc.core_properties.title or '',
            'author': doc.core_properties.author or '',
            'subject': doc.core_properties.subject or '',
            'keywords': doc.core_properties.keywords or '',
            'created': doc.core_properties.created,
            'modified': doc.core_properties.modified
        }
        
        return {
            'success': True,
            'content': text_content,
            'text_content': text_content,
            'clean_content': text_content,
            'thumbnail': None,
            'metadata': metadata,
            'filename': filename,
            'file_type': 'DOCX'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'content': '',
            'metadata': {}
        }

def process_txt_file(file_bytes, filename):
    """Process TXT file and extract content."""
    try:
        # Decode text content
        text_content = file_bytes.decode('utf-8', errors='ignore')
        
        # Basic metadata
        metadata = {
            'title': os.path.splitext(filename)[0],
            'filename': filename
        }
        
        return {
            'success': True,
            'content': text_content,
            'text_content': text_content,
            'clean_content': text_content,
            'thumbnail': None,
            'metadata': metadata,
            'filename': filename,
            'file_type': 'TXT'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'content': '',
            'metadata': {}
        }