"""
Enhanced Content Analysis for GUARDIAN Scoring
Moves beyond keyword matching to sophisticated content depth analysis
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter

class ContentDepthAnalyzer:
    """Analyzes content depth and context rather than simple keyword presence"""
    
    def __init__(self):
        # Core AI policy/technical terms that indicate substantial AI discussion
        self.ai_substantive_terms = [
            'artificial intelligence framework', 'ai governance model', 'ai risk management',
            'ai ethics framework', 'responsible ai deployment', 'ai system lifecycle',
            'ai model validation', 'ai bias mitigation', 'ai transparency requirements',
            'ai accountability measures', 'ai safety protocols', 'ai oversight mechanisms',
            'ai policy development', 'ai regulatory approach', 'ai compliance standards',
            'machine learning governance', 'algorithmic accountability', 'automated decision systems'
        ]
        
        # Quantum substantive terms for real quantum policy/technical content
        self.quantum_substantive_terms = [
            'quantum cryptography implementation', 'post-quantum cryptography standards',
            'quantum key distribution protocols', 'quantum-safe encryption methods',
            'quantum computing security implications', 'quantum threat assessment',
            'quantum readiness strategy', 'quantum technology governance',
            'quantum science policy', 'quantum research framework',
            'quantum technology ethics', 'quantum computing applications',
            'quantum information security', 'quantum algorithm development'
        ]
        
        # Shallow/passing reference indicators
        self.shallow_indicators = [
            'similar to ai', 'like ai', 'as with ai', 'compared to ai',
            'ai has faced', 'ai experienced', 'ai industry',
            'mentioned ai', 'brief ai', 'ai analogy', 'ai comparison'
        ]
    
    def analyze_ai_content_depth(self, text: str, title: str) -> Dict[str, any]:
        """
        Analyze the depth and substance of AI-related content
        Returns comprehensive analysis including depth score and context
        """
        text_lower = text.lower()
        title_lower = title.lower()
        
        # Count substantive AI terms vs shallow mentions
        substantive_matches = sum(1 for term in self.ai_substantive_terms if term in text_lower)
        shallow_matches = sum(1 for indicator in self.shallow_indicators if indicator in text_lower)
        
        # Analyze sentence context around AI mentions
        ai_sentences = self._extract_ai_sentences(text)
        context_analysis = self._analyze_sentence_contexts(ai_sentences, 'ai')
        
        # Calculate content density (AI content per 1000 words)
        word_count = len(text.split())
        ai_density = (substantive_matches * 100) / max(word_count, 1000) * 1000
        
        # Determine if AI is the primary focus or just mentioned in passing
        is_primary_focus = self._is_ai_primary_focus(text, title, substantive_matches, ai_sentences)
        
        return {
            'substantive_terms': substantive_matches,
            'shallow_mentions': shallow_matches,
            'context_quality': context_analysis['quality_score'],
            'policy_depth': context_analysis['policy_depth'],
            'technical_depth': context_analysis['technical_depth'],
            'content_density': ai_density,
            'is_primary_focus': is_primary_focus,
            'ai_sentences_count': len(ai_sentences),
            'recommendation': self._get_ai_scoring_recommendation(
                substantive_matches, shallow_matches, is_primary_focus, ai_density
            )
        }
    
    def analyze_quantum_content_depth(self, text: str, title: str) -> Dict[str, any]:
        """
        Analyze the depth and substance of Quantum-related content
        """
        text_lower = text.lower()
        title_lower = title.lower()
        
        # Count substantive quantum terms
        substantive_matches = sum(1 for term in self.quantum_substantive_terms if term in text_lower)
        
        # Analyze sentence context around quantum mentions
        quantum_sentences = self._extract_quantum_sentences(text)
        context_analysis = self._analyze_sentence_contexts(quantum_sentences, 'quantum')
        
        # Calculate content density
        word_count = len(text.split())
        quantum_density = (substantive_matches * 100) / max(word_count, 1000) * 1000
        
        # Determine if quantum is the primary focus
        is_primary_focus = self._is_quantum_primary_focus(text, title, substantive_matches, quantum_sentences)
        
        return {
            'substantive_terms': substantive_matches,
            'context_quality': context_analysis['quality_score'],
            'policy_depth': context_analysis['policy_depth'],
            'technical_depth': context_analysis['technical_depth'],
            'content_density': quantum_density,
            'is_primary_focus': is_primary_focus,
            'quantum_sentences_count': len(quantum_sentences),
            'recommendation': self._get_quantum_scoring_recommendation(
                substantive_matches, is_primary_focus, quantum_density
            )
        }
    
    def _extract_ai_sentences(self, text: str) -> List[str]:
        """Extract sentences that mention AI-related terms"""
        sentences = re.split(r'[.!?]+', text)
        ai_sentences = []
        
        ai_patterns = [
            r'\bai\b', r'artificial intelligence', r'machine learning', r'neural network',
            r'deep learning', r'automated decision', r'algorithm'
        ]
        
        for sentence in sentences:
            if any(re.search(pattern, sentence, re.IGNORECASE) for pattern in ai_patterns):
                ai_sentences.append(sentence.strip())
        
        return ai_sentences
    
    def _extract_quantum_sentences(self, text: str) -> List[str]:
        """Extract sentences that mention quantum-related terms"""
        sentences = re.split(r'[.!?]+', text)
        quantum_sentences = []
        
        quantum_patterns = [
            r'quantum', r'post-quantum', r'qkd', r'qubit'
        ]
        
        for sentence in sentences:
            if any(re.search(pattern, sentence, re.IGNORECASE) for pattern in quantum_patterns):
                quantum_sentences.append(sentence.strip())
        
        return quantum_sentences
    
    def _analyze_sentence_contexts(self, sentences: List[str], topic: str) -> Dict[str, int]:
        """Analyze the quality and depth of topic discussion in sentences"""
        
        policy_keywords = ['policy', 'framework', 'governance', 'regulation', 'standard', 'guideline']
        technical_keywords = ['implementation', 'protocol', 'system', 'method', 'algorithm', 'security']
        depth_keywords = ['comprehensive', 'detailed', 'systematic', 'strategic', 'critical', 'essential']
        
        policy_depth = 0
        technical_depth = 0
        quality_score = 0
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Score policy depth
            policy_depth += sum(1 for keyword in policy_keywords if keyword in sentence_lower)
            
            # Score technical depth
            technical_depth += sum(1 for keyword in technical_keywords if keyword in sentence_lower)
            
            # Score overall quality based on sentence length and depth indicators
            if len(sentence.split()) > 10:  # Substantial sentences
                quality_score += 2
                if any(keyword in sentence_lower for keyword in depth_keywords):
                    quality_score += 3
            elif len(sentence.split()) > 5:
                quality_score += 1
        
        return {
            'policy_depth': policy_depth,
            'technical_depth': technical_depth,
            'quality_score': quality_score
        }
    
    def _is_ai_primary_focus(self, text: str, title: str, substantive_terms: int, ai_sentences: List[str]) -> bool:
        """Determine if AI is the primary focus of the document"""
        
        # Title indicates AI focus
        if any(term in title.lower() for term in ['ai', 'artificial intelligence', 'machine learning']):
            return True
        
        # High density of substantive AI terms
        if substantive_terms >= 5:
            return True
        
        # High proportion of sentences discuss AI substantially
        total_sentences = len(re.split(r'[.!?]+', text))
        ai_sentence_ratio = len(ai_sentences) / max(total_sentences, 1)
        
        if ai_sentence_ratio > 0.3:  # More than 30% of sentences mention AI
            return True
        
        return False
    
    def _is_quantum_primary_focus(self, text: str, title: str, substantive_terms: int, quantum_sentences: List[str]) -> bool:
        """Determine if Quantum is the primary focus of the document"""
        
        # Title indicates quantum focus
        if 'quantum' in title.lower():
            return True
        
        # High density of substantive quantum terms
        if substantive_terms >= 3:
            return True
        
        # High proportion of sentences discuss quantum
        total_sentences = len(re.split(r'[.!?]+', text))
        quantum_sentence_ratio = len(quantum_sentences) / max(total_sentences, 1)
        
        if quantum_sentence_ratio > 0.2:  # More than 20% of sentences mention quantum
            return True
        
        return False
    
    def _get_ai_scoring_recommendation(self, substantive_terms: int, shallow_mentions: int, 
                                     is_primary_focus: bool, density: float) -> Dict[str, any]:
        """Get scoring recommendation for AI content"""
        
        # If more shallow mentions than substantive terms, likely not AI-focused
        if shallow_mentions > substantive_terms and not is_primary_focus:
            return {
                'should_score': False,
                'reason': 'AI mentioned only in passing comparisons, not substantial policy content',
                'recommended_score': None
            }
        
        # If very low substantive content
        if substantive_terms < 2 and not is_primary_focus:
            return {
                'should_score': False,
                'reason': 'Insufficient AI policy/technical content for meaningful scoring',
                'recommended_score': None
            }
        
        # If minimal but some content
        if substantive_terms < 3 and density < 5:
            return {
                'should_score': True,
                'reason': 'Minimal AI content present',
                'recommended_score': 'low'  # 1-15 range
            }
        
        # If moderate content
        if substantive_terms >= 3 and is_primary_focus:
            return {
                'should_score': True,
                'reason': 'Moderate AI policy content',
                'recommended_score': 'medium'  # 16-50 range
            }
        
        # If substantial content
        if substantive_terms >= 5 and is_primary_focus:
            return {
                'should_score': True,
                'reason': 'Substantial AI policy content',
                'recommended_score': 'high'  # 51-100 range
            }
        
        return {
            'should_score': True,
            'reason': 'Default scoring',
            'recommended_score': 'low'
        }
    
    def _get_quantum_scoring_recommendation(self, substantive_terms: int, 
                                          is_primary_focus: bool, density: float) -> Dict[str, any]:
        """Get scoring recommendation for quantum content"""
        
        if substantive_terms >= 3 and is_primary_focus:
            return {
                'should_score': True,
                'reason': 'Substantial quantum content',
                'recommended_score': 'high'
            }
        elif substantive_terms >= 1 or is_primary_focus:
            return {
                'should_score': True,
                'reason': 'Moderate quantum content',
                'recommended_score': 'medium'
            }
        else:
            return {
                'should_score': False,
                'reason': 'Insufficient quantum content',
                'recommended_score': None
            }

def analyze_document_content_depth(text: str, title: str) -> Dict[str, Dict]:
    """
    Main function to analyze document content depth for both AI and Quantum topics
    """
    analyzer = ContentDepthAnalyzer()
    
    return {
        'ai_analysis': analyzer.analyze_ai_content_depth(text, title),
        'quantum_analysis': analyzer.analyze_quantum_content_depth(text, title)
    }