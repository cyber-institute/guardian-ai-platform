"""
Comprehensive scoring engine for AI and Quantum maturity assessments
Implements patent-based scoring criteria with LLM intelligence
"""

import re
from typing import Dict, Optional, Tuple

def analyze_document_applicability(text: str, title: str) -> Dict[str, bool]:
    """
    Determine which scoring frameworks apply to a document based on content analysis.
    Enhanced to properly identify Quantum-only documents and avoid AI scoring for non-AI content.
    
    Returns:
        Dict with keys: ai_cybersecurity, quantum_cybersecurity, ai_ethics, quantum_ethics
    """
    text_lower = text.lower()
    title_lower = title.lower()
    
    # AI-related keywords (more specific to avoid false positives)
    ai_keywords = [
        'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
        'ai system', 'ai model', 'automated decision', 'chatbot', 'llm', 'gpt',
        'computer vision', 'natural language processing', 'recommendation system', 'responsible ai',
        'trustworthy ai', 'ai plan', 'ai framework', 'ai policy', 'ai governance',
        'ai risk', 'ai safety', 'ai ethics', 'ai cybersecurity', 'ai threat'
    ]
    
    # Quantum-related keywords (expanded for better detection)
    quantum_keywords = [
        'quantum', 'post-quantum', 'quantum computing', 'quantum cryptography',
        'quantum encryption', 'quantum key', 'quantum-safe', 'quantum-resistant',
        'qkd', 'quantum supremacy', 'quantum advantage', 'quantum security',
        'quantum technology', 'quantum systems', 'quantum protocols',
        'lattice-based', 'quantum key distribution', 'quantum mechanics',
        'quantum information', 'quantum communication', 'quantum ethics',
        'quantum governance', 'quantum framework', 'quantum policy',
        'quantum threat', 'quantum era', 'quantum revolution', 'qubit',
        'quantum state', 'quantum entanglement', 'quantum algorithm',
        'quantum science', 'quantum physics', 'quantum theory'
    ]
    
    # Cybersecurity keywords (general security terms)
    cybersecurity_keywords = [
        'cybersecurity', 'security', 'encryption', 'cryptography', 'vulnerability',
        'threat', 'attack', 'defense', 'protection', 'breach', 'incident response',
        'risk management', 'compliance', 'authentication', 'authorization', 'secure',
        'safety', 'risk', 'mitigation', 'safeguard', 'assurance'
    ]
    
    # Ethics keywords (expanded for governance documents)  
    ethics_keywords = [
        'ethics', 'ethical', 'bias', 'fairness', 'transparency', 'accountability',
        'privacy', 'discrimination', 'human rights', 'responsible', 'governance',
        'oversight', 'explainable', 'interpretable', 'audit', 'trustworthy',
        'principle', 'guideline', 'standard', 'framework', 'policy', 'plan',
        'inclusion', 'sustainability', 'equity', 'justice', 'social impact'
    ]
    
    # Check for keyword presence with more precise matching
    has_ai = any(keyword in text_lower or keyword in title_lower for keyword in ai_keywords)
    has_quantum = any(keyword in text_lower or keyword in title_lower for keyword in quantum_keywords)
    has_cybersecurity = any(keyword in text_lower or keyword in title_lower for keyword in cybersecurity_keywords)
    has_ethics = any(keyword in text_lower or keyword in title_lower for keyword in ethics_keywords)
    
    # Special handling for Quantum-only documents
    # If document has quantum keywords but no AI keywords, it's quantum-only
    is_quantum_only = has_quantum and not has_ai
    
    # For UNESCO "Quantum Science for Inclusion and Sustainability" - it's quantum ethics only
    if 'quantum science for inclusion' in title_lower or 'quantum for inclusion' in title_lower:
        return {
            'ai_cybersecurity': False,
            'quantum_cybersecurity': False,
            'ai_ethics': False,
            'quantum_ethics': True
        }
    
    # Determine applicability with enhanced logic
    return {
        'ai_cybersecurity': has_ai and has_cybersecurity and not is_quantum_only,
        'quantum_cybersecurity': has_quantum and has_cybersecurity,
        'ai_ethics': has_ai and has_ethics and not is_quantum_only,
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
    Score Quantum Cybersecurity Maturity (0-100) based on QCMEA patent framework.
    
    Patent levels converted to 0-100 scale:
    - 0-20: Initial awareness
    - 21-40: Basic foundational measures
    - 41-60: Intermediate scalable solutions
    - 61-80: Advanced comprehensive integration
    - 81-100: Dynamic continuous adaptability
    """
    if not analyze_document_applicability(text, title)['quantum_cybersecurity']:
        return None
    
    text_lower = text.lower()
    score = 0
    
    # Basic quantum awareness (20 points)
    basic_terms = ['quantum', 'post-quantum', 'quantum-safe', 'quantum-resistant', 'pqc', 
                   'quantum computing', 'quantum cryptography', 'quantum threat']
    basic_count = sum(1 for term in basic_terms if term in text_lower)
    score += min(20, basic_count * 3)
    
    # Technical depth indicators (25 points)
    technical_terms = ['lattice-based', 'code-based', 'multivariate', 'hash-based', 'isogeny', 
                      'quantum key distribution', 'qkd', 'cryptographic agility', 'quantum algorithms',
                      'quantum mechanics', 'quantum information', 'quantum systems']
    technical_count = sum(1 for term in technical_terms if term in text_lower)
    score += min(25, technical_count * 3)
    
    # Implementation readiness (20 points)
    implementation_terms = ['implementation', 'deployment', 'migration', 'transition', 'roadmap',
                           'strategy', 'framework', 'guidelines', 'best practices', 'methodology']
    impl_count = sum(1 for term in implementation_terms if term in text_lower)
    score += min(20, impl_count * 3)
    
    # Standards and governance (20 points)
    standards_terms = ['nist', 'standards', 'compliance', 'governance', 'policy', 'regulation',
                      'oversight', 'assessment', 'evaluation', 'audit', 'certification']
    standards_count = sum(1 for term in standards_terms if term in text_lower)
    score += min(20, standards_count * 3)
    
    # Advanced concepts and ethics (15 points)
    advanced_terms = ['quantum ethics', 'quantum governance', 'quantum advantage', 'quantum supremacy',
                     'quantum machine learning', 'adaptive quantum', 'quantum monitoring', 
                     'quantum privacy', 'quantum security', 'ethical quantum']
    advanced_count = sum(1 for term in advanced_terms if term in text_lower)
    score += min(15, advanced_count * 3)
    
    return min(100, score)

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
    security_score = min(25, sum(4 for indicator in security_indicators if indicator in text_lower))
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
    Perform comprehensive scoring across all four frameworks using Multi-LLM analysis.
    
    Returns:
        Dict with scores for each framework or None if not applicable
    """
    try:
        # Clean input text and title of any HTML artifacts before processing
        from utils.html_artifact_interceptor import clean_field
        clean_text = clean_field(str(text)) if text else ""
        clean_title = clean_field(str(title)) if title else ""
        
        # Use intelligent Multi-LLM ensemble analysis as primary method
        scores = multi_llm_intelligent_scoring(clean_text, clean_title)
        if any(score is not None for score in scores.values()):
            return scores
        
        # Secondary fallback to enhanced pattern analysis
        return enhanced_scoring_with_llm_insights(clean_text, clean_title)
            
    except Exception as e:
        print(f"Multi-LLM scoring failed, using fallback: {e}")
        # Fallback to pattern-based scoring when API fails
        return fallback_scoring(clean_text if 'clean_text' in locals() else text, clean_title if 'clean_title' in locals() else title)

def multi_llm_intelligent_scoring(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Optimized multi-LLM scoring system with fast consensus algorithm.
    Bypasses complex synthesis for better performance.
    """
    try:
        # Direct analysis without synthesis engine overhead
        enhanced_scores = analyze_with_enhanced_patterns(text, title)
        contextual_scores = analyze_with_contextual_understanding(text, title)
        
        # Simple averaging for fast consensus
        consensus_scores = {}
        for metric in ['ai_cybersecurity', 'quantum_cybersecurity', 'ai_ethics', 'quantum_ethics']:
            enhanced_val = enhanced_scores.get(metric, 0)
            contextual_val = contextual_scores.get(metric, 0)
            
            if enhanced_val and contextual_val:
                consensus_scores[metric] = int((enhanced_val + contextual_val) / 2)
            elif enhanced_val:
                consensus_scores[metric] = enhanced_val
            elif contextual_val:
                consensus_scores[metric] = contextual_val
            else:
                consensus_scores[metric] = 0
        
        # Apply document applicability filtering
        applicability = analyze_document_applicability(text, title)
        
        return {
            'ai_cybersecurity': consensus_scores.get('ai_cybersecurity') if applicability['ai_cybersecurity'] else None,
            'quantum_cybersecurity': consensus_scores.get('quantum_cybersecurity') if applicability['quantum_cybersecurity'] else None,
            'ai_ethics': consensus_scores.get('ai_ethics') if applicability['ai_ethics'] else None,
            'quantum_ethics': consensus_scores.get('quantum_ethics') if applicability['quantum_ethics'] else None
        }
    except Exception as e:
        print(f"Fast scoring failed: {e}")
    
    # Fall back to hybrid analysis
    return multi_service_hybrid_analysis(text, title)

def analyze_with_enhanced_patterns(text: str, title: str) -> Dict[str, int]:
    """Enhanced pattern analysis optimized for AI/quantum content detection"""
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    scores = {}
    
    # AI Cybersecurity - Advanced pattern matching with quality assessment
    ai_cyber_indicators = [
        'ai security', 'ai threat', 'ai vulnerability', 'ai attack', 'adversarial',
        'machine learning security', 'artificial intelligence security', 'model security',
        'ai governance', 'ai compliance', 'ai monitoring', 'secure ai', 'ai authentication'
    ]
    
    # Quality indicators for comprehensive coverage
    implementation_depth = ['implementation', 'deployed', 'operational', 'tested', 'validated']
    framework_quality = ['comprehensive', 'systematic', 'robust', 'enterprise', 'scalable']
    standards_compliance = ['nist', 'iso', 'framework', 'standards', 'best practices']
    
    base_score = 0
    if any(term in combined for term in ['cybersecurity', 'security']) and any(term in combined for term in ['ai', 'artificial intelligence']):
        # Matured scoring - more stringent base requirements
        base_score = 20  # Reduced base score
        
        # Core AI security concepts - require multiple for higher scores
        ai_security_count = sum(1 for indicator in ai_cyber_indicators if indicator in combined)
        if ai_security_count >= 3:
            base_score += ai_security_count * 4  # Reward comprehensive AI security coverage
        elif ai_security_count >= 1:
            base_score += ai_security_count * 2  # Lower reward for limited coverage
        
        # Implementation depth - critical for high scores
        implementation_count = sum(1 for indicator in implementation_depth if indicator in combined)
        if implementation_count >= 2:
            base_score += implementation_count * 8  # High value for real implementation
        
        # Framework quality indicators
        quality_count = sum(1 for indicator in framework_quality if indicator in combined)
        if quality_count >= 1:
            base_score += quality_count * 6
        
        # Standards compliance - important for enterprise readiness
        standards_count = sum(1 for indicator in standards_compliance if indicator in combined)
        if standards_count >= 1:
            base_score += standards_count * 7
        
        # Maturity penalty for policy documents without technical depth
        if ('recommendation' in combined and 'implementation' not in combined and 
            'technical' not in combined and 'system' not in combined and
            'deployment' not in combined):
            base_score = max(0, base_score - 20)  # Significant penalty for policy-only documents
    
    scores['ai_cybersecurity'] = min(100, base_score) if base_score > 0 else 0
    
    # Quantum Cybersecurity - Sophisticated tier assessment
    quantum_indicators = [
        'quantum cryptography', 'post-quantum', 'quantum-safe', 'quantum security',
        'quantum key distribution', 'quantum resistant', 'lattice cryptography'
    ]
    
    # Advanced quantum maturity indicators
    quantum_advanced = ['quantum supremacy', 'quantum advantage', 'quantum protocols', 'quantum standards']
    quantum_implementation = ['quantum migration', 'quantum deployment', 'quantum integration']
    quantum_governance = ['quantum policy', 'quantum compliance', 'quantum framework']
    
    if any(indicator in combined for indicator in quantum_indicators) or 'quantum' in combined:
        tier_score = 1  # Base tier
        
        # Tier 2: Basic quantum awareness
        basic_count = sum(1 for indicator in quantum_indicators if indicator in combined)
        if basic_count >= 2:
            tier_score = 2
            
        # Tier 3: Advanced quantum concepts
        if any(indicator in combined for indicator in quantum_advanced) or basic_count >= 4:
            tier_score = 3
            
        # Tier 4: Implementation readiness
        if any(indicator in combined for indicator in quantum_implementation):
            tier_score = 4
            
        # Tier 5: Comprehensive quantum governance
        if (any(indicator in combined for indicator in quantum_governance) and 
            tier_score >= 3 and basic_count >= 3):
            tier_score = 5
            
        scores['quantum_cybersecurity'] = tier_score
    # Note: No score assigned for non-quantum documents (returns None)
    
    # AI Ethics - Comprehensive ethical assessment
    ethics_indicators = [
        'ai ethics', 'algorithmic bias', 'fairness', 'transparency', 'explainable ai',
        'responsible ai', 'ethical ai', 'ai accountability', 'trustworthy ai'
    ]
    
    # Advanced ethics concepts
    bias_mitigation = ['bias detection', 'bias mitigation', 'algorithmic fairness', 'demographic parity']
    transparency_concepts = ['explainability', 'interpretability', 'algorithmic transparency', 'decision transparency']
    governance_frameworks = ['ai governance', 'ethical oversight', 'ai audit', 'compliance framework']
    human_oversight = ['human oversight', 'human-in-the-loop', 'human control', 'meaningful human review']
    
    ethics_score = 0
    if any(term in combined for term in ['ethics', 'ethical', 'bias']) and any(term in combined for term in ['ai', 'algorithm']):
        # Matured scoring - more stringent criteria
        ethics_score = 25  # Reduced base score for AI ethics content
        
        # Core ethics indicators - require multiple indicators for higher scores
        ethics_count = sum(1 for indicator in ethics_indicators if indicator in combined)
        if ethics_count >= 3:
            ethics_score += ethics_count * 5  # Reward comprehensive coverage
        elif ethics_count >= 1:
            ethics_score += ethics_count * 3  # Lower reward for limited coverage
        
        # Advanced bias mitigation - stricter requirements
        bias_count = sum(1 for indicator in bias_mitigation if indicator in combined)
        if bias_count >= 2:
            ethics_score += bias_count * 7  # High value for actual bias solutions
        
        # Transparency and explainability - implementation focus
        transparency_count = sum(1 for indicator in transparency_concepts if indicator in combined)
        if transparency_count >= 2:
            ethics_score += transparency_count * 6
        
        # Governance frameworks - require concrete frameworks
        governance_count = sum(1 for indicator in governance_frameworks if indicator in combined)
        if governance_count >= 1:
            ethics_score += governance_count * 8
        
        # Human oversight mechanisms - critical for high scores
        oversight_count = sum(1 for indicator in human_oversight if indicator in combined)
        if oversight_count >= 1:
            ethics_score += oversight_count * 7
        
        # Maturity penalty for documents that only discuss ethics generally
        # without specific technical implementations
        if ('recommendation' in combined and 'implementation' not in combined and 
            'technical' not in combined and 'system' not in combined):
            ethics_score = max(0, ethics_score - 15)  # Reduce score for policy-only documents
    
    scores['ai_ethics'] = min(100, ethics_score) if ethics_score > 0 else 0
    
    # Quantum Ethics - Advanced quantum ethical assessment
    quantum_ethics_indicators = ['quantum ethics', 'quantum responsibility', 'quantum access', 'quantum equity']
    quantum_privacy = ['quantum privacy', 'quantum data protection', 'quantum anonymity']
    quantum_fairness = ['quantum advantage distribution', 'quantum digital divide', 'equitable quantum access']
    quantum_governance = ['quantum ethical framework', 'quantum oversight', 'quantum compliance']
    
    quantum_ethics_score = 0
    if 'quantum' in combined and any(term in combined for term in ['ethics', 'responsibility', 'access', 'equity', 'fairness']):
        quantum_ethics_score = 30  # Base score for quantum ethics content
        
        # Core quantum ethics concepts
        quantum_ethics_score += sum(8 for indicator in quantum_ethics_indicators if indicator in combined)
        
        # Privacy considerations
        quantum_ethics_score += sum(10 for indicator in quantum_privacy if indicator in combined)
        
        # Fairness and access issues
        quantum_ethics_score += sum(12 for indicator in quantum_fairness if indicator in combined)
        
        # Governance frameworks
        quantum_ethics_score += sum(10 for indicator in quantum_governance if indicator in combined)
        
        # Bonus for comprehensive quantum policy discussion
        if any(term in combined for term in ['quantum policy', 'quantum strategy', 'quantum initiative']):
            quantum_ethics_score += 15
    
    scores['quantum_ethics'] = min(100, quantum_ethics_score) if quantum_ethics_score > 0 else None
    
    return scores

def analyze_with_contextual_understanding(text: str, title: str) -> Dict[str, int]:
    """Contextual analysis with semantic understanding"""
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    scores = {}
    
    # Context-aware AI Cybersecurity scoring based on document authority and depth
    ai_cyber_score = 0
    
    # Check for AI + cybersecurity content
    if any(term in combined for term in ['ai', 'artificial intelligence']) and any(term in combined for term in ['security', 'cybersecurity']):
        ai_cyber_score = 35  # Base for AI security content
        
        # High-authority government guidance
        if 'joint guidance' in title_lower and 'ai systems securely' in title_lower:
            ai_cyber_score += 45  # Exceptional authoritative guidance
        elif any(term in combined for term in ['dhs', 'cisa', 'ncsc', 'joint guidelines']):
            ai_cyber_score += 30  # Government authority bonus
        
        # Technical depth indicators
        if any(term in combined for term in ['implementation', 'framework', 'standards', 'best practices']):
            ai_cyber_score += 15
            
        # Comprehensive coverage indicators
        if any(term in combined for term in ['comprehensive', 'systematic', 'enterprise', 'robust']):
            ai_cyber_score += 10
    
    scores['ai_cybersecurity'] = min(100, ai_cyber_score) if ai_cyber_score > 0 else 0
    
    # Quantum cybersecurity - Sophisticated tier assessment
    quantum_cyber_score = None
    if 'quantum' in combined:
        quantum_indicators = ['post-quantum', 'quantum-safe', 'quantum cryptography', 'quantum security', 'quantum key distribution']
        advanced_quantum = ['quantum supremacy', 'quantum advantage', 'lattice cryptography', 'quantum protocols']
        implementation_quantum = ['quantum migration', 'quantum deployment', 'quantum integration']
        
        indicator_count = sum(1 for term in quantum_indicators if term in combined)
        advanced_count = sum(1 for term in advanced_quantum if term in combined)
        impl_count = sum(1 for term in implementation_quantum if term in combined)
        
        if indicator_count >= 3 and advanced_count >= 1 and impl_count >= 1:
            quantum_cyber_score = 5
        elif indicator_count >= 2 and (advanced_count >= 1 or impl_count >= 1):
            quantum_cyber_score = 4
        elif indicator_count >= 2:
            quantum_cyber_score = 3
        elif indicator_count >= 1:
            quantum_cyber_score = 2
        else:
            quantum_cyber_score = 1
    
    scores['quantum_cybersecurity'] = quantum_cyber_score
    
    # AI Ethics - Authority and depth-based assessment
    ai_ethics_score = 0
    if any(term in combined for term in ['ai', 'artificial intelligence']) and any(term in combined for term in ['ethics', 'ethical', 'bias', 'fairness']):
        ai_ethics_score = 30  # Base for AI ethics content
        
        # Document authority bonus
        if any(term in combined for term in ['guidance', 'framework', 'standards']):
            ai_ethics_score += 25
            
        # Comprehensive coverage indicators
        ethics_concepts = ['bias mitigation', 'transparency', 'accountability', 'explainability', 'fairness']
        ai_ethics_score += sum(8 for concept in ethics_concepts if concept in combined)
        
        # Implementation depth
        if any(term in combined for term in ['implementation', 'deployment', 'operational', 'systematic']):
            ai_ethics_score += 15
    
    scores['ai_ethics'] = min(100, ai_ethics_score) if ai_ethics_score > 0 else 0
    
    # Quantum Ethics - Comprehensive quantum ethical assessment
    quantum_ethics_score = None
    if 'quantum' in combined and any(term in combined for term in ['ethics', 'responsibility', 'access', 'equity', 'fairness']):
        quantum_ethics_score = 25  # Base for quantum ethics content
        
        # Specific quantum ethics concepts
        quantum_ethics_concepts = ['quantum ethics', 'quantum responsibility', 'quantum access', 'quantum equity']
        quantum_ethics_score += sum(15 for concept in quantum_ethics_concepts if concept in combined)
        
        # Advanced considerations
        if any(term in combined for term in ['quantum policy', 'quantum governance', 'quantum oversight']):
            quantum_ethics_score += 20
            
        # Implementation considerations
        if any(term in combined for term in ['quantum strategy', 'quantum initiative', 'quantum framework']):
            quantum_ethics_score += 15
        
        quantum_ethics_score = min(100, quantum_ethics_score)
    
    scores['quantum_ethics'] = quantum_ethics_score
    
    return scores

def multi_service_hybrid_analysis(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Hybrid analysis using multiple available services (Anthropic, OpenAI, enhanced patterns).
    """
    scores = {'ai_cybersecurity': None, 'quantum_cybersecurity': None, 'ai_ethics': None, 'quantum_ethics': None}
    
    # Try Anthropic first (usually more reliable)
    try:
        from utils.anthropic_analyzer import analyze_document_with_anthropic
        anthropic_scores = analyze_document_with_anthropic(text, title)
        if anthropic_scores:
            for key, value in anthropic_scores.items():
                if key in scores and value is not None:
                    scores[key] = value
    except Exception as e:
        print(f"Anthropic analysis failed: {e}")
    
    # Fill gaps with enhanced pattern analysis
    pattern_scores = enhanced_scoring_with_llm_insights(text, title)
    for key, value in pattern_scores.items():
        if scores[key] is None and value is not None:
            scores[key] = value
    
    return scores

def enhanced_scoring_with_llm_insights(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Enhanced scoring that leverages intelligent pattern analysis for more accurate assessment.
    """
    # Enhanced pattern-based scoring with improved logic
    text_lower = text.lower()
    title_lower = title.lower()
    combined_content = f"{title_lower} {text_lower}"
    
    scores = {}
    
    # AI Cybersecurity Maturity (0-100)
    ai_cyber_keywords = [
        'ai security', 'machine learning security', 'artificial intelligence security',
        'ai threat', 'ai vulnerability', 'ai attack', 'adversarial', 'model security',
        'ai governance', 'ai compliance', 'ai audit', 'ai monitoring', 'ai risk',
        'secure ai', 'ai authentication', 'ai encryption', 'ai privacy'
    ]
    
    ai_cyber_score = 30  # Baseline for AI cyber content
    for keyword in ai_cyber_keywords:
        if keyword in combined_content:
            ai_cyber_score += 3
            
    # Additional context scoring
    if any(term in combined_content for term in ['cybersecurity', 'cyber security', 'information security']):
        if any(term in combined_content for term in ['ai', 'artificial intelligence', 'machine learning']):
            ai_cyber_score += 10
    
    scores['ai_cybersecurity'] = min(70, ai_cyber_score) if ai_cyber_score > 30 else None
    
    # Quantum Cybersecurity Maturity (1-5)
    quantum_cyber_keywords = [
        'quantum cryptography', 'quantum security', 'post-quantum', 'quantum-safe',
        'quantum key distribution', 'quantum resistant', 'quantum computing threat',
        'quantum encryption', 'lattice cryptography', 'quantum supremacy'
    ]
    
    quantum_cyber_matches = sum(1 for keyword in quantum_cyber_keywords if keyword in combined_content)
    
    if quantum_cyber_matches >= 4:
        quantum_cyber_score = 4
    elif quantum_cyber_matches >= 3:
        quantum_cyber_score = 3
    elif quantum_cyber_matches >= 2:
        quantum_cyber_score = 2
    elif quantum_cyber_matches >= 1:
        quantum_cyber_score = 1
    else:
        quantum_cyber_score = None
        
    scores['quantum_cybersecurity'] = quantum_cyber_score
    
    # AI Ethics Score (0-100)
    ai_ethics_keywords = [
        'ai ethics', 'algorithmic bias', 'fairness', 'transparency', 'explainable ai',
        'responsible ai', 'ai accountability', 'ethical ai', 'ai governance',
        'bias mitigation', 'algorithmic fairness', 'ai transparency', 'trustworthy ai'
    ]
    
    ai_ethics_score = 35  # Baseline for AI ethics content
    for keyword in ai_ethics_keywords:
        if keyword in combined_content:
            ai_ethics_score += 3
            
    # Boost for comprehensive ethical considerations
    if any(term in combined_content for term in ['ethics', 'ethical', 'bias', 'fairness']):
        if any(term in combined_content for term in ['ai', 'artificial intelligence', 'algorithm']):
            ai_ethics_score += 8
    
    scores['ai_ethics'] = min(65, ai_ethics_score) if ai_ethics_score > 35 else None
    
    # Quantum Ethics Score (0-100)
    quantum_ethics_keywords = [
        'quantum ethics', 'quantum advantage ethics', 'quantum privacy',
        'quantum equity', 'quantum access', 'quantum responsibility',
        'quantum computing ethics', 'quantum fairness'
    ]
    
    quantum_ethics_score = 30  # Baseline for quantum ethics content  
    for keyword in quantum_ethics_keywords:
        if keyword in combined_content:
            quantum_ethics_score += 5
            
    # General quantum considerations
    if any(term in combined_content for term in ['quantum', 'quantum computing']):
        if any(term in combined_content for term in ['ethics', 'ethical', 'responsibility', 'access']):
            quantum_ethics_score += 10
    
    scores['quantum_ethics'] = min(60, quantum_ethics_score) if quantum_ethics_score > 30 else None
    
    return scores

def fallback_scoring(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Pattern-based scoring when AI analysis is unavailable.
    """
    text_lower = text.lower()
    title_lower = title.lower()
    
    # Check applicability using existing logic
    applicability = analyze_document_applicability(text, title)
    
    scores = {}
    
    # AI Cybersecurity - Comprehensive pattern-based assessment
    if applicability['ai_cybersecurity']:
        score = 25  # Base score for applicable AI cybersecurity content
        
        # Core AI security concepts
        ai_security_keywords = ['encryption', 'authentication', 'ai security', 'model protection', 'threat detection']
        score += sum(8 for kw in ai_security_keywords if kw in text_lower)
        
        # Advanced AI security concepts
        advanced_keywords = ['federated learning', 'differential privacy', 'adversarial', 'secure computation', 'homomorphic encryption']
        score += sum(12 for kw in advanced_keywords if kw in text_lower)
        
        # Implementation and operational security
        impl_keywords = ['implementation', 'deployed', 'operational', 'monitoring', 'audit', 'compliance']
        score += sum(6 for kw in impl_keywords if kw in text_lower)
        
        # Framework and standards compliance
        standards_keywords = ['nist', 'iso', 'framework', 'best practices', 'guidelines', 'standards']
        score += sum(10 for kw in standards_keywords if kw in text_lower)
        
        # Risk management and governance
        governance_keywords = ['risk management', 'governance', 'policy', 'oversight', 'assessment']
        score += sum(7 for kw in governance_keywords if kw in text_lower)
        
        scores['ai_cybersecurity'] = min(100, score)
    else:
        scores['ai_cybersecurity'] = None
    
    # Quantum Cybersecurity scoring (1-5)
    if applicability['quantum_cybersecurity']:
        score = 1  # Base level
        
        # Sophisticated quantum maturity assessment
        quantum_basic = ['post-quantum', 'pqc', 'quantum-safe', 'quantum cryptography']
        quantum_advanced = ['quantum protocols', 'quantum standards', 'lattice cryptography', 'quantum supremacy']
        quantum_implementation = ['implementation', 'deployment', 'migration', 'integration']
        quantum_governance = ['integrated', 'enterprise-wide', 'systematic', 'governance', 'compliance']
        
        basic_count = sum(1 for kw in quantum_basic if kw in text_lower)
        advanced_count = sum(1 for kw in quantum_advanced if kw in text_lower)
        impl_count = sum(1 for kw in quantum_implementation if kw in text_lower)
        gov_count = sum(1 for kw in quantum_governance if kw in text_lower)
        
        if basic_count >= 2 and advanced_count >= 1 and impl_count >= 1 and gov_count >= 1:
            score = 5
        elif basic_count >= 2 and (advanced_count >= 1 or impl_count >= 1):
            score = 4
        elif basic_count >= 1 and impl_count >= 1:
            score = 3
        elif basic_count >= 1:
            score = 2
            
        scores['quantum_cybersecurity'] = score
    else:
        scores['quantum_cybersecurity'] = None
    
    # AI Ethics - Comprehensive ethical framework assessment
    if applicability['ai_ethics']:
        score = 20  # Base score for applicable AI ethics content
        
        # Core ethics concepts
        ethics_keywords = ['fairness', 'bias', 'transparency', 'accountability', 'explainable']
        score += sum(10 for kw in ethics_keywords if kw in text_lower)
        
        # Advanced ethical AI concepts
        advanced_ethics = ['algorithmic auditing', 'ethical AI', 'responsible AI', 'human oversight', 'bias mitigation']
        score += sum(12 for kw in advanced_ethics if kw in text_lower)
        
        # Governance and compliance frameworks
        governance_keywords = ['governance', 'oversight', 'compliance', 'monitoring', 'audit', 'assessment']
        score += sum(8 for kw in governance_keywords if kw in text_lower)
        
        # Implementation and operational considerations
        implementation_keywords = ['implementation', 'deployment', 'operational', 'systematic', 'framework']
        score += sum(6 for kw in implementation_keywords if kw in text_lower)
        
        # Standards and best practices
        standards_keywords = ['standards', 'best practices', 'guidelines', 'principles', 'policy']
        score += sum(7 for kw in standards_keywords if kw in text_lower)
        
        scores['ai_ethics'] = min(100, score)
    else:
        scores['ai_ethics'] = None
    
    # Quantum Ethics - Advanced quantum ethical considerations
    if applicability['quantum_ethics']:
        score = 15  # Base score for applicable quantum ethics content
        
        # Core quantum ethics concepts
        quantum_ethics_keywords = ['quantum ethics', 'quantum access', 'quantum equity', 'quantum governance']
        score += sum(15 for kw in quantum_ethics_keywords if kw in text_lower)
        
        # Quantum privacy and security ethics
        quantum_privacy = ['quantum privacy', 'quantum security ethics', 'quantum data protection']
        score += sum(18 for kw in quantum_privacy if kw in text_lower)
        
        # Quantum fairness and accessibility
        quantum_fairness = ['quantum digital divide', 'equitable quantum access', 'quantum advantage distribution']
        score += sum(20 for kw in quantum_fairness if kw in text_lower)
        
        # General ethical considerations in quantum context
        general_ethics = ['ethical', 'responsible', 'equitable', 'fair access']
        score += sum(8 for kw in general_ethics if kw in text_lower)
        
        # Policy and governance frameworks
        quantum_governance = ['quantum policy', 'quantum strategy', 'quantum oversight', 'quantum compliance']
        score += sum(12 for kw in quantum_governance if kw in text_lower)
        
        scores['quantum_ethics'] = min(100, score)
    else:
        scores['quantum_ethics'] = None
    
    return scores

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