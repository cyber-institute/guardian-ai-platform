"""
Document type classification utility for intelligent analysis verbiage.
"""

import re
from typing import Dict, Tuple

# Standard document types available in the system
DOCUMENT_TYPES = {
    'policy': ['policy', 'policies', 'directive', 'guidelines', 'guidance', 'recommendation', 'unesco recommendation', 'memorandum'],
    'standard': ['standard', 'standards', 'specification', 'spec', 'nist', 'iso', 'fips'],
    'strategy': ['strategy', 'strategic', 'roadmap', 'plan', 'planning'],
    'regulation': ['regulation', 'regulatory', 'compliance', 'law', 'legal', 'rule'],
    'product': ['product', 'software', 'application', 'solution', 'tool', 'platform'],
    'system': ['system', 'architecture', 'infrastructure', 'framework', 'implementation'],
    'procedure': ['procedure', 'process', 'workflow', 'methodology', 'approach'],
    'assessment': ['assessment', 'evaluation', 'analysis', 'report', 'study'],
    'whitepaper': ['whitepaper', 'white paper', 'research', 'paper', 'publication'],
    'manual': ['manual', 'guide', 'handbook', 'documentation', 'instructions']
}

def detect_document_type(title: str, content: str = "") -> str:
    """
    Intelligently detect document type based on title and content analysis.
    
    Args:
        title: Document title
        content: Document content (optional)
        
    Returns:
        Detected document type from DOCUMENT_TYPES keys
    """
    text_to_analyze = f"{title} {content[:500]}".lower()
    
    # Score each document type based on keyword matches
    type_scores = {}
    
    for doc_type, keywords in DOCUMENT_TYPES.items():
        score = 0
        for keyword in keywords:
            # Title matches get higher weight
            title_matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', title.lower()))
            content_matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_to_analyze))
            
            score += title_matches * 3 + content_matches
        
        type_scores[doc_type] = score
    
    # Return the type with highest score, default to 'policy' if no clear match
    best_type = max(type_scores.items(), key=lambda x: x[1])
    return best_type[0] if best_type[1] > 0 else 'policy'

def get_document_descriptor(doc_type: str) -> Tuple[str, str]:
    """
    Get appropriate descriptor and verb for document type.
    
    Args:
        doc_type: Document type
        
    Returns:
        Tuple of (descriptor, verb) for natural language generation
    """
    descriptors = {
        'policy': ('This policy', 'establishes'),
        'standard': ('This standard', 'defines'),
        'strategy': ('This strategy', 'outlines'),
        'regulation': ('This regulation', 'mandates'),
        'product': ('This product', 'provides'),
        'system': ('This system', 'implements'),
        'procedure': ('This procedure', 'describes'),
        'assessment': ('This assessment', 'evaluates'),
        'whitepaper': ('This research', 'presents'),
        'manual': ('This manual', 'guides')
    }
    
    return descriptors.get(doc_type, ('This document', 'demonstrates'))

def get_contextual_analysis_text(score: int, category: str, doc_type: str, title: str = "") -> str:
    """
    Generate contextual analysis text based on document type and score.
    
    Args:
        score: Maturity score (1-5 or 0-100)
        category: Analysis category
        doc_type: Document type
        title: Document title for additional context
        
    Returns:
        Contextual analysis text
    """
    # Convert score to 1-5 scale if needed
    if score > 5:
        maturity_level = min(5, max(1, round(score / 20)))
    else:
        maturity_level = min(5, max(1, round(score)))
    
    descriptor, verb = get_document_descriptor(doc_type)
    
    # Customize analysis based on maturity level and document type
    if maturity_level == 5:
        return f"""
        **Expert-level {category} maturity!** {descriptor} demonstrates advanced understanding 
        and comprehensive implementation of quantum-safe practices. The content {verb} a 
        well-structured approach that is fully prepared for the quantum era.
        """
    elif maturity_level == 4:
        return f"""
        **Advanced {category} foundation.** {descriptor} shows strong awareness and solid 
        implementation strategies for quantum-safe practices. The framework {verb} 
        robust controls with room for minor enhancements.
        """
    elif maturity_level == 3:
        return f"""
        **Developing {category} awareness.** {descriptor} has established good foundational 
        understanding but requires continued improvement in quantum readiness implementation. 
        The content {verb} promising direction with gaps to address.
        """
    elif maturity_level == 2:
        return f"""
        **Basic {category} preparation.** {descriptor} shows fundamental quantum awareness 
        and {verb} initial considerations. Focus should be on expanding technical depth 
        and building comprehensive implementation strategies.
        """
    else:
        return f"""
        **Initial {category} readiness.** {descriptor} represents early-stage quantum 
        preparedness and {verb} basic recognition of quantum computing implications. 
        Significant development needed across all maturity dimensions.
        """