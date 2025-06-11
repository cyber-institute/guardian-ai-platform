#!/usr/bin/env python3
"""
Test quantum cybersecurity scoring fix
"""

import sys
sys.path.append('.')

from utils.comprehensive_scoring import analyze_with_enhanced_patterns, analyze_with_contextual_understanding

def test_quantum_scoring():
    """Test quantum cybersecurity scoring for non-quantum documents"""
    
    # Test with AI cybersecurity document (no quantum content)
    test_title = "Joint Guidance on Deploying AI Systems Securely"
    test_content = """
    This document provides comprehensive guidance on securing AI systems in production environments.
    It covers AI security frameworks, machine learning security best practices, AI threat modeling,
    artificial intelligence vulnerability assessment, and AI governance protocols.
    The guidance includes recommendations for AI authentication, AI encryption standards,
    and AI monitoring systems to ensure robust cybersecurity for artificial intelligence deployments.
    """
    
    print("Testing Quantum Cybersecurity Scoring Fix...")
    print(f"Document: {test_title}")
    print("Content: AI security focused (no quantum content)")
    print()
    
    # Test enhanced patterns
    enhanced_scores = analyze_with_enhanced_patterns(test_content, test_title)
    print("Enhanced Pattern Analysis:")
    print(f"  quantum_cybersecurity: {enhanced_scores['quantum_cybersecurity']}")
    
    # Test contextual understanding
    contextual_scores = analyze_with_contextual_understanding(test_content, test_title)
    print("Contextual Analysis:")
    print(f"  quantum_cybersecurity: {contextual_scores['quantum_cybersecurity']}")
    
    # Test with actual quantum content
    quantum_content = """
    This document addresses post-quantum cryptography migration and quantum-safe algorithms.
    Organizations must prepare for quantum computing threats by implementing lattice-based cryptography,
    quantum key distribution systems, and quantum-resistant encryption protocols.
    """
    
    print("\n" + "="*50)
    print("Testing with Quantum Content:")
    
    enhanced_quantum = analyze_with_enhanced_patterns(quantum_content, "Post-Quantum Cryptography Guide")
    contextual_quantum = analyze_with_contextual_understanding(quantum_content, "Post-Quantum Cryptography Guide")
    
    print("Enhanced Pattern Analysis (Quantum Doc):")
    print(f"  quantum_cybersecurity: {enhanced_quantum['quantum_cybersecurity']}")
    
    print("Contextual Analysis (Quantum Doc):")
    print(f"  quantum_cybersecurity: {contextual_quantum['quantum_cybersecurity']}")

if __name__ == "__main__":
    test_quantum_scoring()