"""
Comprehensive scoring engine for AI and Quantum maturity assessments
Implements patent-based scoring criteria with LLM intelligence
"""

import re
from typing import Dict, Optional, Tuple

def analyze_document_applicability(text: str, title: str) -> Dict[str, bool]:
    """
    Determine which scoring frameworks apply to a document based on content analysis.
    
    Returns:
        Dict with keys: ai_cybersecurity, quantum_cybersecurity, ai_ethics, quantum_ethics
    """
    text_lower = text.lower()
    title_lower = title.lower()
    
    # AI-related keywords
    ai_keywords = [
        'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
        'ai system', 'algorithm', 'automated decision', 'chatbot', 'llm', 'gpt',
        'computer vision', 'natural language', 'recommendation system'
    ]
    
    # Quantum-related keywords
    quantum_keywords = [
        'quantum', 'post-quantum', 'quantum computing', 'quantum cryptography',
        'quantum encryption', 'quantum key', 'quantum-safe', 'quantum-resistant',
        'qkd', 'quantum supremacy', 'quantum advantage'
    ]
    
    # Cybersecurity keywords
    cybersecurity_keywords = [
        'cybersecurity', 'security', 'encryption', 'cryptography', 'vulnerability',
        'threat', 'attack', 'defense', 'protection', 'breach', 'incident response',
        'risk management', 'compliance', 'authentication', 'authorization'
    ]
    
    # Ethics keywords
    ethics_keywords = [
        'ethics', 'ethical', 'bias', 'fairness', 'transparency', 'accountability',
        'privacy', 'discrimination', 'human rights', 'responsible', 'governance',
        'oversight', 'explainable', 'interpretable', 'audit'
    ]
    
    # Check for keyword presence
    has_ai = any(keyword in text_lower or keyword in title_lower for keyword in ai_keywords)
    has_quantum = any(keyword in text_lower or keyword in title_lower for keyword in quantum_keywords)
    has_cybersecurity = any(keyword in text_lower or keyword in title_lower for keyword in cybersecurity_keywords)
    has_ethics = any(keyword in text_lower or keyword in title_lower for keyword in ethics_keywords)
    
    # Determine applicability
    return {
        'ai_cybersecurity': has_ai and has_cybersecurity,
        'quantum_cybersecurity': has_quantum and has_cybersecurity,
        'ai_ethics': has_ai and has_ethics,
        'quantum_ethics': has_quantum and has_ethics
    }

def score_ai_cybersecurity_maturity(text: str, title: str) -> Optional[int]:
    """
    Score AI Cybersecurity Maturity (0-100) based on patent criteria.
    
    Patent criteria from AI Policy patent:
    - Encryption standards for AI systems
    - Authentication mechanisms
    - Threat monitoring and detection
    - Incident response for AI systems
    """
    if not analyze_document_applicability(text, title)['ai_cybersecurity']:
        return None
    
    text_lower = text.lower()
    score = 0
    max_score = 100
    
    # Encryption standards (25 points)
    encryption_indicators = [
        'ai encryption', 'model encryption', 'data encryption', 'encrypted training',
        'secure computation', 'homomorphic encryption', 'federated learning security'
    ]
    encryption_score = min(25, sum(5 for indicator in encryption_indicators if indicator in text_lower))
    score += encryption_score
    
    # Authentication mechanisms (25 points)
    auth_indicators = [
        'ai authentication', 'model authentication', 'api security', 'access control',
        'identity verification', 'multi-factor', 'zero trust', 'credential management'
    ]
    auth_score = min(25, sum(3 for indicator in auth_indicators if indicator in text_lower))
    score += auth_score
    
    # Threat monitoring (25 points)
    monitoring_indicators = [
        'adversarial attack', 'model poisoning', 'data poisoning', 'threat detection',
        'anomaly detection', 'security monitoring', 'ai security testing', 'vulnerability assessment'
    ]
    monitoring_score = min(25, sum(3 for indicator in monitoring_indicators if indicator in text_lower))
    score += monitoring_score
    
    # Incident response (25 points)
    incident_indicators = [
        'incident response', 'security incident', 'breach response', 'recovery plan',
        'forensics', 'containment', 'ai incident', 'security playbook'
    ]
    incident_score = min(25, sum(3 for indicator in incident_indicators if indicator in text_lower))
    score += incident_score
    
    return min(100, score)

def score_quantum_cybersecurity_maturity(text: str, title: str) -> Optional[int]:
    """
    Score Quantum Cybersecurity Maturity (1-5) based on QCMEA patent framework.
    
    Patent levels:
    1. Initial: Basic awareness
    2. Basic: Foundational measures
    3. Intermediate: Scalable solutions
    4. Advanced: Comprehensive integration
    5. Dynamic: Continuous adaptability
    """
    if not analyze_document_applicability(text, title)['quantum_cybersecurity']:
        return None
    
    text_lower = text.lower()
    maturity_score = 1  # Start at Initial level
    
    # Level 2: Basic Maturity - Foundational quantum-resistant measures
    basic_indicators = [
        'post-quantum cryptography', 'quantum-safe', 'quantum-resistant',
        'hybrid cryptographic', 'quantum awareness', 'quantum risk'
    ]
    if any(indicator in text_lower for indicator in basic_indicators):
        maturity_score = 2
    
    # Level 3: Intermediate Maturity - Scalable quantum-safe solutions
    intermediate_indicators = [
        'lattice-based', 'quantum key distribution', 'pqc implementation',
        'quantum migration', 'crypto agility', 'quantum readiness assessment'
    ]
    if any(indicator in text_lower for indicator in intermediate_indicators):
        maturity_score = 3
    
    # Level 4: Advanced Maturity - Comprehensive integration with NIST standards
    advanced_indicators = [
        'nist post-quantum', 'comprehensive quantum', 'quantum integration',
        'quantum governance', 'quantum compliance', 'quantum standards'
    ]
    if any(indicator in text_lower for indicator in advanced_indicators):
        maturity_score = 4
    
    # Level 5: Dynamic Maturity - Continuous adaptability with ML
    dynamic_indicators = [
        'adaptive quantum', 'quantum machine learning', 'continuous quantum',
        'quantum optimization', 'quantum evolution', 'dynamic quantum response'
    ]
    if any(indicator in text_lower for indicator in dynamic_indicators):
        maturity_score = 5
    
    return maturity_score

def score_ai_ethics(text: str, title: str) -> Optional[int]:
    """
    Score AI Ethics (0-100) based on patent ethical compliance criteria.
    
    Patent criteria:
    - Fairness and bias mitigation
    - Transparency and explainability
    - Accountability mechanisms
    - Privacy protection
    """
    if not analyze_document_applicability(text, title)['ai_ethics']:
        return None
    
    text_lower = text.lower()
    score = 0
    
    # Fairness and bias mitigation (25 points)
    fairness_indicators = [
        'bias mitigation', 'algorithmic fairness', 'bias testing', 'fair ai',
        'discrimination prevention', 'equitable', 'bias audit', 'fairness metrics'
    ]
    fairness_score = min(25, sum(3 for indicator in fairness_indicators if indicator in text_lower))
    score += fairness_score
    
    # Transparency and explainability (25 points)
    transparency_indicators = [
        'explainable ai', 'interpretable', 'transparency', 'explainability',
        'ai explanation', 'model interpretation', 'decision transparency', 'algorithmic transparency'
    ]
    transparency_score = min(25, sum(3 for indicator in transparency_indicators if indicator in text_lower))
    score += transparency_score
    
    # Accountability mechanisms (25 points)
    accountability_indicators = [
        'accountability', 'responsible ai', 'ai governance', 'oversight',
        'human oversight', 'ai responsibility', 'ethical review', 'ai audit'
    ]
    accountability_score = min(25, sum(3 for indicator in accountability_indicators if indicator in text_lower))
    score += accountability_score
    
    # Privacy protection (25 points)
    privacy_indicators = [
        'privacy protection', 'data privacy', 'privacy preserving', 'differential privacy',
        'privacy by design', 'data protection', 'personal data', 'privacy rights'
    ]
    privacy_score = min(25, sum(3 for indicator in privacy_indicators if indicator in text_lower))
    score += privacy_score
    
    return min(100, score)

def score_quantum_ethics(text: str, title: str) -> Optional[int]:
    """
    Score Quantum Ethics (0-100) based on emerging quantum ethical considerations.
    
    Emerging criteria:
    - Quantum advantage ethics
    - Quantum privacy implications
    - Quantum security standards
    - Equitable quantum access
    """
    if not analyze_document_applicability(text, title)['quantum_ethics']:
        return None
    
    text_lower = text.lower()
    score = 0
    
    # Quantum advantage ethics (25 points)
    advantage_indicators = [
        'quantum advantage', 'quantum supremacy', 'quantum ethics', 'quantum responsibility',
        'quantum governance', 'quantum oversight', 'quantum accountability'
    ]
    advantage_score = min(25, sum(4 for indicator in advantage_indicators if indicator in text_lower))
    score += advantage_score
    
    # Quantum privacy implications (25 points)
    privacy_indicators = [
        'quantum privacy', 'quantum anonymity', 'quantum confidentiality',
        'quantum data protection', 'quantum surveillance', 'quantum rights'
    ]
    privacy_score = min(25, sum(4 for indicator in privacy_indicators if indicator in text_lower))
    score += privacy_score
    
    # Quantum security standards (25 points)
    security_indicators = [
        'quantum security standards', 'quantum compliance', 'quantum regulation',
        'quantum policy', 'quantum guidelines', 'quantum framework'
    ]
    security_score = min(25, sum(4 for indicator in security_indicators if indicator in security_indicators))
    score += security_score
    
    # Equitable quantum access (25 points)
    access_indicators = [
        'quantum access', 'quantum equity', 'quantum inclusion', 'quantum democracy',
        'quantum divide', 'quantum fairness', 'quantum justice'
    ]
    access_score = min(25, sum(4 for indicator in access_indicators if indicator in text_lower))
    score += access_score
    
    return min(100, score)

def comprehensive_document_scoring(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Perform comprehensive scoring across all four frameworks.
    
    Returns:
        Dict with scores for each framework or None if not applicable
    """
    return {
        'ai_cybersecurity': score_ai_cybersecurity_maturity(text, title),
        'quantum_cybersecurity': score_quantum_cybersecurity_maturity(text, title),
        'ai_ethics': score_ai_ethics(text, title),
        'quantum_ethics': score_quantum_ethics(text, title)
    }

def format_score_display(score: Optional[int], framework: str) -> str:
    """
    Format score for display in the UI.
    
    Args:
        score: The computed score or None if not applicable
        framework: The scoring framework name
        
    Returns:
        Formatted string for display
    """
    if score is None:
        return "N/A"
    
    if framework == 'quantum_cybersecurity':
        # QCMEA uses 1-5 scale
        return str(score)
    else:
        # Others use 0-100 scale
        return str(score)

def get_score_badge_color(score: Optional[int], framework: str) -> str:
    """
    Get appropriate badge color based on score and framework.
    
    Returns:
        CSS color value for the score badge
    """
    if score is None:
        return "#9CA3AF"  # Gray for N/A
    
    if framework == 'quantum_cybersecurity':
        # QCMEA 1-5 scale colors
        colors = {1: "#DC2626", 2: "#EA580C", 3: "#D97706", 4: "#059669", 5: "#7C3AED"}
        return colors.get(score, "#9CA3AF")
    else:
        # 0-100 scale colors
        if score >= 80:
            return "#059669"  # Green
        elif score >= 60:
            return "#D97706"  # Amber
        elif score >= 40:
            return "#EA580C"  # Orange
        else:
            return "#DC2626"  # Red