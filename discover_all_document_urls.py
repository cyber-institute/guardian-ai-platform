"""
Comprehensive URL Discovery for All Documents
Finds original source URLs for every document using intelligent search strategies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import db_manager
from utils.intelligent_url_discovery import discover_document_source_url
from utils.enhanced_url_validator import validate_url_enhanced
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def discover_and_validate_all_urls():
    """
    Discover and validate URLs for all documents in the database
    """
    logger.info("Starting comprehensive URL discovery for all documents...")
    
    # Get all documents
    documents = db_manager.fetch_documents()
    logger.info(f"Found {len(documents)} documents to process")
    
    stats = {
        'total': len(documents),
        'urls_found': 0,
        'urls_validated': 0,
        'landing_pages_detected': 0,
        'broken_links': 0,
        'no_url_found': 0
    }
    
    for i, doc in enumerate(documents):
        doc_id = doc['id']
        title = doc.get('title', 'Untitled')
        author_org = doc.get('author_organization', '')
        doc_type = doc.get('document_type', '')
        current_source = doc.get('source', '')
        
        logger.info(f"Processing document {i+1}/{len(documents)}: {title[:50]}...")
        
        # Step 1: Check if current URL is valid and not a landing page
        current_url_valid = False
        final_url = current_source
        
        if current_source and current_source.startswith(('http://', 'https://')):
            logger.info(f"  Validating existing URL: {current_source}")
            validation_result = validate_url_enhanced(current_source, title, doc_type)
            
            if validation_result['valid'] and not validation_result['is_landing_page']:
                current_url_valid = True
                final_url = validation_result['final_url']
                logger.info(f"  ✓ Existing URL is valid: {validation_result['status']}")
            else:
                logger.info(f"  ✗ Existing URL invalid or landing page: {validation_result['status']}")
                if validation_result['is_landing_page']:
                    stats['landing_pages_detected'] += 1
        
        # Step 2: If no valid URL, try to discover one
        if not current_url_valid:
            logger.info(f"  Discovering new URL for: {title}")
            discovered_url = discover_document_source_url(title, author_org, doc_type)
            
            if discovered_url:
                logger.info(f"  Found potential URL: {discovered_url}")
                # Validate the discovered URL
                validation_result = validate_url_enhanced(discovered_url, title, doc_type)
                
                if validation_result['valid'] and not validation_result['is_landing_page']:
                    final_url = validation_result['final_url']
                    current_url_valid = True
                    stats['urls_found'] += 1
                    logger.info(f"  ✓ Discovered URL is valid: {validation_result['status']}")
                else:
                    logger.info(f"  ✗ Discovered URL invalid or landing page: {validation_result['status']}")
                    if validation_result['is_landing_page']:
                        stats['landing_pages_detected'] += 1
            else:
                logger.info(f"  No URL could be discovered for this document")
                stats['no_url_found'] += 1
        
        # Step 3: Update database with results
        if current_url_valid:
            stats['urls_validated'] += 1
            update_query = """
            UPDATE documents 
            SET source = %s, url_valid = %s, url_status = %s, source_redirect = %s, url_checked = %s
            WHERE id = %s
            """
            db_manager.execute_query(update_query, (
                final_url,
                True,
                'valid',
                final_url if final_url != current_source else '',
                True,
                doc_id
            ))
            logger.info(f"  ✓ Updated database with valid URL")
        else:
            stats['broken_links'] += 1
            update_query = """
            UPDATE documents 
            SET url_valid = %s, url_status = %s, url_checked = %s
            WHERE id = %s
            """
            db_manager.execute_query(update_query, (
                False,
                'no_valid_url_found',
                True,
                doc_id
            ))
            logger.info(f"  ✗ Marked as no valid URL found")
        
        # Rate limiting to be respectful
        time.sleep(2)
    
    # Print final statistics
    logger.info("\n" + "="*60)
    logger.info("URL DISCOVERY COMPLETE")
    logger.info("="*60)
    logger.info(f"Total documents processed: {stats['total']}")
    logger.info(f"URLs found and validated: {stats['urls_validated']}")
    logger.info(f"New URLs discovered: {stats['urls_found']}")
    logger.info(f"Landing pages detected: {stats['landing_pages_detected']}")
    logger.info(f"Broken/invalid links: {stats['broken_links']}")
    logger.info(f"No URL found: {stats['no_url_found']}")
    
    success_rate = (stats['urls_validated'] / stats['total']) * 100
    logger.info(f"Success rate: {success_rate:.1f}%")

def fix_specific_whitehouse_url():
    """
    Fix the specific White House document URL issue
    """
    logger.info("Fixing White House document URL...")
    
    # Find White House documents
    query = """
    SELECT id, title, source, author_organization 
    FROM documents 
    WHERE LOWER(author_organization) LIKE '%white house%' 
       OR LOWER(source) LIKE '%whitehouse.gov%'
    """
    
    whitehouse_docs = db_manager.execute_query(query)
    
    for doc in whitehouse_docs:
        doc_id = doc['id']
        title = doc['title']
        current_source = doc['source']
        
        logger.info(f"Processing White House doc: {title}")
        
        # White House specific URL patterns
        title_clean = title.lower().replace(' ', '-').replace('_', '-')
        title_clean = ''.join(c for c in title_clean if c.isalnum() or c == '-')
        
        # Try specific White House URL patterns
        whitehouse_patterns = [
            f"https://www.whitehouse.gov/briefing-room/statements-releases/2021/{title_clean}/",
            f"https://www.whitehouse.gov/briefing-room/statements-releases/2022/{title_clean}/",
            f"https://www.whitehouse.gov/briefing-room/statements-releases/2023/{title_clean}/",
            f"https://www.whitehouse.gov/wp-content/uploads/2021/{title_clean}.pdf",
            f"https://www.whitehouse.gov/wp-content/uploads/2022/{title_clean}.pdf",
            f"https://www.whitehouse.gov/wp-content/uploads/2023/{title_clean}.pdf",
        ]
        
        # Also try searching for key phrases in the title
        if 'quantum' in title.lower():
            whitehouse_patterns.extend([
                "https://www.whitehouse.gov/briefing-room/statements-releases/2022/05/04/national-security-memorandum-on-promoting-united-states-leadership-in-quantum-computing-while-mitigating-risks-to-vulnerable-cryptographic-systems/",
                "https://www.whitehouse.gov/wp-content/uploads/2022/05/National-Security-Memorandum-10.pdf"
            ])
        
        found_valid_url = False
        for pattern in whitehouse_patterns:
            logger.info(f"  Testing: {pattern}")
            validation_result = validate_url_enhanced(pattern, title)
            
            if validation_result['valid'] and not validation_result['is_landing_page']:
                logger.info(f"  ✓ Found valid White House URL: {pattern}")
                
                update_query = """
                UPDATE documents 
                SET source = %s, url_valid = %s, url_status = %s, source_redirect = %s, url_checked = %s
                WHERE id = %s
                """
                db_manager.execute_query(update_query, (
                    pattern,
                    True,
                    'valid',
                    pattern,
                    True,
                    doc_id
                ))
                found_valid_url = True
                break
            
            time.sleep(1)  # Rate limiting
        
        if not found_valid_url:
            logger.info(f"  ✗ No valid URL found for White House document: {title}")

if __name__ == "__main__":
    # First, fix the specific White House document issue
    fix_specific_whitehouse_url()
    
    # Then run comprehensive discovery for all documents
    discover_and_validate_all_urls()