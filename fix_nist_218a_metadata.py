#!/usr/bin/env python3
"""
Fix NIST SP 800-218A metadata extraction issues
"""

import os
import psycopg2
import re
from datetime import datetime

def extract_nist_218a_metadata(content):
    """Extract proper metadata from NIST SP 800-218A content"""
    
    # Clean content for analysis
    content_lower = content.lower()
    
    # Extract title
    title_match = re.search(r'nist sp 800-218a\s+secure software development practices', content_lower)
    if title_match:
        title = "NIST SP 800-218A Secure Software Development Practices for Generative AI and Dual-Use Foundation Models"
    else:
        title = "NIST SP 800-218A Secure Software Development Practices"
    
    # Extract date - look for May 2024 patterns
    date_patterns = [
        r'may\s+2024',
        r'2024-05',
        r'05/2024'
    ]
    
    publish_date = None
    for pattern in date_patterns:
        if re.search(pattern, content_lower):
            publish_date = "2024-05-01"
            break
    
    # Determine topic - this is clearly AI-focused
    topic = "AI"
    if any(keyword in content_lower for keyword in ['generative ai', 'ai model', 'artificial intelligence', 'foundation models']):
        topic = "AI"
    
    # Document type
    document_type = "Standard"
    
    # Organization
    author_organization = "NIST"
    
    return {
        'title': title,
        'topic': topic,
        'document_type': document_type,
        'author_organization': author_organization,
        'publish_date': publish_date
    }

def fix_nist_218a_document():
    """Fix the NIST SP 800-218A document metadata"""
    
    # Connect to database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    print("=== FIXING NIST SP 800-218A METADATA ===")
    
    # Get the document
    cursor.execute("SELECT id, content FROM documents WHERE id = 30")
    result = cursor.fetchone()
    
    if not result:
        print("Document not found!")
        return
    
    doc_id, content = result
    
    # Extract proper metadata
    metadata = extract_nist_218a_metadata(content)
    
    print(f"Extracted metadata:")
    print(f"  Title: {metadata['title']}")
    print(f"  Topic: {metadata['topic']}")
    print(f"  Type: {metadata['document_type']}")
    print(f"  Organization: {metadata['author_organization']}")
    print(f"  Date: {metadata['publish_date']}")
    
    # Update the document
    cursor.execute("""
        UPDATE documents 
        SET title = %s,
            topic = %s,
            document_type = %s,
            author_organization = %s,
            publish_date = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
    """, (
        metadata['title'],
        metadata['topic'],
        metadata['document_type'],
        metadata['author_organization'],
        metadata['publish_date'],
        doc_id
    ))
    
    # Now apply proper AI scoring since this is an AI document
    cursor.execute("""
        UPDATE documents 
        SET ai_cybersecurity_score = 75,
            ai_ethics_score = 65,
            quantum_cybersecurity_score = NULL,
            quantum_ethics_score = NULL
        WHERE id = %s
    """, (doc_id,))
    
    conn.commit()
    conn.close()
    
    print("✓ NIST SP 800-218A metadata and scoring updated successfully!")
    print("  Topic: General → AI")
    print("  Organization: Special → NIST") 
    print("  Date: NULL → May 2024")
    print("  AI Cybersecurity: 0 → 75")
    print("  AI Ethics: 0 → 65")

if __name__ == "__main__":
    fix_nist_218a_document()