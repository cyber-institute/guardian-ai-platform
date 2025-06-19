"""
Enhanced Pattern-Based Scoring Engine
Combines patent formulas with LLM-informed content analysis patterns
Optimized for comprehensive document scoring without API dependencies
"""

from typing import Dict, Optional
import re

def analyze_content_depth(text: str, title: str) -> Dict[str, int]:
    """
    Analyze content depth using patent-based criteria with LLM-informed patterns
    """
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # Content depth indicators
    implementation_depth = len(re.findall(r'\b(implement|deploy|operational|execute|establish|develop|create|build|design)\w*', combined))
    framework_mentions = len(re.findall(r'\b(framework|standard|guideline|policy|procedure|protocol|methodology)\w*', combined))
    technical_detail = len(re.findall(r'\b(architecture|system|process|mechanism|algorithm|component|structure)\w*', combined))
    
    # Assessment and evaluation indicators
    assessment_terms = len(re.findall(r'\b(assess|evaluat|analyz|measur|test|validat|verif|audit|review)\w*', combined))
    risk_management = len(re.findall(r'\b(risk|threat|vulnerabil|attack|security|protect|defend|mitigat)\w*', combined))
    
    return {
        'implementation_depth': min(25, implementation_depth * 3),
        'framework_quality': min(20, framework_mentions * 4),
        'technical_detail': min(20, technical_detail * 2),
        'assessment_rigor': min(20, assessment_terms * 3),
        'risk_awareness': min(15, risk_management * 2)
    }

def score_ai_cybersecurity_enhanced(text: str, title: str) -> Optional[int]:
    """
    Enhanced AI cybersecurity scoring using patent formulas + LLM insights
    """
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # Must have AI/ML context
    ai_context = any(term in combined for term in [
        'ai', 'artificial intelligence', 'machine learning', 'neural network',
        'deep learning', 'automated', 'intelligent system', 'algorithm'
    ])
    
    # Must have security context
    security_context = any(term in combined for term in [
        'security', 'cybersecurity', 'threat', 'risk', 'vulnerability',
        'attack', 'defense', 'protection', 'secure', 'safety'
    ])
    
    if not (ai_context and security_context):
        return None
    
    base_score = 0
    
    # Core AI security concepts (40 points)
    ai_security_terms = [
        'ai security', 'ai safety', 'secure ai', 'ai governance', 'ai risk',
        'ai threat', 'ai vulnerability', 'adversarial', 'model security',
        'ai robustness', 'ai assurance', 'trustworthy ai', 'responsible ai',
        'artificial intelligence', 'machine learning', 'neural network'
    ]
    ai_security_score = min(40, sum(3 for term in ai_security_terms if term in combined))
    
    # Boost for documents with strong AI + security combination
    if any(ai_term in combined for ai_term in ['ai', 'artificial intelligence', 'machine learning']):
        security_boost = min(20, sum(2 for term in ['security', 'cybersecurity', 'threat', 'risk', 'vulnerability'] if term in combined))
        ai_security_score += security_boost
    
    base_score += min(40, ai_security_score)
    
    # Implementation and deployment (25 points)
    implementation_terms = [
        'deployment', 'implementation', 'operational', 'production',
        'enterprise', 'scalable', 'systematic', 'comprehensive'
    ]
    impl_score = min(25, sum(3 for term in implementation_terms if term in combined))
    base_score += impl_score
    
    # Security practices and controls (25 points)
    security_practices = [
        'authentication', 'authorization', 'encryption', 'monitoring',
        'audit', 'compliance', 'governance', 'oversight', 'testing',
        'validation', 'verification', 'assessment'
    ]
    practices_score = min(25, sum(2 for term in security_practices if term in combined))
    base_score += practices_score
    
    # Advanced security concepts (20 points)
    advanced_terms = [
        'red team', 'penetration', 'vulnerability assessment', 'threat modeling',
        'incident response', 'forensics', 'zero trust', 'defense in depth',
        'security architecture', 'threat intelligence'
    ]
    advanced_score = min(20, sum(4 for term in advanced_terms if term in combined))
    base_score += advanced_score
    
    # Content depth analysis
    depth_analysis = analyze_content_depth(text, title)
    depth_bonus = sum(depth_analysis.values()) // 5  # Scale down depth bonus
    
    final_score = min(100, base_score + depth_bonus)
    return final_score if final_score > 0 else None

def score_ai_ethics_enhanced(text: str, title: str) -> Optional[int]:
    """
    Enhanced AI ethics scoring using patent formulas + LLM insights
    """
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # Must have AI context
    ai_context = any(term in combined for term in [
        'ai', 'artificial intelligence', 'machine learning', 'automated',
        'algorithm', 'intelligent system'
    ])
    
    # Must have ethics/governance context
    ethics_context = any(term in combined for term in [
        'ethics', 'ethical', 'responsible', 'governance', 'accountability',
        'transparency', 'fairness', 'bias', 'trust', 'inclusion'
    ])
    
    if not (ai_context and ethics_context):
        return None
    
    base_score = 0
    
    # Core AI ethics concepts (30 points)
    ai_ethics_terms = [
        'responsible ai', 'ai ethics', 'ethical ai', 'ai governance',
        'trustworthy ai', 'ai accountability', 'ai transparency',
        'algorithmic fairness', 'ai bias', 'explainable ai'
    ]
    ethics_score = min(30, sum(5 for term in ai_ethics_terms if term in combined))
    base_score += ethics_score
    
    # Fairness and bias (25 points)
    fairness_terms = [
        'bias', 'fairness', 'discrimination', 'equity', 'inclusion',
        'diversity', 'representative', 'equitable', 'unbiased'
    ]
    fairness_score = min(25, sum(3 for term in fairness_terms if term in combined))
    base_score += fairness_score
    
    # Transparency and explainability (25 points)
    transparency_terms = [
        'transparency', 'explainable', 'interpretable', 'understandable',
        'clear', 'open', 'accessible', 'comprehensible'
    ]
    transparency_score = min(25, sum(3 for term in transparency_terms if term in combined))
    base_score += transparency_score
    
    # Governance and oversight (20 points)
    governance_terms = [
        'governance', 'oversight', 'accountability', 'responsibility',
        'compliance', 'regulation', 'policy', 'framework', 'guidelines'
    ]
    governance_score = min(20, sum(2 for term in governance_terms if term in combined))
    base_score += governance_score
    
    # Content depth analysis
    depth_analysis = analyze_content_depth(text, title)
    depth_bonus = sum(depth_analysis.values()) // 5
    
    final_score = min(100, base_score + depth_bonus)
    return final_score if final_score > 0 else None

def score_quantum_cybersecurity_enhanced(text: str, title: str) -> Optional[int]:
    """
    Enhanced quantum cybersecurity scoring using patent formulas
    """
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # Must have quantum context
    quantum_context = any(term in combined for term in [
        'quantum', 'post-quantum', 'quantum computing', 'quantum cryptography',
        'quantum-safe', 'quantum threat', 'pqc', 'quantum key'
    ])
    
    # Must have security context
    security_context = any(term in combined for term in [
        'security', 'cybersecurity', 'cryptography', 'encryption',
        'threat', 'risk', 'vulnerability', 'protection'
    ])
    
    if not (quantum_context and security_context):
        return None
    
    base_score = 0
    
    # Core quantum security concepts (35 points)
    quantum_security_terms = [
        'post-quantum cryptography', 'quantum-safe encryption', 'quantum threat',
        'quantum security', 'quantum cryptography', 'quantum key distribution',
        'quantum-resistant', 'cryptographic agility'
    ]
    quantum_score = min(35, sum(7 for term in quantum_security_terms if term in combined))
    base_score += quantum_score
    
    # Implementation readiness (25 points)
    implementation_terms = [
        'migration', 'transition', 'deployment', 'implementation',
        'adoption', 'integration', 'upgrade', 'modernization'
    ]
    impl_score = min(25, sum(4 for term in implementation_terms if term in combined))
    base_score += impl_score
    
    # Threat awareness (25 points)
    threat_terms = [
        'threat', 'risk', 'vulnerability', 'attack', 'cryptanalysis',
        'quantum advantage', 'shor', 'grover', 'quantum supremacy'
    ]
    threat_score = min(25, sum(3 for term in threat_terms if term in combined))
    base_score += threat_score
    
    # Standards and compliance (15 points)
    standards_terms = [
        'nist', 'standard', 'compliance', 'certification', 'framework',
        'guideline', 'recommendation', 'best practice'
    ]
    standards_score = min(15, sum(2 for term in standards_terms if term in combined))
    base_score += standards_score
    
    # Content depth analysis
    depth_analysis = analyze_content_depth(text, title)
    depth_bonus = sum(depth_analysis.values()) // 4
    
    final_score = min(100, base_score + depth_bonus)
    return final_score if final_score > 0 else None

def score_quantum_ethics_enhanced(text: str, title: str) -> Optional[int]:
    """
    Enhanced quantum ethics scoring
    """
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # Must have quantum context
    quantum_context = 'quantum' in combined
    
    # Must have ethics/social context
    ethics_context = any(term in combined for term in [
        'ethics', 'ethical', 'inclusion', 'access', 'equity',
        'sustainability', 'society', 'social', 'governance'
    ])
    
    if not (quantum_context and ethics_context):
        return None
    
    base_score = 0
    
    # Core quantum ethics concepts (35 points)
    quantum_ethics_terms = [
        'quantum ethics', 'quantum governance', 'quantum inclusion',
        'quantum access', 'quantum equity', 'quantum sustainability'
    ]
    ethics_score = min(35, sum(8 for term in quantum_ethics_terms if term in combined))
    base_score += ethics_score
    
    # Access and inclusion (30 points)
    access_terms = [
        'access', 'inclusion', 'equity', 'diversity', 'participation',
        'opportunity', 'education', 'training', 'workforce'
    ]
    access_score = min(30, sum(4 for term in access_terms if term in combined))
    base_score += access_score
    
    # Sustainability and responsibility (25 points)
    sustainability_terms = [
        'sustainability', 'sustainable', 'responsible', 'environmental',
        'energy', 'resource', 'efficiency', 'impact'
    ]
    sustainability_score = min(25, sum(3 for term in sustainability_terms if term in combined))
    base_score += sustainability_score
    
    # Social impact (10 points)
    social_terms = [
        'society', 'social', 'community', 'public', 'benefit',
        'welfare', 'development', 'progress'
    ]
    social_score = min(10, sum(2 for term in social_terms if term in combined))
    base_score += social_score
    
    # Content depth analysis
    depth_analysis = analyze_content_depth(text, title)
    depth_bonus = sum(depth_analysis.values()) // 4
    
    final_score = min(100, base_score + depth_bonus)
    return final_score if final_score > 0 else None

def enhanced_pattern_scoring(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Comprehensive enhanced pattern scoring combining patent formulas with content analysis
    """
    return {
        'ai_cybersecurity': score_ai_cybersecurity_enhanced(text, title),
        'ai_ethics': score_ai_ethics_enhanced(text, title),
        'quantum_cybersecurity': score_quantum_cybersecurity_enhanced(text, title),
        'quantum_ethics': score_quantum_ethics_enhanced(text, title)
    }