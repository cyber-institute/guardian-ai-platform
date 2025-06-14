"""
Web Search-Based URL Discovery for GUARDIAN
Uses search engine APIs to find document source URLs efficiently
"""

import requests
import re
from typing import Optional, List, Dict
from urllib.parse import quote, urlparse
import time
import os

class WebSearchURLDiscovery:
    """
    Find document URLs using web search APIs instead of LLM token usage
    """
    
    def __init__(self):
        # Search API configurations
        self.google_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.google_cx = os.getenv('GOOGLE_SEARCH_CX')
        self.bing_api_key = os.getenv('BING_SEARCH_API_KEY')
        
        # Trusted domains for document sources
        self.trusted_domains = [
            'nist.gov', 'nvlpubs.nist.gov', 'csrc.nist.gov',
            'cisa.gov', 'us-cert.cisa.gov',
            'nasa.gov', 'ntrs.nasa.gov',
            'whitehouse.gov',
            'nsa.gov',
            'doi.org', 'dx.doi.org',
            'ieee.org', 'ieeexplore.ieee.org',
            'iso.org',
            'ietf.org', 'tools.ietf.org',
            'w3.org',
            'acm.org', 'dl.acm.org',
            'arxiv.org',
            'nih.gov', 'ncbi.nlm.nih.gov'
        ]
    
    def find_document_url(self, title: str, organization: str = "", content_snippet: str = "") -> Optional[str]:
        """Find document URL using multiple search strategies"""
        
        # Strategy 1: Extract URL from content if already present
        content_url = self._extract_url_from_content(content_snippet)
        if content_url:
            return content_url
        
        # Strategy 2: Use Google Custom Search API
        if self.google_api_key and self.google_cx:
            google_url = self._search_with_google(title, organization)
            if google_url:
                return google_url
        
        # Strategy 3: Use Bing Search API
        if self.bing_api_key:
            bing_url = self._search_with_bing(title, organization)
            if bing_url:
                return bing_url
        
        # Strategy 4: DuckDuckGo Instant Answer API (free)
        duckduckgo_url = self._search_with_duckduckgo(title, organization)
        if duckduckgo_url:
            return duckduckgo_url
        
        # Strategy 5: Pattern-based construction (fallback)
        pattern_url = self._construct_url_by_pattern(title, organization)
        if pattern_url:
            return pattern_url
        
        return None
    
    def _extract_url_from_content(self, content: str) -> Optional[str]:
        """Extract URLs directly from document content"""
        
        if not content:
            return None
        
        # Look for document URLs in content
        url_patterns = [
            r'https?://[^\s<>"]+\.pdf\b',
            r'https?://doi\.org/[^\s<>"]+',
            r'https?://nvlpubs\.nist\.gov/[^\s<>"]+',
            r'This publication is available.*?from:\s*(https?://[^\s<>"]+)',
            r'Available at:\s*(https?://[^\s<>"]+)',
            r'URL:\s*(https?://[^\s<>"]+)'
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                url = match.group(1) if match.lastindex else match.group(0)
                if self._is_trusted_url(url):
                    return url.strip()
        
        return None
    
    def _search_with_google(self, title: str, organization: str) -> Optional[str]:
        """Search using Google Custom Search API"""
        
        try:
            # Construct search queries
            queries = self._build_search_queries(title, organization)
            
            for query in queries:
                url = f"https://www.googleapis.com/customsearch/v1"
                params = {
                    'key': self.google_api_key,
                    'cx': self.google_cx,
                    'q': query,
                    'num': 5,
                    'fields': 'items(title,link,snippet)'
                }
                
                response = requests.get(url, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data.get('items', []):
                        link = item.get('link', '')
                        if self._is_document_url(link, title):
                            return link
                
                time.sleep(0.1)  # Rate limiting
        
        except Exception as e:
            print(f"Google search error: {e}")
        
        return None
    
    def _search_with_bing(self, title: str, organization: str) -> Optional[str]:
        """Search using Bing Search API"""
        
        try:
            queries = self._build_search_queries(title, organization)
            
            for query in queries:
                url = "https://api.bing.microsoft.com/v7.0/search"
                headers = {'Ocp-Apim-Subscription-Key': self.bing_api_key}
                params = {
                    'q': query,
                    'count': 5,
                    'textFormat': 'Raw'
                }
                
                response = requests.get(url, headers=headers, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data.get('webPages', {}).get('value', []):
                        link = item.get('url', '')
                        if self._is_document_url(link, title):
                            return link
                
                time.sleep(0.1)  # Rate limiting
        
        except Exception as e:
            print(f"Bing search error: {e}")
        
        return None
    
    def _search_with_duckduckgo(self, title: str, organization: str) -> Optional[str]:
        """Search using DuckDuckGo Instant Answer API (free)"""
        
        try:
            queries = self._build_search_queries(title, organization)
            
            for query in queries:
                url = "https://api.duckduckgo.com/"
                params = {
                    'q': query,
                    'format': 'json',
                    'no_html': 1,
                    'skip_disambig': 1
                }
                
                response = requests.get(url, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check abstract URL
                    abstract_url = data.get('AbstractURL', '')
                    if abstract_url and self._is_document_url(abstract_url, title):
                        return abstract_url
                    
                    # Check related topics
                    for topic in data.get('RelatedTopics', []):
                        topic_url = topic.get('FirstURL', '')
                        if topic_url and self._is_document_url(topic_url, title):
                            return topic_url
                
                time.sleep(0.2)  # Rate limiting for free API
        
        except Exception as e:
            print(f"DuckDuckGo search error: {e}")
        
        return None
    
    def _build_search_queries(self, title: str, organization: str) -> List[str]:
        """Build optimized search queries for finding documents"""
        
        queries = []
        
        # Clean title for searching
        title_clean = re.sub(r'[^\w\s-]', '', title)
        title_short = ' '.join(title_clean.split()[:6])  # First 6 words
        
        # Query 1: Exact title with filetype
        queries.append(f'"{title_short}" filetype:pdf')
        
        # Query 2: Title with organization site search
        if organization:
            org_domain = self._get_org_domain(organization)
            if org_domain:
                queries.append(f'site:{org_domain} "{title_short}"')
        
        # Query 3: Title with trusted domains
        for domain in ['nist.gov', 'cisa.gov', 'doi.org']:
            queries.append(f'site:{domain} "{title_short}"')
        
        # Query 4: NIST SP specific search
        nist_match = re.search(r'nist\s+sp\s+(\d+[-\w]*)', title.lower())
        if nist_match:
            sp_number = nist_match.group(1)
            queries.append(f'site:nvlpubs.nist.gov "NIST.SP.{sp_number}"')
        
        # Query 5: Organization + key terms
        if organization:
            key_terms = self._extract_key_terms(title)
            if key_terms:
                queries.append(f'"{organization}" {" ".join(key_terms[:3])}')
        
        return queries[:5]  # Limit to 5 queries to control API usage
    
    def _get_org_domain(self, organization: str) -> Optional[str]:
        """Get the primary domain for an organization"""
        
        org_domains = {
            'NIST': 'nist.gov',
            'CISA': 'cisa.gov',
            'NASA': 'nasa.gov',
            'NSA': 'nsa.gov',
            'White House': 'whitehouse.gov',
            'IEEE': 'ieee.org',
            'ISO': 'iso.org',
            'IETF': 'ietf.org',
            'W3C': 'w3.org'
        }
        
        return org_domains.get(organization.upper())
    
    def _extract_key_terms(self, title: str) -> List[str]:
        """Extract key terms from title for search"""
        
        # Remove common words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        
        words = re.findall(r'\b\w{3,}\b', title.lower())
        key_terms = [word for word in words if word not in stop_words]
        
        return key_terms[:5]
    
    def _is_document_url(self, url: str, title: str) -> bool:
        """Check if URL is likely the correct document"""
        
        if not url or not self._is_trusted_url(url):
            return False
        
        url_lower = url.lower()
        title_lower = title.lower()
        
        # Check if URL contains document-like extensions
        if any(ext in url_lower for ext in ['.pdf', '.doc', '.docx']):
            return True
        
        # Check if URL contains key terms from title
        title_words = re.findall(r'\b\w{4,}\b', title_lower)
        if len(title_words) >= 2:
            matches = sum(1 for word in title_words[:5] if word in url_lower)
            if matches >= 2:
                return True
        
        # Check for NIST SP patterns
        nist_match = re.search(r'nist\s+sp\s+(\d+[-\w]*)', title_lower)
        if nist_match:
            sp_number = nist_match.group(1).replace('-', '.')
            if sp_number in url_lower:
                return True
        
        return False
    
    def _is_trusted_url(self, url: str) -> bool:
        """Check if URL is from a trusted domain"""
        
        try:
            domain = urlparse(url).netloc.lower()
            return any(trusted in domain for trusted in self.trusted_domains)
        except:
            return False
    
    def _construct_url_by_pattern(self, title: str, organization: str) -> Optional[str]:
        """Construct URL using known patterns (fallback)"""
        
        title_clean = re.sub(r'[^\w\s-]', '', title).strip()
        org_lower = organization.lower()
        
        # NIST patterns
        if 'nist' in org_lower or 'nist' in title.lower():
            nist_sp_match = re.search(r'nist\s+sp\s+(\d+[-\w]*)', title.lower())
            if nist_sp_match:
                sp_number = nist_sp_match.group(1)
                return f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.{sp_number}.pdf"
        
        return None

# Global instance
web_search_discovery = WebSearchURLDiscovery()

def find_document_url_with_search(title: str, organization: str = "", content: str = "") -> Optional[str]:
    """Find document URL using web search APIs"""
    return web_search_discovery.find_document_url(title, organization, content)