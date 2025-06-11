#!/usr/bin/env python3
"""
Debug the exact quantum cybersecurity calculation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.comprehensive_scoring import (
    multi_llm_intelligent_scoring,
    analyze_with_enhanced_patterns,
    analyze_with_contextual_understanding,
    score_quantum_cybersecurity_maturity,
    score_quantum_ethics
)

def debug_calculation():
    """Debug step by step calculation"""
    
    # Test documents
    test_cases = [
        {
            'name': 'Non-Quantum AI Document',
            'title': 'AI Security Framework',
            'text': 'This document covers artificial intelligence security, machine learning protection, and AI governance without quantum components.'
        },
        {
            'name': 'Quantum Cybersecurity Document',
            'title': 'Post-Quantum Cryptography Guide',
            'text': 'This document covers post-quantum cryptography, quantum-safe encryption, lattice-based cryptography, and quantum key distribution for quantum-resistant security.'
        },
        {
            'name': 'Mixed AI-Quantum Document',
            'title': 'Quantum-Enhanced AI Security',
            'text': 'This document covers quantum machine learning, quantum-enhanced AI systems, post-quantum cryptography for AI, and quantum artificial intelligence security frameworks.'
        }
    ]
    
    print("=== QUANTUM SCORING DEBUG ANALYSIS ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}")
        print(f"   Title: {test_case['title']}")
        print(f"   Content: {test_case['text'][:80]}...")
        print()
        
        # Test direct quantum cybersecurity function
        direct_quantum_cyber = score_quantum_cybersecurity_maturity(test_case['text'], test_case['title'])
        print(f"   Direct Quantum Cybersecurity: {direct_quantum_cyber}")
        
        # Test direct quantum ethics function
        direct_quantum_ethics = score_quantum_ethics(test_case['text'], test_case['title'])
        print(f"   Direct Quantum Ethics: {direct_quantum_ethics}")
        
        # Test enhanced patterns
        enhanced_scores = analyze_with_enhanced_patterns(test_case['text'], test_case['title'])
        print(f"   Enhanced Patterns:")
        print(f"     - Quantum Cyber: {enhanced_scores.get('quantum_cybersecurity', 'None')}")
        print(f"     - Quantum Ethics: {enhanced_scores.get('quantum_ethics', 'None')}")
        
        # Test contextual understanding
        contextual_scores = analyze_with_contextual_understanding(test_case['text'], test_case['title'])
        print(f"   Contextual Understanding:")
        print(f"     - Quantum Cyber: {contextual_scores.get('quantum_cybersecurity', 'None')}")
        print(f"     - Quantum Ethics: {contextual_scores.get('quantum_ethics', 'None')}")
        
        # Test Multi-LLM synthesis
        multi_llm_scores = multi_llm_intelligent_scoring(test_case['text'], test_case['title'])
        print(f"   Multi-LLM Synthesis:")
        print(f"     - AI Cybersecurity: {multi_llm_scores.get('ai_cybersecurity')}")
        print(f"     - Quantum Cybersecurity: {multi_llm_scores.get('quantum_cybersecurity')}")
        print(f"     - AI Ethics: {multi_llm_scores.get('ai_ethics')}")
        print(f"     - Quantum Ethics: {multi_llm_scores.get('quantum_ethics')}")
        
        print("\n" + "="*60 + "\n")
    
    print("=== SCORING LOGIC VALIDATION ===")
    
    # Validate logical consistency
    non_quantum_case = test_cases[0]
    non_quantum_scores = multi_llm_intelligent_scoring(non_quantum_case['text'], non_quantum_case['title'])
    
    quantum_case = test_cases[1]
    quantum_scores = multi_llm_intelligent_scoring(quantum_case['text'], quantum_case['title'])
    
    print("Non-Quantum Document Results:")
    print(f"  ✓ Quantum Cybersecurity: {non_quantum_scores.get('quantum_cybersecurity')} (should be None)")
    print(f"  ✓ Quantum Ethics: {non_quantum_scores.get('quantum_ethics')} (should be None)")
    print(f"  ✓ AI Cybersecurity: {non_quantum_scores.get('ai_cybersecurity')} (should have value)")
    
    print("\nQuantum Document Results:")
    print(f"  ✓ Quantum Cybersecurity: {quantum_scores.get('quantum_cybersecurity')} (should have value)")
    print(f"  ✓ Quantum Ethics: {quantum_scores.get('quantum_ethics')} (may have value)")
    print(f"  ✓ AI Cybersecurity: {quantum_scores.get('ai_cybersecurity')} (may have value)")
    
    # Final validation
    quantum_cyber_fixed = non_quantum_scores.get('quantum_cybersecurity') is None
    quantum_ethics_fixed = non_quantum_scores.get('quantum_ethics') is None
    quantum_scoring_works = quantum_scores.get('quantum_cybersecurity') is not None
    
    print(f"\n=== FIX VALIDATION ===")
    print(f"Quantum Cybersecurity Fix: {'✅ SUCCESS' if quantum_cyber_fixed else '❌ FAILED'}")
    print(f"Quantum Ethics Fix: {'✅ SUCCESS' if quantum_ethics_fixed else '❌ FAILED'}")
    print(f"Quantum Scoring Works: {'✅ SUCCESS' if quantum_scoring_works else '❌ FAILED'}")
    
    if quantum_cyber_fixed and quantum_ethics_fixed and quantum_scoring_works:
        print(f"\n🎉 ALL QUANTUM SCORING FIXES SUCCESSFUL!")
        print(f"The Multi-LLM system now correctly handles quantum framework applicability.")
    else:
        print(f"\n⚠️  Some issues remain - further debugging needed.")

if __name__ == "__main__":
    debug_calculation()