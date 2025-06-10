"""
Intelligent Document Metadata Extraction System
Uses pattern matching and heuristics to extract document metadata without external APIs
"""

import re
from datetime import datetime
from typing import Dict, Optional, List, Tuple

def extract_document_metadata(content: str, filename: str = "") -> Dict[str, Optional[str]]:
    """
    Extract comprehensive metadata from document content using intelligent pattern matching.
    
    Args:
        content: Full document text content
        filename: Original filename for context
        
    Returns:
        Dict with extracted metadata: title, author_organization, publish_date, document_type, content_preview
    """
    if not content or len(content.strip()) < 50:
        return {
            'title': filename or 'Untitled Document',
            'author_organization': 'Unknown',
            'publish_date': None,
            'document_type': 'Unknown',
            'content_preview': 'Insufficient content for analysis'
        }
    
    # Clean content for analysis
    content_clean = re.sub(r'\s+', ' ', content).strip()
    
    return {
        'title': extract_title(content_clean, filename),
        'author_organization': extract_organization(content_clean),
        'publish_date': extract_date(content_clean),
        'document_type': classify_document_type(content_clean, filename),
        'content_preview': generate_content_preview(content_clean)
    }

def extract_title(content: str, filename: str = "") -> str:
    """Extract document title using pattern matching."""
    
    # Priority 1: Look for explicit title patterns
    title_patterns = [
        r'(?i)title:\s*(.+?)(?:\n|$)',
        r'(?i)document title:\s*(.+?)(?:\n|$)',
        r'(?i)^(.+?)\s*\n\s*(?:abstract|executive summary|introduction)',
        r'(?i)^([A-Z][^.\n]{10,100})\s*\n',  # First line if title-like
        r'(?i)<title[^>]*>([^<]+)</title>',
        r'(?i)^# (.+?)$',  # Markdown heading
        r'(?i)^(.{10,100}?)\s*(?:\n\s*-{3,}|\n\s*={3,})',  # Underlined titles
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, content[:2000], re.MULTILINE)
        if match:
            title = match.group(1).strip()
            if is_valid_title(title):
                return clean_title(title)
    
    # Priority 2: Government/Policy document patterns
    gov_patterns = [
        r'(?i)(NIST\s+(?:SP|Special Publication)\s+[\d-]+[^.\n]*)',
        r'(?i)(Executive Order\s+\d+[^.\n]*)',
        r'(?i)(Public Law\s+\d+[^.\n]*)',
        r'(?i)(Federal Register[^.\n]*)',
        r'(?i)(Presidential\s+(?:Directive|Memorandum)[^.\n]*)',
    ]
    
    for pattern in gov_patterns:
        match = re.search(pattern, content[:1000])
        if match:
            return clean_title(match.group(1))
    
    # Priority 3: Extract from first meaningful sentence
    sentences = re.split(r'[.!?]\s+', content[:1000])
    for sentence in sentences[:3]:
        if len(sentence.strip()) > 20 and len(sentence.strip()) < 200:
            if not re.search(r'(?i)(page|section|chapter|figure|\d+)', sentence):
                return clean_title(sentence.strip())
    
    # Fallback to cleaned filename
    if filename:
        return clean_title(filename.replace('_', ' ').replace('-', ' '))
    
    return 'Untitled Document'

def extract_organization(content: str) -> str:
    """Extract author organization using pattern matching."""
    
    # Government agencies and organizations
    org_patterns = [
        r'(?i)\b(National Institute of Standards and Technology|NIST)\b',
        r'(?i)\b(National Security Agency|NSA)\b',
        r'(?i)\b(Department of Defense|DoD|DOD)\b',
        r'(?i)\b(Department of Homeland Security|DHS)\b',
        r'(?i)\b(Cybersecurity and Infrastructure Security Agency|CISA)\b',
        r'(?i)\b(National Aeronautics and Space Administration|NASA)\b',
        r'(?i)\b(Federal Bureau of Investigation|FBI)\b',
        r'(?i)\b(Central Intelligence Agency|CIA)\b',
        r'(?i)\b(White House|Executive Office)\b',
        r'(?i)\b(European Union|EU|European Commission)\b',
        r'(?i)\b(International Organization for Standardization|ISO)\b',
        r'(?i)\b(Institute of Electrical and Electronics Engineers|IEEE)\b',
        r'(?i)\b(Internet Engineering Task Force|IETF)\b',
        r'(?i)\b(World Wide Web Consortium|W3C)\b',
        r'(?i)\b(MITRE Corporation|MITRE)\b',
        r'(?i)\b(RAND Corporation|RAND)\b',
        r'(?i)\b(Carnegie Mellon University|CMU)\b',
        r'(?i)\b(Massachusetts Institute of Technology|MIT)\b',
        r'(?i)\b(Stanford University)\b',
        r'(?i)\b(University of [A-Z][a-z]+)\b',
    ]
    
    # Check first 2000 characters for organization mentions
    search_text = content[:2000]
    
    for pattern in org_patterns:
        match = re.search(pattern, search_text)
        if match:
            org = match.group(1)
            # Standardize common abbreviations
            if 'NIST' in org.upper() or 'National Institute of Standards' in org:
                return 'NIST'
            elif 'NSA' in org.upper() or 'National Security Agency' in org:
                return 'NSA'
            elif 'NASA' in org.upper() or 'National Aeronautics' in org:
                return 'NASA'
            elif 'White House' in org or 'Executive Office' in org:
                return 'White House'
            elif 'European' in org:
                return 'European Union'
            elif 'DoD' in org.upper() or 'Department of Defense' in org:
                return 'Department of Defense'
            elif 'DHS' in org.upper() or 'Department of Homeland Security' in org:
                return 'DHS'
            elif 'CISA' in org.upper():
                return 'CISA'
            else:
                return org
    
    # Look for "prepared by", "published by", "author" patterns
    author_patterns = [
        r'(?i)(?:prepared|published|authored|developed)\s+by:?\s*([^.\n]{5,50})',
        r'(?i)author[s]?:?\s*([^.\n]{5,50})',
        r'(?i)organization:?\s*([^.\n]{5,50})',
    ]
    
    for pattern in author_patterns:
        match = re.search(pattern, search_text)
        if match:
            return clean_organization_name(match.group(1))
    
    return 'Unknown'

def extract_date(content: str) -> Optional[str]:
    """Extract publication date using pattern matching."""
    
    # Date patterns in order of preference
    date_patterns = [
        r'(?i)(?:published|publication date|date):?\s*([A-Za-z]+ \d{1,2},? \d{4})',
        r'(?i)(?:published|publication date|date):?\s*(\d{1,2}/\d{1,2}/\d{4})',
        r'(?i)(?:published|publication date|date):?\s*(\d{4}-\d{2}-\d{2})',
        r'(?i)(?:published|publication date|date):?\s*([A-Za-z]+ \d{4})',
        r'(?i)(?:revision|version):?\s*([A-Za-z]+ \d{4})',
        r'\b(\d{4}-\d{2}-\d{2})\b',  # ISO date format
        r'\b([A-Za-z]+ \d{1,2}, \d{4})\b',  # Month day, year
        r'\b([A-Za-z]+ \d{4})\b',  # Month year
    ]
    
    search_text = content[:1500]  # Focus on document header
    
    for pattern in date_patterns:
        matches = re.findall(pattern, search_text)
        for match in matches:
            normalized_date = normalize_date(match)
            if normalized_date:
                return normalized_date
    
    return None

def classify_document_type(content: str, filename: str = "") -> str:
    """Classify document type based on content analysis."""
    
    content_lower = content.lower()
    filename_lower = filename.lower() if filename else ""
    
    # Check for explicit document type declarations
    type_patterns = {
        'Policy': [r'(?i)\bpolicy\b', r'(?i)\bexecutive order\b', r'(?i)\bdirective\b'],
        'Standard': [r'(?i)\bstandard\b', r'(?i)\bspecification\b', r'(?i)\bnist sp\b', r'(?i)\biso \d+\b'],
        'Strategy': [r'(?i)\bstrategy\b', r'(?i)\bstrategic plan\b', r'(?i)\broadmap\b'],
        'Framework': [r'(?i)\bframework\b', r'(?i)\bmethodology\b', r'(?i)\bapproach\b'],
        'Guideline': [r'(?i)\bguideline\b', r'(?i)\bguidance\b', r'(?i)\brecommendation\b'],
        'Report': [r'(?i)\breport\b', r'(?i)\bassessment\b', r'(?i)\banalysis\b'],
        'Research': [r'(?i)\bresearch\b', r'(?i)\bpaper\b', r'(?i)\bstudy\b', r'(?i)\babstract\b'],
        'Whitepaper': [r'(?i)\bwhite paper\b', r'(?i)\bwhitepaper\b'],
        'Regulation': [r'(?i)\bregulation\b', r'(?i)\brule\b', r'(?i)\bfederal register\b'],
        'Directive': [r'(?i)\bdirective\b', r'(?i)\bmemorandum\b', r'(?i)\border\b']
    }
    
    # Score each type based on pattern matches
    type_scores = {}
    for doc_type, patterns in type_patterns.items():
        score = 0
        for pattern in patterns:
            # Higher weight for title/filename matches
            if re.search(pattern, filename_lower):
                score += 5
            # Content matches
            matches = len(re.findall(pattern, content_lower[:2000]))
            score += matches
        type_scores[doc_type] = score
    
    # Return the highest scoring type
    if type_scores:
        best_type = max(type_scores.keys(), key=lambda x: type_scores[x])
        if type_scores[best_type] > 0:
            return best_type
    
    return 'Unknown'

def generate_content_preview(content: str) -> str:
    """Generate intelligent content preview."""
    
    # Remove common document headers and footers
    content = re.sub(r'(?i)^.*?(?:table of contents|abstract|executive summary)', '', content, flags=re.DOTALL)
    content = re.sub(r'(?i)(?:page \d+|draft|confidential|proprietary).*$', '', content, flags=re.MULTILINE)
    
    # Find the most substantive paragraph
    paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 100]
    
    if not paragraphs:
        # Fallback to sentences
        sentences = re.split(r'[.!?]\s+', content)
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 50 and len(s.strip()) < 300]
        if meaningful_sentences:
            return ' '.join(meaningful_sentences[:2]) + '.'
        return content[:200] + '...' if len(content) > 200 else content
    
    # Select best paragraph (avoid lists, headers, etc.)
    best_paragraph = None
    for para in paragraphs[:5]:  # Check first 5 paragraphs
        if not re.search(r'^[•\-\*]|^\d+\.|\s{4,}', para):  # Not a list item
            if not re.search(r'(?i)^(figure|table|appendix|section)', para):  # Not a header
                best_paragraph = para
                break
    
    if not best_paragraph:
        best_paragraph = paragraphs[0]
    
    # Truncate to reasonable length
    if len(best_paragraph) > 300:
        sentences = re.split(r'[.!?]\s+', best_paragraph)
        preview = sentences[0]
        for sentence in sentences[1:]:
            if len(preview + ' ' + sentence) <= 300:
                preview += ' ' + sentence
            else:
                break
        return preview + '.'
    
    return best_paragraph

def is_valid_title(text: str) -> bool:
    """Check if extracted text is a valid title."""
    if len(text) < 5 or len(text) > 200:
        return False
    if re.search(r'^\d+$|^page \d+|^section|^chapter|^figure', text.lower()):
        return False
    if text.count('\n') > 2:
        return False
    return True

def clean_title(text: str) -> str:
    """Clean and format extracted title."""
    # Remove file extensions
    text = re.sub(r'\.(pdf|doc|docx|txt)$', '', text, flags=re.IGNORECASE)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove leading/trailing punctuation
    text = text.strip('.,;:!?-_')
    # Capitalize appropriately
    if text.isupper() and len(text) > 20:
        text = text.title()
    return text

def clean_organization_name(text: str) -> str:
    """Clean extracted organization name."""
    text = text.strip()
    # Remove common prefixes/suffixes
    text = re.sub(r'(?i)^(by |the |a )', '', text)
    text = re.sub(r'(?i)( and associates| inc\.?| corp\.?| llc)$', '', text)
    return text.strip()

def normalize_date(date_str: str) -> Optional[str]:
    """Normalize date string to YYYY-MM-DD format."""
    date_str = date_str.strip()
    
    # Try different date formats
    formats = [
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%B %d, %Y',
        '%B %Y',
        '%b %d, %Y',
        '%b %Y'
    ]
    
    for fmt in formats:
        try:
            if fmt.endswith('%Y') and not fmt.endswith('%d, %Y'):
                # Month-year format, assume day 1
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-01')
            else:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    return None