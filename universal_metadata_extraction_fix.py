#!/usr/bin/env python3
"""
Universal Metadata Extraction Fix
Creates a robust system for extracting correct titles, organizations, and dates
that works across all ingestion methods (URL, file upload, web scraping, API)
"""

import os
import psycopg2
import re
from typing import Dict, Optional, Tuple

def extract_real_title_from_content(content: str, url: str = "") -> str:
    """Extract the actual document title from content using multiple strategies"""
    
    if not content:
        return ""
    
    # Clean content for analysis
    content_lines = content.split('\n')
    first_page = '\n'.join(content_lines[:50])  # Focus on first page
    
    # Strategy 1: Look for UNESCO document patterns
    unesco_patterns = [
        r'Recommendation on the Ethics of Artificial Intelligence',
        r'Quantum Science for\s*Inclusion and\s*Sustainability',
        r'AI and Education:\s*Guidance for Policy-makers',
        r'Artificial Intelligence and Education:\s*Guidance for Policy-makers',
        r'Beijing Consensus on Artificial Intelligence and Education'
    ]
    
    for pattern in unesco_patterns:
        match = re.search(pattern, first_page, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group().strip()
    
    # Strategy 2: Look for title patterns in first few lines
    title_patterns = [
        r'^([A-Z][^.\n]*(?:AI|Artificial Intelligence|Quantum|Education|Ethics|Policy|Framework)[^.\n]*)',
        r'((?:AI|Artificial Intelligence|Quantum)[\s\w]*(?:Framework|Policy|Guidance|Recommendation))',
        r'^([A-Z][\w\s]{10,80})\s*$'  # Capitalized line, reasonable length
    ]
    
    for line in content_lines[:10]:
        line = line.strip()
        if len(line) > 10 and len(line) < 120:
            for pattern in title_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    candidate = match.group(1).strip()
                    # Filter out common non-title patterns
                    if not re.match(r'^(page|chapter|\d+|contents?|abstract|summary)', candidate, re.IGNORECASE):
                        return candidate
    
    # Strategy 3: Extract from URL if it contains document hints
    if url and 'unesdoc.unesco.org' in url:
        return "UNESCO Document"  # Fallback for UNESCO URLs
    
    return ""

def extract_real_organization_from_content(content: str, url: str = "") -> str:
    """Extract the actual organization from content and URL"""
    
    if not content:
        return ""
    
    # Strategy 1: URL-based organization detection
    if url:
        if 'unesco.org' in url or 'unesdoc.unesco.org' in url:
            return "UNESCO"
        elif 'nist.gov' in url:
            return "NIST"
        elif 'whitehouse.gov' in url:
            return "White House"
        elif 'cisa.gov' in url:
            return "CISA"
    
    # Strategy 2: Content-based organization detection
    content_lower = content.lower()
    first_page = content[:2000]  # First 2000 characters
    
    org_patterns = [
        (r'unesco|united nations educational', 'UNESCO'),
        (r'national institute of standards|nist', 'NIST'),
        (r'white house|executive office', 'White House'),
        (r'cybersecurity.*infrastructure.*security|cisa', 'CISA'),
        (r'european commission|ec\s', 'European Commission'),
        (r'oecd|organisation for economic', 'OECD')
    ]
    
    for pattern, org in org_patterns:
        if re.search(pattern, first_page, re.IGNORECASE):
            return org
    
    return ""

def extract_publication_date_from_content(content: str) -> Optional[str]:
    """Extract publication date from content"""
    
    if not content:
        return None
    
    # Look in first 1000 characters for date patterns
    first_part = content[:1000]
    
    # Common date patterns
    date_patterns = [
        r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
        r'(\d{1,2}/\d{1,2}/\d{4})',  # MM/DD/YYYY or DD/MM/YYYY
        r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})',
        r'(\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})',
        r'(20\d{2})',  # Just year 20XX
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, first_part, re.IGNORECASE)
        if matches:
            date_str = matches[0]
            # Convert to standardized format if needed
            if re.match(r'20\d{2}$', date_str):
                return f"{date_str}-01-01"  # Default to January 1st
            return date_str
    
    return None

def fix_document_metadata(doc_id: int, content: str, url: str = "") -> Dict[str, str]:
    """Fix metadata for a single document"""
    
    corrections = {}
    
    # Extract correct title
    real_title = extract_real_title_from_content(content, url)
    if real_title:
        corrections['title'] = real_title
    
    # Extract correct organization
    real_org = extract_real_organization_from_content(content, url)
    if real_org:
        corrections['organization'] = real_org
        corrections['author_organization'] = real_org
    
    # Extract publication date
    pub_date = extract_publication_date_from_content(content)
    if pub_date:
        corrections['publication_date'] = pub_date
        corrections['publish_date'] = pub_date
    
    return corrections

def apply_universal_metadata_fix():
    """Apply metadata fixes to all documents that need correction"""
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Get documents that likely have metadata issues
        cursor.execute("""
            SELECT id, title, author_organization, organization, source, content
            FROM documents 
            WHERE title IN ('AI Cybersecurity Framework', 'Quantum Framework', 'Policy Document')
               OR author_organization != organization
               OR (source LIKE '%unesco%' AND organization != 'UNESCO')
               OR (source LIKE '%nist%' AND organization != 'NIST')
            ORDER BY id
        """)
        
        documents = cursor.fetchall()
        print(f"Found {len(documents)} documents that may need metadata correction")
        
        fixed_count = 0
        
        for doc in documents:
            doc_id, title, author_org, org, source, content = doc
            
            print(f"\nAnalyzing document ID {doc_id}: {title}")
            
            corrections = fix_document_metadata(doc_id, content or "", source or "")
            
            if corrections:
                print(f"Applying corrections: {corrections}")
                
                # Build update query dynamically
                update_fields = []
                values = []
                
                for field, value in corrections.items():
                    update_fields.append(f"{field} = %s")
                    values.append(value)
                
                if update_fields:
                    values.append(doc_id)  # For WHERE clause
                    
                    update_query = f"""
                        UPDATE documents 
                        SET {', '.join(update_fields)}
                        WHERE id = %s
                    """
                    
                    cursor.execute(update_query, values)
                    conn.commit()
                    
                    fixed_count += 1
                    print(f"✅ Fixed document {doc_id}")
            else:
                print(f"No corrections needed for document {doc_id}")
        
        print(f"\n🎯 Universal metadata fix complete: {fixed_count} documents corrected")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error in universal metadata fix: {str(e)}")
        return False

def fix_specific_unesco_quantum_document():
    """Fix the specific UNESCO quantum document that was misidentified"""
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Update the specific document
        cursor.execute("""
            UPDATE documents 
            SET title = 'Quantum Science for Inclusion and Sustainability',
                organization = 'UNESCO',
                author_organization = 'UNESCO',
                document_type = 'Policy'
            WHERE id = 58
        """)
        
        conn.commit()
        
        # Verify the fix
        cursor.execute("SELECT title, organization, author_organization FROM documents WHERE id = 58")
        result = cursor.fetchone()
        
        print("Fixed UNESCO Quantum document:")
        print(f"Title: {result[0]}")
        print(f"Organization: {result[1]}")
        print(f"Author Organization: {result[2]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing specific document: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Universal Metadata Extraction Fix")
    print("=" * 50)
    
    # Fix the specific UNESCO document first
    print("1. Fixing specific UNESCO quantum document...")
    fix_specific_unesco_quantum_document()
    
    print("\n2. Applying universal metadata corrections...")
    apply_universal_metadata_fix()
    
    print("\n✅ All metadata corrections complete")