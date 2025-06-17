"""
Enhanced Content Preview System for GUARDIAN
Generates meaningful, readable content previews without formatting artifacts
"""

import re
from typing import Optional

def clean_and_enhance_preview(content: str, max_length: int = 800) -> str:
    """Clean content and create comprehensive intelligent preview"""
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
    
    # Extract meaningful sentences with intelligent selection
    sentences = re.split(r'[.!?]+', clean_text)
    meaningful_sentences = []
    
    # Priority keywords for intelligent sentence selection
    priority_keywords = [
        'artificial intelligence', 'machine learning', 'cybersecurity', 'quantum',
        'policy', 'framework', 'security', 'governance', 'ethics', 'risk',
        'threat', 'vulnerability', 'compliance', 'standard', 'regulation',
        'implementation', 'assessment', 'management', 'protection', 'privacy'
    ]
    
    # Score sentences by relevance and quality
    scored_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 25 and not sentence.lower().startswith(('table', 'figure', 'page', 'section')):
            score = 0
            sentence_lower = sentence.lower()
            
            # Score based on priority keywords
            for keyword in priority_keywords:
                if keyword in sentence_lower:
                    score += 2
            
            # Prefer sentences with specific information
            if any(word in sentence_lower for word in ['framework', 'approach', 'system', 'process']):
                score += 1
            
            # Prefer longer, more informative sentences
            if len(sentence) > 50:
                score += 1
            if len(sentence) > 100:
                score += 1
            
            scored_sentences.append((score, sentence))
    
    # Sort by score and select best sentences
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    
    current_length = 0
    for score, sentence in scored_sentences:
        if current_length + len(sentence) + 2 <= max_length:  # +2 for '. '
            meaningful_sentences.append(sentence)
            current_length += len(sentence) + 2
        else:
            # Try to fit partial sentence if space allows
            remaining_space = max_length - current_length - 3  # -3 for '...'
            if remaining_space > 50:  # Only if meaningful space remains
                partial = sentence[:remaining_space].rsplit(' ', 1)[0]
                meaningful_sentences.append(partial + '...')
            break
    
    if meaningful_sentences:
        preview = '. '.join(meaningful_sentences)
        if not preview.endswith(('.', '...', '!', '?')):
            preview += '.'
        return preview
    else:
        # Enhanced fallback for edge cases
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
    """Generate comprehensive intelligent preview with strategic analysis"""
    content = doc.get('content', '') or doc.get('content_preview', '') or ''
    title = doc.get('title', '')
    
    if not content:
        return "No content available for preview"
    
    # Generate comprehensive preview with strategic insights
    enhanced_preview = create_strategic_preview(content, title, max_length=1200)
    
    # Add contextual framework analysis
    frameworks = analyze_framework_coverage(content)
    if frameworks:
        framework_context = f"Framework Coverage: {', '.join(frameworks)}. "
        return framework_context + enhanced_preview
    
    return enhanced_preview

def create_strategic_preview(content: str, title: str = "", max_length: int = 1200) -> str:
    """Create strategic preview focusing on policy implications and recommendations"""
    if not content:
        return "No content available for preview"
    
    # Clean content
    clean_text = re.sub(r'<[^>]+>', '', content)
    clean_text = re.sub(r'&[a-zA-Z]+;', ' ', clean_text)
    clean_text = re.sub(r'\*+', '', clean_text)
    clean_text = re.sub(r'#+\s*', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Strategic analysis keywords with high relevance
    strategic_keywords = {
        'objective': ['objective', 'goal', 'purpose', 'aim', 'mission'],
        'approach': ['approach', 'methodology', 'strategy', 'framework', 'model'],
        'implementation': ['implementation', 'deployment', 'execution', 'operationalization'],
        'compliance': ['compliance', 'adherence', 'conformance', 'requirement', 'standard'],
        'risk': ['risk', 'threat', 'vulnerability', 'challenge', 'concern'],
        'recommendation': ['recommend', 'suggest', 'propose', 'advise', 'guideline'],
        'governance': ['governance', 'oversight', 'management', 'administration', 'control'],
        'assessment': ['assessment', 'evaluation', 'analysis', 'review', 'examination']
    }
    
    # Extract sentences and categorize by strategic value
    sentences = re.split(r'[.!?]+', clean_text)
    categorized_sentences = {category: [] for category in strategic_keywords.keys()}
    general_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 30:
            sentence_lower = sentence.lower()
            categorized = False
            
            for category, keywords in strategic_keywords.items():
                if any(keyword in sentence_lower for keyword in keywords):
                    categorized_sentences[category].append(sentence)
                    categorized = True
                    break
            
            if not categorized:
                general_sentences.append(sentence)
    
    # Build strategic preview prioritizing key insights
    preview_parts = []
    current_length = 0
    
    # Priority order for strategic content
    priority_categories = ['objective', 'approach', 'implementation', 'recommendation', 'governance', 'assessment', 'compliance', 'risk']
    
    for category in priority_categories:
        if categorized_sentences[category] and current_length < max_length:
            # Select best sentence from category
            best_sentence = max(categorized_sentences[category], 
                              key=lambda s: len(s) if len(s) < 200 else 100)
            
            if current_length + len(best_sentence) + 2 <= max_length:
                preview_parts.append(best_sentence)
                current_length += len(best_sentence) + 2
    
    # Add general sentences if space allows
    for sentence in general_sentences:
        if current_length + len(sentence) + 2 <= max_length:
            # Prefer sentences with policy-relevant terms
            policy_terms = ['policy', 'regulation', 'law', 'act', 'directive', 'order']
            if any(term in sentence.lower() for term in policy_terms):
                preview_parts.append(sentence)
                current_length += len(sentence) + 2
        else:
            break
    
    # Fill remaining space with highest-quality general content
    remaining_sentences = [s for s in general_sentences if s not in preview_parts]
    for sentence in remaining_sentences[:3]:  # Limit to avoid overwhelming
        if current_length + len(sentence) + 2 <= max_length:
            preview_parts.append(sentence)
            current_length += len(sentence) + 2
    
    if preview_parts:
        preview = '. '.join(preview_parts)
        if not preview.endswith(('.', '...', '!', '?')):
            preview += '.'
        return preview
    else:
        # Intelligent fallback
        return clean_and_enhance_preview(content, max_length)

def analyze_framework_coverage(content: str) -> list:
    """Analyze which governance frameworks are covered in the content"""
    if not content:
        return []
    
    content_lower = content.lower()
    frameworks = []
    
    framework_indicators = {
        'NIST': ['nist', 'national institute of standards'],
        'ISO': ['iso ', 'international organization for standardization'],
        'GDPR': ['gdpr', 'general data protection regulation'],
        'SOC': ['soc ', 'service organization control'],
        'FISMA': ['fisma', 'federal information security'],
        'Cybersecurity Framework': ['cybersecurity framework', 'csf'],
        'AI Ethics': ['ai ethics', 'artificial intelligence ethics', 'responsible ai'],
        'Quantum Security': ['quantum security', 'post-quantum', 'quantum-safe'],
        'Risk Management': ['risk management', 'risk assessment', 'risk framework']
    }
    
    for framework, indicators in framework_indicators.items():
        if any(indicator in content_lower for indicator in indicators):
            frameworks.append(framework)
    
    return frameworks[:4]  # Limit to most relevant frameworks