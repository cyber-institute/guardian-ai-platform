#!/usr/bin/env python3
"""
Comprehensive Metadata Fix for All Documents
Restores proper titles, organizations, dates, and scores while protecting manually corrected documents
"""

import os
import psycopg2
from datetime import datetime
import re

def fix_organization_names():
    """Fix truncated organization names"""
    fixes = {
        'bility': 'Cybersecurity and Infrastructure Security Agency (CISA)',
        'ONOMIC': 'The White House',
        'Design approach to AI-based software across the di': 'NIST'
    }
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    for bad_org, correct_org in fixes.items():
        cursor.execute("""
            UPDATE documents 
            SET author_organization = %s,
                organization = %s
            WHERE author_organization = %s
            AND id NOT IN (10, 26, 27, 28, 29, 30, 43, 63)
        """, (correct_org, correct_org, bad_org))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Fixed truncated organization names")

def restore_missing_scores():
    """Restore missing scores for key documents"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    # NIST AI Risk Management Framework
    cursor.execute("""
        UPDATE documents 
        SET ai_cybersecurity_score = 95,
            ai_ethics_score = 90
        WHERE id = 43 AND (ai_cybersecurity_score IS NULL OR ai_ethics_score IS NULL)
    """)
    
    # NIST SP 800-218A
    cursor.execute("""
        UPDATE documents 
        SET ai_cybersecurity_score = 85,
            ai_ethics_score = 75
        WHERE id = 30 AND (ai_cybersecurity_score IS NULL OR ai_ethics_score IS NULL)
    """)
    
    # NASA Responsible AI Plan
    cursor.execute("""
        UPDATE documents 
        SET ai_cybersecurity_score = 80,
            ai_ethics_score = 95
        WHERE id = 27 AND (ai_cybersecurity_score IS NULL OR ai_ethics_score IS NULL)
    """)
    
    # NIST AI Framework (26)
    cursor.execute("""
        UPDATE documents 
        SET ai_cybersecurity_score = 90,
            ai_ethics_score = 85
        WHERE id = 26 AND (ai_cybersecurity_score IS NULL OR ai_ethics_score IS NULL)
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Restored missing scores for key documents")

def add_publication_dates():
    """Add publication dates where missing"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    date_updates = [
        (43, '2023-01-26'),  # NIST AI RMF 1.0
        (30, '2024-05-01'),  # NIST SP 800-218A
        (27, '2024-03-01'),  # NASA Responsible AI Plan
        (26, '2023-01-26'),  # NIST AI Framework
        (48, '2023-10-30'),  # NSM-10
    ]
    
    for doc_id, pub_date in date_updates:
        cursor.execute("""
            UPDATE documents 
            SET publication_date = %s,
                publish_date = %s
            WHERE id = %s AND publication_date IS NULL
        """, (pub_date, pub_date, doc_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Added missing publication dates")

def fix_generic_titles():
    """Fix any remaining generic titles while protecting manually set ones"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    # Get documents with generic titles that aren't protected
    cursor.execute("""
        SELECT id, title, source FROM documents 
        WHERE (title LIKE '%Cybersecurity Document%' 
               OR title LIKE '%Document from%'
               OR title = 'Untitled'
               OR LENGTH(title) < 15)
        AND id NOT IN (10, 26, 27, 28, 29, 30, 43, 63)
    """)
    
    docs_to_fix = cursor.fetchall()
    
    for doc_id, current_title, source in docs_to_fix:
        # Extract title from URL if possible
        new_title = extract_title_from_url(source)
        if new_title and new_title != current_title:
            cursor.execute("""
                UPDATE documents 
                SET title = %s
                WHERE id = %s
            """, (new_title, doc_id))
            print(f"   Fixed title for document {doc_id}: {new_title[:50]}...")
    
    conn.commit()
    cursor.close()
    conn.close()

def extract_title_from_url(url):
    """Extract meaningful title from URL"""
    if not url:
        return None
    
    # Common patterns for extracting titles from URLs
    if 'nist.gov' in url:
        if '800-218A' in url:
            return "NIST Special Publication 800-218A: Secure Software Development Framework"
        elif 'ai-rmf' in url or 'AI-RMF' in url:
            return "NIST AI Risk Management Framework (AI RMF 1.0)"
    
    elif 'whitehouse.gov' in url:
        if 'nsm-10' in url or 'NSM-10' in url:
            return "National Security Memorandum on Critical and Emerging Technologies"
    
    elif 'nasa.gov' in url:
        if 'responsible' in url.lower() and 'ai' in url.lower():
            return "NASA Responsible AI Plan"
    
    elif 'cisa.gov' in url:
        if 'playbook' in url.lower():
            return "AI Cybersecurity Collaboration Playbook"
    
    return None

def main():
    """Run comprehensive metadata fixes"""
    print("🔧 Comprehensive Metadata Fix")
    print("=" * 35)
    
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL environment variable not set")
        return
    
    try:
        fix_organization_names()
        restore_missing_scores()
        add_publication_dates()
        fix_generic_titles()
        
        print("\n✅ All metadata fixes completed successfully!")
        
        # Verify the fixes
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM documents 
            WHERE title NOT LIKE '%Cybersecurity Document%' 
            AND title != 'Untitled' 
            AND LENGTH(title) > 15
        """)
        good_titles = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM documents")
        total_docs = cursor.fetchone()[0]
        
        print(f"📊 Status: {good_titles}/{total_docs} documents have proper titles")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error during fixes: {str(e)}")

if __name__ == "__main__":
    main()