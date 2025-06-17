#!/usr/bin/env python3
"""
Test the fixed quantum cybersecurity scoring system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.comprehensive_scoring import score_quantum_cybersecurity_maturity, analyze_document_applicability

def test_quantum_scoring_variation():
    """Test that quantum documents get varied scores based on content"""
    
    test_documents = [
        {
            'title': 'Basic Quantum Awareness Document',
            'content': 'This document mentions quantum computing threats and the need for quantum-safe cryptography. Basic awareness of post-quantum security.',
            'expected_range': (1, 2)
        },
        {
            'title': 'Intermediate Quantum Implementation Guide', 
            'content': 'Comprehensive guide covering lattice-based cryptography, quantum key distribution, and pqc implementation strategies. Includes migration roadmap and deployment considerations for quantum-resistant systems.',
            'expected_range': (2, 4)
        },
        {
            'title': 'Advanced NIST Post-Quantum Standards',
            'content': 'Detailed analysis of NIST post-quantum cryptography standards including lattice-based, code-based, multivariate, and hash-based approaches. Covers implementation guidelines, governance frameworks, compliance requirements, and hybrid systems integration for enterprise deployment.',
            'expected_range': (4, 5)
        },
        {
            'title': 'Dynamic Quantum Security Framework',
            'content': 'Cutting-edge framework for adaptive quantum security featuring quantum machine learning, continuous quantum monitoring, quantum evolution protocols, and dynamic quantum response systems. Includes comprehensive governance, NIST compliance, hybrid systems, quantum supremacy considerations, and enterprise-wide implementation strategies with cryptographic agility.',
            'expected_range': (5, 5)
        }
    ]
    
    print("Testing Fixed Quantum Scoring System")
    print("=" * 50)
    
    scores = []
    for i, doc in enumerate(test_documents, 1):
        # Check applicability
        applicability = analyze_document_applicability(doc['content'], doc['title'])
        print(f"\nTest {i}: {doc['title']}")
        print(f"Quantum applicable: {applicability['quantum_cybersecurity']}")
        
        if applicability['quantum_cybersecurity']:
            score = score_quantum_cybersecurity_maturity(doc['content'], doc['title'])
            scores.append(score)
            expected_min, expected_max = doc['expected_range']
            
            print(f"Score: {score}")
            print(f"Expected range: {expected_min}-{expected_max}")
            
            if expected_min <= score <= expected_max:
                print("✅ Score within expected range")
            else:
                print("❌ Score outside expected range")
        else:
            print("Document not applicable for quantum scoring")
    
    print(f"\n" + "=" * 50)
    print("Scoring Variation Analysis:")
    print(f"All scores: {scores}")
    
    if len(set(scores)) == len(scores):
        print("✅ SUCCESS: All documents received different scores")
    elif len(set(scores)) > 1:
        print(f"⚠️  PARTIAL: {len(set(scores))} unique scores from {len(scores)} documents")
    else:
        print("❌ FAILURE: All documents received identical scores")
    
    return scores

if __name__ == "__main__":
    test_quantum_scoring_variation()