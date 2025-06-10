"""
Document Thumbnail Generator
Creates visual thumbnails for different document types and organizations
"""

import base64
from io import BytesIO
import re

def generate_thumbnail_svg(doc_title, doc_type, organization):
    """
    Generate SVG thumbnail based on document metadata.
    
    Args:
        doc_title: Document title
        doc_type: Type of document (e.g., 'Standard', 'Guideline', 'Report')
        organization: Source organization
        
    Returns:
        Base64 encoded SVG thumbnail
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

def get_thumbnail_html(doc_title, doc_type, organization):
    """Get HTML img tag for document thumbnail"""
    thumbnail_data = generate_thumbnail_svg(doc_title, doc_type, organization)
    return f'<img src="{thumbnail_data}" style="width:40px;height:50px;margin-right:8px;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,0.2);" alt="Document thumbnail">'