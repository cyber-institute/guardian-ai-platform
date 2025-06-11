#!/usr/bin/env python3
"""
Debug the exact quantum cybersecurity calculation
"""

import sys
sys.path.append('.')

from utils.comprehensive_scoring import analyze_with_enhanced_patterns, analyze_with_contextual_understanding

def debug_calculation():
    """Debug step by step calculation"""
    
    test_title = "Joint Guidance on Deploying AI Systems Securely"
    test_content = """AI security frameworks, machine learning security best practices, AI threat modeling."""
    
    # Get raw scores
    enhanced = analyze_with_enhanced_patterns(test_content, test_title)
    contextual = analyze_with_contextual_understanding(test_content, test_title)
    
    print("Raw Input Scores:")
    print(f"Enhanced patterns: {enhanced['quantum_cybersecurity']}")
    print(f"Contextual analysis: {contextual['quantum_cybersecurity']}")
    
    # Calculate weighted average manually
    # Weights from synthesis engine: enhanced=0.85, contextual=0.80
    weight1 = 0.85 * 0.85  # confidence * service weight
    weight2 = 0.80 * 0.80  # confidence * service weight
    
    weighted_sum = (enhanced['quantum_cybersecurity'] * weight1) + (contextual['quantum_cybersecurity'] * weight2)
    total_weight = weight1 + weight2
    
    manual_average = weighted_sum / total_weight
    
    print(f"\nManual Calculation:")
    print(f"Weight 1: {weight1}")
    print(f"Weight 2: {weight2}")
    print(f"Weighted sum: {weighted_sum}")
    print(f"Total weight: {total_weight}")
    print(f"Manual average: {manual_average}")
    print(f"After max(1, min(5, {manual_average})): {max(1, min(5, manual_average))}")

if __name__ == "__main__":
    debug_calculation()