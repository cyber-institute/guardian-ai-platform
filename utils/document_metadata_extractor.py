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
    
    # Clean content for analysis - remove HTML first
    content_clean = re.sub(r'<[^>]+>', '', content)  # Remove HTML tags
    content_clean = re.sub(r"style='[^']*'", '', content_clean)  # Remove style attributes
    content_clean = re.sub(r'style="[^"]*"', '', content_clean)  # Remove style attributes with double quotes
    content_clean = re.sub(r'&\w+;', ' ', content_clean)  # Remove HTML entities
    content_clean = re.sub(r'\s+', ' ', content_clean).strip()  # Normalize whitespace
    
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
    """Extract author organization using enhanced pattern matching."""
    
    # Enhanced NIST detection patterns - check multiple locations in document
    nist_indicators = [
        r'(?i)\bnist\b',
        r'(?i)national\s+institute\s+of\s+standards',
        r'(?i)commerce\.gov',
        r'(?i)nvlpubs\.nist\.gov',
        r'(?i)csrc\.nist\.gov',
        r'(?i)nist\.gov',
        r'(?i)sp\s*800-',  # NIST Special Publication format
        r'(?i)special\s+publication\s+800',
        r'(?i)cybersecurity\s+framework',
        r'(?i)gaithersburg,?\s+md',
        r'(?i)boulder,?\s+co',
        r'(?i)nist\s+(sp|special\s+publication|cybersecurity)',
        r'(?i)(quantum|post-quantum|cryptographic)\s+(standard|implementation|guide)',
    ]
    
    # Check entire document for NIST indicators with higher priority
    for pattern in nist_indicators:
        if re.search(pattern, content[:3000]):  # Check first 3000 chars
            return 'NIST'
    
    # Comprehensive organization patterns - government, academic, industry, standards
    org_patterns = [
        # Government agencies
        (r'(?i)\b(National Security Agency|NSA)\b', 'NSA'),
        (r'(?i)\b(Department of Defense|DoD|DOD)\b', 'Department of Defense'),
        (r'(?i)\b(Department of Homeland Security|DHS)\b', 'DHS'),
        (r'(?i)\b(Cybersecurity and Infrastructure Security Agency|CISA)\b', 'CISA'),
        (r'(?i)\b(National Aeronautics and Space Administration|NASA)\b', 'NASA'),
        (r'(?i)\b(Federal Bureau of Investigation|FBI)\b', 'FBI'),
        (r'(?i)\b(Central Intelligence Agency|CIA)\b', 'CIA'),
        (r'(?i)\b(White House|Executive Office)\b', 'White House'),
        (r'(?i)\b(Government Accountability Office|GAO)\b', 'GAO'),
        
        # International organizations
        (r'(?i)\b(European Union|EU|European Commission)\b', 'European Union'),
        (r'(?i)\b(United Nations|UN)\b', 'United Nations'),
        (r'(?i)\b(World Bank)\b', 'World Bank'),
        (r'(?i)\b(International Monetary Fund|IMF)\b', 'IMF'),
        
        # Standards bodies
        (r'(?i)\b(International Organization for Standardization|ISO)\b', 'ISO'),
        (r'(?i)\b(Institute of Electrical and Electronics Engineers|IEEE)\b', 'IEEE'),
        (r'(?i)\b(Internet Engineering Task Force|IETF)\b', 'IETF'),
        (r'(?i)\b(World Wide Web Consortium|W3C)\b', 'W3C'),
        (r'(?i)\b(Object Management Group|OMG)\b', 'OMG'),
        (r'(?i)\b(International Telecommunication Union|ITU)\b', 'ITU'),
        
        # Research institutions & think tanks
        (r'(?i)\b(MITRE Corporation|MITRE)\b', 'MITRE'),
        (r'(?i)\b(RAND Corporation|RAND)\b', 'RAND'),
        (r'(?i)\b(Brookings Institution|Brookings)\b', 'Brookings Institution'),
        (r'(?i)\b(Center for Strategic and International Studies|CSIS)\b', 'CSIS'),
        (r'(?i)\b(Atlantic Council)\b', 'Atlantic Council'),
        (r'(?i)\b(Pew Research)\b', 'Pew Research'),
        
        # Major universities
        (r'(?i)\b(Massachusetts Institute of Technology|MIT)\b', 'MIT'),
        (r'(?i)\b(Stanford University)\b', 'Stanford University'),
        (r'(?i)\b(Harvard University|Harvard)\b', 'Harvard University'),
        (r'(?i)\b(Carnegie Mellon University|CMU)\b', 'Carnegie Mellon'),
        (r'(?i)\b(University of California[,\s]+(Berkeley|UCLA|San Diego|Davis))\b', None),
        (r'(?i)\b(Georgia Institute of Technology|Georgia Tech)\b', 'Georgia Tech'),
        (r'(?i)\b(Princeton University|Princeton)\b', 'Princeton University'),
        (r'(?i)\b(Yale University|Yale)\b', 'Yale University'),
        (r'(?i)\b(University of [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', None),
        
        # Tech companies
        (r'(?i)\b(Microsoft Corporation|Microsoft)\b', 'Microsoft'),
        (r'(?i)\b(Google LLC|Google Inc|Google)\b', 'Google'),
        (r'(?i)\b(Amazon Web Services|AWS|Amazon)\b', 'Amazon'),
        (r'(?i)\b(International Business Machines|IBM)\b', 'IBM'),
        (r'(?i)\b(Apple Inc|Apple)\b', 'Apple'),
        (r'(?i)\b(Meta Platforms|Facebook|Meta)\b', 'Meta'),
        (r'(?i)\b(Tesla Inc|Tesla)\b', 'Tesla'),
        (r'(?i)\b(NVIDIA Corporation|NVIDIA)\b', 'NVIDIA'),
        (r'(?i)\b(Intel Corporation|Intel)\b', 'Intel'),
        (r'(?i)\b(Cisco Systems|Cisco)\b', 'Cisco'),
        
        # Consulting firms
        (r'(?i)\b(McKinsey & Company|McKinsey)\b', 'McKinsey'),
        (r'(?i)\b(Boston Consulting Group|BCG)\b', 'BCG'),
        (r'(?i)\b(Deloitte)\b', 'Deloitte'),
        (r'(?i)\b(PricewaterhouseCoopers|PwC)\b', 'PwC'),
        (r'(?i)\b(Ernst & Young|EY)\b', 'EY'),
        (r'(?i)\b(KPMG)\b', 'KPMG'),
        (r'(?i)\b(Accenture)\b', 'Accenture'),
    ]
    
    # Check first 2000 characters for organization mentions
    search_text = content[:2000]
    
    for pattern, standardized_name in org_patterns:
        match = re.search(pattern, search_text)
        if match:
            return standardized_name if standardized_name else match.group(1)
    
    # Look for "prepared by", "published by", "author" patterns
    author_patterns = [
        r'(?i)(?:prepared|published|authored|developed)\s+by:?\s*([^.\n]{5,80})',
        r'(?i)author[s]?:?\s*([^.\n]{5,80})',
        r'(?i)organization:?\s*([^.\n]{5,80})',
        r'(?i)affiliation:?\s*([^.\n]{5,80})',
        r'(?i)institution:?\s*([^.\n]{5,80})',
        r'(?i)company:?\s*([^.\n]{5,80})',
    ]
    
    for pattern in author_patterns:
        match = re.search(pattern, search_text)
        if match:
            org_name = clean_organization_name(match.group(1))
            if org_name != 'Unknown':
                return org_name
    
    # Look for email domains to infer organizations
    email_patterns = [
        r'@([a-zA-Z0-9.-]+\.(edu|gov|org|com))',
        r'([a-zA-Z0-9.-]+\.(edu|gov|org))',  # Educational and government domains
    ]
    
    for pattern in email_patterns:
        matches = re.findall(pattern, search_text)
        for match in matches:
            domain = match[0] if isinstance(match, tuple) else match
            org_from_domain = extract_org_from_domain(domain)
            if org_from_domain:
                return org_from_domain
    
    # Look for copyright and footer information
    footer_patterns = [
        r'(?i)©\s*\d{4}\s+([^.\n]{5,50})',
        r'(?i)copyright\s+\d{4}\s+([^.\n]{5,50})',
        r'(?i)all\s+rights\s+reserved[.,]\s*([^.\n]{5,50})',
    ]
    
    # Check both header and footer for copyright info
    full_search = content[:1500] + content[-1000:] if len(content) > 1500 else content
    
    for pattern in footer_patterns:
        match = re.search(pattern, full_search)
        if match:
            org_name = clean_organization_name(match.group(1))
            if org_name != 'Unknown':
                return org_name
    
    return 'Unknown'

def extract_org_from_domain(domain: str) -> Optional[str]:
    """Extract organization name from email domain."""
    domain = domain.lower()
    
    # Known domain mappings
    domain_mappings = {
        'nist.gov': 'NIST',
        'mit.edu': 'MIT',
        'stanford.edu': 'Stanford University', 
        'harvard.edu': 'Harvard University',
        'cmu.edu': 'Carnegie Mellon',
        'berkeley.edu': 'UC Berkeley',
        'ucla.edu': 'UCLA',
        'microsoft.com': 'Microsoft',
        'google.com': 'Google',
        'ibm.com': 'IBM',
        'amazon.com': 'Amazon',
        'apple.com': 'Apple',
        'cisco.com': 'Cisco',
        'intel.com': 'Intel',
        'nvidia.com': 'NVIDIA',
        'mitre.org': 'MITRE',
        'rand.org': 'RAND Corporation',
        'ieee.org': 'IEEE',
    }
    
    if domain in domain_mappings:
        return domain_mappings[domain]
    
    # Extract organization from domain structure
    if domain.endswith('.edu'):
        # University domain
        parts = domain.split('.')
        if len(parts) >= 2:
            university_name = parts[0].replace('-', ' ').title()
            return f"{university_name} University"
    
    elif domain.endswith('.gov'):
        # Government domain
        parts = domain.split('.')
        if len(parts) >= 2:
            return parts[0].upper()
    
    return None

def extract_date(content: str) -> Optional[str]:
    """Extract publication date using comprehensive pattern matching."""
    
    # Enhanced date patterns for various document formats
    date_patterns = [
        # Explicit date labels
        r'(?i)(?:published|publication\s+date|date\s+published|issued|release\s+date):?\s*([A-Za-z]+ \d{1,2},? \d{4})',
        r'(?i)(?:published|publication\s+date|date\s+published|issued|release\s+date):?\s*(\d{1,2}/\d{1,2}/\d{4})',
        r'(?i)(?:published|publication\s+date|date\s+published|issued|release\s+date):?\s*(\d{4}-\d{2}-\d{2})',
        r'(?i)(?:published|publication\s+date|date\s+published|issued|release\s+date):?\s*([A-Za-z]+ \d{4})',
        r'(?i)(?:updated|revised|modified|version):?\s*([A-Za-z]+ \d{1,2},? \d{4})',
        r'(?i)(?:updated|revised|modified|version):?\s*(\d{4}-\d{2}-\d{2})',
        r'(?i)(?:updated|revised|modified|version):?\s*([A-Za-z]+ \d{4})',
        
        # Document metadata patterns
        r'(?i)(?:copyright|©)\s*(\d{4})',
        r'(?i)(?:final|draft|version).*?(\d{4})',
        r'(?i)(?:sp|special\s+publication).*?(\d{4})',  # NIST SP format
        
        # Common date formats in document headers
        r'\b(\d{1,2}\s+[A-Za-z]+\s+\d{4})\b',  # 15 March 2024
        r'\b([A-Za-z]+\s+\d{1,2},?\s+\d{4})\b',  # March 15, 2024
        r'\b(\d{4}-\d{2}-\d{2})\b',  # 2024-03-15
        r'\b(\d{2}/\d{2}/\d{4})\b',  # 03/15/2024
        r'\b(\d{1,2}/\d{1,2}/\d{4})\b',  # 3/15/2024
        r'\b([A-Za-z]+\s+\d{4})\b',  # March 2024
        
        # Year-only patterns as last resort
        r'(?i)(?:published|issued|released).*?(\d{4})',
        r'\b(20[12]\d)\b',  # Years 2010-2029
    ]
    
    # Search both header and footer areas where dates are commonly found
    header_text = content[:2000]
    footer_text = content[-1000:] if len(content) > 1000 else content
    search_areas = [header_text, footer_text]
    
    for search_text in search_areas:
        for pattern in date_patterns:
            matches = re.findall(pattern, search_text)
            for match in matches:
                normalized_date = normalize_date(match)
                if normalized_date and is_valid_year(normalized_date):
                    return normalized_date
    
    return None

def is_valid_year(date_str: str) -> bool:
    """Check if extracted date contains a reasonable year."""
    year_match = re.search(r'(20[0-2]\d)', date_str)
    if year_match:
        year = int(year_match.group(1))
        return 2000 <= year <= 2030  # Reasonable range for documents
    return False

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
    """Generate intelligent content preview with comprehensive cleaning."""
    
    if not content:
        return 'No meaningful content available'
    
    # Comprehensive HTML and CSS cleaning
    cleaned = content
    
    # Remove all HTML tags and their contents
    cleaned = re.sub(r'<script[^>]*>.*?</script>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<style[^>]*>.*?</style>', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'<[^>]+>', '', cleaned)  # Remove all HTML tags
    
    # Remove CSS style attributes and properties
    cleaned = re.sub(r"style\s*=\s*['\"][^'\"]*['\"]", '', cleaned)
    cleaned = re.sub(r'margin-[a-z-]*:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'padding-[a-z-]*:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'background-[a-z-]*:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'color:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'font-[a-z-]*:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'border-[a-z-]*:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    
    # Remove HTML entities
    cleaned = re.sub(r'&[a-zA-Z][a-zA-Z0-9]*;', ' ', cleaned)
    cleaned = re.sub(r'&#[0-9]+;', ' ', cleaned)
    cleaned = re.sub(r'&#x[0-9a-fA-F]+;', ' ', cleaned)
    
    # Remove remaining angle brackets and CSS artifacts
    cleaned = re.sub(r'[<>{}]', ' ', cleaned)
    cleaned = re.sub(r'display:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'align-items:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'justify-content:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
    
    # Clean up document artifacts
    cleaned = re.sub(r'(?i)^.*?(?:table of contents|abstract|executive summary)', '', cleaned, flags=re.DOTALL)
    cleaned = re.sub(r'(?i)(?:page \d+|draft|confidential|proprietary).*$', '', cleaned, flags=re.MULTILINE)
    
    # Normalize whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    
    # Extract meaningful sentences
    sentences = re.split(r'[.!?]\s+', cleaned)
    meaningful_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        # Filter out technical artifacts and ensure meaningful content
        if (len(sentence) > 25 and len(sentence) < 500 and 
            not re.search(r'^\d+\s*$|^[A-Z]\s*$|^[a-z]\s*$', sentence) and
            not re.search(r'margin|padding|background|color:|font-|border-|display:', sentence, re.IGNORECASE) and
            sentence.count(' ') > 4 and  # At least 5 words
            not sentence.startswith(('div', 'span', 'strong', 'AI Cyber', 'Q Cyber', 'AI Ethics', 'Q Ethics'))):
            meaningful_sentences.append(sentence)
            if len(meaningful_sentences) >= 2:
                break
    
    if meaningful_sentences:
        preview = '. '.join(meaningful_sentences) + '.'
        # Final cleanup and truncation
        preview = re.sub(r'\s+', ' ', preview).strip()
        if len(preview) > 300:
            preview = preview[:297] + '...'
        return preview
    
    # Last resort: extract first meaningful chunk
    words = cleaned.split()
    if len(words) > 10:
        # Take first 30 words that don't look like CSS/HTML artifacts
        clean_words = [w for w in words[:50] if not re.search(r'margin|padding|color|font|background', w, re.IGNORECASE)]
        if len(clean_words) > 10:
            return ' '.join(clean_words[:30]) + '...'
    
    return 'Document content requires manual review'

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