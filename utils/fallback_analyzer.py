"""
Fallback document analysis when OpenAI API is unavailable
Uses pattern matching and heuristics for metadata extraction
"""

import re
from typing import Dict, Optional
from datetime import datetime

def extract_metadata_fallback(content: str, source: str = "") -> Dict[str, Optional[str]]:
    """
    Extract metadata using pattern matching when AI analysis fails.
    
    Args:
        content: Document text content
        source: Source URL or filename
        
    Returns:
        Dict with extracted metadata
    """
    
    # Extract title using common patterns
    title = extract_title_fallback(content, source)
    
    # Extract document type based on content patterns
    doc_type = classify_document_type_fallback(content)
    
    # Extract organization/author info
    organization = extract_organization_fallback(content)
    
    # Extract date patterns
    pub_date = extract_date_fallback(content)
    
    # Generate content preview
    preview = generate_preview_fallback(content)
    
    return {
        'title': title,
        'author_organization': organization,
        'publish_date': pub_date,
        'document_type': doc_type,
        'content_preview': preview
    }

def extract_title_fallback(content: str, source: str) -> str:
    """Extract document title using pattern matching."""
    
    # Try common title patterns
    title_patterns = [
        r'^(.{1,100})\n',  # First line
        r'title:\s*(.+)',  # Title: format
        r'Title:\s*(.+)',  # Title: format
        r'TITLE:\s*(.+)',  # TITLE: format
        r'([A-Z][^.\n]{10,80})',  # Capitalized sentence
    ]
    
    for pattern in title_patterns:
        try:
            match = re.search(pattern, content[:500], re.IGNORECASE | re.MULTILINE)
            if match:
                title = match.group(1).strip()
                if len(title) > 10 and not title.lower().startswith('http'):
                    return title[:100]
        except IndexError:
            continue
    
    # Fallback to source-based title
    if 'pdf' in source.lower():
        return f"PDF Document from {source.split('/')[-2] if '/' in source else 'URL'}"
    elif source:
        return f"Document from {source.split('/')[-2] if '/' in source else source}"
    
    return "Untitled Document"

def classify_document_type_fallback(content: str) -> str:
    """Classify document type based on content patterns."""
    
    content_lower = content.lower()
    
    # Policy/Framework indicators
    if any(word in content_lower for word in ['policy', 'framework', 'standard', 'guideline']):
        if 'framework' in content_lower:
            return 'Framework'
        elif 'policy' in content_lower:
            return 'Policy'
        elif 'standard' in content_lower:
            return 'Standard'
        else:
            return 'Guideline'
    
    # Research/Report indicators
    if any(word in content_lower for word in ['research', 'study', 'analysis', 'findings']):
        return 'Research'
    
    # Technical/Whitepaper indicators
    if any(word in content_lower for word in ['whitepaper', 'technical', 'implementation']):
        return 'Whitepaper'
    
    # Regulation/Directive indicators
    if any(word in content_lower for word in ['regulation', 'directive', 'compliance']):
        return 'Regulation'
    
    return 'Report'

def extract_organization_fallback(content: str) -> str:
    """Extract organization/author information."""
    
    # Common organization patterns
    org_patterns = [
        r'(?:published by|by|author:|from)\s*([A-Z][^.\n]{5,50})',
        r'((?:National|Federal|Department|Ministry|Institute|Agency|Bureau|Office)[^.\n]{5,40})',
        r'([A-Z]{2,10})\s*(?:Report|Document|Publication)',
        r'©\s*\d{4}\s*([^.\n]{5,40})',
    ]
    
    for pattern in org_patterns:
        try:
            match = re.search(pattern, content[:1000], re.IGNORECASE)
            if match:
                org = match.group(1).strip()
                if len(org) > 5 and not org.isdigit():
                    return org[:50]
        except (IndexError, AttributeError):
            continue
    
    return 'Unknown'

def extract_date_fallback(content: str) -> Optional[str]:
    """Extract publication date using pattern matching."""
    
    # Date patterns
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(?:published|date|updated):\s*(\d{4}-\d{2}-\d{2})',
        r'(?:published|date|updated):\s*(\w+ \d{1,2}, \d{4})',
        r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY
        r'(\w+ \d{4})',  # Month Year
    ]
    
    for pattern in date_patterns:
        try:
            match = re.search(pattern, content[:1000], re.IGNORECASE)
            if match:
                date_str = match.group(1)
                # Try to normalize to YYYY-MM-DD format
                if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                    return date_str
                # For other formats, just return current year if we can't parse
                current_year = datetime.now().year
                if str(current_year) in date_str or str(current_year-1) in date_str:
                    return f"{current_year}-01-01"
        except (IndexError, AttributeError):
            continue
    
    return None

def generate_preview_fallback(content: str) -> str:
    """Generate a content preview without AI analysis."""
    
    # Clean and extract meaningful sentences
    sentences = re.split(r'[.!?]\s+', content[:1000])
    
    # Filter out very short or non-meaningful sentences
    meaningful_sentences = []
    for sentence in sentences[:5]:
        sentence = sentence.strip()
        if (len(sentence) > 20 and 
            not sentence.lower().startswith('http') and
            not sentence.isdigit() and
            len(sentence.split()) > 3):
            meaningful_sentences.append(sentence)
    
    if meaningful_sentences:
        preview = '. '.join(meaningful_sentences[:2])
        return preview[:300] + "..." if len(preview) > 300 else preview
    
    # Fallback to first paragraph
    paragraphs = content.split('\n\n')
    for para in paragraphs[:3]:
        para = para.strip()
        if len(para) > 50:
            return para[:300] + "..." if len(para) > 300 else para
    
    return "Document analysis available without detailed preview."