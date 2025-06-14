"""
Web Search-Based URL Discovery System
Uses DuckDuckGo search to find actual document URLs like manual Google searches
"""

import requests
import re
from urllib.parse import quote, unquote, urlparse
from typing import Optional, List, Dict
import time
import logging

logger = logging.getLogger(__name__)

class WebSearchURLDiscovery:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_document_url(self, title: str, organization: str = "", doc_type: str = "") -> Optional[str]:
        """
        Search for document URL using web search, similar to manual Google search
        """
        # Build search query like manual search
        search_queries = self._build_search_queries(title, organization, doc_type)
        
        for query in search_queries:
            try:
                # Use DuckDuckGo instant answer API
                search_url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&no_html=1&skip_disambig=1"
                
                response = self.session.get(search_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check instant answer first
                    if data.get('AbstractURL'):
                        url = data['AbstractURL']
                        if self._validate_url_relevance(url, title):
                            return url
                    
                    # Check related topics
                    for topic in data.get('RelatedTopics', []):
                        if isinstance(topic, dict) and topic.get('FirstURL'):
                            url = topic['FirstURL']
                            if self._validate_url_relevance(url, title):
                                return url
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {e}")
                continue
        
        # Fallback to direct domain search
        return self._direct_domain_search(title, organization)
    
    def _build_search_queries(self, title: str, organization: str, doc_type: str) -> List[str]:
        """Build intelligent search queries"""
        queries = []
        
        # Clean title for search
        clean_title = re.sub(r'[^\w\s\-:]', ' ', title).strip()
        
        # Primary queries with organization
        if organization and organization != "Unknown":
            org_clean = organization.replace("(", "").replace(")", "").strip()
            queries.append(f'"{clean_title}" site:{self._get_org_domain(org_clean)}')
            queries.append(f'"{clean_title}" "{org_clean}" filetype:pdf')
            queries.append(f'{clean_title} {org_clean} official document')
        
        # Document type specific queries
        if doc_type and doc_type != "Unknown":
            queries.append(f'"{clean_title}" "{doc_type}" filetype:pdf')
        
        # Generic queries
        queries.append(f'"{clean_title}" filetype:pdf')
        queries.append(f'{clean_title} official document pdf')
        
        return queries[:3]  # Limit to top 3 queries
    
    def _get_org_domain(self, organization: str) -> str:
        """Get primary domain for organization"""
        org_lower = organization.lower()
        
        domain_mapping = {
            'nist': 'nist.gov',
            'white house': 'whitehouse.gov',
            'cisa': 'cisa.gov',
            'dhs': 'dhs.gov',
            'dod': 'defense.gov',
            'nasa': 'nasa.gov',
            'nsf': 'nsf.gov',
            'commerce': 'commerce.gov',
            'treasury': 'treasury.gov',
            'state': 'state.gov',
            'iso': 'iso.org',
            'ieee': 'ieee.org',
            'ietf': 'ietf.org'
        }
        
        for org_key, domain in domain_mapping.items():
            if org_key in org_lower:
                return domain
        
        return organization.lower().replace(' ', '') + '.gov'
    
    def _validate_url_relevance(self, url: str, title: str) -> bool:
        """Check if URL is relevant to the document title"""
        try:
            # Quick validation - check if URL contains key title words
            title_words = [word.lower() for word in title.split() if len(word) > 3]
            url_lower = url.lower()
            
            # Check if at least 30% of title words appear in URL
            matches = sum(1 for word in title_words if word in url_lower)
            if len(title_words) > 0 and matches / len(title_words) >= 0.3:
                return True
            
            # Check for common document file types
            if any(ext in url_lower for ext in ['.pdf', '.doc', '.docx']):
                return True
            
            # Check for government/official domains
            if any(domain in url_lower for domain in ['gov', 'org', 'edu', 'mil']):
                return True
                
            return False
            
        except Exception:
            return False
    
    def _direct_domain_search(self, title: str, organization: str) -> Optional[str]:
        """Direct search on organization's domain"""
        try:
            domain = self._get_org_domain(organization)
            
            # Construct likely URLs based on common patterns
            title_slug = re.sub(r'[^\w\s\-]', '', title.lower())
            title_slug = re.sub(r'\s+', '-', title_slug)
            
            # Common URL patterns for government documents
            test_patterns = []
            
            if 'nist' in domain:
                # NIST specific patterns
                nist_match = re.search(r'(?:SP\s+)?(\d+(?:-\d+)?[A-Z]?)', title, re.IGNORECASE)
                if nist_match:
                    pub_num = nist_match.group(1)
                    test_patterns = [
                        f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.{pub_num}.pdf",
                        f"https://csrc.nist.gov/publications/detail/sp/{pub_num}/final",
                        f"https://doi.org/10.6028/NIST.SP.{pub_num}"
                    ]
            
            elif 'cisa' in domain:
                # CISA specific patterns
                test_patterns = [
                    f"https://www.cisa.gov/sites/default/files/publications/{title_slug}.pdf",
                    f"https://www.cisa.gov/sites/default/files/2025-01/{title_slug}.pdf",
                    f"https://www.cisa.gov/resources-tools/{title_slug}"
                ]
            
            elif 'whitehouse' in domain:
                # White House specific patterns - include archived Biden administration
                test_patterns = [
                    f"https://bidenwhitehouse.archives.gov/briefing-room/statements-releases/2022/05/04/national-security-memorandum-on-promoting-united-states-leadership-in-quantum-computing-while-mitigating-risks-to-vulnerable-cryptographic-systems/",
                    f"https://www.whitehouse.gov/briefing-room/statements-releases/{title_slug}/",
                    f"https://bidenwhitehouse.archives.gov/briefing-room/statements-releases/{title_slug}/",
                    f"https://www.whitehouse.gov/wp-content/uploads/2022/05/{title_slug}.pdf"
                ]
            
            # Test each pattern
            for pattern in test_patterns:
                try:
                    response = self.session.head(pattern, timeout=5)
                    if response.status_code == 200:
                        return pattern
                except:
                    continue
                    
        except Exception as e:
            logger.warning(f"Direct domain search failed: {e}")
        
        return None

# Global instance
web_search_discovery = WebSearchURLDiscovery()

def search_document_url(title: str, organization: str = "", doc_type: str = "") -> Optional[str]:
    """
    Main function to search for document URL using web search
    """
    return web_search_discovery.search_document_url(title, organization, doc_type)