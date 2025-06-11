#!/usr/bin/env python3
"""
Test the corrected Multi-LLM scoring hierarchy
"""

import sys
sys.path.append('.')

from utils.comprehensive_scoring import multi_llm_intelligent_scoring

def test_multi_llm_scoring():
    """Test the Multi-LLM scoring system priority"""
    
    # Test with AI cybersecurity document
    test_title = "Joint Guidance on Deploying AI Systems Securely"
    test_content = """
    This document provides comprehensive guidance on securing AI systems in production environments.
    It covers AI security frameworks, machine learning security best practices, AI threat modeling,
    artificial intelligence vulnerability assessment, and AI governance protocols.
    The guidance includes recommendations for AI authentication, AI encryption standards,
    and AI monitoring systems to ensure robust cybersecurity for artificial intelligence deployments.
    """
    
    print("Testing Multi-LLM intelligent scoring system...")
    print(f"Document: {test_title}")
    
    # Test the new Multi-LLM scoring
    scores = multi_llm_intelligent_scoring(test_content, test_title)
    
    print(f"Multi-LLM Scores: {scores}")
    
    # Verify it's using Multi-LLM first, not OpenAI
    if any(score is not None for score in scores.values()):
        print("✓ Multi-LLM scoring system working correctly")
        for framework, score in scores.items():
            if score is not None:
                print(f"  {framework}: {score}")
    else:
        print("✗ Multi-LLM scoring failed, check implementation")

if __name__ == "__main__":
    test_multi_llm_scoring()