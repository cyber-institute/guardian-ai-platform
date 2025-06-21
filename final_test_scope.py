#!/usr/bin/env python3
"""Final test of all updated scope detection functions"""

import sys
sys.path.append('.')

from all_docs_tab import (
    analyze_ai_cybersecurity_content, 
    analyze_quantum_cybersecurity_content,
    analyze_ai_ethics_content, 
    analyze_quantum_ethics_content
)

def test_all_functions():
    winnie_content = "Once upon a time in a forest lived a bear named Winnie-the-Pooh. He loved honey and had many adventures with his friends Piglet, Eeyore, and Christopher Robin."
    
    functions = [
        ("AI Cybersecurity", analyze_ai_cybersecurity_content),
        ("Quantum Cybersecurity", analyze_quantum_cybersecurity_content),
        ("AI Ethics", analyze_ai_ethics_content),
        ("Quantum Ethics", analyze_quantum_ethics_content)
    ]
    
    expected = "children's literature rather than a cybersecurity, AI, or quantum technology policy document. Scoring may not be meaningful for this content type."
    
    all_passed = True
    for name, func in functions:
        result = func(winnie_content, "N/A")
        if expected in result:
            print(f"✅ {name}: Simple scope message working")
        else:
            print(f"❌ {name}: Still showing complex analysis")
            all_passed = False
    
    if all_passed:
        print("\n🎉 SUCCESS: All functions now return simple scope messages for out-of-scope documents!")
    else:
        print("\n❌ Some functions still need fixing")
    
    return all_passed

if __name__ == "__main__":
    test_all_functions()