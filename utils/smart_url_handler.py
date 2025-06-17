"""
Smart URL Handler with Human-Guided Fallback
Handles URLs intelligently with clear user guidance for blocked sites
"""

import requests
import trafilatura
from typing import Dict, Optional, List
from urllib.parse import urlparse
import time
import random

class SmartURLHandler:
    """Intelligent URL handler with human guidance for blocked sites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        })
        
        # Known problematic domains that require manual handling
        self.manual_domains = {
            'unesdoc.unesco.org': {
                'name': 'UNESCO Document Repository',
                'instructions': [
                    "1. Open the UNESCO URL in your browser",
                    "2. If prompted, accept cookies or terms",
                    "3. Download the PDF file manually",
                    "4. Upload the downloaded PDF using the file upload option instead"
                ],
                'alternative': 'Try searching for the document title on unesco.org or use file upload'
            },
            'jstor.org': {
                'name': 'JSTOR Academic Papers',
                'instructions': [
                    "1. Access through institutional login or JSTOR account",
                    "2. Download the PDF manually",
                    "3. Upload using file upload feature"
                ],
                'alternative': 'Use institutional access or search for open access version'
            }
        }
    
    def handle_url(self, url: str) -> Dict[str, any]:
        """Main URL handling with intelligent fallback"""
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # Check if this is a known problematic domain
        for problem_domain, info in self.manual_domains.items():
            if problem_domain in domain:
                return self._create_manual_guidance(url, info)
        
        # Try automated extraction for accessible sites
        try:
            return self._extract_automatically(url)
        except Exception as e:
            # If automated fails, provide guidance
            return self._create_fallback_guidance(url, str(e))
    
    def _extract_automatically(self, url: str) -> Dict[str, any]:
        """Attempt automated extraction for accessible URLs"""
        
        # Add random delay to be respectful
        time.sleep(random.uniform(0.5, 1.5))
        
        try:
            # Method 1: Direct request
            response = self.session.get(url, timeout=20, allow_redirects=True)
            response.raise_for_status()
            
            # Check for access denied indicators
            if self._is_access_denied(response):
                raise requests.exceptions.RequestException("Access denied by website")
            
            # Extract content
            content = trafilatura.extract(response.text, include_comments=False, include_tables=True)
            
            if not content or len(content.strip()) < 100:
                # Try alternative extraction
                content = self._extract_basic_content(response.text)
            
            if not content or len(content.strip()) < 50:
                raise Exception("Insufficient content extracted")
            
            # Extract metadata
            metadata = self._extract_basic_metadata(response.text, url)
            
            return {
                'success': True,
                'method': 'automated',
                'content': content,
                'metadata': metadata,
                'url': url,
                'title': metadata.get('title', self._generate_title_from_url(url)),
                'organization': self._detect_organization_from_url(url),
                'document_type': 'Web Document'
            }
            
        except Exception as e:
            raise Exception(f"Automated extraction failed: {str(e)}")
    
    def _is_access_denied(self, response) -> bool:
        """Check if response indicates access denied"""
        
        if response.status_code == 403:
            return True
        
        content_lower = response.text.lower()
        denied_indicators = [
            'access denied', 'forbidden', 'blocked', 'not authorized',
            'automated access', 'robot', 'captcha', 'cloudflare'
        ]
        
        return any(indicator in content_lower for indicator in denied_indicators)
    
    def _extract_basic_content(self, html_content: str) -> str:
        """Basic content extraction fallback"""
        
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up text
            lines = text.split('\n')
            meaningful_lines = [line.strip() for line in lines if len(line.strip()) > 20]
            
            return ' '.join(meaningful_lines[:100])  # Limit content
            
        except Exception:
            return ""
    
    def _extract_basic_metadata(self, html_content: str, url: str) -> Dict[str, str]:
        """Extract basic metadata from HTML"""
        
        import re
        metadata = {}
        
        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        
        # Extract meta description
        desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
        if desc_match:
            metadata['description'] = desc_match.group(1).strip()
        
        return metadata
    
    def _generate_title_from_url(self, url: str) -> str:
        """Generate title from URL path"""
        
        parsed_url = urlparse(url)
        path_parts = [part for part in parsed_url.path.split('/') if part]
        
        if path_parts:
            title = path_parts[-1]
            title = re.sub(r'\.[a-zA-Z0-9]+$', '', title)  # Remove extension
            title = re.sub(r'[-_]+', ' ', title)  # Replace hyphens/underscores
            return title.title()
        
        return f"Document from {parsed_url.netloc}"
    
    def _detect_organization_from_url(self, url: str) -> str:
        """Detect organization from URL domain"""
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        org_mappings = {
            'nist.gov': 'NIST',
            'nasa.gov': 'NASA',
            'dhs.gov': 'DHS',
            'cisa.gov': 'CISA',
            'whitehouse.gov': 'White House',
            'unesco.org': 'UNESCO',
            'unesdoc.unesco.org': 'UNESCO'
        }
        
        for domain_pattern, org_name in org_mappings.items():
            if domain_pattern in domain:
                return org_name
        
        # Extract from domain
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            return domain_parts[-2].replace('-', ' ').title()
        
        return 'Unknown'
    
    def _create_manual_guidance(self, url: str, info: Dict) -> Dict[str, any]:
        """Create manual guidance for problematic domains"""
        
        return {
            'success': False,
            'method': 'manual_required',
            'url': url,
            'domain_name': info['name'],
            'reason': 'This website blocks automated access',
            'instructions': info['instructions'],
            'alternative': info['alternative'],
            'recommendation': 'Use file upload instead of URL upload for this document'
        }
    
    def _create_fallback_guidance(self, url: str, error: str) -> Dict[str, any]:
        """Create fallback guidance for failed extractions"""
        
        return {
            'success': False,
            'method': 'extraction_failed',
            'url': url,
            'reason': f'Unable to extract content: {error}',
            'instructions': [
                "1. Open the URL in your browser",
                "2. Save the document/page content manually", 
                "3. Upload the saved file using the file upload option"
            ],
            'alternative': 'Try file upload instead of URL upload',
            'recommendation': 'Manual download and file upload recommended'
        }

# Global instance
smart_url_handler = SmartURLHandler()