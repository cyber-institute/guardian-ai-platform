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
    
    # Enhanced title patterns for government and AI content
    title_patterns = [
        # Joint guidance and multi-line titles - capture full title
        r'JOINT GUIDANCE\s*\n\s*(DEPLOYING AI SYSTEMS SECURELY:\s*(?:\n[^.\n]+)*?)(?:\n\n|\nDeploying|\nThe)',
        r'(DEPLOYING AI SYSTEMS SECURELY:\s*Best Security Practices[^.\n]*(?:\n[^.\n]*)*?)(?:\n\n|\nDeploying|\nThe)',
        r'(Best Security Practices\s*For Deploying[^.\n]*(?:\n[^.\n]*)*?)(?:\n\n|\nDeploying|\nThe)',
        
        # Specific AI/Cybersecurity title patterns - prioritize these
        r'(Artificial Intelligence\s+Cybersecurity\s+Guidelines?)',
        r'(AI\s+Systems?\s+Security)',
        r'(Deploying\s+AI\s+Systems?\s+Securely)',
        r'(AI\s+(?:Cybersecurity|Security)\s+(?:Framework|Guidelines?|Guidance))',
        r'(Artificial Intelligence\s+(?:Security|Cybersecurity)\s+(?:Framework|Guidelines?|Guidance))',
        r'(Cybersecurity\s+for\s+(?:AI|Artificial Intelligence))',
        r'(Machine Learning\s+Security\s+(?:Framework|Guidelines?|Guidance))',
        
        # HTML title and heading tags
        r'<title[^>]*>([^<]+)</title>',  # HTML title tag
        r'<h1[^>]*>([^<]+)</h1>',  # H1 tag
        r'<h2[^>]*>([^<]+)</h2>',  # H2 tag
        
        # Multi-line title patterns for government documents
        r'([A-Z][A-Z\s]{10,}:\s*[^.\n]+(?:\n[^.\n]+)*?)(?:\n\n|\nThe|\n[A-Z][a-z])',
        
        # Government agency documents
        r'((?:CISA|NIST|NSA)\s+[^.\n]{10,60})',
        
        # Standalone meaningful titles (not part of lists or descriptions)
        r'^\s*([A-Z][^.\n]{15,80})\s*$',  # Single line titles
        r'title:\s*(.+)',  # Title: format
        r'Title:\s*(.+)',  # Title: format
        r'TITLE:\s*(.+)',  # TITLE: format
        
        # Content-based title extraction with proper boundaries
        r'([A-Z][^.\n]{15,60}(?:Guidelines?|Framework|Strategy|Policy|Report|Practices|Guidance))',
    ]
    
    for pattern in title_patterns:
        try:
            match = re.search(pattern, content[:1000], re.IGNORECASE | re.MULTILINE)
            if match:
                title = match.group(1).strip()
                # Clean up HTML entities and extra whitespace
                title = re.sub(r'<[^>]+>', '', title)  # Remove HTML tags
                title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
                title = title.replace('&nbsp;', ' ').replace('&amp;', '&')
                
                if (len(title) > 10 and 
                    not title.lower().startswith('http') and
                    not title.lower().startswith('skip to') and
                    not title.lower().startswith('search') and
                    not title.lower().startswith('webpage') and
                    not title.lower().startswith('document from') and
                    not title.lower().startswith('pdf from') and
                    not title.isdigit()):
                    return title[:100]
        except (IndexError, AttributeError):
            continue
    
    # Content-based intelligent fallback - extract meaningful titles from content
    content_words = content.lower()
    
    # Look for key phrases that could form meaningful titles
    key_phrases = []
    
    if 'ai' in content_words and ('security' in content_words or 'cybersecurity' in content_words):
        if 'deployment' in content_words or 'deploying' in content_words:
            key_phrases.append("AI System Deployment Security")
        elif 'framework' in content_words:
            key_phrases.append("AI Cybersecurity Framework")
        elif 'guidance' in content_words or 'guideline' in content_words:
            key_phrases.append("AI Security Guidance")
        else:
            key_phrases.append("AI Cybersecurity")
    
    if 'quantum' in content_words and 'security' in content_words:
        key_phrases.append("Quantum Security")
    
    if 'machine learning' in content_words and 'security' in content_words:
        key_phrases.append("Machine Learning Security")
    
    # Try to find the first meaningful sentence or heading
    sentences = content[:500].split('\n')
    for sentence in sentences:
        sentence = sentence.strip()
        if (len(sentence) > 15 and len(sentence) < 80 and 
            not sentence.lower().startswith('skip') and
            not sentence.lower().startswith('search') and
            not sentence.lower().startswith('menu') and
            any(word in sentence.lower() for word in ['security', 'cybersecurity', 'ai', 'artificial', 'framework', 'guidance', 'policy'])):
            return sentence
    
    # Use key phrases if found
    if key_phrases:
        base_title = key_phrases[0]
        # Add source context if helpful
        if 'cisa.gov' in source.lower():
            return f"CISA {base_title}"
        elif 'nist.gov' in source.lower():
            return f"NIST {base_title}"
        else:
            return base_title
    
    # Final fallback based on source context
    if 'cisa.gov' in source.lower():
        return "CISA Cybersecurity Document"
    elif 'nist.gov' in source.lower():
        return "NIST Security Document" 
    
    return "Cybersecurity Document"

def classify_document_type_fallback(content: str) -> str:
    """Classify document type based on content patterns."""
    
    content_lower = content.lower()
    
    # AI/Cybersecurity specific classifications
    if any(word in content_lower for word in ['ai cybersecurity', 'artificial intelligence security', 'machine learning security']):
        if 'framework' in content_lower or 'guideline' in content_lower:
            return 'Framework'
        elif 'policy' in content_lower:
            return 'Policy'
        else:
            return 'Guideline'
    
    # Government document indicators
    if any(word in content_lower for word in ['cisa', 'nist', 'federal', 'government']):
        if 'framework' in content_lower:
            return 'Framework'
        elif 'guideline' in content_lower or 'guidance' in content_lower:
            return 'Guideline'
        elif 'standard' in content_lower:
            return 'Standard'
        else:
            return 'Policy'
    
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
    
    # Enhanced organization patterns for government documents
    org_patterns = [
        # Multi-agency collaboration patterns
        r'(National Security Agency[^.\n]*(?:CISA|Cybersecurity)[^.\n]*)',
        r'(NSA[^.\n]*(?:CISA|along with)[^.\n]*)',
        r'(CISA[^.\n]*(?:NSA|National Security)[^.\n]*)',
        
        # Specific agency patterns
        r'(National Security Agency\'s?\s+[A-Z][^.\n]{0,30})',
        r'(Cybersecurity and Infrastructure Security Agency)',
        r'(National Institute of Standards and Technology)',
        r'(CISA|NSA|NIST|DHS)',
        
        # General patterns
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
    
    # Enhanced date patterns for government documents
    date_patterns = [
        # Standard formats
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(?:published|date|updated|issued):\s*(\d{4}-\d{2}-\d{2})',
        r'(?:published|date|updated|issued):\s*(\w+ \d{1,2}, \d{4})',
        r'(?:published|date|updated|issued):\s*(\d{1,2}/\d{1,2}/\d{4})',
        
        # Government document patterns
        r'(?:published|issued):\s*(\w+ \d{4})',  # "Published: April 2024"
        r'(?:published|issued)\s+(\w+ \d{4})',  # "Published March 2024"
        r'(\w+ \d{1,2}, \d{4})',  # "March 15, 2024"
        r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY
        r'(\d{4})',  # Just year - common in government docs
        
        # Version and revision dates
        r'(?:version|revision|updated)\s+(\w+ \d{4})',
        r'(?:v\d+\.\d+\s+)?(\w+ \d{4})',  # "v1.0 March 2024"
        
        # Copyright and footer dates
        r'©\s*(\d{4})',
        r'copyright\s+(\d{4})',
    ]
    
    for pattern in date_patterns:
        try:
            match = re.search(pattern, content[:2000], re.IGNORECASE)
            if match:
                date_str = match.group(1)
                
                # Try to normalize to YYYY-MM-DD format
                if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                    return date_str
                
                # Handle month/year formats
                month_year_pattern = r'(\w+)\s+(\d{4})'
                month_match = re.match(month_year_pattern, date_str)
                if month_match:
                    month_name, year = month_match.groups()
                    month_map = {
                        'january': '01', 'february': '02', 'march': '03', 'april': '04',
                        'may': '05', 'june': '06', 'july': '07', 'august': '08',
                        'september': '09', 'october': '10', 'november': '11', 'december': '12',
                        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                        'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09',
                        'oct': '10', 'nov': '11', 'dec': '12'
                    }
                    month_num = month_map.get(month_name.lower())
                    if month_num:
                        return f"{year}-{month_num}-01"
                
                # Handle MM/DD/YYYY format
                if re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str):
                    parts = date_str.split('/')
                    if len(parts) == 3:
                        month, day, year = parts
                        return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                
                # Handle full date formats like "March 15, 2024"
                full_date_pattern = r'(\w+)\s+(\d{1,2}),\s+(\d{4})'
                full_match = re.match(full_date_pattern, date_str)
                if full_match:
                    month_name, day, year = full_match.groups()
                    month_map = {
                        'january': '01', 'february': '02', 'march': '03', 'april': '04',
                        'may': '05', 'june': '06', 'july': '07', 'august': '08',
                        'september': '09', 'october': '10', 'november': '11', 'december': '12'
                    }
                    month_num = month_map.get(month_name.lower())
                    if month_num:
                        return f"{year}-{month_num}-{day.zfill(2)}"
                
                # Just year - check if it's recent
                if re.match(r'\d{4}', date_str):
                    year = int(date_str)
                    current_year = datetime.now().year
                    if 2020 <= year <= current_year:
                        return f"{year}-01-01"
                        
        except (IndexError, AttributeError, ValueError):
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