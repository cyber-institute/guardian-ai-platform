"""
Multi-LLM Ensemble Scoring Engine for GUARDIAN
Implements patent-based scoring with keyword identification + contextual AI analysis
"""

import os
from typing import Dict, Optional, List, Tuple
import re

def analyze_document_with_openai(text: str, title: str) -> Dict[str, Optional[int]]:
    """Use OpenAI for content and context-aware scoring analysis"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        prompt = f"""
You are an expert AI/cybersecurity analyst. Analyze this document for AI and quantum maturity scores.

Document Title: {title}
Document Content: {text[:4000]}...

Score each category 0-100 based on content depth and implementation maturity:

1. AI Cybersecurity (0-100): How well does this document address AI system security, threats, vulnerabilities, secure deployment, authentication, monitoring, and governance?

2. AI Ethics (0-100): How well does this document address responsible AI, fairness, bias mitigation, transparency, accountability, governance, and ethical principles?

3. Quantum Cybersecurity (0-100): How well does this document address quantum computing security, post-quantum cryptography, quantum-safe encryption, and quantum threat mitigation?

4. Quantum Ethics (0-100): How well does this document address quantum technology ethics, access, inclusion, governance, and societal impact?

Return ONLY valid scores (positive integers 0-100) or null if not applicable. Format as JSON:
{{"ai_cybersecurity": score_or_null, "ai_ethics": score_or_null, "quantum_cybersecurity": score_or_null, "quantum_ethics": score_or_null}}
"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        import json
        content = response.choices[0].message.content
        if content:
            result = json.loads(content)
            
            # Validate and normalize scores
            validated_scores = {}
            for key in ['ai_cybersecurity', 'ai_ethics', 'quantum_cybersecurity', 'quantum_ethics']:
                score = result.get(key)
                if score is not None and isinstance(score, (int, float)) and 0 <= score <= 100:
                    validated_scores[key] = int(score)
                else:
                    validated_scores[key] = None
                    
            return validated_scores
        
    except Exception as e:
        print(f"OpenAI analysis failed: {e}")
        return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}

def analyze_document_with_anthropic(text: str, title: str) -> Dict[str, Optional[int]]:
    """Use Anthropic Claude for content and context-aware scoring analysis"""
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        prompt = f"""
Analyze this document as an AI/cybersecurity expert for maturity scoring.

Title: {title}
Content: {text[:4000]}...

Provide maturity scores (0-100) for each applicable category based on content depth, implementation detail, and practical guidance:

AI Cybersecurity: Security frameworks, threat models, vulnerability assessment, secure deployment, authentication, monitoring, governance for AI systems.

AI Ethics: Responsible AI development, fairness, bias mitigation, transparency, explainability, accountability, governance, ethical principles.

Quantum Cybersecurity: Quantum computing security, post-quantum cryptography, quantum-safe protocols, quantum threat mitigation, cryptographic agility.

Quantum Ethics: Quantum technology ethics, equitable access, inclusion, societal impact, quantum governance principles.

Respond with JSON format only:
{{"ai_cybersecurity": score_or_null, "ai_ethics": score_or_null, "quantum_cybersecurity": score_or_null, "quantum_ethics": score_or_null}}

Use null for categories not substantially covered. Scores 0-100 based on coverage depth and implementation maturity.
"""

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        # Extract JSON from response
        if hasattr(response.content[0], 'text'):
            content = response.content[0].text
        else:
            content = str(response.content[0])
        
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            
            # Validate and normalize scores
            validated_scores = {}
            for key in ['ai_cybersecurity', 'ai_ethics', 'quantum_cybersecurity', 'quantum_ethics']:
                score = result.get(key)
                if score is not None and isinstance(score, (int, float)) and 0 <= score <= 100:
                    validated_scores[key] = int(score)
                else:
                    validated_scores[key] = None
                    
            return validated_scores
        
    except Exception as e:
        print(f"Anthropic analysis failed: {e}")
        
    return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}

def keyword_based_scoring(text: str, title: str) -> Dict[str, int]:
    """Patent-based keyword scoring with enhanced detection"""
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    scores = {'ai_cybersecurity': 0, 'ai_ethics': 0, 'quantum_cybersecurity': 0, 'quantum_ethics': 0}
    
    # AI Cybersecurity Keywords with weighted scoring
    ai_cyber_keywords = {
        'high_value': ['ai security framework', 'ai threat model', 'secure ai deployment', 'ai governance'],
        'medium_value': ['ai security', 'artificial intelligence security', 'machine learning security', 'ai threat', 'ai vulnerability'],
        'base_value': ['cybersecurity', 'security', 'threat', 'vulnerability', 'attack', 'defense', 'protection']
    }
    
    # AI Ethics Keywords  
    ai_ethics_keywords = {
        'high_value': ['responsible ai', 'ai ethics framework', 'algorithmic fairness', 'ai governance'],
        'medium_value': ['ai ethics', 'bias mitigation', 'ai transparency', 'explainable ai', 'ai accountability'],
        'base_value': ['ethics', 'ethical', 'fairness', 'bias', 'transparency', 'accountability', 'responsible']
    }
    
    # Quantum Cybersecurity Keywords
    quantum_cyber_keywords = {
        'high_value': ['post-quantum cryptography', 'quantum-safe encryption', 'quantum threat model'],
        'medium_value': ['quantum security', 'quantum cryptography', 'quantum computing security', 'quantum threat'],
        'base_value': ['quantum', 'cryptographic', 'encryption', 'cryptography']
    }
    
    # Quantum Ethics Keywords
    quantum_ethics_keywords = {
        'high_value': ['quantum ethics', 'quantum governance', 'quantum inclusion'],
        'medium_value': ['quantum access', 'quantum equity', 'quantum sustainability'],
        'base_value': ['inclusion', 'sustainability', 'access', 'equity']
    }
    
    # Score AI Cybersecurity
    if any(term in combined for term in ['ai', 'artificial intelligence', 'machine learning']):
        for keyword in ai_cyber_keywords['high_value']:
            if keyword in combined:
                scores['ai_cybersecurity'] += 20
        for keyword in ai_cyber_keywords['medium_value']:
            if keyword in combined:
                scores['ai_cybersecurity'] += 10
        for keyword in ai_cyber_keywords['base_value']:
            if keyword in combined:
                scores['ai_cybersecurity'] += 3
                
    # Score AI Ethics
    if any(term in combined for term in ['ai', 'artificial intelligence', 'machine learning']):
        for keyword in ai_ethics_keywords['high_value']:
            if keyword in combined:
                scores['ai_ethics'] += 20
        for keyword in ai_ethics_keywords['medium_value']:
            if keyword in combined:
                scores['ai_ethics'] += 10
        for keyword in ai_ethics_keywords['base_value']:
            if keyword in combined:
                scores['ai_ethics'] += 3
                
    # Score Quantum Cybersecurity
    if 'quantum' in combined:
        for keyword in quantum_cyber_keywords['high_value']:
            if keyword in combined:
                scores['quantum_cybersecurity'] += 25
        for keyword in quantum_cyber_keywords['medium_value']:
            if keyword in combined:
                scores['quantum_cybersecurity'] += 15
        for keyword in quantum_cyber_keywords['base_value']:
            if keyword in combined:
                scores['quantum_cybersecurity'] += 5
                
    # Score Quantum Ethics
    if 'quantum' in combined:
        for keyword in quantum_ethics_keywords['high_value']:
            if keyword in combined:
                scores['quantum_ethics'] += 25
        for keyword in quantum_ethics_keywords['medium_value']:
            if keyword in combined:
                scores['quantum_ethics'] += 15
        for keyword in quantum_ethics_keywords['base_value']:
            if keyword in combined:
                scores['quantum_ethics'] += 5
    
    # Cap scores at 100
    for key in scores:
        scores[key] = min(100, scores[key])
    
    return scores

def multi_llm_ensemble_scoring(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Patent-based multi-LLM ensemble scoring engine
    Combines keyword identification with contextual AI analysis
    """
    
    # Step 1: Check document scope and applicability
    applicability = enhanced_document_applicability(text, title)
    
    # If document is out of scope, return None for all scores
    if applicability.get('scope_message'):
        return {
            'ai_cybersecurity': None,
            'ai_ethics': None, 
            'quantum_cybersecurity': None,
            'quantum_ethics': None,
            'scope_message': applicability['scope_message']
        }
    
    # Step 2: Keyword-based initial scoring
    keyword_scores = keyword_based_scoring(text, title)
    
    # Step 3: Multi-LLM contextual analysis
    openai_scores = analyze_document_with_openai(text, title)
    anthropic_scores = analyze_document_with_anthropic(text, title)
    
    # Step 4: Ensemble combination following patent formulas
    final_scores = {}
    
    for framework in ['ai_cybersecurity', 'ai_ethics', 'quantum_cybersecurity', 'quantum_ethics']:
        # Check if framework applies to this document
        if not applicability.get(framework, False):
            final_scores[framework] = None
            continue
            
        keyword_score = keyword_scores[framework]
        openai_score = openai_scores[framework]
        anthropic_score = anthropic_scores[framework]
        
        # Only proceed if there's some indication of relevance
        if keyword_score > 0 or openai_score is not None or anthropic_score is not None:
            
            # Collect valid scores for ensemble
            valid_scores = []
            
            if keyword_score > 0:
                valid_scores.append(keyword_score)
            if openai_score is not None and openai_score > 0:
                valid_scores.append(openai_score)
            if anthropic_score is not None and anthropic_score > 0:
                valid_scores.append(anthropic_score)
            
            if valid_scores:
                # Patent formula: weighted ensemble with contextual boost
                if len(valid_scores) >= 2:
                    # Multiple sources - use weighted average with consensus boost
                    ensemble_score = sum(valid_scores) / len(valid_scores)
                    # Consensus boost for multiple agreeing sources
                    consensus_boost = min(10, len(valid_scores) * 3)
                    final_score = min(100, int(ensemble_score + consensus_boost))
                else:
                    # Single source - use with confidence penalty
                    final_score = max(1, int(valid_scores[0] * 0.8))
                
                final_scores[framework] = final_score
            else:
                final_scores[framework] = None
        else:
            final_scores[framework] = None
    
    return final_scores

def detect_document_scope(text: str, title: str) -> Dict[str, any]:
    """
    Detect if document is out of scope (children's books, religious texts, etc.)
    Returns scope analysis with recommendations for handling
    """
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # Out-of-scope indicators
    childrens_indicators = [
        'once upon a time', 'fairy tale', 'children\'s book', 'bedtime story',
        'picture book', 'nursery rhyme', 'little red riding hood', 'goldilocks',
        'three little pigs', 'sleeping beauty', 'cinderella'
    ]
    
    religious_indicators = [
        'bible', 'quran', 'torah', 'gospel', 'scripture', 'holy book',
        'religious text', 'prayer', 'psalm', 'verse', 'biblical',
        'jesus', 'allah', 'god almighty', 'prophet', 'blessing'
    ]
    
    legal_foundational_indicators = [
        'constitution', 'bill of rights', 'amendment', 'we the people',
        'declaration of independence', 'magna carta', 'founding fathers',
        'constitutional convention', 'federalist papers'
    ]
    
    literature_indicators = [
        'novel', 'poetry', 'poem', 'fiction', 'literature', 'chapter one',
        'shakespeare', 'dickens', 'twain', 'austen', 'hemingway'
    ]
    
    # Check for out-of-scope content
    is_childrens = any(indicator in combined for indicator in childrens_indicators)
    is_religious = any(indicator in combined for indicator in religious_indicators)
    is_foundational_legal = any(indicator in combined for indicator in legal_foundational_indicators)
    is_literature = any(indicator in combined for indicator in literature_indicators)
    
    # Check if document is likely out of scope
    out_of_scope = is_childrens or is_religious or is_foundational_legal or is_literature
    
    # Determine document type for messaging
    document_type = "unknown"
    if is_childrens:
        document_type = "children's literature"
    elif is_religious:
        document_type = "religious text"
    elif is_foundational_legal:
        document_type = "foundational legal document"
    elif is_literature:
        document_type = "literary work"
    
    return {
        'out_of_scope': out_of_scope,
        'document_type': document_type,
        'reason': f"This appears to be {document_type} rather than a cybersecurity, AI, or quantum technology policy document."
    }

def enhanced_document_applicability(text: str, title: str) -> Dict[str, bool]:
    """Enhanced applicability check using multi-LLM insights"""
    
    # First check if document is out of scope
    scope_analysis = detect_document_scope(text, title)
    if scope_analysis['out_of_scope']:
        return {
            'ai_cybersecurity': False,
            'quantum_cybersecurity': False,
            'ai_ethics': False,
            'quantum_ethics': False,
            'scope_message': scope_analysis['reason']
        }
    
    text_lower = text.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # More inclusive applicability based on any substantial mention
    ai_present = any(term in combined for term in [
        'ai', 'artificial intelligence', 'machine learning', 'neural network',
        'deep learning', 'automated', 'intelligent system'
    ])
    
    quantum_present = any(term in combined for term in [
        'quantum', 'post-quantum', 'quantum computing', 'quantum cryptography',
        'quantum-safe', 'quantum threat', 'pqc'
    ])
    
    cyber_context = any(term in combined for term in [
        'security', 'cybersecurity', 'threat', 'risk', 'vulnerability',
        'attack', 'defense', 'protection', 'secure', 'safety'
    ])
    
    ethics_context = any(term in combined for term in [
        'ethics', 'ethical', 'responsible', 'governance', 'accountability',
        'transparency', 'fairness', 'bias', 'inclusion', 'equity', 'policy'
    ])
    
    return {
        'ai_cybersecurity': ai_present and cyber_context,
        'quantum_cybersecurity': quantum_present and cyber_context,
        'ai_ethics': ai_present and ethics_context,
        'quantum_ethics': quantum_present and ethics_context
    }