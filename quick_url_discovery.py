"""
Quick URL Discovery and Enhanced Validation
Fast implementation for immediate results
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import db_manager
import requests
import re
from urllib.parse import urljoin

def quick_discover_urls():
    """
    Quick URL discovery for documents without valid URLs
    """
    print("Starting quick URL discovery...")
    
    # Get documents that need URL discovery
    query = """
    SELECT id, title, source, author_organization, document_type
    FROM documents 
    WHERE url_valid IS NULL OR url_valid = false
    ORDER BY id
    """
    
    docs = db_manager.execute_query(query)
    print(f"Found {len(docs)} documents needing URL discovery")
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    updates = []
    
    for doc in docs:
        doc_id = doc['id']
        title = doc['title']
        org = doc.get('author_organization', '')
        current_source = doc.get('source', '')
        
        print(f"Processing: {title[:50]}...")
        
        found_url = None
        
        # Strategy 1: Fix White House document specifically
        if 'white house' in org.lower() or 'quantum policy' in title.lower():
            whitehouse_urls = [
                "https://www.whitehouse.gov/briefing-room/statements-releases/2022/05/04/national-security-memorandum-on-promoting-united-states-leadership-in-quantum-computing-while-mitigating-risks-to-vulnerable-cryptographic-systems/",
                "https://www.whitehouse.gov/wp-content/uploads/2022/05/National-Security-Memorandum-10.pdf"
            ]
            
            for url in whitehouse_urls:
                try:
                    response = session.head(url, timeout=5)
                    if response.status_code == 200:
                        found_url = url
                        print(f"  ✓ Found White House URL: {url}")
                        break
                except:
                    continue
        
        # Strategy 2: NIST documents
        elif 'nist' in org.lower():
            # Extract NIST publication number if available
            nist_match = re.search(r'(?:NIST\s+)?(?:SP\s+)?(\d+(?:-\d+)?[A-Z]?)', title, re.IGNORECASE)
            if nist_match:
                pub_num = nist_match.group(1)
                nist_urls = [
                    f"https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.{pub_num}.pdf",
                    f"https://csrc.nist.gov/publications/detail/sp/{pub_num}/final"
                ]
                
                for url in nist_urls:
                    try:
                        response = session.head(url, timeout=5)
                        if response.status_code == 200:
                            found_url = url
                            print(f"  ✓ Found NIST URL: {url}")
                            break
                    except:
                        continue
        
        # Strategy 3: CISA documents
        elif 'cisa' in org.lower():
            title_slug = re.sub(r'[^\w\s-]', '', title.lower()).replace(' ', '-')
            cisa_urls = [
                f"https://www.cisa.gov/resources-tools/{title_slug}",
                f"https://www.cisa.gov/sites/default/files/publications/{title_slug}.pdf"
            ]
            
            for url in cisa_urls:
                try:
                    response = session.head(url, timeout=5)
                    if response.status_code == 200:
                        found_url = url
                        print(f"  ✓ Found CISA URL: {url}")
                        break
                except:
                    continue
        
        # Strategy 4: Check if current URL is actually valid but marked invalid
        if not found_url and current_source and current_source.startswith('http'):
            try:
                response = session.get(current_source, timeout=10)
                if response.status_code == 200:
                    content = response.text.lower()
                    # Check if it's not a generic landing page
                    if not any(indicator in content for indicator in ['page not found', '404', 'not available', 'search results']):
                        # Check if title words appear in content
                        title_words = [w.lower() for w in title.split() if len(w) > 3]
                        matches = sum(1 for word in title_words if word in content)
                        if matches >= len(title_words) * 0.3:  # 30% match threshold
                            found_url = response.url
                            print(f"  ✓ Validated existing URL: {found_url}")
            except:
                pass
        
        # Update database
        if found_url:
            updates.append((found_url, True, 'valid', found_url, True, doc_id))
        else:
            updates.append((current_source, False, 'no_url_found', '', True, doc_id))
            print(f"  ✗ No URL found for: {title[:30]}")
    
    # Batch update database
    if updates:
        update_query = """
        UPDATE documents 
        SET source = %s, url_valid = %s, url_status = %s, source_redirect = %s, url_checked = %s
        WHERE id = %s
        """
        
        for update in updates:
            db_manager.execute_query(update_query, update)
    
    print(f"\nCompleted! Updated {len(updates)} documents")
    
    # Show final statistics
    stats_query = """
    SELECT 
        COUNT(*) as total,
        SUM(CASE WHEN url_valid = true THEN 1 ELSE 0 END) as valid_urls,
        SUM(CASE WHEN url_valid = false THEN 1 ELSE 0 END) as invalid_urls
    FROM documents
    """
    
    stats = db_manager.execute_query(stats_query)[0]
    print(f"Final stats: {stats['valid_urls']}/{stats['total']} documents have valid URLs")

if __name__ == "__main__":
    quick_discover_urls()