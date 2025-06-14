#!/usr/bin/env python3
"""
Test the final organization acronym conversion system
"""

from utils.organization_acronym_converter import convert_org_to_acronym

def test_final_system():
    """Test the complete acronym conversion system"""
    
    print("=== TESTING FINAL ORGANIZATION ACRONYM SYSTEM ===")
    
    # Test cases that should convert
    conversion_tests = [
        ("National Institute of Standards and Technology", "NIST"),
        ("Cybersecurity and Infrastructure Security Agency", "CISA"), 
        ("National Security Agency", "NSA"),
        ("Department of Homeland Security", "DHS"),
        ("Institute of Electrical and Electronics Engineers", "IEEE"),
        ("Massachusetts Institute of Technology", "MIT"),
        ("National Aeronautics and Space Administration", "NASA"),
        ("Federal Bureau of Investigation", "FBI"),
        ("International Organization for Standardization", "ISO"),
        ("Information Technology Industry Council", "ITI")
    ]
    
    # Test cases that should NOT convert (already acronyms or short names)
    no_conversion_tests = [
        ("NIST", "NIST"),  # Already an acronym
        ("NASA", "NASA"),  # Already an acronym
        ("CISA", "CISA"),  # Already an acronym
        ("Unknown", "Unknown"),  # Edge case
        ("White House", "White House"),  # Short proper name
        ("Special", "Special")  # Edge case from our problem
    ]
    
    print("Testing conversions that SHOULD happen:")
    all_passed = True
    for input_org, expected in conversion_tests:
        result = convert_org_to_acronym(input_org)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result != expected:
            all_passed = False
        print(f"  {input_org:<50} → {result:<10} {status}")
        if result != expected:
            print(f"    Expected: {expected}")
    
    print(f"\nTesting cases that should NOT convert:")
    for input_org, expected in no_conversion_tests:
        result = convert_org_to_acronym(input_org)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result != expected:
            all_passed = False
        print(f"  {input_org:<20} → {result:<20} {status}")
        if result != expected:
            print(f"    Expected: {expected}")
    
    print(f"\n=== OVERALL RESULT ===")
    if all_passed:
        print("✅ All tests passed! Organization acronym system is working correctly.")
    else:
        print("❌ Some tests failed. System needs adjustment.")
    
    return all_passed

if __name__ == "__main__":
    test_final_system()