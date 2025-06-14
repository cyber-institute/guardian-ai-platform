"""
Quick URL validation script for document links
"""

from utils.url_validator import URLValidator
import psycopg2
import os

def quick_validation():
    """Run quick validation on all document URLs"""
    
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
    print(f"Found {len(documents)} documents with URLs to validate")
    
    validator = URLValidator()
    
    for doc_id, title, source_url in documents:
        print(f"Checking: {title[:40]}...")
        print(f"  URL: {source_url}")
        
        is_valid, status, redirect = validator.validate_url(source_url)
        
        print(f"  Status: {status}")
        if redirect:
            print(f"  Redirects to: {redirect}")
        
        # Update database
        cursor.execute("""
            UPDATE documents 
            SET url_valid = %s, 
                url_status = %s,
                url_checked = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (is_valid, status, doc_id))
        
        if redirect:
            cursor.execute("""
                UPDATE documents 
                SET source_redirect = %s
                WHERE id = %s
            """, (redirect, doc_id))
        
        conn.commit()
        print(f"  {'✓ Valid' if is_valid else '✗ Invalid'}")
        print()
    
    cursor.close()
    conn.close()
    print("Validation complete!")

if __name__ == "__main__":
    quick_validation()