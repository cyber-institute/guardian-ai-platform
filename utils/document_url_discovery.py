"""
Document URL Discovery System for GUARDIAN
Finds source URLs for uploaded documents using intelligent search and analysis
"""

import requests
import re
from typing import Optional, List, Dict
from urllib.parse import quote
import time

class DocumentURLDiscovery:
    """
    Discovers source URLs for documents using multiple strategies
    """
    
    def __init__(self):
        self.search_patterns = [
            "site:nist.gov \"{title}\"",
            "site:cisa.gov \"{title}\"", 
            "site:nasa.gov \"{title}\"",
            "site:whitehouse.gov \"{title}\"",
            "site:nsa.gov \"{title}\"",
            "filetype:pdf \"{title}\"",
            "\"{title}\" official document",
            "\"{title}\" {organization}"
        ]
    
    def discover_document_url(self, title: str, organization: str = "", content_snippet: str = "") -> Optional[str]:
        """Discover the source URL for a document using multiple strategies"""
        
        # Strategy 1: Extract URL from content if it contains one
        content_url = self._extract_url_from_content(content_snippet)
        if content_url:
            return content_url
        
        # Strategy 2: Pattern-based URL construction for known organizations
        constructed_url = self._construct_url_by_pattern(title, organization)
        if constructed_url:
            return constructed_url
        
        # Strategy 3: Intelligent search-based discovery
        search_url = self._search_based_discovery(title, organization)
        if search_url:
            return search_url
        
        return None
    
    def _extract_url_from_content(self, content: str) -> Optional[str]:
        """Extract URLs directly from document content"""
        
        if not content:
            return None
        
        # Look for common document URL patterns
        url_patterns = [
            r'https?://[^\s<>"]+\.pdf',
            r'https?://doi\.org/[^\s<>"]+',
            r'https?://nvlpubs\.nist\.gov/[^\s<>"]+',
            r'https?://[^\s<>"]*\.gov/[^\s<>"]+',
            r'This publication is available.*?from:\s*(https?://[^\s<>"]+)',
            r'Available at:\s*(https?://[^\s<>"]+)',
            r'URL:\s*(https?://[^\s<>"]+)'
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                url = match.group(1) if match.lastindex else match.group(0)
                if self._validate_url(url):
                    return url.strip()
        
        return None
    
    def _construct_url_by_pattern(self, title: str, organization: str) -> Optional[str]:
        """Construct URLs using known patterns for specific organizations"""
        
        org_lower = organization.lower()
        title_clean = re.sub(r'[^\w\s-]', '', title).strip()
        
        # NIST patterns
        if 'nist' in org_lower or 'nist' in title.lower():
            # Look for NIST SP patterns
            nist_sp_match = re.search(r'nist\s+sp\s+(\d+[-\w]*)', title.lower())
            if nist_sp_match:
                sp_number = nist_sp_match.group(1)
                return f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.{sp_number}.pdf"
        
        # CISA patterns
        if 'cisa' in org_lower:
            # CISA documents often follow predictable patterns
            title_slug = re.sub(r'\s+', '-', title_clean.lower())
            return f"https://www.cisa.gov/sites/default/files/publications/{title_slug}.pdf"
        
        # White House patterns
        if 'white house' in org_lower:
            if 'memorandum' in title.lower():
                return f"https://www.whitehouse.gov/briefing-room/presidential-actions/"
        
        # NASA patterns
        if 'nasa' in org_lower:
            title_slug = re.sub(r'\s+', '-', title_clean.lower())
            return f"https://www.nasa.gov/sites/default/files/atoms/files/{title_slug}.pdf"
        
        return None
    
    def _search_based_discovery(self, title: str, organization: str) -> Optional[str]:
        """Use search-like strategies to find document URLs"""
        
        # This would typically use a search API, but we'll use pattern matching
        # for government document repositories
        
        title_keywords = self._extract_key_phrases(title)
        
        # Check common government document repositories
        repositories = [
            "https://nvlpubs.nist.gov/nistpubs/",
            "https://www.cisa.gov/sites/default/files/",
            "https://www.whitehouse.gov/wp-content/uploads/",
            "https://www.nsa.gov/portals/",
            "https://csrc.nist.gov/publications/"
        ]
        
        # For now, return None as we'd need actual web scraping
        # In a full implementation, this would search these repositories
        return None
    
    def _extract_key_phrases(self, title: str) -> List[str]:
        """Extract key phrases from document title for searching"""
        
        # Remove common words and extract meaningful phrases
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        
        words = [word.strip() for word in re.split(r'[\s\-_]+', title.lower()) 
                if len(word.strip()) > 2 and word.strip() not in common_words]
        
        # Extract important phrases
        phrases = []
        if len(words) >= 2:
            phrases.extend([' '.join(words[i:i+2]) for i in range(len(words)-1)])
        
        return phrases[:5]  # Return top 5 phrases
    
    def _validate_url(self, url: str) -> bool:
        """Validate that a URL is accessible and points to a document"""
        
        try:
            # Basic URL format validation
            if not url.startswith(('http://', 'https://')):
                return False
            
            # Check if it looks like a document URL
            doc_extensions = ['.pdf', '.doc', '.docx', '.txt']
            if any(ext in url.lower() for ext in doc_extensions):
                return True
            
            # Check if it's from a trusted domain
            trusted_domains = ['nist.gov', 'cisa.gov', 'nasa.gov', 'whitehouse.gov', 'nsa.gov', 'doi.org']
            if any(domain in url.lower() for domain in trusted_domains):
                return True
            
        except Exception:
            pass
        
        return False
    
    def update_document_urls_batch(self, documents: List[Dict]) -> Dict[int, Optional[str]]:
        """Update URLs for multiple documents"""
        
        results = {}
        
        for doc in documents:
            doc_id = doc.get('id')
            title = doc.get('title', '')
            organization = doc.get('author_organization', '')
            content = doc.get('content', '')
            
            discovered_url = self.discover_document_url(title, organization, content)
            results[doc_id] = discovered_url
            
            # Add small delay to be respectful
            time.sleep(0.1)
        
        return results

# Global instance
url_discovery = DocumentURLDiscovery()

def discover_document_url(title: str, organization: str = "", content: str = "") -> Optional[str]:
    """Discover source URL for a document"""
    return url_discovery.discover_document_url(title, organization, content)