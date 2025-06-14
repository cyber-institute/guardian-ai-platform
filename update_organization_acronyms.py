#!/usr/bin/env python3
"""
Update all existing documents to use proper organization acronyms
"""

import os
import psycopg2
from utils.organization_acronym_converter import convert_org_to_acronym

def update_all_organization_acronyms():
    """Update all documents to use proper organization acronyms"""
    
    # Connect to database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    print("=== UPDATING ORGANIZATION ACRONYMS ===")
    
    # Get all documents with their current organization names
    cursor.execute("SELECT id, title, author_organization FROM documents WHERE author_organization IS NOT NULL")
    documents = cursor.fetchall()
    
    print(f"Found {len(documents)} documents to process...")
    
    updated_count = 0
    conversions = {}
    
    for doc_id, title, current_org in documents:
        if current_org and current_org.strip():
            # Convert to acronym
            acronym_org = convert_org_to_acronym(current_org)
            
            # Only update if there's a meaningful change
            if acronym_org != current_org:
                cursor.execute("""
                    UPDATE documents 
                    SET author_organization = %s,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (acronym_org, doc_id))
                
                updated_count += 1
                conversions[current_org] = acronym_org
                
                print(f"  Updated: {title[:50]}...")
                print(f"    {current_org} → {acronym_org}")
    
    # Commit all changes
    conn.commit()
    conn.close()
    
    print(f"\n=== CONVERSION SUMMARY ===")
    print(f"✓ Updated {updated_count} documents")
    
    if conversions:
        print(f"\nOrganization Conversions:")
        for original, acronym in conversions.items():
            print(f"  {original} → {acronym}")
    else:
        print("No conversions needed - all organizations already use proper acronyms")

def test_acronym_converter():
    """Test the acronym converter with various organization names"""
    
    print(f"\n=== TESTING ACRONYM CONVERTER ===")
    
    test_organizations = [
        "National Institute of Standards and Technology",
        "Cybersecurity and Infrastructure Security Agency", 
        "National Security Agency",
        "Department of Homeland Security",
        "Institute of Electrical and Electronics Engineers",
        "Massachusetts Institute of Technology",
        "National Aeronautics and Space Administration",
        "Federal Bureau of Investigation",
        "International Organization for Standardization",
        "World Wide Web Consortium",
        "Information Technology Industry Council",
        "Special",  # Edge case from our problematic document
        "NIST",    # Already an acronym
        "Unknown"  # Edge case
    ]
    
    print("Testing organization name conversions:")
    for org in test_organizations:
        acronym = convert_org_to_acronym(org)
        status = "✓ CONVERTED" if acronym != org else "→ NO CHANGE"
        print(f"  {org:<50} → {acronym:<10} {status}")

if __name__ == "__main__":
    test_acronym_converter()
    update_all_organization_acronyms()