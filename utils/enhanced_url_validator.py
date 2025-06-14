"""
Enhanced URL Validator with Landing Page Detection
Detects when URLs redirect to generic landing pages vs actual documents
"""

import requests
import re
from urllib.parse import urlparse, urljoin
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class EnhancedURLValidator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Generic landing page indicators
        self.landing_page_indicators = [
            'page not found',
            '404 error',
            'not available',
            'under maintenance',
            'coming soon',
            'home page',
            'main page',
            'welcome to',
            'site index',
            'directory listing',
            'search results',
            'browse documents',
            'document library',
            'publication archive'
        ]
        
        # Document-specific content indicators
        self.document_indicators = [
            'abstract',
            'executive summary',
            'table of contents',
            'introduction',
            'methodology',
            'conclusion',
            'references',
            'bibliography',
            'appendix',
            'figure',
            'table',
            'section',
            'chapter'
        ]
    
    def validate_url_with_content_check(self, url: str, expected_title: str = "", doc_type: str = "") -> Dict[str, any]:
        """
        Validate URL and detect if it leads to actual document vs landing page
        """
        try:
            # First, check if URL is accessible
            response = self.session.get(url, timeout=15, allow_redirects=True)
            
            if response.status_code != 200:
                return {
                    'valid': False,
                    'status': f'HTTP {response.status_code}',
                    'is_landing_page': False,
                    'final_url': url,
                    'content_type': 'unknown'
                }
            
            final_url = response.url
            content_type = response.headers.get('content-type', '').lower()
            
            # Check if it's a PDF (direct document)
            if 'pdf' in content_type:
                return {
                    'valid': True,
                    'status': 'valid_pdf',
                    'is_landing_page': False,
                    'final_url': final_url,
                    'content_type': 'pdf'
                }
            
            # Analyze HTML content for landing page detection
            if 'html' in content_type:
                content = response.text.lower()
                
                # Check for landing page indicators
                landing_score = sum(1 for indicator in self.landing_page_indicators if indicator in content)
                
                # Check for document-specific content
                document_score = sum(1 for indicator in self.document_indicators if indicator in content)
                
                # Check title match if provided
                title_match = False
                if expected_title:
                    title_words = [word.lower() for word in expected_title.split() if len(word) > 3]
                    title_matches = sum(1 for word in title_words if word in content)
                    title_match = title_matches >= len(title_words) * 0.5  # 50% of title words
                
                # Determine if it's a landing page
                is_landing_page = (
                    landing_score > 2 or  # Multiple landing page indicators
                    (landing_score > 0 and document_score == 0) or  # Some landing indicators, no document content
                    ('search' in final_url and 'results' in final_url) or  # Search results page
                    ('browse' in final_url or 'library' in final_url) or  # Document library page
                    (expected_title and not title_match and document_score < 2)  # Title doesn't match and little document content
                )
                
                # Check for PDF links on the page
                pdf_links = self._find_pdf_links(content, final_url)
                if pdf_links and is_landing_page:
                    # Try to find the most relevant PDF
                    best_pdf = self._find_best_pdf_match(pdf_links, expected_title)
                    if best_pdf:
                        return {
                            'valid': True,
                            'status': 'redirected_to_pdf',
                            'is_landing_page': False,
                            'final_url': best_pdf,
                            'content_type': 'pdf'
                        }
                
                return {
                    'valid': not is_landing_page,
                    'status': 'landing_page' if is_landing_page else 'valid_html',
                    'is_landing_page': is_landing_page,
                    'final_url': final_url,
                    'content_type': 'html',
                    'title_match': title_match if expected_title else None,
                    'landing_score': landing_score,
                    'document_score': document_score
                }
            
            # Other content types
            return {
                'valid': True,
                'status': 'valid_other',
                'is_landing_page': False,
                'final_url': final_url,
                'content_type': content_type
            }
            
        except requests.exceptions.Timeout:
            return {
                'valid': False,
                'status': 'timeout',
                'is_landing_page': False,
                'final_url': url,
                'content_type': 'unknown'
            }
        except requests.exceptions.ConnectionError:
            return {
                'valid': False,
                'status': 'connection_error',
                'is_landing_page': False,
                'final_url': url,
                'content_type': 'unknown'
            }
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            return {
                'valid': False,
                'status': f'error: {str(e)}',
                'is_landing_page': False,
                'final_url': url,
                'content_type': 'unknown'
            }
    
    def _find_pdf_links(self, html_content: str, base_url: str) -> list:
        """Find PDF links in HTML content"""
        pdf_links = []
        
        # Find all href attributes that point to PDFs
        pdf_pattern = r'href=["\']([^"\']*\.pdf[^"\']*)["\']'
        matches = re.findall(pdf_pattern, html_content, re.IGNORECASE)
        
        for match in matches:
            if match.startswith('http'):
                pdf_links.append(match)
            else:
                # Convert relative URLs to absolute
                absolute_url = urljoin(base_url, match)
                pdf_links.append(absolute_url)
        
        return pdf_links
    
    def _find_best_pdf_match(self, pdf_links: list, expected_title: str) -> Optional[str]:
        """Find the PDF that best matches the expected title"""
        if not expected_title:
            return pdf_links[0] if pdf_links else None
        
        title_words = expected_title.lower().split()
        best_match = None
        best_score = 0
        
        for pdf_url in pdf_links:
            url_lower = pdf_url.lower()
            score = sum(1 for word in title_words if len(word) > 3 and word in url_lower)
            
            if score > best_score:
                best_score = score
                best_match = pdf_url
        
        return best_match if best_score > 0 else (pdf_links[0] if pdf_links else None)

# Global instance
enhanced_validator = EnhancedURLValidator()

def validate_url_enhanced(url: str, expected_title: str = "", doc_type: str = "") -> Dict[str, any]:
    """
    Enhanced URL validation with landing page detection
    """
    return enhanced_validator.validate_url_with_content_check(url, expected_title, doc_type)