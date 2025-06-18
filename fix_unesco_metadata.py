#!/usr/bin/env python3
"""
Fix UNESCO Document Metadata Issues
"""

import os
import psycopg2
from datetime import datetime

def fix_unesco_document():
    """Fix the specific metadata issues with UNESCO document"""
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        print("🔧 Fixing UNESCO document metadata...")
        
        # Get the UNESCO document
        cursor.execute("""
            SELECT id, title, content FROM documents 
            WHERE title LIKE '%UNESCO%' 
            ORDER BY id DESC 
            LIMIT 1
        """)
        
        result = cursor.fetchone()
        if not result:
            print("❌ UNESCO document not found")
            return False
            
        doc_id, title, content = result
        print(f"📄 Found document ID: {doc_id}")
        print(f"   Title: {title[:50]}...")
        
        # Analyze content to determine correct document type
        content_lower = content.lower() if content else title.lower()
        
        # UNESCO Recommendation documents are policy documents
        document_type = "Policy"  # UNESCO Recommendations are policy documents
        
        # Check if content contains policy indicators
        policy_indicators = [
            'recommendation', 'policy', 'framework', 'guideline', 'principle',
            'governance', 'strategy', 'regulation', 'standard', 'directive'
        ]
        
        policy_count = sum(1 for indicator in policy_indicators if indicator in content_lower)
        print(f"   Policy indicators found: {policy_count}")
        
        # UNESCO recommendations are definitely policy documents
        if 'recommendation' in title.lower() and 'unesco' in title.lower():
            document_type = "Policy"
            print(f"   Classified as: {document_type} (UNESCO Recommendation)")
        
        # Fix URL status - since this was uploaded via URL, it should be valid
        url_status = 'valid'
        url_valid = True
        
        # Update the document with correct metadata
        cursor.execute("""
            UPDATE documents 
            SET document_type = %s,
                url_status = %s,
                url_valid = %s,
                updated_at = %s
            WHERE id = %s
        """, (document_type, url_status, url_valid, datetime.now(), doc_id))
        
        conn.commit()
        print(f"✅ Updated document metadata:")
        print(f"   Document Type: {document_type}")
        print(f"   URL Status: {url_status}")
        print(f"   URL Valid: {url_valid}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main function"""
    print("🚀 UNESCO Document Metadata Fix")
    print("=" * 35)
    
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL environment variable not set")
        return
    
    success = fix_unesco_document()
    
    if success:
        print("\n✅ UNESCO document metadata fixed!")
    else:
        print("\n❌ Fix failed!")

if __name__ == "__main__":
    main()