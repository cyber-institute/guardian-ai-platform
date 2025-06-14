"""
Self-Healing URL System
Automatically discovers, validates, and fixes broken document URLs using intelligent search strategies
"""

import logging
import psycopg2
import os
import time
from typing import Dict, List, Optional, Tuple
import re
from urllib.parse import urlparse, urljoin
import requests
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.url_validator import URLValidator
except ImportError:
    # Fallback URL validator if import fails
    class URLValidator:
        def __init__(self):
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
        
        def validate_url(self, url):
            try:
                response = self.session.head(url, timeout=10, allow_redirects=True)
                if 200 <= response.status_code < 400:
                    return True, "Valid", response.url if response.url != url else None
                else:
                    return False, f"HTTP {response.status_code}", None
            except:
                return False, "Connection failed", None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SelfHealingURLSystem:
    def __init__(self):
        self.validator = URLValidator()
        self.trusted_domains = {
            'nist.gov', 'nvlpubs.nist.gov', 'cisa.gov', 'whitehouse.gov',
            'nasa.gov', 'nsa.gov', 'doi.org', 'arxiv.org', 'acm.org',
            'ieee.org', 'iso.org', 'ietf.org', 'w3.org', 'ncbi.nlm.nih.gov'
        }
        
    def heal_all_urls(self) -> Dict[str, int]:
        """
        Automatically heal all broken or missing URLs in the database
        Returns: {'healed': count, 'failed': count, 'skipped': count}
        """
        try:
            conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
            cursor = conn.cursor()
            
            # Get documents that need URL healing
            cursor.execute("""
                SELECT id, title, author_organization, content, source, url_valid, url_status
                FROM documents 
                WHERE (source IS NULL OR source = '' OR url_valid = false OR url_valid IS NULL)
                AND title IS NOT NULL
                ORDER BY id
            """)
            
            documents = cursor.fetchall()
            logger.info(f"Found {len(documents)} documents needing URL healing")
            
            stats = {'healed': 0, 'failed': 0, 'skipped': 0}
            
            for doc_id, title, org, content, current_url, url_valid, url_status in documents:
                try:
                    logger.info(f"Healing URL for: {title[:50]}...")
                    
                    # Try multiple healing strategies
                    new_url = self._heal_document_url(title, org or '', content or '', current_url)
                    
                    if new_url:
                        # Validate the discovered URL
                        is_valid, status, redirect = self.validator.validate_url(new_url)
                        
                        if is_valid:
                            # Update database with healed URL
                            final_url = redirect if redirect else new_url
                            
                            cursor.execute("""
                                UPDATE documents 
                                SET source = %s,
                                    url_valid = true,
                                    url_status = %s,
                                    url_checked = CURRENT_TIMESTAMP,
                                    source_redirect = %s
                                WHERE id = %s
                            """, (new_url, status, redirect, doc_id))
                            
                            conn.commit()
                            stats['healed'] += 1
                            logger.info(f"✓ Healed: {title[:40]} -> {final_url}")
                        else:
                            stats['failed'] += 1
                            logger.warning(f"✗ Found URL but invalid: {new_url} ({status})")
                    else:
                        stats['failed'] += 1
                        logger.warning(f"✗ Could not find URL for: {title[:40]}")
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    stats['failed'] += 1
                    logger.error(f"Error healing URL for {title}: {e}")
            
            cursor.close()
            conn.close()
            
            logger.info(f"URL healing complete: {stats['healed']} healed, {stats['failed']} failed")
            return stats
            
        except Exception as e:
            logger.error(f"Database error during URL healing: {e}")
            return {'healed': 0, 'failed': 0, 'skipped': 0}
    
    def _heal_document_url(self, title: str, organization: str, content: str, current_url: str = None) -> Optional[str]:
        """
        Heal a single document URL using multiple strategies
        """
        # Strategy 1: Build intelligent URL patterns first (most reliable)
        pattern_url = self._build_intelligent_url_pattern(title, organization)
        if pattern_url:
            return pattern_url
        
        # Strategy 2: Try fixing common URL patterns
        if current_url:
            fixed_url = self._fix_common_url_issues(current_url, title, organization)
            if fixed_url and fixed_url != current_url:
                return fixed_url
        
        # Strategy 3: Extract URLs from content
        content_url = self._extract_url_from_content(content, title)
        if content_url and self._is_trusted_domain(content_url):
            return content_url
        
        return None
    
    def _fix_common_url_issues(self, url: str, title: str, organization: str) -> Optional[str]:
        """
        Fix common URL issues like broken paths, outdated domains, etc.
        """
        if not url or not url.startswith('http'):
            return None
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Fix common NIST URL patterns
        if 'nist' in domain or 'nist' in organization.lower():
            # Try different NIST URL patterns
            patterns = [
                f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/{self._extract_nist_id(title, url)}.pdf",
                f"https://doi.org/10.6028/{self._extract_nist_id(title, url)}",
                f"https://csrc.nist.gov/publications/detail/sp/{self._extract_sp_number(title)}/final"
            ]
            
            for pattern in patterns:
                if pattern and 'None' not in pattern:
                    return pattern
        
        # Fix common CISA URL patterns  
        if 'cisa' in domain or 'cisa' in organization.lower():
            # Try updated CISA paths
            filename = self._extract_filename_from_title(title)
            if filename:
                return f"https://www.cisa.gov/sites/default/files/publications/{filename}.pdf"
        
        # Fix whitehouse.gov patterns
        if 'whitehouse.gov' in domain:
            # Try different whitehouse patterns
            if 'quantum' in title.lower():
                return "https://www.whitehouse.gov/briefing-room/presidential-actions/2022/05/04/national-security-memorandum-on-promoting-united-states-leadership-in-quantum-computing-while-mitigating-risks-to-vulnerable-cryptographic-systems/"
        
        # Try HTTPS upgrade if HTTP
        if url.startswith('http://'):
            return url.replace('http://', 'https://')
        
        return None
    
    def _extract_url_from_content(self, content: str, title: str) -> Optional[str]:
        """
        Extract potential URLs from document content
        """
        if not content:
            return None
        
        # Look for URLs in content
        url_patterns = [
            r'https?://[^\s<>"]{20,}\.pdf',
            r'https?://doi\.org/[^\s<>"]+',
            r'https?://nvlpubs\.nist\.gov/[^\s<>"]+',
            r'https?://www\.cisa\.gov/[^\s<>"]+',
            r'https?://www\.whitehouse\.gov/[^\s<>"]+',
        ]
        
        for pattern in url_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if self._is_relevant_url(match, title):
                    return match.strip('.,;')
        
        return None
    
    def _build_intelligent_url_pattern(self, title: str, organization: str) -> Optional[str]:
        """
        Build intelligent URL patterns based on document metadata
        """
        title_lower = title.lower()
        org_lower = organization.lower()
        
        # NIST patterns
        if 'nist' in org_lower or 'nist' in title_lower:
            sp_match = re.search(r'sp\s*800[-\s]*(\d+)([a-z]?)', title_lower)
            if sp_match:
                sp_num = sp_match.group(1)
                sp_suffix = sp_match.group(2) or ''
                return f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-{sp_num}{sp_suffix}.pdf"
            
            # AI framework
            if 'ai risk management' in title_lower or 'ai rmf' in title_lower:
                return "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf"
        
        # CISA patterns
        if 'cisa' in org_lower or 'cisa' in title_lower:
            if 'ai cybersecurity' in title_lower:
                return "https://www.cisa.gov/sites/default/files/publications/ai-cybersecurity-collaboration-playbook.pdf"
            if 'secure ai' in title_lower and 'development' in title_lower:
                return "https://www.cisa.gov/news-events/news/guidelines-secure-ai-system-development"
        
        # NASA patterns
        if 'nasa' in org_lower:
            if 'responsible ai' in title_lower:
                return "https://ntrs.nasa.gov/api/citations/20220013471/downloads/RAI%20Plan%20Sept%201%202022.pdf"
        
        # Whitehouse patterns
        if 'white house' in org_lower or 'whitehouse' in org_lower:
            if 'quantum' in title_lower:
                return "https://www.whitehouse.gov/briefing-room/presidential-actions/2022/05/04/national-security-memorandum-on-promoting-united-states-leadership-in-quantum-computing-while-mitigating-risks-to-vulnerable-cryptographic-systems/"
        
        return None
    
    def _extract_nist_id(self, title: str, url: str = '') -> Optional[str]:
        """Extract NIST publication ID from title or URL"""
        # Look in title first
        patterns = [
            r'NIST\.?SP\.?800[-\s]*(\d+)([a-zA-Z]?)',
            r'SP\s*800[-\s]*(\d+)([a-zA-Z]?)',
            r'800[-\s]*(\d+)([a-zA-Z]?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                return f"NIST.SP.800-{match.group(1)}{match.group(2).lower()}"
        
        # Look in URL if provided
        if url:
            match = re.search(r'NIST\.SP\.800[-\.](\d+)([a-zA-Z]?)', url, re.IGNORECASE)
            if match:
                return f"NIST.SP.800-{match.group(1)}{match.group(2).lower()}"
        
        return None
    
    def _extract_sp_number(self, title: str) -> Optional[str]:
        """Extract SP number from title"""
        match = re.search(r'sp\s*800[-\s]*(\d+)', title, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_filename_from_title(self, title: str) -> Optional[str]:
        """Generate filename from title"""
        # Convert title to potential filename
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'\s+', '-', filename.strip())
        return filename[:50] if filename else None
    
    def _is_trusted_domain(self, url: str) -> bool:
        """Check if URL is from a trusted domain"""
        try:
            domain = urlparse(url).netloc.lower()
            return any(trusted in domain for trusted in self.trusted_domains)
        except:
            return False
    
    def _is_relevant_url(self, url: str, title: str) -> bool:
        """Check if URL is relevant to the document title"""
        url_lower = url.lower()
        title_words = set(re.findall(r'\b\w{3,}\b', title.lower()))
        
        # Check for key terms in URL
        relevant_count = sum(1 for word in title_words if word in url_lower)
        return relevant_count >= 2 or any(word in url_lower for word in ['nist', 'cisa', 'ai', 'quantum', 'security'])
    
    def schedule_periodic_healing(self):
        """
        Schedule periodic URL healing (would be called by a scheduler)
        """
        logger.info("Starting scheduled URL healing...")
        stats = self.heal_all_urls()
        logger.info(f"Scheduled healing complete: {stats}")
        return stats

def heal_all_document_urls():
    """
    Main function to heal all document URLs
    """
    healer = SelfHealingURLSystem()
    return healer.heal_all_urls()

if __name__ == "__main__":
    # Run URL healing
    stats = heal_all_document_urls()
    print(f"URL Healing Results: {stats}")