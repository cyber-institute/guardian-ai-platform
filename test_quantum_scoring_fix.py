#!/usr/bin/env python3
"""
Test quantum cybersecurity scoring fix
"""

import sys
sys.path.append('.')

from utils.comprehensive_scoring import multi_llm_intelligent_scoring

def test_quantum_scoring():
    """Test quantum cybersecurity scoring for non-quantum documents"""
    
    test_title = "Joint Guidance on Deploying AI Systems Securely"
    test_content = """AI security frameworks, machine learning security best practices, AI threat modeling."""
    
    print("Testing quantum cybersecurity scoring for non-quantum document...")
    print(f"Title: {test_title}")
    print(f"Content snippet: {test_content[:100]}...")
    
    # Test multi-LLM scoring
    scores = multi_llm_intelligent_scoring(test_content, test_title)
    
    print(f"\nMulti-LLM Scores:")
    for metric, score in scores.items():
        if score is not None:
            print(f"  {metric}: {score}")
        else:
            print(f"  {metric}: Not applicable")
    
    # Specifically test quantum cybersecurity
    quantum_score = scores.get('quantum_cybersecurity')
    print(f"\nQuantum Cybersecurity Analysis:")
    print(f"  Score: {quantum_score}")
    print(f"  Expected: 1 (minimal quantum relevance)")
    print(f"  Status: {'✓ CORRECT' if quantum_score == 1 else '✗ INCORRECT - should be 1'}")

if __name__ == "__main__":
    test_quantum_scoring()