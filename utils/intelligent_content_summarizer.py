"""
Intelligent Content Summarizer for Document Previews
Analyzes entire document content to generate concise 1-2 sentence summaries
"""

import re
from typing import Dict, List, Tuple
from collections import Counter

class IntelligentContentSummarizer:
    """
    Advanced content summarizer that analyzes full document text
    and generates contextually relevant 1-2 sentence summaries
    """
    
    def __init__(self):
        self.policy_keywords = {
            'framework': 'establishes a framework for',
            'strategy': 'outlines strategic approaches to',
            'guidance': 'provides guidance on',
            'standard': 'defines standards for',
            'regulation': 'regulates',
            'memorandum': 'directs policy regarding',
            'directive': 'mandates requirements for',
            'assessment': 'evaluates and assesses',
            'implementation': 'details implementation of',
            'requirements': 'specifies requirements for'
        }
        
        self.topic_keywords = {
            'ai': ['artificial intelligence', 'machine learning', 'ai systems', 'neural networks', 'algorithms'],
            'quantum': ['quantum computing', 'quantum cryptography', 'post-quantum', 'quantum supremacy', 'quantum technology'],
            'cybersecurity': ['cybersecurity', 'information security', 'cyber threats', 'data protection', 'security framework'],
            'privacy': ['privacy', 'data privacy', 'personal information', 'privacy protection'],
            'ethics': ['ethics', 'ethical', 'responsible', 'fairness', 'transparency', 'accountability'],
            'risk': ['risk management', 'risk assessment', 'threats', 'vulnerabilities', 'mitigation']
        }
    
    def generate_intelligent_summary(self, content: str, title: str = "", doc_type: str = "") -> str:
        """
        Generate an intelligent 1-2 sentence summary of the entire document
        
        Args:
            content: Full document text
            title: Document title for context
            doc_type: Document type for framing
            
        Returns:
            Concise 1-2 sentence summary
        """
        
        if not content or len(content.strip()) < 50:
            return "Document content is too brief for meaningful analysis."
        
        # Clean and prepare content
        cleaned_content = self._clean_content(content)
        
        # Extract key information
        main_topics = self._identify_main_topics(cleaned_content, title)
        key_purposes = self._extract_key_purposes(cleaned_content, doc_type)
        important_entities = self._extract_entities(cleaned_content)
        scope_and_impact = self._analyze_scope(cleaned_content)
        
        # Generate contextual summary
        summary = self._construct_summary(
            main_topics, key_purposes, important_entities, 
            scope_and_impact, title, doc_type
        )
        
        return summary
    
    def _clean_content(self, content: str) -> str:
        """Clean content for analysis"""
        # Remove excessive whitespace and normalize
        content = re.sub(r'\s+', ' ', content)
        
        # Remove common document artifacts
        content = re.sub(r'page \d+', '', content, flags=re.IGNORECASE)
        content = re.sub(r'table of contents?', '', content, flags=re.IGNORECASE)
        content = re.sub(r'appendix [a-z]', '', content, flags=re.IGNORECASE)
        
        return content.strip()
    
    def _identify_main_topics(self, content: str, title: str = "") -> List[str]:
        """Identify main topics discussed in the document"""
        content_lower = (content + " " + title).lower()
        identified_topics = []
        
        for topic, keywords in self.topic_keywords.items():
            topic_score = sum(1 for keyword in keywords if keyword in content_lower)
            if topic_score >= 2:  # Requires multiple mentions
                identified_topics.append(topic)
        
        # Sort by relevance (frequency of related terms)
        topic_scores = {}
        for topic in identified_topics:
            score = sum(content_lower.count(keyword) for keyword in self.topic_keywords[topic])
            topic_scores[topic] = score
        
        return sorted(identified_topics, key=lambda x: topic_scores.get(x, 0), reverse=True)
    
    def _extract_key_purposes(self, content: str, doc_type: str) -> List[str]:
        """Extract the main purposes and actions from the document"""
        content_lower = content.lower()
        purposes = []
        
        # Look for action verbs and purposes
        action_patterns = [
            r'this (?:document|framework|policy|standard|memorandum) ([^.]{20,80})',
            r'(?:establishes|provides|outlines|defines|mandates|requires|directs) ([^.]{15,60})',
            r'the purpose (?:of this document )?is to ([^.]{15,60})',
            r'(?:shall|will|must) ([^.]{15,60})',
            r'(?:addresses|focuses on|covers) ([^.]{15,60})'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, content_lower, re.IGNORECASE)
            for match in matches[:3]:  # Limit to most relevant
                cleaned_match = re.sub(r'\s+', ' ', match.strip())
                if len(cleaned_match) > 10:
                    purposes.append(cleaned_match)
        
        return purposes[:2]  # Return top 2 purposes
    
    def _extract_entities(self, content: str) -> List[str]:
        """Extract important organizations, agencies, and entities"""
        # Common government and tech entities
        entity_patterns = [
            r'\b(?:NIST|NSA|CIA|FBI|DHS|DOD|NASA|NSF|DARPA|CISA)\b',
            r'\b(?:White House|Congress|Department of [A-Z][a-z]+)\b',
            r'\b(?:European Union|EU|United Nations|UN|NATO)\b',
            r'\b(?:OpenAI|Google|Microsoft|Amazon|Meta|Apple|IBM)\b',
            r'\bNational Institute of [A-Za-z\s]+\b',
            r'\b[A-Z][a-z]+ (?:Agency|Administration|Institute|Foundation|Council)\b'
        ]
        
        entities = set()
        for pattern in entity_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            entities.update(matches)
        
        return list(entities)[:3]  # Return top 3 entities
    
    def _analyze_scope(self, content: str) -> str:
        """Analyze the scope and impact of the document"""
        content_lower = content.lower()
        
        scope_indicators = {
            'national': ['national', 'federal', 'united states', 'country-wide'],
            'international': ['international', 'global', 'worldwide', 'cross-border'],
            'industry': ['industry', 'sector', 'commercial', 'private sector'],
            'government': ['government', 'federal agencies', 'public sector'],
            'research': ['research', 'academic', 'scientific', 'universities']
        }
        
        scope_scores = {}
        for scope, indicators in scope_indicators.items():
            score = sum(content_lower.count(indicator) for indicator in indicators)
            if score > 0:
                scope_scores[scope] = score
        
        if scope_scores:
            primary_scope = max(scope_scores.keys(), key=lambda x: scope_scores[x])
            return primary_scope
        
        return "general"
    
    def _construct_summary(self, topics: List[str], purposes: List[str], 
                          entities: List[str], scope: str, title: str, doc_type: str) -> str:
        """Construct the final summary from analyzed components"""
        
        # Start with document type context
        doc_type_lower = doc_type.lower()
        if doc_type_lower in self.policy_keywords:
            action_phrase = self.policy_keywords[doc_type_lower]
        else:
            action_phrase = "addresses"
        
        # Build topic phrase
        if topics:
            if len(topics) == 1:
                topic_phrase = topics[0].replace('_', ' ')
            elif len(topics) == 2:
                topic_phrase = f"{topics[0].replace('_', ' ')} and {topics[1].replace('_', ' ')}"
            else:
                topic_phrase = f"{topics[0].replace('_', ' ')}, {topics[1].replace('_', ' ')}, and other emerging technologies"
        else:
            topic_phrase = "emerging technology governance"
        
        # Build main sentence
        if purposes and len(purposes) > 0:
            # Use the first identified purpose
            purpose = purposes[0].strip()
            if not purpose.endswith('.'):
                purpose += "."
            main_sentence = f"This {doc_type_lower} {action_phrase} {topic_phrase} by {purpose}"
        else:
            main_sentence = f"This {doc_type_lower} {action_phrase} {topic_phrase} governance and implementation."
        
        # Add scope/entity context if relevant
        context_sentence = ""
        if entities:
            primary_entity = entities[0]
            if scope in ['national', 'federal']:
                context_sentence = f" It provides {scope} guidance for {primary_entity} and related organizations."
            else:
                context_sentence = f" The document focuses on {primary_entity} implementations and requirements."
        elif scope in ['national', 'international']:
            context_sentence = f" It establishes {scope} standards and requirements for implementation."
        
        # Combine and clean up
        full_summary = main_sentence + context_sentence
        
        # Clean up any awkward phrasing
        full_summary = re.sub(r'\s+', ' ', full_summary)
        full_summary = full_summary.replace('  ', ' ')
        full_summary = full_summary.strip()
        
        # Ensure reasonable length (aim for 1-2 sentences, max 250 characters)
        if len(full_summary) > 250:
            # Truncate to first sentence if too long
            first_sentence = full_summary.split('.')[0] + '.'
            if len(first_sentence) < 200:
                return first_sentence
            else:
                return full_summary[:247] + "..."
        
        return full_summary

# Global instance
intelligent_summarizer = IntelligentContentSummarizer()

def generate_intelligent_content_preview(content: str, title: str = "", doc_type: str = "") -> str:
    """
    Generate intelligent content preview for documents
    
    Args:
        content: Full document text
        title: Document title
        doc_type: Document type
        
    Returns:
        Concise 1-2 sentence summary
    """
    return intelligent_summarizer.generate_intelligent_summary(content, title, doc_type)