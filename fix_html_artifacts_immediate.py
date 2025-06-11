#!/usr/bin/env python3
"""
Immediate HTML Artifacts Fix
Clean all metadata fields to remove HTML artifacts like </div> and fix "pecial" issues
"""

import os
import psycopg2
import re
from typing import Any

def ultra_clean_field(value: Any) -> str:
    """Ultra-aggressive cleaning for any field type"""
    if not value or value in [None, 'None', 'null']:
        return 'Unknown'
    
    # Convert to string and initial cleaning
    text = str(value).strip()
    
    if not text or text.lower() in ['none', 'null', 'undefined']:
        return 'Unknown'
    
    # Remove ALL HTML tags and fragments - multiple passes
    for _ in range(5):  # More cleaning passes
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'</[^>]*>', '', text)
        text = re.sub(r'<[^>]*', '', text)
        text = re.sub(r'[^<]*>', '', text)
    
    # Remove HTML entities
    text = re.sub(r'&[#a-zA-Z0-9]+;?', '', text)
    
    # Remove specific problematic artifacts - expanded list
    artifacts = [
        '</div>', '<div>', '<div', '</span>', '<span>', '<span',
        '</p>', '<p>', '<p', '</h1>', '<h1>', '</h2>', '<h2>',
        '</h3>', '<h3>', '</h4>', '<h4>', '</h5>', '<h5>',
        '</strong>', '<strong>', '</em>', '<em>', '</b>', '<b>',
        '</i>', '<i>', '</u>', '<u>', '</br>', '<br>', '<br/>',
        'style=', 'class=', 'id=', 'href=', 'src=', 'alt=',
        '&nbsp;', '&amp;', '&lt;', '&gt;', '&quot;', '&#39;',
        'div>', 'span>', '/div', '/span', 'div', 'span',
        '</div', '<div>', '</span', '<span>', '</p', '<p>',
        'onclick=', 'onload=', 'width=', 'height=', 'border=',
        'margin=', 'padding=', 'color=', 'background=', 'font='
    ]
    
    for artifact in artifacts:
        text = text.replace(artifact, ' ')
    
    # Remove remaining brackets, quotes, and attribute patterns
    text = re.sub(r'[<>"\'`]', '', text)
    text = re.sub(r'\w+\s*=\s*["\'][^"\']*["\']', '', text)
    text = re.sub(r'\w+\s*=\s*\w+', '', text)
    
    # Fix "pecial" -> "Special" (common OCR/extraction error)
    text = re.sub(r'\bpecial\b', 'Special', text, flags=re.IGNORECASE)
    
    # Remove common HTML words that leak through
    html_words = ['div', 'span', 'style', 'class', 'href', 'src', 'alt']
    for word in html_words:
        text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)
    
    # Normalize whitespace
    text = ' '.join(text.split()).strip()
    
    # Final validation - if still contains artifacts, return Unknown
    if re.search(r'[<>]|&\w+;|\w+=|/>', text) or len(text) < 2:
        return 'Unknown'
    
    return text

def fix_metadata_immediately():
    """Fix all document metadata immediately"""
    print("Starting immediate metadata cleanup for HTML artifacts...")
    
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            print("DATABASE_URL environment variable not found")
            return
            
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get all documents with metadata
        cursor.execute("""
            SELECT id, title, author_organization, publish_date::text, document_type, content_preview 
            FROM documents
        """)
        documents = cursor.fetchall()
        
        print(f"Processing {len(documents)} documents...")
        
        updated_count = 0
        for doc_id, title, org, date, doc_type, preview in documents:
            
            # Clean each field
            clean_title = ultra_clean_field(title)
            clean_org = ultra_clean_field(org)
            clean_date = ultra_clean_field(date) if date and str(date) != 'None' else 'Date not available'
            clean_type = ultra_clean_field(doc_type)
            clean_preview = ultra_clean_field(preview)
            
            # Update document with cleaned metadata
            cursor.execute("""
                UPDATE documents 
                SET title = %s, 
                    author_organization = %s, 
                    publish_date = %s,
                    document_type = %s,
                    content_preview = %s
                WHERE id = %s
            """, (clean_title, clean_org, clean_date, clean_type, clean_preview, doc_id))
            
            updated_count += 1
            if updated_count % 10 == 0:
                print(f"Updated {updated_count} documents...")
        
        conn.commit()
        print(f"Successfully cleaned metadata for {updated_count} documents")
        
        # Verify cleanup
        print("\nVerifying cleanup...")
        cursor.execute("""
            SELECT id, title, author_organization, publish_date::text, document_type 
            FROM documents 
            WHERE title LIKE '%<%' OR title LIKE '%>%' 
               OR author_organization LIKE '%<%' OR author_organization LIKE '%>%'
               OR document_type LIKE '%<%' OR document_type LIKE '%>%'
               OR title LIKE '%pecial%'
               OR author_organization LIKE '%pecial%'
            LIMIT 5
        """)
        
        remaining_artifacts = cursor.fetchall()
        if remaining_artifacts:
            print(f"WARNING: {len(remaining_artifacts)} documents still contain artifacts:")
            for doc in remaining_artifacts:
                print(f"  Doc {doc[0]}: {doc[1][:50]}...")
        else:
            print("✓ All HTML artifacts successfully removed!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Error during cleanup: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_metadata_immediately()