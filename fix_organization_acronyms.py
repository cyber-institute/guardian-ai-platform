#!/usr/bin/env python3
"""
Fix organization acronyms in database with proper mappings
"""

import os
import psycopg2

def fix_problematic_organization_acronyms():
    """Fix the problematic organization acronym conversions in the database"""
    
    # Connect to database
    database_url = os.getenv('DATABASE_URL')
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    print("=== FIXING PROBLEMATIC ORGANIZATION ACRONYMS ===")
    
    # Define correct mappings for the problematic conversions
    corrections = {
        "NASA": "NIST",  # Fix the incorrect NIST → NASA conversion
        "DAASA": "Unknown",  # Fix the generated acronym
        "HO": "White House",  # Fix person name to organization
        "WH": "White House"  # Keep this one as is - reasonable acronym
    }
    
    fixed_count = 0
    
    for incorrect_org, correct_org in corrections.items():
        cursor.execute("""
            UPDATE documents 
            SET author_organization = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE author_organization = %s
        """, (correct_org, incorrect_org))
        
        rows_affected = cursor.rowcount
        if rows_affected > 0:
            print(f"  Fixed {rows_affected} documents: {incorrect_org} → {correct_org}")
            fixed_count += rows_affected
    
    # Commit changes
    conn.commit()
    
    # Verify the corrections
    print(f"\n=== VERIFICATION ===")
    cursor.execute("SELECT DISTINCT author_organization FROM documents ORDER BY author_organization")
    organizations = [row[0] for row in cursor.fetchall() if row[0]]
    
    print("Current organization list:")
    for org in organizations:
        print(f"  {org}")
    
    conn.close()
    print(f"\n✓ Fixed {fixed_count} organization entries")

def add_custom_organization_mappings():
    """Add custom organization mappings to handle edge cases"""
    
    from utils.organization_acronym_converter import add_organization_mapping
    
    # Add mappings for organizations that need special handling
    custom_mappings = {
        "The White House": "White House",
        "National Security Agency's Artificial Intelligence": "NSA",
        "Design approach to AI-based software across the di": "Unknown"
    }
    
    print("\n=== ADDING CUSTOM ORGANIZATION MAPPINGS ===")
    for full_name, acronym in custom_mappings.items():
        add_organization_mapping(full_name, acronym)
        print(f"  Added mapping: {full_name} → {acronym}")

if __name__ == "__main__":
    fix_problematic_organization_acronyms()
    add_custom_organization_mappings()