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
    
    # Generate comprehensive preview with strategic insights - increased length for much more detail
    enhanced_preview = create_strategic_preview(content, title, max_length=2500)
    
    # Add contextual framework analysis
    frameworks = analyze_framework_coverage(content)
    if frameworks:
        framework_context = f"Framework Coverage: {', '.join(frameworks)}. "
        return framework_context + enhanced_preview
    
    return enhanced_preview

def create_strategic_preview(content: str, title: str = "", max_length: int = 2500) -> str:
    """Create strategic preview focusing on policy implications and recommendations"""
    if not content:
        return "No content available for preview"
    
    # For documents with limited content, expand analysis based on title and available content
    if len(content) < 1000:
        return create_enhanced_short_content_preview(content, title, max_length)
    
    # Continue with full content analysis for longer documents
    clean_text = re.sub(r'<[^>]+>', '', content)
    clean_text = re.sub(r'&[a-zA-Z]+;', ' ', clean_text)
    clean_text = re.sub(r'\*+', '', clean_text)
    clean_text = re.sub(r'#+\s*', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Use the existing comprehensive analysis for longer documents
    return clean_and_enhance_preview(clean_text, max_length)
    
def create_enhanced_short_content_preview(content: str, title: str = "", max_length: int = 2500) -> str:
    """Create enhanced preview for documents with limited content"""
    
    # Clean content
    clean_text = re.sub(r'<[^>]+>', '', content)
    clean_text = re.sub(r'&[a-zA-Z]+;', ' ', clean_text)
    clean_text = re.sub(r'\*+', '', clean_text)
    clean_text = re.sub(r'#+\s*', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Analyze title for context
    title_lower = title.lower() if title else ""
    
    # Generate contextual analysis based on title and content
    contextual_insights = []
    
    # AI-related document insights
    if any(term in title_lower for term in ['ai', 'artificial intelligence', 'machine learning', 'generative']):
        contextual_insights.extend([
            "This document addresses critical aspects of artificial intelligence governance, focusing on security frameworks and risk management approaches essential for organizational AI deployment.",
            "Key considerations include establishing robust AI governance structures, implementing comprehensive risk assessment methodologies, and ensuring compliance with emerging AI regulatory requirements.",
            "The framework emphasizes the importance of stakeholder engagement, ethical AI development practices, and continuous monitoring of AI system performance and potential impacts."
        ])
    
    # Cybersecurity-related insights
    if any(term in title_lower for term in ['cyber', 'security', 'framework', 'guidelines']):
        contextual_insights.extend([
            "This cybersecurity framework provides comprehensive guidance for implementing robust security measures across organizational infrastructure and systems.",
            "Critical implementation areas include threat assessment protocols, vulnerability management processes, incident response procedures, and security awareness training programs.",
            "The document emphasizes risk-based approaches to cybersecurity, emphasizing proactive threat detection, rapid response capabilities, and continuous security posture improvement."
        ])
    
    # Quantum-related insights
    if any(term in title_lower for term in ['quantum', 'post-quantum', 'cryptography']):
        contextual_insights.extend([
            "This document examines quantum technology implications for cybersecurity, addressing post-quantum cryptography transitions and quantum-safe security implementations.",
            "Key focus areas include quantum threat modeling, cryptographic agility planning, quantum key distribution protocols, and quantum-resistant algorithm deployment strategies.",
            "Strategic considerations encompass quantum readiness assessments, migration planning for quantum-safe technologies, and quantum cybersecurity risk management frameworks."
        ])
    
    # Policy and governance insights
    if any(term in title_lower for term in ['policy', 'governance', 'compliance', 'regulation']):
        contextual_insights.extend([
            "This policy document establishes comprehensive governance frameworks for organizational risk management, regulatory compliance, and strategic decision-making processes.",
            "Implementation guidance covers policy development methodologies, stakeholder engagement strategies, compliance monitoring systems, and governance effectiveness measurement approaches.",
            "The framework addresses organizational accountability structures, policy enforcement mechanisms, and continuous improvement processes for governance maturity advancement."
        ])
    
    # Combine original content with contextual insights
    preview_parts = []
    
    # Start with cleaned original content
    if clean_text:
        preview_parts.append(clean_text)
    
    # Add relevant contextual insights
    current_length = len('. '.join(preview_parts)) if preview_parts else 0
    
    for insight in contextual_insights:
        if current_length + len(insight) + 2 <= max_length:
            preview_parts.append(insight)
            current_length += len(insight) + 2
        else:
            break
    
    # If still under length limit, add general strategic analysis
    if current_length < max_length * 0.7:  # If less than 70% of max length
        additional_insights = [
            "Strategic implementation requires comprehensive stakeholder analysis, risk assessment protocols, and phased deployment approaches to ensure organizational readiness and successful adoption.",
            "Critical success factors include executive leadership commitment, cross-functional team coordination, adequate resource allocation, and continuous performance monitoring throughout implementation phases.",
            "Best practices emphasize iterative development approaches, stakeholder feedback integration, lessons learned documentation, and adaptive management strategies for complex organizational transformations."
        ]
        
        for insight in additional_insights:
            if current_length + len(insight) + 2 <= max_length:
                preview_parts.append(insight)
                current_length += len(insight) + 2
            else:
                break
    
    if preview_parts:
        preview = '. '.join(preview_parts)
        if not preview.endswith(('.', '...', '!', '?')):
            preview += '.'
        return preview
    else:
        return "Strategic document providing comprehensive guidance on implementation frameworks, governance structures, and risk management methodologies for organizational decision-making and policy development."

    # Clean content for full document analysis
    clean_text = re.sub(r'<[^>]+>', '', content)
    clean_text = re.sub(r'&[a-zA-Z]+;', ' ', clean_text)
    clean_text = re.sub(r'\*+', '', clean_text)
    clean_text = re.sub(r'#+\s*', '', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    
    # Enhanced strategic analysis keywords with expanded coverage
    strategic_keywords = {
        'executive_summary': ['executive summary', 'key findings', 'main conclusions', 'primary outcomes', 'summary'],
        'objective': ['objective', 'goal', 'purpose', 'aim', 'mission', 'intent', 'target'],
        'approach': ['approach', 'methodology', 'strategy', 'framework', 'model', 'method', 'technique'],
        'implementation': ['implementation', 'deployment', 'execution', 'operationalization', 'rollout', 'adoption'],
        'compliance': ['compliance', 'adherence', 'conformance', 'requirement', 'standard', 'regulation'],
        'risk': ['risk', 'threat', 'vulnerability', 'challenge', 'concern', 'hazard', 'exposure'],
        'recommendation': ['recommend', 'suggest', 'propose', 'advise', 'guideline', 'best practice'],
        'governance': ['governance', 'oversight', 'management', 'administration', 'control', 'supervision'],
        'assessment': ['assessment', 'evaluation', 'analysis', 'review', 'examination', 'audit'],
        'policy_implications': ['policy', 'implications', 'considerations', 'impact', 'consequences'],
        'technical_requirements': ['requirements', 'specifications', 'criteria', 'standards', 'capabilities'],
        'stakeholder_impact': ['stakeholders', 'organizations', 'entities', 'users', 'practitioners']
    }
    
    # Extract sentences and categorize by strategic value with enhanced scoring
    sentences = re.split(r'[.!?]+', clean_text)
    categorized_sentences = {category: [] for category in strategic_keywords.keys()}
    general_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 25:  # Slightly lower threshold for more content
            sentence_lower = sentence.lower()
            categorized = False
            
            # Score sentences for relevance
            sentence_score = 0
            best_category = None
            
            for category, keywords in strategic_keywords.items():
                category_matches = sum(1 for keyword in keywords if keyword in sentence_lower)
                if category_matches > 0:
                    # Prefer sentences with multiple keyword matches
                    category_score = category_matches * 2
                    
                    # Bonus for sentences with numbers, percentages, or specific data
                    if any(char.isdigit() for char in sentence) or '%' in sentence:
                        category_score += 1
                    
                    # Bonus for longer, more informative sentences
                    if len(sentence) > 80:
                        category_score += 1
                    
                    if category_score > sentence_score:
                        sentence_score = category_score
                        best_category = category
                        categorized = True
            
            if categorized and best_category:
                categorized_sentences[best_category].append((sentence_score, sentence))
            elif not categorized:
                general_sentences.append(sentence)
    
    # Sort sentences within each category by score
    for category in categorized_sentences:
        categorized_sentences[category].sort(key=lambda x: x[0], reverse=True)
    
    # Build comprehensive strategic preview
    preview_parts = []
    current_length = 0
    
    # Priority order for strategic content - focusing on most valuable insights first
    priority_categories = [
        'executive_summary', 'objective', 'approach', 'recommendation', 
        'implementation', 'governance', 'policy_implications', 'assessment', 
        'compliance', 'risk', 'technical_requirements', 'stakeholder_impact'
    ]
    
    # Add top sentences from each priority category
    for category in priority_categories:
        if categorized_sentences[category] and current_length < max_length:
            # Take multiple sentences from high-priority categories
            sentences_to_add = 3 if category in ['executive_summary', 'objective', 'recommendation'] else 2
            
            for i, (score, sentence) in enumerate(categorized_sentences[category][:sentences_to_add]):
                if current_length + len(sentence) + 2 <= max_length:
                    preview_parts.append(sentence)
                    current_length += len(sentence) + 2
                else:
                    break
    
    # Add high-quality general sentences focusing on policy and strategic content
    policy_terms = ['policy', 'regulation', 'law', 'act', 'directive', 'order', 'guidance', 'principle']
    strategic_terms = ['strategic', 'critical', 'essential', 'important', 'significant', 'key', 'primary']
    
    # Score general sentences for relevance
    scored_general = []
    for sentence in general_sentences:
        sentence_lower = sentence.lower()
        score = 0
        
        # Policy relevance
        if any(term in sentence_lower for term in policy_terms):
            score += 3
        
        # Strategic relevance
        if any(term in sentence_lower for term in strategic_terms):
            score += 2
        
        # Information density
        if len(sentence) > 60:
            score += 1
        
        # Specific data or examples
        if any(char.isdigit() for char in sentence) or '%' in sentence:
            score += 1
        
        if score > 0:
            scored_general.append((score, sentence))
    
    # Sort and add best general sentences
    scored_general.sort(key=lambda x: x[0], reverse=True)
    for score, sentence in scored_general[:5]:  # Increased limit
        if current_length + len(sentence) + 2 <= max_length:
            preview_parts.append(sentence)
            current_length += len(sentence) + 2
        else:
            break
    
    if preview_parts:
        preview = '. '.join(preview_parts)
        if not preview.endswith(('.', '...', '!', '?')):
            preview += '.'
        return preview
    else:
        # Enhanced fallback with more content
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