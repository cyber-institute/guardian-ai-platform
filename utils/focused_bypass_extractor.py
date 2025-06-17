"""
Focused Bypass Extractor
Streamlined system for bypassing specific website protections with targeted techniques
"""

import requests
import time
import random
from typing import Dict, Optional
from urllib.parse import urlparse
import re

class FocusedBypassExtractor:
    """Focused extractor with specific bypass techniques for protected sites"""
    
    def __init__(self):
        self.session = requests.Session()
        self._setup_stealth_session()
    
    def _setup_stealth_session(self):
        """Configure session with stealth characteristics"""
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'DNT': '1'
        })
    
    def extract_with_bypass(self, url: str) -> Dict[str, any]:
        """Main extraction method with focused bypass techniques"""
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        if 'unesco.org' in domain:
            return self._extract_unesco_document(url)
        elif any(gov_domain in domain for gov_domain in ['gov', 'mil']):
            return self._extract_government_document(url)
        else:
            return self._extract_standard_document(url)
    
    def _extract_unesco_document(self, url: str) -> Dict[str, any]:
        """Targeted UNESCO document extraction"""
        
        # Extract document ID from URL
        doc_id = self._extract_unesco_doc_id(url)
        
        if doc_id:
            # Try multiple UNESCO access patterns
            access_patterns = [
                f'https://unesdoc.unesco.org/images/0038/{doc_id[2:4]}/{doc_id}eng.pdf',
                f'https://unesdoc.unesco.org/rest/annotationSVC/DownloadWatermarkedAttachment/attach_import_{doc_id}.pdf',
                f'https://unesdoc.unesco.org/ark:/48223/pf0000{doc_id}.locale=en'
            ]
            
            for pattern_url in access_patterns:
                result = self._attempt_document_extraction(pattern_url)
                if result['success']:
                    result['original_url'] = url
                    return result
        
        # Multi-step session approach
        try:
            # Step 1: Visit homepage to establish session
            self.session.get('https://unesdoc.unesco.org/', timeout=15)
            time.sleep(1.5)
            
            # Step 2: Access document with established session
            self.session.headers['Referer'] = 'https://unesdoc.unesco.org/'
            response = self.session.get(url, timeout=20)
            
            if response.status_code == 200:
                return self._process_html_response(response, url)
                
        except Exception:
            pass
        
        return {'success': False, 'error': 'UNESCO document access blocked'}
    
    def _extract_unesco_doc_id(self, url: str) -> Optional[str]:
        """Extract document ID from UNESCO URL"""
        
        # Pattern: pf0000123456
        match = re.search(r'pf0000(\d+)', url)
        if match:
            return match.group(1)
        
        # Pattern: direct numeric ID
        match = re.search(r'/(\d{6,})/?$', url)
        if match:
            return match.group(1)
        
        return None
    
    def _attempt_document_extraction(self, url: str) -> Dict[str, any]:
        """Attempt document extraction from URL"""
        
        try:
            response = self.session.get(url, timeout=15, allow_redirects=True)
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '').lower()
                
                if 'application/pdf' in content_type:
                    return self._extract_pdf_content(response.content, url)
                elif 'text/html' in content_type:
                    return self._process_html_response(response, url)
                    
        except Exception:
            pass
        
        return {'success': False}
    
    def _extract_pdf_content(self, pdf_content: bytes, url: str) -> Dict[str, any]:
        """Extract text from PDF content"""
        
        try:
            import PyPDF2
            from io import BytesIO
            
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
            text_content = ""
            
            for page in pdf_reader.pages[:10]:  # Limit to first 10 pages for efficiency
                page_text = page.extract_text()
                if page_text:
                    text_content += page_text + "\n"
            
            if len(text_content.strip()) > 200:
                title = self._extract_title_from_pdf_text(text_content)
                return {
                    'success': True,
                    'text_content': text_content,
                    'title': title,
                    'organization': 'UNESCO',
                    'document_type': 'PDF Document',
                    'extraction_method': 'direct_pdf_access'
                }
                
        except Exception:
            pass
        
        return {'success': False}
    
    def _process_html_response(self, response, url: str) -> Dict[str, any]:
        """Process HTML response for content extraction"""
        
        try:
            import trafilatura
            
            # Extract main content
            text_content = trafilatura.extract(response.text, include_comments=False, include_tables=True)
            
            if text_content and len(text_content.strip()) > 200:
                title = self._extract_title_from_html(response.text) or self._extract_title_from_content(text_content)
                organization = self._detect_organization_from_url(url)
                
                return {
                    'success': True,
                    'text_content': text_content,
                    'title': title,
                    'organization': organization,
                    'document_type': 'Web Document',
                    'extraction_method': 'html_extraction'
                }
                
        except Exception:
            pass
        
        return {'success': False}
    
    def _extract_title_from_pdf_text(self, content: str) -> str:
        """Extract title from PDF text content"""
        
        lines = content.split('\n')
        for line in lines[:15]:  # Check first 15 lines
            line = line.strip()
            if 20 <= len(line) <= 150:  # Reasonable title length
                # Remove excessive whitespace and check if it looks like a title
                clean_line = ' '.join(line.split())
                if not any(char in clean_line for char in ['©', '©', 'page', 'Page']):
                    return clean_line
        
        return "UNESCO Document"
    
    def _extract_title_from_html(self, html_content: str) -> Optional[str]:
        """Extract title from HTML"""
        
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
            if len(title) > 5 and len(title) < 200:
                return title
        
        return None
    
    def _extract_title_from_content(self, content: str) -> str:
        """Extract title from content text"""
        
        lines = content.split('\n')
        for line in lines[:10]:
            line = line.strip()
            if 15 <= len(line) <= 120 and line.count('.') < 2:
                return line
        
        return "Document"
    
    def _detect_organization_from_url(self, url: str) -> str:
        """Detect organization from URL"""
        
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        if 'unesco.org' in domain:
            return 'UNESCO'
        elif 'nist.gov' in domain:
            return 'NIST'
        elif 'nasa.gov' in domain:
            return 'NASA'
        elif 'dhs.gov' in domain:
            return 'DHS'
        elif 'whitehouse.gov' in domain:
            return 'White House'
        
        return 'Unknown'
    
    def _extract_government_document(self, url: str) -> Dict[str, any]:
        """Extract from government sites with lighter protection"""
        
        try:
            self.session.headers['Referer'] = 'https://www.google.com/'
            response = self.session.get(url, timeout=20)
            
            if response.status_code == 200:
                return self._process_html_response(response, url)
                
        except Exception:
            pass
        
        return {'success': False, 'error': 'Government document access failed'}
    
    def _extract_standard_document(self, url: str) -> Dict[str, any]:
        """Standard document extraction for unprotected sites"""
        
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                return self._process_html_response(response, url)
                
        except Exception:
            pass
        
        return {'success': False, 'error': 'Standard document extraction failed'}

# Global instance
focused_bypass = FocusedBypassExtractor()