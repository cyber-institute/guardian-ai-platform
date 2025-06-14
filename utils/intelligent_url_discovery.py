"""
Intelligent URL Discovery System
Finds original source URLs for documents using multiple search strategies
"""

import requests
import re
import time
from urllib.parse import quote, urljoin
from typing import Optional, List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class IntelligentURLDiscovery:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def discover_document_url(self, title: str, author_org: str = "", doc_type: str = "", content_preview: str = "") -> Optional[str]:
        """
        Discover the original URL for a document using intelligent search strategies
        """
        # Strategy 1: Government document patterns
        if gov_url := self._search_government_sources(title, author_org):
            return gov_url
            
        # Strategy 2: Standards body patterns  
        if standards_url := self._search_standards_bodies(title, author_org):
            return standards_url
            
        # Strategy 3: Academic/research patterns
        if academic_url := self._search_academic_sources(title, author_org):
            return academic_url
            
        # Strategy 4: Generic web search with validation
        if web_url := self._search_web_sources(title, author_org, doc_type):
            return web_url
            
        return None
    
    def _search_government_sources(self, title: str, author_org: str) -> Optional[str]:
        """Search government and agency websites"""
        # Government domain mappings
        gov_domains = {
            'nist': ['nist.gov', 'csrc.nist.gov', 'nvlpubs.nist.gov'],
            'cisa': ['cisa.gov', 'us-cert.cisa.gov'],
            'dhs': ['dhs.gov'],
            'white house': ['whitehouse.gov'],
            'dod': ['defense.gov', 'disa.mil'],
            'nasa': ['nasa.gov'],
            'nsf': ['nsf.gov'],
            'commerce': ['commerce.gov'],
            'nsa': ['nsa.gov'],
            'fbi': ['fbi.gov'],
            'treasury': ['treasury.gov'],
            'state': ['state.gov']
        }
        
        org_lower = author_org.lower()
        title_clean = self._clean_title_for_search(title)
        
        # Find matching government domains
        matching_domains = []
        for org_key, domains in gov_domains.items():
            if org_key in org_lower:
                matching_domains.extend(domains)
        
        # Search each domain
        for domain in matching_domains:
            if url := self._search_domain_for_document(domain, title_clean, title):
                return url
                
        return None
    
    def _search_standards_bodies(self, title: str, author_org: str) -> Optional[str]:
        """Search standards organizations"""
        standards_domains = {
            'iso': ['iso.org'],
            'ieee': ['ieee.org', 'ieeexplore.ieee.org'],
            'ietf': ['ietf.org', 'tools.ietf.org'],
            'w3c': ['w3.org'],
            'oasis': ['oasis-open.org'],
            'itut': ['itu.int'],
            'ansi': ['ansi.org']
        }
        
        org_lower = author_org.lower()
        title_clean = self._clean_title_for_search(title)
        
        matching_domains = []
        for org_key, domains in standards_domains.items():
            if org_key in org_lower:
                matching_domains.extend(domains)
        
        for domain in matching_domains:
            if url := self._search_domain_for_document(domain, title_clean, title):
                return url
                
        return None
    
    def _search_academic_sources(self, title: str, author_org: str) -> Optional[str]:
        """Search academic and research sources"""
        academic_domains = [
            'arxiv.org',
            'acm.org',
            'springer.com', 
            'sciencedirect.com',
            'researchgate.net',
            'semanticscholar.org'
        ]
        
        title_clean = self._clean_title_for_search(title)
        
        for domain in academic_domains:
            if url := self._search_domain_for_document(domain, title_clean, title):
                return url
                
        return None
    
    def _search_web_sources(self, title: str, author_org: str, doc_type: str) -> Optional[str]:
        """Search general web sources with validation"""
        # Build search queries
        queries = self._build_search_queries(title, author_org, doc_type)
        
        for query in queries:
            if url := self._search_with_validation(query, title):
                return url
                
        return None
    
    def _clean_title_for_search(self, title: str) -> str:
        """Clean title for better search results"""
        # Remove common prefixes/suffixes
        title = re.sub(r'^(The\s+|A\s+|An\s+)', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s+(Report|Document|Policy|Framework|Guidelines?|Standards?)$', '', title, flags=re.IGNORECASE)
        
        # Remove version numbers and dates
        title = re.sub(r'\s+v?\d+(\.\d+)*\s*$', '', title)
        title = re.sub(r'\s+\(\d{4}\)', '', title)
        
        # Clean special characters for URL searching
        title = re.sub(r'[^\w\s\-]', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        
        return title
    
    def _build_search_queries(self, title: str, author_org: str, doc_type: str) -> List[str]:
        """Build intelligent search queries"""
        queries = []
        
        title_clean = self._clean_title_for_search(title)
        
        # Primary query with organization
        if author_org and author_org != "Unknown":
            queries.append(f'"{title_clean}" site:{author_org.lower().replace(" ", "")}')
            queries.append(f'"{title_clean}" "{author_org}" filetype:pdf')
        
        # Document type specific queries
        if doc_type and doc_type != "Unknown":
            queries.append(f'"{title_clean}" "{doc_type}" filetype:pdf')
        
        # Generic queries
        queries.append(f'"{title_clean}" filetype:pdf')
        queries.append(f'{title_clean} official document')
        
        return queries
    
    def _search_domain_for_document(self, domain: str, title_clean: str, original_title: str) -> Optional[str]:
        """Search specific domain for document"""
        try:
            # Try different search patterns
            search_patterns = [
                f'site:{domain} "{title_clean}"',
                f'site:{domain} {title_clean.replace(" ", "+")}',
                f'site:{domain} "{original_title}"'
            ]
            
            for pattern in search_patterns:
                # Use DuckDuckGo or similar search API if available
                # For now, construct likely URLs based on domain patterns
                if probable_url := self._construct_probable_url(domain, title_clean):
                    if self._validate_url_content(probable_url, original_title):
                        return probable_url
                        
        except Exception as e:
            logger.warning(f"Error searching domain {domain}: {e}")
            
        return None
    
    def _construct_probable_url(self, domain: str, title_clean: str) -> Optional[str]:
        """Construct probable URLs based on domain patterns"""
        title_slug = title_clean.lower().replace(' ', '-').replace('_', '-')
        title_slug = re.sub(r'[^\w\-]', '', title_slug)
        
        # Domain-specific URL patterns
        url_patterns = {
            'nist.gov': [
                f'https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.{title_slug}.pdf',
                f'https://csrc.nist.gov/publications/detail/{title_slug}',
                f'https://www.nist.gov/publications/{title_slug}'
            ],
            'cisa.gov': [
                f'https://www.cisa.gov/resources-tools/{title_slug}',
                f'https://www.cisa.gov/sites/default/files/publications/{title_slug}.pdf'
            ],
            'whitehouse.gov': [
                f'https://www.whitehouse.gov/briefing-room/statements-releases/{title_slug}/',
                f'https://www.whitehouse.gov/wp-content/uploads/{title_slug}.pdf'
            ]
        }
        
        if domain in url_patterns:
            for pattern in url_patterns[domain]:
                try:
                    response = self.session.head(pattern, timeout=5)
                    if response.status_code == 200:
                        return pattern
                except:
                    continue
                    
        return None
    
    def _search_with_validation(self, query: str, title: str) -> Optional[str]:
        """Search web with content validation"""
        # This would integrate with a search API
        # For now, return None as we need search API credentials
        return None
    
    def _validate_url_content(self, url: str, expected_title: str) -> bool:
        """Validate that URL contains expected document content"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return False
                
            content = response.text.lower()
            title_words = expected_title.lower().split()
            
            # Check if significant portion of title words appear in content
            matches = sum(1 for word in title_words if len(word) > 3 and word in content)
            match_ratio = matches / len([w for w in title_words if len(w) > 3])
            
            return match_ratio > 0.6  # 60% of title words must match
            
        except Exception as e:
            logger.warning(f"Error validating URL {url}: {e}")
            return False

# Global instance
url_discovery = IntelligentURLDiscovery()

def discover_document_source_url(title: str, author_org: str = "", doc_type: str = "", content_preview: str = "") -> Optional[str]:
    """
    Main function to discover document source URL
    """
    return url_discovery.discover_document_url(title, author_org, doc_type, content_preview)