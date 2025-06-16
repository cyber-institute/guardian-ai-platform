"""
URL Content Extraction System
Extracts and processes content from web URLs for document ingestion
"""

import requests
import trafilatura
import re
from typing import Dict, Optional
from urllib.parse import urlparse, urljoin
import time

class URLContentExtractor:
    """Extract and process content from web URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_from_url(self, url: str) -> Dict[str, any]:
        """Extract content, metadata, and generate document info from URL"""
        
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return self._error_result("Invalid URL format")
            
            # Fetch the webpage
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Extract content using trafilatura with enhanced fallback methods
            text_content = trafilatura.extract(response.text, include_comments=False, include_tables=True)
            
            # If trafilatura fails, try alternative extraction methods
            if not text_content or len(text_content.strip()) < 50:
                text_content = self._fallback_content_extraction(response.text, url)
            
            if not text_content or len(text_content.strip()) < 50:
                return self._error_result("Could not extract sufficient readable content from URL")
            
            # Enhanced metadata extraction using multi-LLM system
            from utils.enhanced_metadata_extractor import extract_enhanced_metadata
            
            # Extract comprehensive metadata
            enhanced_metadata = extract_enhanced_metadata(
                title="",  # Will be extracted from content
                content=text_content,
                url=url,
                filename=parsed_url.path.split('/')[-1] if parsed_url.path else ""
            )
            
            # Use enhanced metadata with fallback to basic extraction
            basic_metadata = self._extract_metadata(response.text, url)
            
            title = enhanced_metadata.get('title', 'Unknown')
            if title == 'Unknown' or self._is_generic_title(title):
                title = basic_metadata.get('title') or self._generate_title_from_url(url)
            
            organization = enhanced_metadata.get('organization', 'Unknown')
            if organization == 'Unknown':
                organization = self._detect_organization(url, text_content, basic_metadata)
            
            return {
                'success': True,
                'title': title,
                'text_content': text_content,
                'url': url,
                'organization': organization,
                'metadata': enhanced_metadata,
                'document_type': enhanced_metadata.get('document_type', self._classify_document_type(text_content, url)),
                'author': enhanced_metadata.get('author', 'Unknown'),
                'publication_date': enhanced_metadata.get('publication_date', 'Unknown'),
                'description': enhanced_metadata.get('description', 'Unknown'),
                'source': 'url_extraction'
            }
            
        except requests.RequestException as e:
            return self._error_result(f"Failed to fetch URL: {str(e)}")
        except Exception as e:
            return self._error_result(f"Extraction failed: {str(e)}")
    
    def _extract_metadata(self, html_content: str, url: str) -> Dict[str, str]:
        """Extract metadata from HTML content"""
        
        metadata = {}
        
        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Extract meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if desc_match:
            metadata['description'] = desc_match.group(1).strip()
        
        # Extract meta author
        author_match = re.search(r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if author_match:
            metadata['author'] = author_match.group(1).strip()
        
        # Extract publication date
        date_patterns = [
            r'<meta[^>]*property=["\']article:published_time["\'][^>]*content=["\']([^"\']+)["\']',
            r'<meta[^>]*name=["\']date["\'][^>]*content=["\']([^"\']+)["\']',
            r'<time[^>]*datetime=["\']([^"\']+)["\']'
        ]
        
        for pattern in date_patterns:
            date_match = re.search(pattern, html_content, re.IGNORECASE)
            if date_match:
                metadata['publish_date'] = date_match.group(1).strip()
                break
        
        # Extract keywords
        keywords_match = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if keywords_match:
            metadata['keywords'] = keywords_match.group(1).strip()
        
        return metadata
    
    def _detect_organization(self, url: str, content: str, metadata: Dict[str, str]) -> str:
        """Detect organization from URL, content, and metadata"""
        
        # Extract from URL domain
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Government and organization domains
        org_mappings = {
            'nasa.gov': 'NASA',
            'nist.gov': 'National Institute of Standards and Technology',
            'dhs.gov': 'Department of Homeland Security',
            'cisa.gov': 'Cybersecurity and Infrastructure Security Agency',
            'nsa.gov': 'National Security Agency',
            'doe.gov': 'Department of Energy',
            'ncsc.gov.uk': 'UK National Cyber Security Centre',
            'enisa.europa.eu': 'European Union Agency for Cybersecurity',
            'bsi.bund.de': 'German Federal Office for Information Security',
            'anssi.gouv.fr': 'French National Cybersecurity Agency',
            'cse-cst.gc.ca': 'Communications Security Establishment Canada',
            'asd.gov.au': 'Australian Signals Directorate'
        }
        
        # Check exact domain matches
        for domain_pattern, org_name in org_mappings.items():
            if domain_pattern in domain:
                return org_name
        
        # Extract from content patterns
        org_patterns = [
            r'(?:published by|issued by|from)\s+([A-Z][^.]*?(?:Agency|Department|Institute|Office|Centre|Center))',
            r'([A-Z][^.]*?(?:NASA|NIST|DHS|CISA|NSA|NCSC))',
            r'(National[^.]*?(?:Institute|Agency|Office|Centre|Center))',
            r'(Department of[^.]*?)(?:\.|,|\n)'
        ]
        
        content_sample = content[:1000]
        for pattern in org_patterns:
            match = re.search(pattern, content_sample, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Extract from metadata
        if 'author' in metadata:
            return metadata['author']
        
        # Fallback to domain name cleaning
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            org_name = domain_parts[-2].replace('-', ' ').title()
            return f"{org_name} (from {domain})"
        
        return f"Organization from {domain}"
    
    def _generate_title_from_url(self, url: str) -> str:
        """Generate a title from URL if no title found"""
        
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        
        if path_parts:
            # Use the last meaningful path component
            title_candidate = path_parts[-1]
            
            # Remove file extensions
            title_candidate = re.sub(r'\.[a-zA-Z0-9]+$', '', title_candidate)
            
            # Replace hyphens and underscores with spaces
            title_candidate = re.sub(r'[-_]+', ' ', title_candidate)
            
            # Capitalize
            return title_candidate.title()
        
        # Fallback to domain
        return f"Document from {parsed_url.netloc}"
    
    def _is_generic_title(self, title: str) -> bool:
        """Check if a title is too generic to be useful"""
        generic_titles = [
            "cybersecurity document", "document", "untitled", "no title",
            "web document", "pdf document", "government document"
        ]
        return title.lower() in generic_titles or len(title) < 10
    
    def _classify_document_type(self, content: str, url: str) -> str:
        """Classify document type based on content and URL"""
        
        content_lower = content.lower()
        url_lower = url.lower()
        
        # Check for specific document types
        if any(term in content_lower for term in ['framework', 'standard', 'guideline', 'best practice']):
            return 'Framework'
        elif any(term in content_lower for term in ['policy', 'regulation', 'directive', 'mandate']):
            return 'Policy'
        elif any(term in content_lower for term in ['research', 'study', 'analysis', 'survey']):
            return 'Research'
        elif any(term in content_lower for term in ['threat', 'vulnerability', 'security alert', 'advisory']):
            return 'Security Advisory'
        elif any(term in url_lower for term in ['pdf', 'doc', 'report']):
            return 'Report'
        else:
            return 'Web Document'
    
    def _error_result(self, error_message: str) -> Dict[str, any]:
        """Return error result structure"""
        return {
            'success': False,
            'error': error_message,
            'title': '',
            'text_content': '',
            'url': '',
            'organization': '',
            'metadata': {},
            'document_type': 'Unknown',
            'source': 'url_extraction'
        }

def extract_url_content(url: str) -> Dict[str, any]:
    """Main function to extract content from URL"""
    extractor = URLContentExtractor()
    return extractor.extract_from_url(url)