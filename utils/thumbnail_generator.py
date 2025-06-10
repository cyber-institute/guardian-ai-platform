"""
Document Thumbnail Generator
Creates actual thumbnails from PDF files and other documents
"""

import base64
from io import BytesIO
import re
import os
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import tempfile

def generate_pdf_thumbnail(file_path, doc_id):
    """
    Generate actual thumbnail from PDF file.
    
    Args:
        file_path: Path to the PDF file
        doc_id: Document ID for caching
        
    Returns:
        Base64 encoded thumbnail image or None if failed
    """
    try:
        # Check if thumbnail already exists in cache
        thumbnail_cache_path = f"thumbnails/thumb_{doc_id}.png"
        
        if os.path.exists(thumbnail_cache_path):
            with open(thumbnail_cache_path, 'rb') as f:
                img_data = f.read()
                return image_to_base64(img_data)
        
        # Create thumbnails directory if it doesn't exist
        os.makedirs("thumbnails", exist_ok=True)
        
        # Convert first page of PDF to image
        if os.path.exists(file_path):
            pages = convert_from_path(file_path, first_page=1, last_page=1, dpi=150)
        else:
            return None
            
        if not pages:
            return None
            
        # Get first page
        page = pages[0]
        
        # Resize to thumbnail size (120x150 - 3x the original 40x50)
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
        thumbnail.save(thumbnail_cache_path, 'PNG', optimize=True)
        
        # Convert to base64
        buffer = BytesIO()
        thumbnail.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        
        return image_to_base64(img_data)
        
    except Exception as e:
        print(f"Error generating PDF thumbnail: {e}")
        return None

def generate_pdf_thumbnail_from_bytes(pdf_bytes, doc_id):
    """
    Generate thumbnail from PDF bytes data.
    
    Args:
        pdf_bytes: PDF file as bytes
        doc_id: Document ID for caching
        
    Returns:
        Base64 encoded thumbnail image or None if failed
    """
    try:
        # Check if thumbnail already exists in cache
        thumbnail_cache_path = f"thumbnails/thumb_{doc_id}.png"
        
        if os.path.exists(thumbnail_cache_path):
            with open(thumbnail_cache_path, 'rb') as f:
                img_data = f.read()
                return image_to_base64(img_data)
        
        # Create thumbnails directory if it doesn't exist
        os.makedirs("thumbnails", exist_ok=True)
        
        # Convert first page of PDF to image
        pages = convert_from_bytes(pdf_bytes, first_page=1, last_page=1, dpi=150)
            
        if not pages:
            return None
            
        # Get first page
        page = pages[0]
        
        # Resize to thumbnail size (120x150 - 3x the original 40x50)
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
        thumbnail.save(thumbnail_cache_path, 'PNG', optimize=True)
        
        # Convert to base64
        buffer = BytesIO()
        thumbnail.save(buffer, format='PNG')
        img_data = buffer.getvalue()
        
        return image_to_base64(img_data)
        
    except Exception as e:
        print(f"Error generating PDF thumbnail from bytes: {e}")
        return None

def image_to_base64(img_data):
    """Convert image bytes to base64 data URL"""
    img_b64 = base64.b64encode(img_data).decode('utf-8')
    return f"data:image/png;base64,{img_b64}"

def is_nist_document(org, title):
    """Check if document is from NIST"""
    indicators = ['nist', 'national institute of standards', 'ai rmf', 'ai 100-1']
    org_lower = org.lower() if org else ''
    title_lower = title.lower() if title else ''
    return any(indicator in org_lower or indicator in title_lower for indicator in indicators)

def is_eu_document(org, title):
    """Check if document is from EU"""
    indicators = ['european', 'eu', 'regulation (eu)', 'eur-lex', 'europa.eu']
    org_lower = org.lower() if org else ''
    title_lower = title.lower() if title else ''
    return any(indicator in org_lower or indicator in title_lower for indicator in indicators)

def is_nasa_document(org, title):
    """Check if document is from NASA"""
    indicators = ['nasa', 'ntrs.nasa.gov', 'national aeronautics']
    org_lower = org.lower() if org else ''
    title_lower = title.lower() if title else ''
    return any(indicator in org_lower or indicator in title_lower for indicator in indicators)

def is_academic_document(org, title):
    """Check if document is academic"""
    indicators = ['university', 'college', 'institute', 'arxiv', 'ieee', 'acm']
    org_lower = org.lower() if org else ''
    return any(indicator in org_lower for indicator in indicators)

def is_government_document(org, title):
    """Check if document is government"""
    indicators = ['department', 'agency', 'federal', 'government', '.gov']
    org_lower = org.lower() if org else ''
    return any(indicator in org_lower for indicator in indicators)

def create_nist_thumbnail(title, doc_type):
    """Create NIST-styled thumbnail"""
    # Extract document number if present
    doc_number = extract_nist_number(title)
    
    svg = f"""
    <svg width="80" height="100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="nistGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#1e3a8a;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="80" height="100" fill="url(#nistGrad)" rx="4"/>
        <rect x="8" y="8" width="64" height="84" fill="white" rx="2"/>
        <text x="40" y="25" text-anchor="middle" font-family="Arial" font-size="8" font-weight="bold" fill="#1e3a8a">NIST</text>
        <text x="40" y="40" text-anchor="middle" font-family="Arial" font-size="6" fill="#374151">{doc_number}</text>
        <text x="40" y="55" text-anchor="middle" font-family="Arial" font-size="5" fill="#6b7280">AI Framework</text>
        <circle cx="40" cy="70" r="8" fill="#dbeafe"/>
        <text x="40" y="74" text-anchor="middle" font-family="Arial" font-size="8" fill="#1e3a8a">AI</text>
        <text x="40" y="88" text-anchor="middle" font-family="Arial" font-size="4" fill="#9ca3af">{doc_type}</text>
    </svg>
    """
    return svg_to_base64(svg)

def create_eu_thumbnail(title, doc_type):
    """Create EU-styled thumbnail"""
    svg = f"""
    <svg width="80" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="80" height="100" fill="#003399" rx="4"/>
        <rect x="8" y="8" width="64" height="84" fill="white" rx="2"/>
        <rect x="12" y="12" width="56" height="16" fill="#003399" rx="1"/>
        <text x="40" y="22" text-anchor="middle" font-family="Arial" font-size="6" font-weight="bold" fill="white">EU</text>
        <circle cx="20" cy="40" r="2" fill="#ffcc00"/>
        <circle cx="28" cy="38" r="2" fill="#ffcc00"/>
        <circle cx="36" cy="38" r="2" fill="#ffcc00"/>
        <circle cx="44" cy="38" r="2" fill="#ffcc00"/>
        <circle cx="52" cy="40" r="2" fill="#ffcc00"/>
        <circle cx="60" cy="45" r="2" fill="#ffcc00"/>
        <circle cx="60" cy="55" r="2" fill="#ffcc00"/>
        <circle cx="52" cy="60" r="2" fill="#ffcc00"/>
        <circle cx="44" cy="62" r="2" fill="#ffcc00"/>
        <circle cx="36" cy="62" r="2" fill="#ffcc00"/>
        <circle cx="28" cy="62" r="2" fill="#ffcc00"/>
        <circle cx="20" cy="60" r="2" fill="#ffcc00"/>
        <text x="40" y="78" text-anchor="middle" font-family="Arial" font-size="5" fill="#003399">Regulation</text>
        <text x="40" y="88" text-anchor="middle" font-family="Arial" font-size="4" fill="#666">{doc_type}</text>
    </svg>
    """
    return svg_to_base64(svg)

def create_nasa_thumbnail(title, doc_type):
    """Create NASA-styled thumbnail"""
    svg = f"""
    <svg width="80" height="100" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="nasaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#1e293b;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="80" height="100" fill="url(#nasaGrad)" rx="4"/>
        <rect x="8" y="8" width="64" height="84" fill="white" rx="2"/>
        <ellipse cx="40" cy="30" rx="15" ry="8" fill="#dc2626"/>
        <text x="40" y="34" text-anchor="middle" font-family="Arial" font-size="7" font-weight="bold" fill="white">NASA</text>
        <circle cx="40" cy="55" r="12" fill="#f3f4f6" stroke="#374151" stroke-width="1"/>
        <path d="M 35 50 Q 40 45 45 50 Q 40 60 35 50" fill="#3b82f6"/>
        <circle cx="42" cy="52" r="2" fill="#fbbf24"/>
        <text x="40" y="75" text-anchor="middle" font-family="Arial" font-size="5" fill="#374151">Technical</text>
        <text x="40" y="85" text-anchor="middle" font-family="Arial" font-size="5" fill="#374151">Report</text>
        <text x="40" y="95" text-anchor="middle" font-family="Arial" font-size="4" fill="#9ca3af">{doc_type}</text>
    </svg>
    """
    return svg_to_base64(svg)

def create_academic_thumbnail(title, doc_type):
    """Create academic-styled thumbnail"""
    svg = f"""
    <svg width="80" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="80" height="100" fill="#059669" rx="4"/>
        <rect x="8" y="8" width="64" height="84" fill="white" rx="2"/>
        <polygon points="25,20 40,15 55,20 55,35 40,30 25,35" fill="#059669"/>
        <text x="40" y="50" text-anchor="middle" font-family="Arial" font-size="6" font-weight="bold" fill="#059669">ACADEMIC</text>
        <text x="40" y="65" text-anchor="middle" font-family="Arial" font-size="5" fill="#374151">Research</text>
        <text x="40" y="80" text-anchor="middle" font-family="Arial" font-size="4" fill="#6b7280">{doc_type}</text>
    </svg>
    """
    return svg_to_base64(svg)

def create_government_thumbnail(title, doc_type):
    """Create government-styled thumbnail"""
    svg = f"""
    <svg width="80" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="80" height="100" fill="#7c2d12" rx="4"/>
        <rect x="8" y="8" width="64" height="84" fill="white" rx="2"/>
        <rect x="35" y="15" width="10" height="25" fill="#7c2d12"/>
        <rect x="20" y="25" width="8" height="15" fill="#7c2d12"/>
        <rect x="52" y="25" width="8" height="15" fill="#7c2d12"/>
        <rect x="15" y="40" width="50" height="3" fill="#7c2d12"/>
        <text x="40" y="55" text-anchor="middle" font-family="Arial" font-size="5" font-weight="bold" fill="#7c2d12">GOVERNMENT</text>
        <text x="40" y="70" text-anchor="middle" font-family="Arial" font-size="5" fill="#374151">Official</text>
        <text x="40" y="85" text-anchor="middle" font-family="Arial" font-size="4" fill="#6b7280">{doc_type}</text>
    </svg>
    """
    return svg_to_base64(svg)

def create_generic_thumbnail(title, doc_type):
    """Create generic document thumbnail"""
    svg = f"""
    <svg width="80" height="100" xmlns="http://www.w3.org/2000/svg">
        <rect width="80" height="100" fill="#6b7280" rx="4"/>
        <rect x="8" y="8" width="64" height="84" fill="white" rx="2"/>
        <rect x="15" y="20" width="50" height="2" fill="#d1d5db"/>
        <rect x="15" y="30" width="45" height="2" fill="#d1d5db"/>
        <rect x="15" y="40" width="40" height="2" fill="#d1d5db"/>
        <rect x="15" y="50" width="35" height="2" fill="#d1d5db"/>
        <text x="40" y="70" text-anchor="middle" font-family="Arial" font-size="5" fill="#374151">Document</text>
        <text x="40" y="85" text-anchor="middle" font-family="Arial" font-size="4" fill="#6b7280">{doc_type}</text>
    </svg>
    """
    return svg_to_base64(svg)

def extract_nist_number(title):
    """Extract NIST document number from title"""
    if not title:
        return "AI 100-1"
    
    # Look for patterns like "AI 100-1", "NIST AI 100-1", etc.
    patterns = [
        r'AI\s*(\d+(?:-\d+)?)',
        r'NIST\s*AI\s*(\d+(?:-\d+)?)',
        r'(\d+(?:-\d+))'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            return f"AI {match.group(1)}"
    
    return "AI DOC"

def svg_to_base64(svg_content):
    """Convert SVG content to base64 data URL"""
    svg_bytes = svg_content.encode('utf-8')
    svg_b64 = base64.b64encode(svg_bytes).decode('utf-8')
    return f"data:image/svg+xml;base64,{svg_b64}"

def get_thumbnail_html(doc_title, doc_type, organization, doc_id=None, file_path=None):
    """Get HTML img tag for document thumbnail"""
    thumbnail_data = None
    
    # Try to find PDF file in attached_assets directory
    pdf_path = find_pdf_in_assets(doc_title, organization)
    
    # Try to generate real PDF thumbnail first
    if pdf_path:
        thumbnail_data = generate_pdf_thumbnail(pdf_path, doc_id or hash(doc_title))
    elif doc_id and file_path:
        thumbnail_data = generate_pdf_thumbnail(file_path, doc_id)
    
    # Fallback to SVG if PDF thumbnail fails
    if not thumbnail_data:
        thumbnail_data = generate_thumbnail_svg(doc_title, doc_type, organization)
    
    # 3x size: 120x150 instead of 40x50
    return f'<img src="{thumbnail_data}" style="width:120px;height:150px;margin-right:8px;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,0.2);" alt="Document thumbnail">'

def find_pdf_in_assets(doc_title, organization):
    """Find corresponding PDF file in attached_assets directory"""
    assets_dir = "attached_assets"
    
    if not os.path.exists(assets_dir):
        return None
        
    # Get all PDF files in the directory
    pdf_files = [f for f in os.listdir(assets_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        return None
    
    # Clean and prepare matching strings
    title_lower = doc_title.lower() if doc_title else ""
    org_lower = organization.lower() if organization else ""
    
    # Remove debug prints for production
    # print(f"Debug: Looking for PDF match - Title: '{title_lower}', Org: '{org_lower}'")
    # print(f"Debug: Available PDFs: {pdf_files}")
    
    for pdf_file in pdf_files:
        pdf_lower = pdf_file.lower()
        
        # Check for NIST documents with broader matching
        if ('nist' in org_lower or 'nist' in title_lower or 'ai risk management framework' in title_lower or 'national institute of standards' in title_lower) and 'nist' in pdf_lower:
            return os.path.join(assets_dir, pdf_file)
            
        # Check for EU documents with broader matching  
        if ('european' in org_lower or 'europa.eu' in org_lower or 'eur-lex' in org_lower or 'regulation (eu)' in title_lower or 'webpage from eur-lex.europa.eu' in title_lower) and ('eu' in pdf_lower or 'europa' in pdf_lower):
            return os.path.join(assets_dir, pdf_file)
            
        # Check for NASA documents with broader matching
        if ('nasa' in org_lower or 'ntrs.nasa.gov' in org_lower or 'pdf document from ntrs.nasa.gov' in title_lower) and 'nasa' in pdf_lower:
            return os.path.join(assets_dir, pdf_file)
            
        # Check for AI-related documents
        if 'ai' in title_lower and 'ai' in pdf_lower:
            return os.path.join(assets_dir, pdf_file)
            
        # Check for direct filename matches (remove common suffixes)
        title_clean = re.sub(r'[^\w\s]', '', title_lower).strip()
        if title_clean and any(word in pdf_lower for word in title_clean.split() if len(word) > 3):
            return os.path.join(assets_dir, pdf_file)
    
    # Enhanced fallback matching - match any available PDF for web-scraped documents
    if any(indicator in title_lower for indicator in ['webpage from', 'pdf document from', 'document from']):
        # For web-scraped documents, try to match by domain first, then use first available
        if 'eur-lex.europa.eu' in title_lower:
            # Look for EU-related PDFs
            for pdf_file in pdf_files:
                if any(eu_indicator in pdf_file.lower() for eu_indicator in ['eu', 'europa', 'regulation']):
                    return os.path.join(assets_dir, pdf_file)
        elif 'ntrs.nasa.gov' in title_lower:
            # Look for NASA-related PDFs
            for pdf_file in pdf_files:
                if 'nasa' in pdf_file.lower():
                    return os.path.join(assets_dir, pdf_file)
        
        # If no domain-specific match, use the first available PDF
        if pdf_files:
            return os.path.join(assets_dir, pdf_files[0])
    
    # If no specific match found, try to find any PDF that might be related
    # by checking if the title contains document-like keywords
    for pdf_file in pdf_files:
        # Return the first available PDF for documents that seem policy-related
        if any(keyword in title_lower for keyword in ['policy', 'framework', 'guideline', 'standard', 'regulation']):
            return os.path.join(assets_dir, pdf_file)
    return None

def get_real_pdf_thumbnail(doc_id, file_path=None, pdf_bytes=None):
    """Get real PDF thumbnail with fallback"""
    if file_path:
        return generate_pdf_thumbnail(file_path, doc_id)
    elif pdf_bytes:
        return generate_pdf_thumbnail_from_bytes(pdf_bytes, doc_id)
    return None

def generate_thumbnail_svg(doc_title, doc_type, organization):
    """
    Generate SVG thumbnail based on document metadata (fallback only).
    """
    
    # Determine thumbnail style based on organization and type
    if is_nist_document(organization, doc_title):
        return create_nist_thumbnail(doc_title, doc_type)
    elif is_eu_document(organization, doc_title):
        return create_eu_thumbnail(doc_title, doc_type)
    elif is_nasa_document(organization, doc_title):
        return create_nasa_thumbnail(doc_title, doc_type)
    elif is_academic_document(organization, doc_title):
        return create_academic_thumbnail(doc_title, doc_type)
    elif is_government_document(organization, doc_title):
        return create_government_thumbnail(doc_title, doc_type)
    else:
        return create_generic_thumbnail(doc_title, doc_type)