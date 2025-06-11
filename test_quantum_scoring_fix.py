#!/usr/bin/env python3
"""
Test quantum cybersecurity scoring fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.comprehensive_scoring import (
    multi_llm_intelligent_scoring,
    analyze_with_enhanced_patterns, 
    analyze_with_contextual_understanding,
    score_quantum_cybersecurity_maturity
)

def test_quantum_scoring():
    """Test quantum cybersecurity scoring for non-quantum documents"""
    
    # Test document with no quantum content
    non_quantum_text = """
    This document discusses artificial intelligence security frameworks and 
    cybersecurity best practices for AI systems. It covers machine learning 
    model protection, authentication mechanisms, and threat detection for 
    traditional AI applications.
    """
    non_quantum_title = "AI Cybersecurity Framework for Traditional Systems"
    
    print("Testing Non-Quantum Document:")
    print(f"Title: {non_quantum_title}")
    print(f"Content preview: {non_quantum_text[:100]}...")
    print()
    
    # Test direct quantum cybersecurity scoring function
    print("1. Direct quantum cybersecurity function:")
    direct_score = score_quantum_cybersecurity_maturity(non_quantum_text, non_quantum_title)
    print(f"   Result: {direct_score} (should be None for non-quantum content)")
    print()
    
    # Test enhanced patterns function
    print("2. Enhanced patterns analysis:")
    enhanced_scores = analyze_with_enhanced_patterns(non_quantum_text, non_quantum_title)
    quantum_cyber_enhanced = enhanced_scores.get('quantum_cybersecurity')
    print(f"   Quantum cybersecurity: {quantum_cyber_enhanced} (should be None/missing for non-quantum)")
    print()
    
    # Test contextual understanding function
    print("3. Contextual understanding analysis:")
    contextual_scores = analyze_with_contextual_understanding(non_quantum_text, non_quantum_title)
    quantum_cyber_contextual = contextual_scores.get('quantum_cybersecurity')
    print(f"   Quantum cybersecurity: {quantum_cyber_contextual} (should be None/missing for non-quantum)")
    print()
    
    # Test Multi-LLM intelligent scoring
    print("4. Multi-LLM intelligent scoring:")
    multi_llm_scores = multi_llm_intelligent_scoring(non_quantum_text, non_quantum_title)
    quantum_cyber_multi = multi_llm_scores.get('quantum_cybersecurity')
    print(f"   Quantum cybersecurity: {quantum_cyber_multi} (should be None for non-quantum)")
    print(f"   AI cybersecurity: {multi_llm_scores.get('ai_cybersecurity')} (should have a score)")
    print()
    
    # Test with actual quantum content for comparison
    quantum_text = """
    This document outlines post-quantum cryptography standards and quantum-safe 
    encryption protocols. It discusses lattice-based cryptography, quantum key 
    distribution systems, and quantum-resistant authentication mechanisms for 
    preparing systems against quantum computing threats.
    """
    quantum_title = "Post-Quantum Cryptography Implementation Guide"
    
    print("Testing Quantum Document (for comparison):")
    print(f"Title: {quantum_title}")
    print()
    
    # Test quantum document scoring
    quantum_direct = score_quantum_cybersecurity_maturity(quantum_text, quantum_title)
    quantum_multi = multi_llm_intelligent_scoring(quantum_text, quantum_title)
    
    print("5. Quantum document scoring:")
    print(f"   Direct function: {quantum_direct} (should have a score 1-5)")
    print(f"   Multi-LLM: {quantum_multi.get('quantum_cybersecurity')} (should have a score)")
    print()
    
    # Summary
    print("=== SCORING FIX VERIFICATION ===")
    print(f"Non-quantum document quantum cybersecurity scores:")
    print(f"  - Direct function: {direct_score}")
    print(f"  - Enhanced patterns: {quantum_cyber_enhanced}")
    print(f"  - Contextual understanding: {quantum_cyber_contextual}")
    print(f"  - Multi-LLM synthesis: {quantum_cyber_multi}")
    print()
    print(f"Quantum document quantum cybersecurity scores:")
    print(f"  - Direct function: {quantum_direct}")
    print(f"  - Multi-LLM synthesis: {quantum_multi.get('quantum_cybersecurity')}")
    print()
    
    # Check if fix is working
    non_quantum_scores = [direct_score, quantum_cyber_enhanced, quantum_cyber_contextual, quantum_cyber_multi]
    quantum_scores = [quantum_direct, quantum_multi.get('quantum_cybersecurity')]
    
    print("Fix Status:")
    if all(score is None for score in non_quantum_scores):
        print("✅ SUCCESS: All non-quantum scoring methods correctly return None")
    else:
        print("❌ ISSUE: Some methods still return scores for non-quantum content:")
        for i, score in enumerate(non_quantum_scores):
            methods = ["Direct", "Enhanced", "Contextual", "Multi-LLM"]
            if score is not None:
                print(f"    - {methods[i]}: {score}")
    
    if any(score is not None for score in quantum_scores):
        print("✅ SUCCESS: Quantum documents correctly receive scores")
    else:
        print("❌ ISSUE: Quantum documents not receiving scores")

if __name__ == "__main__":
    test_quantum_scoring()