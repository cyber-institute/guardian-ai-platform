"""
Calculate AI framework scores for NIST AI Risk Management Framework
"""

def calculate_ai_cybersecurity_score(content, title):
    """Calculate AI Cybersecurity Framework score"""
    content_lower = content.lower()
    title_lower = title.lower()
    
    score = 0
    
    # Core AI security concepts (15 points each)
    security_indicators = [
        'risk management', 'security', 'trustworthy', 'governance',
        'accountability', 'transparency', 'fairness', 'reliability'
    ]
    
    for indicator in security_indicators:
        if indicator in content_lower or indicator in title_lower:
            score += 15
    
    # AI-specific security terms (10 points each)
    ai_security_terms = [
        'ai risk', 'artificial intelligence', 'machine learning',
        'bias', 'privacy', 'safety', 'robustness'
    ]
    
    for term in ai_security_terms:
        if term in content_lower or term in title_lower:
            score += 10
    
    # Framework-specific terms (5 points each)
    framework_terms = ['framework', 'standard', 'guideline', 'nist']
    
    for term in framework_terms:
        if term in content_lower or term in title_lower:
            score += 5
    
    return min(score, 100)  # Cap at 100

def calculate_ai_ethics_score(content, title):
    """Calculate AI Ethics Framework score"""
    content_lower = content.lower()
    title_lower = title.lower()
    
    score = 0
    
    # Core ethics concepts (20 points each)
    ethics_indicators = [
        'fairness', 'accountability', 'transparency', 'bias',
        'ethics', 'responsible', 'trustworthy'
    ]
    
    for indicator in ethics_indicators:
        if indicator in content_lower or indicator in title_lower:
            score += 20
    
    # AI ethics specific terms (15 points each)
    ai_ethics_terms = [
        'ai governance', 'algorithmic fairness', 'explainable ai',
        'human oversight', 'privacy protection'
    ]
    
    for term in ai_ethics_terms:
        if term in content_lower or term in title_lower:
            score += 15
    
    # Risk management ethics (10 points each)
    risk_ethics_terms = ['risk management', 'harm mitigation', 'societal impact']
    
    for term in risk_ethics_terms:
        if term in content_lower or term in title_lower:
            score += 10
    
    return min(score, 100)  # Cap at 100

# NIST document content and title
content = """Download the AI RMF 1.0 View the AI RMF Playbook Visit the AI Resource Center In collaboration with the private and public sectors, NIST has developed a framework to better manage risks to individuals, organizations, and society associated with artificial intelligence (AI). The NIST AI Risk Management Framework"""

title = "NIST AI Risk Management Framework"

# Calculate scores
ai_cybersecurity_score = calculate_ai_cybersecurity_score(content, title)
ai_ethics_score = calculate_ai_ethics_score(content, title)

print(f"AI Cybersecurity Framework Score: {ai_cybersecurity_score}")
print(f"AI Ethics Framework Score: {ai_ethics_score}")

# Create metadata JSON
import json

metadata = {
    "framework_scores": {
        "ai_cybersecurity": ai_cybersecurity_score,
        "ai_ethics": ai_ethics_score
    },
    "topic_corrected": True,
    "scoring_method": "content_analysis"
}

print(f"Metadata JSON: {json.dumps(metadata)}")