#!/usr/bin/env python3
"""
Fix metadata extraction and restore URL discovery for existing documents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import db_manager
from utils.enhanced_ocr_metadata import extract_enhanced_metadata_from_content
from utils.restore_url_discovery import discover_document_source_url
import time

def fix_unesco_document():
    """Fix the specific UNESCO document metadata"""
    print("=== FIXING UNESCO DOCUMENT METADATA ===")
    
    # Find documents with "Quantum Science" in the title
    query = """
    SELECT id, title, content, author_organization, document_type, source
    FROM documents 
    WHERE title ILIKE '%quantum science%' OR title ILIKE '%inclusion%' OR title ILIKE '%sustainability%'
    ORDER BY id DESC
    LIMIT 5
    """
    
    docs = db_manager.execute_query(query)
    
    if not docs:
        print("No UNESCO documents found to fix")
        return
    
    for doc in docs:
        doc_id = doc['id']
        title = doc['title']
        content = doc['content']
        current_org = doc.get('author_organization', '')
        current_type = doc.get('document_type', '')
        current_source = doc.get('source', '')
        
        print(f"\nProcessing document: {title[:50]}...")
        print(f"Current org: {current_org}")
        print(f"Current type: {current_type}")
        
        # Apply enhanced metadata extraction
        try:
            enhanced_metadata = extract_enhanced_metadata_from_content(content)
            
            new_title = enhanced_metadata.get('title', title)
            new_org = enhanced_metadata.get('author_organization', current_org)
            new_type = enhanced_metadata.get('document_type', current_type)
            new_date = enhanced_metadata.get('publish_date', None)
            
            print(f"Enhanced title: {new_title}")
            print(f"Enhanced org: {new_org}")
            print(f"Enhanced type: {new_type}")
            print(f"Enhanced date: {new_date}")
            
            # Check if this is the UNESCO document
            if 'unesco' in new_org.lower() or 'quantum science for inclusion' in new_title.lower():
                print("✓ UNESCO document detected - applying corrections")
                
                # Correct the metadata
                corrected_title = "Quantum Science for Inclusion and Sustainability"
                corrected_org = "UNESCO"
                corrected_type = "Policy Brief"
                
                # Discover URL for UNESCO document
                discovered_url = None
                if not current_source or 'pending' in current_source.lower():
                    print("Discovering UNESCO document URL...")
                    discovered_url = discover_document_source_url(corrected_title, corrected_org, corrected_type)
                    if discovered_url:
                        print(f"✓ URL discovered: {discovered_url}")
                    else:
                        print("No URL found")
                
                # Update database
                update_query = """
                UPDATE documents 
                SET title = %s, 
                    author_organization = %s, 
                    document_type = %s,
                    publish_date = %s,
                    source = %s,
                    url_valid = %s,
                    url_status = %s,
                    url_checked = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """
                
                final_url = discovered_url if discovered_url else current_source
                url_valid = True if discovered_url else None
                url_status = 'discovered' if discovered_url else 'pending'
                
                db_manager.execute_query(update_query, (
                    corrected_title,
                    corrected_org, 
                    corrected_type,
                    new_date,
                    final_url,
                    url_valid,
                    url_status,
                    True,
                    doc_id
                ))
                
                print(f"✓ Updated UNESCO document metadata")
                print(f"  Title: {corrected_title}")
                print(f"  Organization: {corrected_org}")
                print(f"  Type: {corrected_type}")
                if discovered_url:
                    print(f"  URL: {discovered_url}")
            
        except Exception as e:
            print(f"Error processing document {doc_id}: {str(e)}")

def fix_pending_urls():
    """Fix documents showing 'link pending' by discovering their URLs"""
    print("\n=== FIXING PENDING URLs ===")
    
    # Find documents with no valid URLs
    query = """
    SELECT id, title, author_organization, document_type, source
    FROM documents 
    WHERE (source IS NULL OR source = '' OR source ILIKE '%pending%' OR url_valid IS NULL OR url_valid = false)
    ORDER BY id DESC
    LIMIT 10
    """
    
    docs = db_manager.execute_query(query)
    
    print(f"Found {len(docs)} documents needing URL discovery")
    
    discovered_count = 0
    
    for doc in docs:
        doc_id = doc['id']
        title = doc['title']
        org = doc.get('author_organization', '')
        doc_type = doc.get('document_type', '')
        current_source = doc.get('source', '')
        
        print(f"\nDiscovering URL for: {title[:50]}...")
        print(f"Organization: {org}")
        print(f"Type: {doc_type}")
        
        try:
            discovered_url = discover_document_source_url(title, org, doc_type)
            
            if discovered_url:
                print(f"✓ URL discovered: {discovered_url}")
                
                # Update database
                update_query = """
                UPDATE documents 
                SET source = %s,
                    url_valid = %s,
                    url_status = %s,
                    url_checked = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """
                
                db_manager.execute_query(update_query, (
                    discovered_url,
                    True,
                    'discovered',
                    True,
                    doc_id
                ))
                
                discovered_count += 1
            else:
                print("No URL found")
                
                # Mark as checked but no URL found
                update_query = """
                UPDATE documents 
                SET url_valid = %s,
                    url_status = %s,
                    url_checked = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                """
                
                db_manager.execute_query(update_query, (
                    False,
                    'no_url_found',
                    True,
                    doc_id
                ))
            
            # Rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Error discovering URL for document {doc_id}: {str(e)}")
    
    print(f"\n=== URL DISCOVERY SUMMARY ===")
    print(f"URLs discovered: {discovered_count}")
    print(f"Documents processed: {len(docs)}")

def main():
    """Main function to fix metadata and URLs"""
    print("Starting metadata and URL fixes...")
    
    # Fix UNESCO document first
    fix_unesco_document()
    
    # Fix pending URLs
    fix_pending_urls()
    
    print("\n=== FIXES COMPLETE ===")

if __name__ == "__main__":
    main()