#!/usr/bin/env python3
"""
Test enhanced metadata extraction on NIST SP 800-218A
"""

import os
import psycopg2
from utils.enhanced_metadata_extractor import extract_enhanced_metadata

def test_nist_218a_extraction():
    """Test metadata extraction on the problematic document"""
    
    # Connect to database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Get the full content of NIST SP 800-218A
    cursor.execute("SELECT id, title, content FROM documents WHERE id = 30")
    result = cursor.fetchone()
    
    if not result:
        print("Document not found!")
        return
    
    doc_id, current_title, content = result
    
    print("=== TESTING ENHANCED METADATA EXTRACTION ===")
    print(f"Document ID: {doc_id}")
    print(f"Current Title: {current_title}")
    print(f"Content Length: {len(content)} characters")
    print(f"Content Preview: {content[:200]}...")
    
    # Test enhanced extraction
    extracted_metadata = extract_enhanced_metadata(content, current_title)
    
    print(f"\n=== EXTRACTED METADATA ===")
    for key, value in extracted_metadata.items():
        print(f"{key}: {value}")
    
    # Analyze framework applicability
    print(f"\n=== FRAMEWORK APPLICABILITY ===")
    applicability = extracted_metadata.get('framework_applicability', {})
    for framework, should_apply in applicability.items():
        status = "✓ SHOULD APPLY" if should_apply else "✗ SHOULD NOT APPLY"
        print(f"{framework}: {status}")
    
    conn.close()

if __name__ == "__main__":
    test_nist_218a_extraction()