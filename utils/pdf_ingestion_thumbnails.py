"""
PDF Thumbnail Extraction During Document Ingestion
Extracts real first-page thumbnails from PDF files during upload/ingestion
"""

import base64
import os
import tempfile
from io import BytesIO
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image
import hashlib

def extract_pdf_thumbnail_during_ingestion(pdf_bytes, doc_id, filename=""):
    """
    Extract thumbnail from PDF bytes during document ingestion.
    
    Args:
        pdf_bytes: Raw PDF file bytes
        doc_id: Document ID for caching
        filename: Original filename for context
        
    Returns:
        Base64 encoded thumbnail or None if extraction fails
    """
    try:
        # Convert first page of PDF to image
        pages = convert_from_bytes(pdf_bytes, first_page=1, last_page=1, dpi=150)
        
        if not pages:
            return None
            
        # Get first page
        page = pages[0]
        
        # Resize to thumbnail size (120x150 - 3x the standard size)
        thumbnail_size = (120, 150)
        page.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Create new image with white background
        thumbnail = Image.new('RGB', thumbnail_size, 'white')
        
        # Calculate position to center the image
        x = (thumbnail_size[0] - page.width) // 2
        y = (thumbnail_size[1] - page.height) // 2
        
        # Paste the page onto the white background
        thumbnail.paste(page, (x, y))
        
        # Save to cache with doc_id
        os.makedirs("thumbnails", exist_ok=True)
        cache_path = f"thumbnails/ingested_thumb_{doc_id}.png"
        thumbnail.save(cache_path, 'PNG', optimize=True)
        
        # Convert to base64 for immediate use
        buffer = BytesIO()
        thumbnail.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        
        img_b64 = base64.b64encode(img_data).decode('utf-8')
        return f"data:image/png;base64,{img_b64}"
        
    except Exception as e:
        print(f"Error extracting PDF thumbnail: {e}")
        return None

def extract_pdf_thumbnail_from_path(pdf_path, doc_id):
    """
    Extract thumbnail from PDF file path during ingestion.
    
    Args:
        pdf_path: Path to PDF file
        doc_id: Document ID for caching
        
    Returns:
        Base64 encoded thumbnail or None if extraction fails
    """
    try:
        if not os.path.exists(pdf_path):
            return None
            
        # Convert first page of PDF to image
        pages = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
        
        if not pages:
            return None
            
        # Get first page
        page = pages[0]
        
        # Resize to thumbnail size (120x150)
        thumbnail_size = (120, 150)
        page.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Create new image with white background
        thumbnail = Image.new('RGB', thumbnail_size, 'white')
        
        # Calculate position to center the image
        x = (thumbnail_size[0] - page.width) // 2
        y = (thumbnail_size[1] - page.height) // 2
        
        # Paste the page onto the white background
        thumbnail.paste(page, (x, y))
        
        # Save to cache
        os.makedirs("thumbnails", exist_ok=True)
        cache_path = f"thumbnails/ingested_thumb_{doc_id}.png"
        thumbnail.save(cache_path, 'PNG', optimize=True)
        
        # Convert to base64
        buffer = BytesIO()
        thumbnail.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        
        img_b64 = base64.b64encode(img_data).decode('utf-8')
        return f"data:image/png;base64,{img_b64}"
        
    except Exception as e:
        print(f"Error extracting PDF thumbnail from path: {e}")
        return None

def process_uploaded_pdf_with_thumbnail(uploaded_file, doc_id):
    """
    Process uploaded PDF file and extract both content and thumbnail with intelligent region detection.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        doc_id: Document ID for storage
        
    Returns:
        Dict containing extracted text content, thumbnail data, and region analysis
    """
    try:
        # Read PDF bytes
        pdf_bytes = uploaded_file.read()
        uploaded_file.seek(0)  # Reset file pointer
        
        # Extract thumbnail
        thumbnail_data = extract_pdf_thumbnail_during_ingestion(pdf_bytes, doc_id, uploaded_file.name)
        
        # Extract text content using existing text extraction methods
        try:
            import pypdf
            from io import BytesIO
            
            pdf_reader = pypdf.PdfReader(BytesIO(pdf_bytes))
            text_content = ""
            
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
                
        except Exception as text_error:
            print(f"Error extracting text from PDF: {text_error}")
            text_content = f"PDF file uploaded: {uploaded_file.name}"
        
        # Perform intelligent region detection using multi-LLM analysis
        region_metadata = {}
        try:
            from utils.region_detector import extract_enhanced_metadata_with_region
            
            # Extract title from filename
            title = uploaded_file.name.replace('.pdf', '').replace('_', ' ').title()
            
            # Use first 1000 characters for region analysis
            content_sample = text_content[:1000]
            
            # Extract organization from content or use filename
            org_name = "Unknown"
            if len(text_content) > 50:
                # Try to extract organization from early content
                import re
                org_patterns = [
                    r'(?:published by|from|issued by|prepared by)\s+([A-Z][^.]*?)(?:\.|,|\n)',
                    r'([A-Z][A-Za-z\s&]+(?:Institute|University|Department|Agency|Organization))',
                    r'(National[^.]*?)(?:\.|,|\n)',
                    r'(Department of[^.]*?)(?:\.|,|\n)'
                ]
                
                for pattern in org_patterns:
                    match = re.search(pattern, text_content[:500], re.IGNORECASE)
                    if match:
                        org_name = match.group(1).strip()
                        break
            
            region_metadata = extract_enhanced_metadata_with_region(title, content_sample, org_name)
            print(f"Region detected for {uploaded_file.name}: {region_metadata.get('detected_region', 'Unknown')} (confidence: {region_metadata.get('region_confidence', 0):.2f})")
            
        except Exception as region_error:
            print(f"Region detection failed: {region_error}")
            region_metadata = {
                'detected_region': 'Unknown',
                'region_confidence': 0.0,
                'region_reasoning': 'Region detection unavailable',
                'region_indicators': []
            }
        
        return {
            'text_content': text_content.strip(),
            'thumbnail_data': thumbnail_data,
            'file_type': 'pdf',
            'filename': uploaded_file.name,
            'region_metadata': region_metadata
        }
        
    except Exception as e:
        print(f"Error processing uploaded PDF: {e}")
        return {
            'text_content': f"PDF file uploaded: {uploaded_file.name}",
            'thumbnail_data': None,
            'file_type': 'pdf',
            'filename': uploaded_file.name
        }

def get_ingested_thumbnail_html(doc_id):
    """
    Get HTML for thumbnail that was extracted during ingestion.
    
    Args:
        doc_id: Document ID
        
    Returns:
        HTML img tag for the thumbnail or None if not available
    """
    cache_path = f"thumbnails/ingested_thumb_{doc_id}.png"
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'rb') as f:
                img_data = f.read()
                img_b64 = base64.b64encode(img_data).decode('utf-8')
                thumbnail_data = f"data:image/png;base64,{img_b64}"
                
            return f'<img src="{thumbnail_data}" style="width:120px;height:150px;margin-right:8px;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,0.2);" alt="Document thumbnail">'
        except:
            return None
    
    return None

def store_pdf_with_thumbnail(pdf_file_path, doc_id, title, organization="", doc_type=""):
    """
    Store PDF file with thumbnail extraction for batch ingestion.
    
    Args:
        pdf_file_path: Path to PDF file
        doc_id: Document ID
        title: Document title
        organization: Document organization
        doc_type: Document type
        
    Returns:
        Dict with processing results
    """
    try:
        # Extract thumbnail
        thumbnail_data = extract_pdf_thumbnail_from_path(pdf_file_path, doc_id)
        
        # Extract text content
        try:
            import pypdf
            
            with open(pdf_file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text_content = ""
                
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
                    
        except Exception as text_error:
            print(f"Error extracting text from PDF: {text_error}")
            text_content = f"PDF file: {os.path.basename(pdf_file_path)}"
        
        return {
            'success': True,
            'text_content': text_content.strip(),
            'thumbnail_extracted': thumbnail_data is not None,
            'thumbnail_path': f"thumbnails/ingested_thumb_{doc_id}.png" if thumbnail_data else None
        }
        
    except Exception as e:
        print(f"Error storing PDF with thumbnail: {e}")
        return {
            'success': False,
            'error': str(e),
            'thumbnail_extracted': False
        }