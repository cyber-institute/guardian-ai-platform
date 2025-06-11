#!/usr/bin/env python3
"""
Debug the intelligent synthesis engine to find quantum scoring issue
"""

import sys
sys.path.append('.')

from utils.intelligent_synthesis_engine import intelligent_synthesis_engine
from utils.comprehensive_scoring import analyze_with_enhanced_patterns, analyze_with_contextual_understanding

def debug_synthesis():
    """Debug the synthesis process step by step"""
    
    test_title = "Joint Guidance on Deploying AI Systems Securely"
    test_content = """AI security frameworks, machine learning security best practices, AI threat modeling."""
    
    # Get individual scores
    enhanced_scores = analyze_with_enhanced_patterns(test_content, test_title)
    contextual_scores = analyze_with_contextual_understanding(test_content, test_title)
    
    print("Individual Analysis Results:")
    print(f"Enhanced patterns quantum_cybersecurity: {enhanced_scores['quantum_cybersecurity']}")
    print(f"Contextual analysis quantum_cybersecurity: {contextual_scores['quantum_cybersecurity']}")
    
    # Create mock responses exactly as in the scoring function
    mock_responses = [
        {
            'service_name': 'anthropic_analyzer',
            'confidence': 0.85,
            'scores': enhanced_scores,
            'processing_time': 1.2,
            'metadata': {
                'domain_relevance': 90,
                'key_insights': ['comprehensive_analysis', 'pattern_based_scoring']
            }
        },
        {
            'service_name': 'openai_analyzer', 
            'confidence': 0.80,
            'scores': contextual_scores,
            'processing_time': 1.5,
            'metadata': {
                'domain_relevance': 85,
                'key_insights': ['contextual_scoring', 'semantic_analysis']
            }
        }
    ]
    
    print("\nMock Responses:")
    for i, response in enumerate(mock_responses):
        print(f"Response {i+1} quantum_cybersecurity: {response['scores']['quantum_cybersecurity']}")
    
    # Run synthesis
    synthesis_result = intelligent_synthesis_engine.synthesize_optimal_consensus(
        mock_responses,
        "comprehensive_scoring",
        target_confidence=0.85
    )
    
    print(f"\nSynthesis Result:")
    print(f"quantum_cybersecurity: {synthesis_result['scores']['quantum_cybersecurity']}")
    print(f"Full scores: {synthesis_result['scores']}")
    print(f"Method used: {synthesis_result.get('synthesis_method', 'unknown')}")
    print(f"Confidence: {synthesis_result.get('confidence', 'unknown')}")
    
    # Debug confidence and variance calculation
    confidences = [r['confidence'] for r in mock_responses]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    import numpy as np
    confidence_variance = np.var(confidences) if len(confidences) > 1 else 0
    
    print(f"\nConfidence Analysis:")
    print(f"Individual confidences: {confidences}")
    print(f"Average confidence: {avg_confidence}")
    print(f"Confidence variance: {confidence_variance}")
    print(f"Weighted ensemble criteria: avg_confidence > 0.8 and variance < 0.1")
    print(f"Meets criteria: {avg_confidence > 0.8 and confidence_variance < 0.1}")

if __name__ == "__main__":
    debug_synthesis()