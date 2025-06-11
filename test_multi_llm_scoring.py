#!/usr/bin/env python3
"""
Test the corrected Multi-LLM scoring hierarchy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.comprehensive_scoring import multi_llm_intelligent_scoring

def check_expectation(score, expected):
    """Helper to check if score matches expectation"""
    if expected == 'should have score':
        return score is not None and score > 0
    elif expected == 'should be None':
        return score is None
    elif expected == 'should be None or low':
        return score is None or (score is not None and score < 30)
    elif expected == 'may have score':
        return True  # Either None or a score is acceptable
    return True

if __name__ == "__main__":
    test_cases = [
        {
            'name': 'Pure AI Cybersecurity Document',
            'title': 'AI Security Framework Implementation Guide',
            'text': '''This comprehensive guide outlines security frameworks for artificial intelligence systems. 
            It covers machine learning model protection, AI threat detection, secure AI development practices,
            authentication mechanisms for AI systems, and cybersecurity best practices for AI deployments.
            The framework includes AI governance, compliance monitoring, and incident response procedures 
            specifically designed for AI-powered applications.''',
            'expected': {
                'ai_cybersecurity': 'should have score',
                'quantum_cybersecurity': 'should be None',
                'ai_ethics': 'may have score',
                'quantum_ethics': 'should be None'
            }
        },
        {
            'name': 'Pure Quantum Cybersecurity Document', 
            'title': 'Post-Quantum Cryptography Standards',
            'text': '''This document provides comprehensive guidelines for implementing post-quantum cryptography
            and quantum-safe encryption protocols. It covers lattice-based cryptography, quantum key distribution,
            quantum-resistant authentication mechanisms, and preparation strategies for quantum computing threats.
            The standards include quantum cryptography implementation, quantum security frameworks, and
            quantum-safe migration procedures for existing systems.''',
            'expected': {
                'ai_cybersecurity': 'may have score',
                'quantum_cybersecurity': 'should have score',
                'ai_ethics': 'should be None',
                'quantum_ethics': 'may have score'
            }
        },
        {
            'name': 'AI Ethics Policy Document',
            'title': 'Responsible AI Development and Ethical Guidelines',
            'text': '''This policy framework addresses ethical considerations in artificial intelligence development.
            It covers algorithmic bias mitigation, AI fairness principles, transparency in AI decision-making,
            accountability mechanisms for AI systems, and responsible AI governance. The guidelines include
            ethical AI development practices, trustworthy AI principles, and frameworks for addressing
            AI discrimination and ensuring equitable AI deployment across diverse populations.''',
            'expected': {
                'ai_cybersecurity': 'may have score',
                'quantum_cybersecurity': 'should be None',
                'ai_ethics': 'should have score',
                'quantum_ethics': 'should be None'
            }
        }
    ]
    
    print("=== MULTI-LLM SCORING SYSTEM TEST ===\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['name']}")
        print(f"   Title: {test_case['title']}")
        print(f"   Content preview: {test_case['text'][:100]}...")
        print()
        
        # Get Multi-LLM scores
        scores = multi_llm_intelligent_scoring(test_case['text'], test_case['title'])
        
        print("   Multi-LLM Scores:")
        for framework, score in scores.items():
            expected = test_case['expected'].get(framework, 'N/A')
            status = "✅" if check_expectation(score, expected) else "❌"
            print(f"     {framework}: {score} ({expected}) {status}")
        
        print()
    
    print("=== SCORING LOGIC VERIFICATION ===")
    print("Testing that quantum frameworks only score quantum-relevant content...")
    
    # Test non-quantum document doesn't get quantum scores
    non_quantum_scores = multi_llm_intelligent_scoring(
        test_cases[0]['text'], test_cases[0]['title']  # Pure AI document
    )
    
    quantum_cyber_score = non_quantum_scores.get('quantum_cybersecurity')
    quantum_ethics_score = non_quantum_scores.get('quantum_ethics')
    
    print(f"Non-quantum document quantum cybersecurity: {quantum_cyber_score}")
    print(f"Non-quantum document quantum ethics: {quantum_ethics_score}")
    
    if quantum_cyber_score is None and quantum_ethics_score is None:
        print("✅ SUCCESS: Non-quantum documents correctly receive None for quantum frameworks")
    else:
        print("❌ ISSUE: Non-quantum documents incorrectly receiving quantum scores")
    
    # Test quantum document gets quantum scores
    quantum_scores = multi_llm_intelligent_scoring(
        test_cases[1]['text'], test_cases[1]['title']  # Pure quantum document
    )
    
    q_cyber = quantum_scores.get('quantum_cybersecurity')
    q_ethics = quantum_scores.get('quantum_ethics')
    
    print(f"Quantum document quantum cybersecurity: {q_cyber}")
    print(f"Quantum document quantum ethics: {q_ethics}")
    
    if q_cyber is not None:
        print("✅ SUCCESS: Quantum documents correctly receive quantum cybersecurity scores")
    else:
        print("❌ ISSUE: Quantum documents not receiving quantum cybersecurity scores")