"""
Enhanced Content Preview System for GUARDIAN
Generates meaningful, readable content previews without formatting artifacts
"""

import re
from typing import Optional

def clean_and_enhance_preview(content: str, max_length: int = 400) -> str:
    """Clean content and create meaningful preview without asterisks or formatting"""
    if not content:
        return "No content available for preview"
    
    # Remove HTML tags and artifacts
    clean_text = re.sub(r'<[^>]+>', '', content)
    clean_text = re.sub(r'&[a-zA-Z]+;', ' ', clean_text)
    
    # Remove asterisks and markdown formatting
    clean_text = re.sub(r'\*+', '', clean_text)
    clean_text = re.sub(r'#+\s*', '', clean_text)
    clean_text = re.sub(r'[-_]{3,}', '', clean_text)
    
    # Remove multiple whitespace and normalize
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = clean_text.strip()
    
    # Extract meaningful sentences
    sentences = re.split(r'[.!?]+', clean_text)
    meaningful_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        # Skip very short or meaningless fragments
        if len(sentence) > 20 and not sentence.lower().startswith(('table', 'figure', 'page')):
            meaningful_sentences.append(sentence)
        
        # Build preview until we reach max length
        current_preview = '. '.join(meaningful_sentences) + '.'
        if len(current_preview) >= max_length:
            break
    
    if meaningful_sentences:
        preview = '. '.join(meaningful_sentences) + '.'
        if len(preview) > max_length:
            preview = preview[:max_length].rsplit(' ', 1)[0] + '...'
        return preview
    else:
        # Fallback to first clean text if no good sentences found
        if len(clean_text) > max_length:
            return clean_text[:max_length].rsplit(' ', 1)[0] + '...'
        return clean_text

def extract_key_topics(content: str, num_topics: int = 3) -> list:
    """Extract key topics from content for enhanced preview context"""
    if not content:
        return []
    
    # Common topic indicators
    ai_terms = ['artificial intelligence', 'machine learning', 'neural network', 'AI system', 'algorithm']
    cyber_terms = ['cybersecurity', 'security framework', 'risk management', 'threat', 'vulnerability']
    quantum_terms = ['quantum computing', 'quantum cryptography', 'post-quantum', 'qubit']
    policy_terms = ['policy', 'regulation', 'compliance', 'governance', 'standard']
    
    content_lower = content.lower()
    topics = []
    
    if any(term in content_lower for term in ai_terms):
        topics.append('AI Technology')
    if any(term in content_lower for term in cyber_terms):
        topics.append('Cybersecurity')
    if any(term in content_lower for term in quantum_terms):
        topics.append('Quantum Technology')
    if any(term in content_lower for term in policy_terms):
        topics.append('Policy Framework')
    
    return topics[:num_topics]

def generate_enhanced_preview(doc: dict) -> str:
    """Generate enhanced preview with topic context"""
    content = doc.get('content_preview', '') or ''
    
    # Clean and enhance the preview
    enhanced_preview = clean_and_enhance_preview(content, max_length=350)
    
    # Add topic context if available
    topics = extract_key_topics(content)
    if topics and enhanced_preview != "No content available for preview":
        topic_context = f"Topics: {', '.join(topics)}. "
        # Adjust preview length to accommodate topic context
        adjusted_preview = clean_and_enhance_preview(content, max_length=300)
        return topic_context + adjusted_preview
    
    return enhanced_preview