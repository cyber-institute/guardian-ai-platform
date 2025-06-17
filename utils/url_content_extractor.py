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
from .focused_bypass_extractor import focused_bypass

class URLContentExtractor:
    """Extract and process content from web URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        # Advanced human-like headers to bypass automation detection
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })
        
        # Additional session configuration for better compatibility
        self.session.max_redirects = 10
        
        # User agents pool for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
        ]
    
    def extract_from_url(self, url: str) -> Dict[str, any]:
        """Extract content, metadata, and generate document info from URL"""
        
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return self._error_result("Invalid URL format")
            
            # Use focused bypass system for protected sites like UNESCO
            bypass_result = focused_bypass.extract_with_bypass(url)
            
            if bypass_result.get('success'):
                # Successfully bypassed protection and extracted content
                return {
                    'success': True,
                    'text_content': bypass_result['text_content'],
                    'title': bypass_result['title'],
                    'organization': bypass_result['organization'],
                    'document_type': bypass_result['document_type'],
                    'extraction_method': bypass_result.get('extraction_method', 'focused_bypass'),
                    'url': bypass_result.get('original_url', url)
                }
            
            # Fallback to standard method if bypass didn't work
            response = self._fetch_with_human_behavior(url)
            
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
                url=url
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
    
    def _fallback_content_extraction(self, html_content: str, url: str) -> str:
        """Fallback content extraction for JavaScript-heavy sites"""
        
        from bs4 import BeautifulSoup
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
            
            # Extract text from specific containers commonly used for content
            content_selectors = [
                'main', 'article', '.content', '#content', '.main-content',
                '.post-content', '.entry-content', '.page-content',
                '[role="main"]', '.container', '.wrapper'
            ]
            
            extracted_text = ""
            
            for selector in content_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True, separator=' ')
                    if len(text) > len(extracted_text):
                        extracted_text = text
            
            # If no specific containers found, extract all text
            if not extracted_text or len(extracted_text.strip()) < 100:
                extracted_text = soup.get_text(strip=True, separator=' ')
            
            # Clean up the extracted text
            lines = extracted_text.split('\n')
            meaningful_lines = []
            
            for line in lines:
                line = line.strip()
                # Skip very short lines, navigation items, and common web elements
                if (len(line) > 20 and 
                    not line.lower().startswith(('menu', 'navigation', 'home', 'about', 'contact')) and
                    not re.match(r'^[A-Z\s]{2,20}$', line)):  # Skip all-caps navigation
                    meaningful_lines.append(line)
            
            result = ' '.join(meaningful_lines)
            
            # For TikTok and similar sites, extract from JSON-LD or other structured data
            if 'tiktok.com' in url.lower():
                result = self._extract_tiktok_content(soup, result)
            
            return result[:10000]  # Limit content length
            
        except Exception as e:
            # Last resort - basic text extraction
            text = re.sub(r'<[^>]+>', '', html_content)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:5000]
    
    def _extract_tiktok_content(self, soup, fallback_text: str) -> str:
        """Extract content specifically from TikTok transparency pages"""
        
        # Look for JSON-LD structured data
        json_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_scripts:
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict) and 'description' in data:
                    return data['description']
            except:
                continue
        
        # Look for meta descriptions and content
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            description = meta_desc['content']
            if len(description) > 100:
                return f"TikTok Transparency: {description}\n\n{fallback_text[:2000]}"
        
        # Look for specific TikTok content sections
        content_sections = soup.find_all(['div', 'section'], class_=re.compile(r'content|policy|transparency'))
        if content_sections:
            tiktok_content = []
            for section in content_sections:
                text = section.get_text(strip=True, separator=' ')
                if len(text) > 50:
                    tiktok_content.append(text)
            
            if tiktok_content:
                return ' '.join(tiktok_content)
        
        return fallback_text
    
    def _extract_title_from_content(self, content: str, url: str) -> str:
        """Extract title from content or generate from URL"""
        
        # Try to find title-like text at the beginning of content
        lines = content.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if len(line) > 10 and len(line) < 200:
                # Check if line looks like a title (no excessive punctuation)
                if line.count('.') < 3 and line.count(',') < 3:
                    return line
        
        # Fallback to URL-based title
        return self._generate_title_from_url(url)
    
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
    
    def _fetch_with_human_behavior(self, url: str):
        """Fetch URL with human-like behavior to bypass automation detection"""
        import random
        
        # Rotate user agent
        user_agent = random.choice(self.user_agents)
        self.session.headers.update({'User-Agent': user_agent})
        
        # Add random delay to mimic human browsing
        time.sleep(random.uniform(1, 3))
        
        # Site-specific handling for known problematic sites
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        # UNESCO specific handling
        if 'unesco.org' in domain:
            return self._fetch_unesco_document(url)
        
        # Add referer header for more realistic requests
        if 'gov' in domain:
            self.session.headers.update({
                'Referer': f"https://{domain}/",
                'Origin': f"https://{domain}"
            })
        
        # Try multiple approaches for difficult sites
        for attempt in range(3):
            try:
                # Method 1: Standard request
                response = self.session.get(url, timeout=30, allow_redirects=True)
                
                # Check for access denied or automation detection
                if response.status_code == 403 or 'access denied' in response.text.lower() or 'automated' in response.text.lower():
                    if attempt < 2:  # Try alternative methods
                        time.sleep(random.uniform(2, 5))
                        continue
                    else:
                        # Method 2: Try with different headers
                        self.session.headers.update({
                            'Sec-Fetch-Site': 'same-origin',
                            'Sec-Fetch-Mode': 'cors',
                            'X-Requested-With': 'XMLHttpRequest'
                        })
                        response = self.session.get(url, timeout=30)
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt == 2:  # Last attempt
                    raise e
                time.sleep(random.uniform(2, 4))
        
        raise requests.exceptions.RequestException("All fetch attempts failed")
    
    def _fetch_unesco_document(self, url: str):
        """Advanced handling for UNESCO documents with multiple bypass strategies"""
        
        # Strategy 1: Try with cloudscraper (bypass Cloudflare)
        try:
            import cloudscraper
            scraper = cloudscraper.create_scraper(
                browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True}
            )
            response = scraper.get(url, timeout=30)
            response.raise_for_status()
            return response
        except ImportError:
            pass  # cloudscraper not available
        except Exception:
            pass  # Try next strategy
        
        # Strategy 2: Multi-step session with realistic browsing pattern
        unesco_session = requests.Session()
        
        # Set comprehensive browser headers
        unesco_session.headers.update({
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
            'sec-ch-ua-platform': '"Windows"'
        })
        
        try:
            # Step 1: Visit main UNESCO site first
            unesco_session.get('https://unesdoc.unesco.org/', timeout=15)
            time.sleep(2)
            
            # Step 2: Visit a search page to appear more human-like
            search_url = 'https://unesdoc.unesco.org/search'
            unesco_session.get(search_url, timeout=15)
            time.sleep(1)
            
            # Step 3: Add referer header and try document
            unesco_session.headers['Referer'] = 'https://unesdoc.unesco.org/search'
            response = unesco_session.get(url, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                return response
            
        except Exception:
            pass
        
        # Strategy 3: Alternative UNESCO URL patterns
        if '/ark:/' in url:
            # Try alternative URL formats
            alternatives = [
                url.replace('/ark:/', '/ark:/48223/'),
                url + '.pdf',
                url + '/PDF/' + url.split('/')[-1] + 'eng.pdf.multi'
            ]
            
            for alt_url in alternatives:
                try:
                    response = unesco_session.get(alt_url, timeout=20)
                    if response.status_code == 200 and len(response.content) > 1000:
                        return response
                except:
                    continue
        
        # Strategy 4: Use requests-html for JavaScript rendering
        try:
            from requests_html import HTMLSession
            session = HTMLSession()
            r = session.get(url)
            r.html.render(timeout=20)  # This will execute JavaScript
            
            # Create mock response
            class MockResponse:
                def __init__(self, content):
                    self.text = content
                    self.status_code = 200
                def raise_for_status(self):
                    pass
            
            return MockResponse(r.html.html)
            
        except ImportError:
            pass
        except Exception:
            pass
        
        # Strategy 5: Direct PDF fetch attempt
        if not url.endswith('.pdf'):
            pdf_variants = [
                url + '.pdf',
                url.replace('/ark:/', '/ark:/48223/pf0000') + '.pdf',
                url + '/PDF/' + url.split('/')[-1] + 'eng.pdf'
            ]
            
            for pdf_url in pdf_variants:
                try:
                    response = requests.get(pdf_url, headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }, timeout=20)
                    
                    if response.status_code == 200 and response.headers.get('content-type', '').startswith('application/pdf'):
                        # For PDF files, extract text using PyPDF2
                        try:
                            import PyPDF2
                            from io import BytesIO
                            
                            pdf_reader = PyPDF2.PdfReader(BytesIO(response.content))
                            text_content = ""
                            for page in pdf_reader.pages:
                                text_content += page.extract_text() + "\n"
                            
                            class MockResponse:
                                def __init__(self, content):
                                    self.text = content
                                    self.status_code = 200
                                def raise_for_status(self):
                                    pass
                            
                            return MockResponse(text_content)
                        except:
                            pass
                except:
                    continue
        
        # Final fallback with error
        raise requests.exceptions.RequestException(f"Unable to access UNESCO document at {url}. The site may be blocking automated access.")
    
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