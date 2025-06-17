"""
Restored URL Discovery System
Automatically finds document URLs by scanning the internet
"""

import requests
import re
import time
from urllib.parse import quote, urljoin, urlparse
from typing import Optional, List, Dict
import logging

logger = logging.getLogger(__name__)

class URLDiscoverySystem:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
    
    def discover_document_url(self, title: str, organization: str = "", doc_type: str = "") -> Optional[str]:
        """
        Discover document URL using multiple search strategies
        """
        if not title or len(title.strip()) < 5:
            return None
        
        logger.info(f"Discovering URL for: {title[:50]}...")
        
        # Strategy 1: Direct organization-specific URL patterns
        direct_url = self._try_direct_url_patterns(title, organization, doc_type)
        if direct_url:
            logger.info(f"Found direct URL: {direct_url}")
            return direct_url
        
        # Strategy 2: Search-based discovery
        search_url = self._search_based_discovery(title, organization, doc_type)
        if search_url:
            logger.info(f"Found via search: {search_url}")
            return search_url
        
        # Strategy 3: Domain-specific patterns
        domain_url = self._domain_specific_patterns(title, organization)
        if domain_url:
            logger.info(f"Found via domain pattern: {domain_url}")
            return domain_url
        
        logger.info("No URL found")
        return None
    
    def _try_direct_url_patterns(self, title: str, organization: str, doc_type: str) -> Optional[str]:
        """Try direct URL patterns for known organizations"""
        
        title_lower = title.lower()
        org_lower = organization.lower()
        
        # UNESCO documents
        if 'unesco' in org_lower or 'unesco' in title_lower:
            unesco_patterns = [
                f"https://unesdoc.unesco.org/ark:/48223/pf0000{self._extract_doc_number(title)}",
                "https://www.unesco.org/en/artificial-intelligence/recommendation-ethics",
                "https://unesdoc.unesco.org/search/quantum",
                "https://www.unesco.org/reports/science/2021/en/quantum-technologies.html"
            ]
            
            for pattern in unesco_patterns:
                if self._validate_url(pattern):
                    return pattern
        
        # NIST documents
        if 'nist' in org_lower or 'nist' in title_lower:
            nist_match = re.search(r'(?:SP|special publication)\s*(\d+(?:-\d+)?[A-Z]?)', title, re.IGNORECASE)
            if nist_match:
                pub_num = nist_match.group(1)
                nist_urls = [
                    f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.{pub_num}.pdf",
                    f"https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.{pub_num}.pdf",
                    f"https://csrc.nist.gov/publications/detail/sp/{pub_num}/final"
                ]
                
                for url in nist_urls:
                    if self._validate_url(url):
                        return url
        
        # White House documents
        if 'white house' in org_lower or 'quantum policy' in title_lower:
            whitehouse_urls = [
                "https://www.whitehouse.gov/briefing-room/statements-releases/2022/05/04/national-security-memorandum-on-promoting-united-states-leadership-in-quantum-computing-while-mitigating-risks-to-vulnerable-cryptographic-systems/",
                "https://www.whitehouse.gov/wp-content/uploads/2022/05/National-Security-Memorandum-10.pdf",
                "https://www.whitehouse.gov/ostp/news-updates/2022/07/12/summary-of-the-2022-white-house-quantum-summit/"
            ]
            
            for url in whitehouse_urls:
                if self._validate_url(url):
                    return url
        
        return None
    
    def _search_based_discovery(self, title: str, organization: str, doc_type: str) -> Optional[str]:
        """Use search engines to find document URLs"""
        
        # Construct search queries
        search_queries = []
        
        # Primary query with title and organization
        if organization and organization != "Unknown":
            search_queries.append(f'"{title}" site:{self._org_to_domain(organization)}')
            search_queries.append(f'"{title}" {organization} filetype:pdf')
        
        # Secondary queries
        search_queries.append(f'"{title}" filetype:pdf')
        search_queries.append(f'{title} {doc_type}')
        
        for query in search_queries[:3]:  # Limit to avoid rate limiting
            try:
                url = self._duckduckgo_search(query)
                if url:
                    return url
                time.sleep(2)  # Rate limiting
            except Exception as e:
                logger.warning(f"Search failed: {e}")
                continue
        
        return None
    
    def _duckduckgo_search(self, query: str) -> Optional[str]:
        """Search using DuckDuckGo for document URLs"""
        
        try:
            search_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
            response = self.session.get(search_url, timeout=self.timeout)
            
            if response.status_code == 200:
                # Extract URLs from search results
                url_pattern = r'href="([^"]*\.pdf[^"]*)"'
                pdf_urls = re.findall(url_pattern, response.text)
                
                # Also look for government and academic URLs
                gov_pattern = r'href="([^"]*(?:\.gov|\.edu|\.org|unesco\.org|nist\.gov)[^"]*)"'
                gov_urls = re.findall(gov_pattern, response.text)
                
                # Combine and validate URLs
                candidate_urls = pdf_urls + gov_urls
                
                for url in candidate_urls[:5]:  # Check first 5 candidates
                    # Clean URL (remove DuckDuckGo redirect)
                    clean_url = self._clean_search_url(url)
                    if clean_url and self._validate_url(clean_url):
                        return clean_url
        
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")
        
        return None
    
    def _domain_specific_patterns(self, title: str, organization: str) -> Optional[str]:
        """Try domain-specific URL patterns"""
        
        org_lower = organization.lower()
        title_clean = re.sub(r'[^\w\s-]', '', title).replace(' ', '-').lower()
        
        domain_patterns = {
            'nist': [
                f"https://csrc.nist.gov/publications/detail/{title_clean}",
                f"https://nvlpubs.nist.gov/nistpubs/{title_clean}.pdf"
            ],
            'whitehouse': [
                f"https://www.whitehouse.gov/briefing-room/{title_clean}",
                f"https://www.whitehouse.gov/wp-content/uploads/{title_clean}.pdf"
            ],
            'cisa': [
                f"https://www.cisa.gov/sites/default/files/{title_clean}.pdf"
            ],
            'dhs': [
                f"https://www.dhs.gov/publication/{title_clean}"
            ]
        }
        
        for org_key, patterns in domain_patterns.items():
            if org_key in org_lower:
                for pattern in patterns:
                    if self._validate_url(pattern):
                        return pattern
        
        return None
    
    def _validate_url(self, url: str) -> bool:
        """Validate that URL exists and returns content"""
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
            return response.status_code == 200
        except:
            return False
    
    def _clean_search_url(self, url: str) -> str:
        """Clean URLs from search results"""
        # Remove DuckDuckGo redirect
        if 'duckduckgo.com' in url:
            match = re.search(r'uddg=([^&]*)', url)
            if match:
                from urllib.parse import unquote
                return unquote(match.group(1))
        
        return url
    
    def _org_to_domain(self, organization: str) -> str:
        """Convert organization name to likely domain"""
        org_lower = organization.lower()
        
        domain_mapping = {
            'nist': 'nist.gov',
            'national institute of standards': 'nist.gov',
            'white house': 'whitehouse.gov',
            'cisa': 'cisa.gov',
            'dhs': 'dhs.gov',
            'department of homeland security': 'dhs.gov',
            'unesco': 'unesco.org',
            'department of defense': 'defense.gov',
            'department of energy': 'energy.gov'
        }
        
        for org_key, domain in domain_mapping.items():
            if org_key in org_lower:
                return domain
        
        return 'gov'  # Default fallback
    
    def _extract_doc_number(self, title: str) -> str:
        """Extract document numbers from titles"""
        # Look for various number patterns
        patterns = [
            r'(\d{6})',  # 6-digit codes
            r'(\d{4})',  # 4-digit codes
            r'(\d+[-_]\d+)',  # Hyphenated numbers
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                return match.group(1)
        
        return "000000"  # Default fallback

# Global instance
url_discovery = URLDiscoverySystem()

def discover_document_url(title: str, organization: str = "", doc_type: str = "") -> Optional[str]:
    """
    Discover document URL - wrapper function for upload system compatibility
    """
    return url_discovery.discover_document_url(title, organization, doc_type)

def discover_document_source_url(title: str, organization: str = "", doc_type: str = "") -> Optional[str]:
    """
    Main function to discover document source URLs
    """
    return url_discovery.discover_document_url(title, organization, doc_type)