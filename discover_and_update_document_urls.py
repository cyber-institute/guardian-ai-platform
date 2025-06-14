#!/usr/bin/env python3
"""
Discover and update URLs for all existing documents
"""

import os
import psycopg2
from utils.document_url_discovery import discover_document_url

def discover_urls_for_all_documents():
    """Discover source URLs for all documents in the database"""
    
    # Connect to database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    print("=== DISCOVERING DOCUMENT URLs ===")
    
    # Get all documents
    cursor.execute("SELECT id, title, author_organization, content, source FROM documents")
    documents = cursor.fetchall()
    
    print(f"Processing {len(documents)} documents...")
    
    updated_count = 0
    discovered_urls = {}
    
    for doc_id, title, organization, content, current_source in documents:
        # Skip if URL already exists
        if current_source and current_source.startswith(('http://', 'https://')):
            print(f"  ✓ {title[:50]}... (URL already exists)")
            continue
        
        # Discover URL
        discovered_url = discover_document_url(title, organization or "", content or "")
        
        if discovered_url:
            # Update database
            cursor.execute("""
                UPDATE documents 
                SET source = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (discovered_url, doc_id))
            
            updated_count += 1
            discovered_urls[doc_id] = discovered_url
            
            print(f"  🔗 {title[:50]}...")
            print(f"     → {discovered_url}")
        else:
            print(f"  ⚠ {title[:50]}... (No URL found)")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n=== DISCOVERY SUMMARY ===")
    print(f"✓ Updated {updated_count} documents with discovered URLs")
    
    if discovered_urls:
        print(f"\nDiscovered URLs:")
        for doc_id, url in discovered_urls.items():
            print(f"  Document {doc_id}: {url}")

def test_url_discovery():
    """Test URL discovery with sample documents"""
    
    print(f"\n=== TESTING URL DISCOVERY ===")
    
    test_cases = [
        {
            "title": "NIST SP 800-218A Secure Software Development Practices for Generative AI and Dual-Use Foundation Models",
            "organization": "NIST",
            "content": "This publication is available free of charge from: https://doi.org/10.6028/NIST.SP.800-218A"
        },
        {
            "title": "NIST Special Publication 800-63-3 Digital Identity Guidelines",
            "organization": "NIST", 
            "content": "NIST Special Publication 800-63-3"
        },
        {
            "title": "DHS CISA and UK NCSC Release Joint Guidelines for Secure AI System Development",
            "organization": "CISA",
            "content": "Joint guidelines for secure AI development"
        }
    ]
    
    for test in test_cases:
        print(f"\nTesting: {test['title'][:60]}...")
        discovered_url = discover_document_url(test['title'], test['organization'], test['content'])
        
        if discovered_url:
            print(f"  ✓ Discovered: {discovered_url}")
        else:
            print(f"  ✗ No URL found")

if __name__ == "__main__":
    test_url_discovery()
    discover_urls_for_all_documents()