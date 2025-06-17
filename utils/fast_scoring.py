"""
Fast Scoring System for GUARDIAN
Optimized scoring without complex synthesis for better performance
"""

import re
from typing import Dict, Optional

def fast_comprehensive_scoring(text: str, title: str) -> Dict[str, Optional[int]]:
    """Fast comprehensive scoring that bypasses synthesis engine"""
    
    # Basic text preprocessing
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # AI cybersecurity patterns
    ai_cyber_patterns = [
        'ai security', 'artificial intelligence security', 'machine learning security',
        'ai threat', 'adversarial ai', 'ai governance', 'ai risk management',
        'neural network security', 'deep learning security', 'ai safety'
    ]
    
    # Quantum cybersecurity patterns  
    quantum_cyber_patterns = [
        'quantum cryptography', 'quantum security', 'post-quantum',
        'quantum computing security', 'quantum-resistant', 'quantum key'
    ]
    
    # AI ethics patterns
    ai_ethics_patterns = [
        'ai ethics', 'ai bias', 'algorithmic bias', 'ai fairness',
        'ai transparency', 'explainable ai', 'ai accountability'
    ]
    
    # Quantum ethics patterns
    quantum_ethics_patterns = [
        'quantum ethics', 'quantum computing ethics', 'quantum privacy'
    ]
    
    def calculate_score(patterns, text, max_score=100):
        """Calculate score based on pattern matching"""
        score = 0
        word_count = len(text.split())
        
        for pattern in patterns:
            matches = len(re.findall(pattern, text, re.IGNORECASE))
            if matches > 0:
                # Base score for presence
                score += 20
                # Additional score for frequency
                frequency_bonus = min(matches * 5, 30)
                score += frequency_bonus
        
        # Normalize by document length
        if word_count > 100:
            length_factor = min(word_count / 500, 2.0)
            score = int(score * length_factor)
        
        return min(score, max_score)
    
    # Calculate scores
    scores = {}
    
    # AI Cybersecurity
    if any(pattern in combined for pattern in ['ai', 'artificial intelligence', 'machine learning']):
        scores['ai_cybersecurity'] = calculate_score(ai_cyber_patterns, combined)
    else:
        scores['ai_cybersecurity'] = None
    
    # Quantum Cybersecurity (1-5 scale)
    if any(pattern in combined for pattern in ['quantum', 'post-quantum']):
        base_score = calculate_score(quantum_cyber_patterns, combined)
        scores['quantum_cybersecurity'] = min(max(int(base_score / 20), 1), 5)
    else:
        scores['quantum_cybersecurity'] = None
    
    # AI Ethics
    if any(pattern in combined for pattern in ['ai', 'artificial intelligence', 'ethics']):
        scores['ai_ethics'] = calculate_score(ai_ethics_patterns, combined)
    else:
        scores['ai_ethics'] = None
    
    # Quantum Ethics (1-5 scale)
    if any(pattern in combined for pattern in ['quantum', 'ethics']):
        base_score = calculate_score(quantum_ethics_patterns, combined)
        scores['quantum_ethics'] = min(max(int(base_score / 20), 1), 5)
    else:
        scores['quantum_ethics'] = None
    
    # Apply minimum thresholds for detected topics
    if scores['ai_cybersecurity'] is not None and scores['ai_cybersecurity'] < 20:
        scores['ai_cybersecurity'] = 20
    if scores['ai_ethics'] is not None and scores['ai_ethics'] < 20:
        scores['ai_ethics'] = 20
    if scores['quantum_cybersecurity'] is not None and scores['quantum_cybersecurity'] < 1:
        scores['quantum_cybersecurity'] = 1
    if scores['quantum_ethics'] is not None and scores['quantum_ethics'] < 1:
        scores['quantum_ethics'] = 1
    
    return scores