"""
URL Validation System for Document Links
Validates that URLs are accessible and return valid content before making them clickable
"""

import requests
import logging
from typing import Dict, Optional, Tuple
import time
from urllib.parse import urlparse
import psycopg2
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class URLValidator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
        self.verified_urls = set()
        self.broken_urls = set()
        
    def validate_url(self, url: str) -> Tuple[bool, str, Optional[str]]:
        """
        Validate a single URL
        Returns: (is_valid, status_message, redirect_url)
        """
        if not url or not url.strip():
            return False, "Empty URL", None
            
        url = url.strip()
        
        # Check cache first
        if url in self.verified_urls:
            return True, "Previously verified", None
        if url in self.broken_urls:
            return False, "Previously failed", None
            
        try:
            # Parse URL to ensure it's valid
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL format", None
                
            logger.info(f"Validating URL: {url}")
            
            # Make HEAD request first (faster)
            try:
                response = self.session.head(url, timeout=self.timeout, allow_redirects=True)
                status_code = response.status_code
                final_url = response.url
                
                # If HEAD is not allowed, try GET
                if status_code == 405:
                    response = self.session.get(url, timeout=self.timeout, allow_redirects=True, stream=True)
                    status_code = response.status_code
                    final_url = response.url
                    response.close()  # Close stream immediately
                    
            except requests.exceptions.RequestException:
                # If HEAD fails, try GET
                response = self.session.get(url, timeout=self.timeout, allow_redirects=True, stream=True)
                status_code = response.status_code
                final_url = response.url
                response.close()
                
            # Check if URL is accessible
            if 200 <= status_code < 400:
                self.verified_urls.add(url)
                if final_url != url:
                    logger.info(f"URL redirected: {url} -> {final_url}")
                    return True, f"Valid (redirected to {final_url})", final_url
                else:
                    return True, "Valid", None
                    
            elif status_code == 404:
                self.broken_urls.add(url)
                return False, "Resource not found (404)", None
                
            elif status_code == 403:
                self.broken_urls.add(url)
                return False, "Access forbidden (403)", None
                
            elif status_code >= 500:
                return False, f"Server error ({status_code})", None
                
            else:
                self.broken_urls.add(url)
                return False, f"HTTP {status_code}", None
                
        except requests.exceptions.Timeout:
            return False, "Request timeout", None
            
        except requests.exceptions.ConnectionError:
            return False, "Connection failed", None
            
        except requests.exceptions.RequestException as e:
            return False, f"Request error: {str(e)}", None
            
        except Exception as e:
            logger.error(f"Unexpected error validating {url}: {e}")
            return False, f"Validation error: {str(e)}", None
            
    def validate_batch(self, urls: list, delay: float = 0.5) -> Dict[str, Dict]:
        """
        Validate multiple URLs with rate limiting
        Returns: {url: {'valid': bool, 'status': str, 'redirect': str}}
        """
        results = {}
        
        for i, url in enumerate(urls):
            if url:
                is_valid, status, redirect = self.validate_url(url)
                results[url] = {
                    'valid': is_valid,
                    'status': status,
                    'redirect': redirect
                }
                
                # Rate limiting
                if i < len(urls) - 1:
                    time.sleep(delay)
                    
            logger.info(f"Validated {i+1}/{len(urls)} URLs")
            
        return results
        
    def update_database_url_status(self):
        """
        Validate all URLs in the database and update their status
        """
        try:
            # Connect to database
            conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
            cursor = conn.cursor()
            
            # Get all documents with source URLs
            cursor.execute("""
                SELECT id, title, source 
                FROM documents 
                WHERE source IS NOT NULL 
                AND source != '' 
                AND source LIKE 'http%'
                ORDER BY id
            """)
            
            documents = cursor.fetchall()
            logger.info(f"Found {len(documents)} documents with URLs to validate")
            
            validation_results = []
            
            for doc_id, title, source_url in documents:
                logger.info(f"Validating: {title[:50]}... -> {source_url}")
                
                is_valid, status, redirect = self.validate_url(source_url)
                
                validation_results.append({
                    'id': doc_id,
                    'title': title,
                    'url': source_url,
                    'valid': is_valid,
                    'status': status,
                    'redirect': redirect
                })
                
                # Update database with validation status
                cursor.execute("""
                    UPDATE documents 
                    SET url_valid = %s, 
                        url_status = %s,
                        url_checked = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (is_valid, status, doc_id))
                
                # If URL redirected, optionally update with final URL
                if redirect and redirect != source_url:
                    logger.info(f"URL redirected for {title}: {source_url} -> {redirect}")
                    cursor.execute("""
                        UPDATE documents 
                        SET source_redirect = %s
                        WHERE id = %s
                    """, (redirect, doc_id))
                
                conn.commit()
                time.sleep(0.5)  # Rate limiting
                
            cursor.close()
            conn.close()
            
            # Print summary
            valid_count = sum(1 for r in validation_results if r['valid'])
            invalid_count = len(validation_results) - valid_count
            
            logger.info(f"Validation complete: {valid_count} valid, {invalid_count} invalid URLs")
            
            # Print broken URLs for review
            broken_urls = [r for r in validation_results if not r['valid']]
            if broken_urls:
                logger.warning("Broken URLs found:")
                for broken in broken_urls:
                    logger.warning(f"  {broken['title'][:40]}... -> {broken['url']} ({broken['status']})")
                    
            return validation_results
            
        except Exception as e:
            logger.error(f"Database validation error: {e}")
            return []

def validate_single_url(url: str) -> Tuple[bool, str]:
    """
    Quick validation for a single URL
    Returns: (is_valid, status_message)
    """
    validator = URLValidator()
    is_valid, status, _ = validator.validate_url(url)
    return is_valid, status

def validate_all_document_urls():
    """
    Validate all document URLs in the database
    """
    validator = URLValidator()
    return validator.update_database_url_status()

if __name__ == "__main__":
    # Run validation on all URLs
    results = validate_all_document_urls()
    print(f"Validated {len(results)} URLs")