"""
Enhanced OCR Metadata Extraction System
Specifically designed to handle UNESCO and other international organization documents
"""

import re
from typing import Dict, Optional, List, Tuple
import logging

logger = logging.getLogger(__name__)

def extract_enhanced_metadata_from_content(content: str, existing_metadata: dict = None) -> Dict[str, str]:
    """
    Extract comprehensive metadata from document content with enhanced OCR capabilities
    Specifically handles UNESCO, NIST, and other organizational documents
    """
    if not content or len(content.strip()) < 50:
        return {
            'title': 'Document content too short for analysis',
            'author_organization': 'Unknown',
            'document_type': 'Document',
            'publish_date': None
        }
    
    # Clean content for better parsing
    clean_content = _clean_content_for_ocr(content)
    
    # Extract metadata using specialized functions
    title = _extract_title_enhanced(clean_content, existing_metadata)
    organization = _extract_organization_enhanced(clean_content, existing_metadata)
    doc_type = _extract_document_type_enhanced(clean_content, title)
    pub_date = _extract_date_enhanced(clean_content, existing_metadata)
    
    return {
        'title': title,
        'author_organization': organization,
        'document_type': doc_type,
        'publish_date': pub_date
    }

def _clean_content_for_ocr(content: str) -> str:
    """Clean content to improve OCR metadata extraction"""
    # Remove excessive whitespace but preserve structure
    content = re.sub(r'\n\s*\n', '\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    
    # Remove PDF artifacts
    content = re.sub(r'This publication is available free of charge.*?(?=\n)', '', content)
    content = re.sub(r'Page \d+ of \d+', '', content)
    content = re.sub(r'\d+\s*$', '', content, flags=re.MULTILINE)  # Remove page numbers at end of lines
    
    return content.strip()

def _extract_title_enhanced(content: str, existing_metadata: dict = None) -> str:
    """Enhanced title extraction with UNESCO and international organization support"""
    
    # First check if we have clean PDF metadata title
    if existing_metadata and existing_metadata.get('title'):
        pdf_title = existing_metadata['title'].strip()
        if len(pdf_title) > 5 and not pdf_title.lower().startswith('untitled'):
            return pdf_title
    
    lines = content.split('\n')
    
    # UNESCO specific patterns
    unesco_patterns = [
        r'(Quantum Science for\s*Inclusion and\s*Sustainability)',
        r'(Quantum Science for Inclusion and Sustainability)',
        r'(AI and the Future of Learning)',
        r'(Artificial Intelligence and Education)',
        r'(Digital Transformation in Education)',
        r'([A-Z][A-Za-z\s&,-]{15,80})\s*(?:Policy brief|Policy Brief)',
    ]
    
    # Check for UNESCO patterns first
    full_text = ' '.join(lines[:20])  # First 20 lines
    for pattern in unesco_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            title = matches[0].strip()
            if len(title) > 10:
                return title
    
    # Government document patterns
    gov_patterns = [
        r'(National Quantum Initiative\s+[A-Za-z\s&,-]{10,80})',
        r'(The\s+U\.?S\.?\s+Approach\s+to\s+Quantum\s+[A-Za-z\s&,-]{5,60})',
        r'(Post-Quantum\s+Cryptography\s+[A-Za-z\s&,-]{5,60})',
        r'(NIST\s+Special\s+Publication\s+\d+[\w-]*\s+[A-Za-z\s&,-]{10,80})',
        r'(Quantum\s+[A-Za-z\s&,-]{10,80})\s+(?:Framework|Policy|Strategy|Guidelines?)',
    ]
    
    for pattern in gov_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            title = matches[0].strip()
            if len(title) > 15:
                return title
    
    # Look for title in document structure
    for i, line in enumerate(lines[:15]):
        line = line.strip()
        
        # Skip if line is too short or contains common artifacts
        if (len(line) < 10 or 
            any(skip in line.lower() for skip in ['page ', 'www.', 'http', 'copyright', '©']) or
            re.match(r'^\d+$|^[A-Z]{2,}$|^\W+$', line)):
            continue
        
        # Check if this looks like a title
        if (20 <= len(line) <= 200 and
            not line.lower().startswith(('section ', 'chapter ', 'part ', 'table ', 'figure ')) and
            len(line.split()) >= 3):
            
            # Enhanced validation for title-like content
            if (line[0].isupper() and 
                not line.endswith('.') and
                sum(1 for c in line if c.isupper()) / len(line) < 0.7):  # Not all caps
                return line
    
    # Final fallback - look for longest meaningful line
    candidate_lines = []
    for line in lines[:10]:
        line = line.strip()
        if (15 <= len(line) <= 150 and
            len(line.split()) >= 4 and
            not any(skip in line.lower() for skip in ['page ', 'section ', 'copyright', 'www.', 'http'])):
            candidate_lines.append(line)
    
    if candidate_lines:
        # Return the longest candidate
        return max(candidate_lines, key=len)
    
    return "Document Title Not Extracted"

def _extract_organization_enhanced(content: str, existing_metadata: dict = None) -> str:
    """Enhanced organization extraction with UNESCO and international support"""
    
    lines = content.split('\n')
    full_text = ' '.join(lines[:25])  # First 25 lines
    
    # UNESCO specific detection
    unesco_indicators = [
        r'UNESCO',
        r'United Nations Educational, Scientific and Cultural Organization',
        r'unesco\.org',
        r'Education Sector'
    ]
    
    for indicator in unesco_indicators:
        if re.search(indicator, full_text, re.IGNORECASE):
            return "UNESCO"
    
    # Enhanced organization patterns
    org_patterns = [
        # Government agencies
        r'(?:U\.?S\.?\s+)?(?:DEPARTMENT|DEPT\.?)\s+OF\s+([A-Z][A-Za-z\s&,-]{5,60})',
        r'(?:OFFICE|BUREAU|AGENCY)\s+(?:OF|FOR)\s+([A-Z][A-Za-z\s&,-]{5,60})',
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:DEPARTMENT|AGENCY|BUREAU|OFFICE|ADMINISTRATION)',
        
        # International organizations
        r'(UNITED NATIONS[A-Za-z\s&,-]{0,60})',
        r'(WORLD BANK[A-Za-z\s&,-]{0,40})',
        r'(INTERNATIONAL[A-Za-z\s&,-]{5,60})',
        r'(EUROPEAN[A-Za-z\s&,-]{5,60})',
        
        # Research institutions
        r'(NATIONAL INSTITUTE[A-Za-z\s&,-]{5,60})',
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:INSTITUTE|CENTER|CENTRE)',
        r'(CENTER FOR [A-Z][A-Za-z\s&,-]{5,60})',
        
        # Standards organizations
        r'(NIST)',
        r'(National Institute of Standards and Technology)',
        r'(ISO)',
        r'(International Organization for Standardization)',
        
        # Corporate/Think tanks
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:FOUNDATION|COUNCIL|ASSOCIATION)',
        r'([A-Z][A-Za-z\s&,-]{5,60})\s+(?:CORPORATION|COMPANY|LLC|INC\.?)',
    ]
    
    for pattern in org_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            org_name = matches[0].strip()
            if len(org_name) > 3 and len(org_name) < 100:
                return org_name
    
    # Look for organization in document structure
    for line in lines[:20]:
        line = line.strip()
        
        # Check for organization-like patterns
        if (re.match(r'^[A-Z][A-Z\s&]{8,50}$', line) and  # All caps organization
            not any(skip in line.lower() for skip in ['page ', 'section ', 'chapter ', 'part '])):
            return line
        
        # Check for copyright/attribution lines
        copyright_match = re.search(r'©\s*\d{4}\s*([A-Za-z\s&,-]{5,80})', line)
        if copyright_match:
            org = copyright_match.group(1).strip()
            if len(org) > 5:
                return org
    
    return "Unknown"

def _extract_document_type_enhanced(content: str, title: str) -> str:
    """Enhanced document type extraction"""
    
    content_lower = content.lower()
    title_lower = title.lower()
    
    # Specific type patterns
    type_patterns = {
        'Policy Brief': [
            r'policy\s+brief',
            r'brief.*policy',
            r'policy\s+paper',
        ],
        'Framework': [
            r'framework',
            r'guideline',
            r'standard',
            r'specification',
        ],
        'Strategy': [
            r'strategy',
            r'strategic\s+plan',
            r'roadmap',
        ],
        'Report': [
            r'report',
            r'assessment',
            r'evaluation',
            r'analysis',
        ],
        'Policy': [
            r'policy',
            r'regulation',
            r'directive',
            r'memorandum',
        ],
        'Research': [
            r'research',
            r'study',
            r'investigation',
            r'survey',
        ],
        'Standard': [
            r'standard',
            r'specification',
            r'requirement',
        ]
    }
    
    # Check title and content for type indicators
    for doc_type, patterns in type_patterns.items():
        for pattern in patterns:
            if re.search(pattern, title_lower) or re.search(pattern, content_lower[:1000]):
                return doc_type
    
    # Default classification
    if 'nist' in content_lower[:500]:
        return 'Standard'
    elif 'white house' in content_lower[:500]:
        return 'Policy'
    elif 'unesco' in content_lower[:500]:
        return 'Policy Brief'
    
    return 'Document'

def _extract_date_enhanced(content: str, existing_metadata: dict = None) -> Optional[str]:
    """Enhanced date extraction"""
    
    # Check PDF metadata first
    if existing_metadata and existing_metadata.get('creation_date'):
        pdf_date = existing_metadata['creation_date']
        if pdf_date and len(str(pdf_date)) >= 4:
            return str(pdf_date)[:10]  # Return YYYY-MM-DD format
    
    lines = content.split('\n')
    full_text = ' '.join(lines[:30])  # First 30 lines
    
    # Date patterns
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY or DD/MM/YYYY
        r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4})',
        r'(\d{4})',  # Just year as fallback
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, full_text, re.IGNORECASE)
        if matches:
            date_str = matches[0]
            # Validate year is reasonable
            year_match = re.search(r'(20\d{2})', date_str)
            if year_match:
                year = int(year_match.group(1))
                if 1990 <= year <= 2030:
                    return date_str
    
    return None