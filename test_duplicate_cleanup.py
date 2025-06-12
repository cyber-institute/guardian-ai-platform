"""
Test Duplicate Cleanup Functionality
Debug why duplicate removal isn't working in refresh analysis
"""

import sys
sys.path.append('.')

from utils.duplicate_cleanup import get_duplicate_summary, auto_cleanup_exact_duplicates, identify_duplicate_groups
from utils.db import fetch_documents

def test_duplicate_detection():
    """Test the duplicate detection system"""
    print("=== Testing Duplicate Detection ===")
    
    # Get all documents
    docs = fetch_documents()
    print(f"Total documents in database: {len(docs)}")
    
    # Check for duplicates
    duplicate_groups = identify_duplicate_groups()
    print(f"Duplicate groups found: {len(duplicate_groups)}")
    
    for i, group in enumerate(duplicate_groups):
        print(f"\nGroup {i+1}:")
        print(f"  Type: {group['type']}")
        print(f"  Count: {group['count']}")
        print(f"  Confidence: {group.get('confidence', 'N/A')}")
        if 'title' in group:
            print(f"  Title: {group['title'][:100]}...")
        print(f"  Document IDs: {[doc.get('id') for doc in group['documents']]}")
    
    return duplicate_groups

def test_duplicate_summary():
    """Test duplicate summary function"""
    print("\n=== Testing Duplicate Summary ===")
    
    try:
        summary = get_duplicate_summary()
        print(f"Summary: {summary}")
        return summary
    except Exception as e:
        print(f"Error getting duplicate summary: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_auto_cleanup():
    """Test automatic cleanup function"""
    print("\n=== Testing Auto Cleanup ===")
    
    try:
        result = auto_cleanup_exact_duplicates()
        print(f"Cleanup result: {result}")
        return result
    except Exception as e:
        print(f"Error during auto cleanup: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run all tests"""
    print("Starting duplicate cleanup debugging...\n")
    
    # Test duplicate detection
    groups = test_duplicate_detection()
    
    # Test summary
    summary = test_duplicate_summary()
    
    # Test cleanup (only if duplicates found)
    if summary and summary.get('total_duplicate_groups', 0) > 0:
        cleanup_result = test_auto_cleanup()
    else:
        print("\nNo duplicates found - skipping cleanup test")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()