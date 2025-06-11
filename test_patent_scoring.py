"""
Test Patent Scoring Integration
Verify that the comprehensive patent scoring system works correctly
"""

import os
import sys
sys.path.append('.')

from utils.patent_scoring_engine import ComprehensivePatentScoringEngine
from utils.comprehensive_patent_scoring import apply_comprehensive_patent_scoring

def test_ai_cybersecurity_content():
    """Test scoring for AI cybersecurity content"""
    print("Testing AI Cybersecurity Content...")
    
    ai_content = """
    NIST AI Risk Management Framework
    
    This document provides guidelines for managing AI risks in cybersecurity contexts.
    It covers machine learning security, adversarial attacks, model robustness,
    data poisoning prevention, and AI system monitoring. The framework addresses
    authentication mechanisms, access controls, and threat detection using AI.
    
    Key areas include:
    - AI model security and validation
    - Machine learning pipeline protection
    - Automated threat response systems
    - AI-powered intrusion detection
    - Cybersecurity risk assessment for AI systems
    """
    
    scoring_engine = ComprehensivePatentScoringEngine()
    scores = scoring_engine.assess_document_comprehensive(ai_content, "NIST AI Risk Management Framework")
    
    print(f"AI Cybersecurity Score: {scores['ai_cybersecurity_score']}/100")
    print(f"Quantum Cybersecurity Score: {scores['quantum_cybersecurity_score']}/5")
    print(f"AI Ethics Score: {scores['ai_ethics_score']}/100")
    print(f"Quantum Ethics Score: {scores['quantum_ethics_score']}/100")
    
    return scores

def test_quantum_cybersecurity_content():
    """Test scoring for quantum cybersecurity content"""
    print("\nTesting Quantum Cybersecurity Content...")
    
    quantum_content = """
    NIST Post-Quantum Cryptography Standards
    
    This document outlines cryptographic algorithms resistant to quantum computing attacks.
    It covers quantum key distribution, post-quantum cryptographic algorithms,
    quantum-safe encryption methods, and quantum threat mitigation strategies.
    
    Key areas include:
    - Post-quantum cryptographic algorithms
    - Quantum key distribution protocols
    - Quantum-resistant digital signatures
    - Quantum threat assessment methodologies
    - Migration strategies from classical to quantum-safe cryptography
    """
    
    scoring_engine = ComprehensivePatentScoringEngine()
    scores = scoring_engine.assess_document_comprehensive(quantum_content, "NIST Post-Quantum Cryptography Standards")
    
    print(f"AI Cybersecurity Score: {scores['ai_cybersecurity_score']}/100")
    print(f"Quantum Cybersecurity Score: {scores['quantum_cybersecurity_score']}/5")
    print(f"AI Ethics Score: {scores['ai_ethics_score']}/100")
    print(f"Quantum Ethics Score: {scores['quantum_ethics_score']}/100")
    
    return scores

def test_ai_ethics_content():
    """Test scoring for AI ethics content"""
    print("\nTesting AI Ethics Content...")
    
    ethics_content = """
    AI Ethics and Responsible AI Development
    
    This document addresses ethical considerations in AI development and deployment.
    It covers algorithmic bias, fairness in machine learning, transparency requirements,
    accountability frameworks, and human oversight of AI systems.
    
    Key areas include:
    - Algorithmic fairness and bias mitigation
    - AI transparency and explainability
    - Human-AI interaction ethics
    - Privacy protection in AI systems
    - Responsible AI governance frameworks
    """
    
    scoring_engine = ComprehensivePatentScoringEngine()
    scores = scoring_engine.assess_document_comprehensive(ethics_content, "AI Ethics and Responsible AI Development")
    
    print(f"AI Cybersecurity Score: {scores['ai_cybersecurity_score']}/100")
    print(f"Quantum Cybersecurity Score: {scores['quantum_cybersecurity_score']}/5")
    print(f"AI Ethics Score: {scores['ai_ethics_score']}/100")
    print(f"Quantum Ethics Score: {scores['quantum_ethics_score']}/100")
    
    return scores

def test_comprehensive_scoring_application():
    """Test applying comprehensive scoring to all documents"""
    print("\nTesting Comprehensive Scoring Application...")
    
    try:
        processed = apply_comprehensive_patent_scoring()
        print(f"Applied patent scoring to {processed} documents")
        return True
    except Exception as e:
        print(f"Error applying comprehensive scoring: {e}")
        return False

if __name__ == "__main__":
    print("=== Patent Scoring Integration Test ===\n")
    
    # Test individual scoring frameworks
    ai_scores = test_ai_cybersecurity_content()
    quantum_scores = test_quantum_cybersecurity_content()
    ethics_scores = test_ai_ethics_content()
    
    # Test comprehensive application
    success = test_comprehensive_scoring_application()
    
    print("\n=== Test Summary ===")
    print(f"AI Cybersecurity framework: {'✓' if ai_scores['ai_cybersecurity_score'] > 0 else '✗'}")
    print(f"Quantum Cybersecurity framework: {'✓' if quantum_scores['quantum_cybersecurity_score'] > 0 else '✗'}")
    print(f"AI Ethics framework: {'✓' if ethics_scores['ai_ethics_score'] > 0 else '✗'}")
    print(f"Comprehensive application: {'✓' if success else '✗'}")