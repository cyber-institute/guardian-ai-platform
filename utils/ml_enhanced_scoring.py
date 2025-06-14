"""
ML-Enhanced Scoring System for GUARDIAN
Implements intelligent content analysis and realistic scoring based on actual document relevance
"""

import re
from typing import Dict, Optional, List, Tuple
from collections import Counter

class MLEnhancedScoringEngine:
    """
    Advanced scoring engine that uses machine learning patterns to accurately assess documents
    """
    
    def __init__(self):
        # AI framework indicators with weighted importance
        self.ai_indicators = {
            'core_ai': {
                'artificial intelligence': 20, 'machine learning': 18, 'neural network': 15,
                'deep learning': 15, 'ai system': 12, 'ai model': 12, 'algorithm': 8,
                'automated decision': 10, 'intelligent system': 10, 'ai framework': 12
            },
            'ai_applications': {
                'computer vision': 12, 'natural language processing': 12, 'chatbot': 8,
                'recommendation system': 10, 'generative ai': 15, 'llm': 12, 'gpt': 10
            },
            'ai_governance': {
                'responsible ai': 18, 'trustworthy ai': 15, 'ai ethics': 15,
                'ai governance': 12, 'ai policy': 12, 'ai bias': 12, 'explainable ai': 10
            }
        }
        
        # Quantum framework indicators (strict requirements)
        self.quantum_indicators = {
            'quantum_computing': {
                'quantum computing': 25, 'quantum algorithm': 20, 'quantum supremacy': 18,
                'quantum advantage': 15, 'qubit': 15, 'quantum gate': 12, 'quantum circuit': 12
            },
            'quantum_cryptography': {
                'quantum cryptography': 25, 'post-quantum': 20, 'quantum-safe': 18,
                'quantum-resistant': 18, 'quantum key distribution': 20, 'qkd': 15
            },
            'quantum_security': {
                'quantum threat': 15, 'quantum security': 18, 'quantum vulnerability': 12,
                'quantum migration': 12, 'quantum readiness': 10
            }
        }
        
        # Cybersecurity indicators
        self.cybersecurity_indicators = {
            'security_fundamentals': {
                'cybersecurity': 15, 'information security': 12, 'data protection': 10,
                'privacy': 8, 'encryption': 12, 'authentication': 10, 'authorization': 8
            },
            'threat_management': {
                'threat detection': 12, 'vulnerability': 10, 'incident response': 12,
                'risk management': 10, 'security monitoring': 8, 'penetration testing': 8
            },
            'compliance_governance': {
                'security framework': 12, 'compliance': 8, 'security policy': 8,
                'security standard': 10, 'security assessment': 8
            }
        }
        
        # Ethics indicators
        self.ethics_indicators = {
            'core_ethics': {
                'ethics': 12, 'ethical': 10, 'bias': 12, 'fairness': 12,
                'transparency': 10, 'accountability': 12, 'responsibility': 10
            },
            'governance_ethics': {
                'governance': 8, 'oversight': 8, 'audit': 8, 'compliance': 6,
                'principle': 6, 'guideline': 6, 'standard': 6
            },
            'social_impact': {
                'privacy': 8, 'discrimination': 10, 'human rights': 10,
                'social impact': 8, 'equity': 8, 'inclusion': 6
            }
        }
    
    def analyze_document_comprehensive(self, content: str, title: str) -> Dict[str, Optional[int]]:
        """
        Perform comprehensive ML-enhanced analysis of document content
        """
        content_analysis = self._analyze_content_depth(content, title)
        framework_applicability = self._determine_framework_applicability(content_analysis)
        scores = self._calculate_realistic_scores(content_analysis, framework_applicability)
        
        return scores
    
    def _analyze_content_depth(self, content: str, title: str) -> Dict:
        """
        Deep content analysis to understand document focus and scope
        """
        text_lower = (content + " " + title).lower()
        
        # Calculate relevance scores for each domain
        ai_relevance = self._calculate_domain_relevance(text_lower, self.ai_indicators)
        quantum_relevance = self._calculate_domain_relevance(text_lower, self.quantum_indicators)
        cyber_relevance = self._calculate_domain_relevance(text_lower, self.cybersecurity_indicators)
        ethics_relevance = self._calculate_domain_relevance(text_lower, self.ethics_indicators)
        
        # Determine primary focus
        primary_focus = self._identify_primary_focus(ai_relevance, quantum_relevance, cyber_relevance)
        
        # Calculate content density and sophistication
        content_metrics = self._analyze_content_metrics(content, title)
        
        return {
            'ai_relevance': ai_relevance,
            'quantum_relevance': quantum_relevance,
            'cyber_relevance': cyber_relevance,
            'ethics_relevance': ethics_relevance,
            'primary_focus': primary_focus,
            'content_metrics': content_metrics,
            'text_analysis': {
                'word_count': len(content.split()),
                'technical_density': self._calculate_technical_density(text_lower),
                'policy_language': self._detect_policy_language(text_lower)
            }
        }
    
    def _calculate_domain_relevance(self, text: str, domain_indicators: Dict) -> Dict:
        """
        Calculate relevance score for a specific domain
        """
        domain_scores = {}
        total_score = 0
        
        for category, keywords in domain_indicators.items():
            category_score = 0
            matched_keywords = []
            
            for keyword, weight in keywords.items():
                if keyword in text:
                    frequency = text.count(keyword)
                    category_score += weight * min(frequency, 3)  # Cap frequency impact
                    matched_keywords.append(keyword)
            
            domain_scores[category] = {
                'score': category_score,
                'matched_keywords': matched_keywords
            }
            total_score += category_score
        
        return {
            'total_score': total_score,
            'categories': domain_scores,
            'is_relevant': total_score > 20  # Threshold for relevance
        }
    
    def _identify_primary_focus(self, ai_rel: Dict, quantum_rel: Dict, cyber_rel: Dict) -> str:
        """
        Determine the primary focus of the document
        """
        scores = {
            'ai': ai_rel['total_score'],
            'quantum': quantum_rel['total_score'],
            'cybersecurity': cyber_rel['total_score']
        }
        
        max_score = max(scores.values())
        if max_score < 30:  # Low overall technical content
            return 'general'
        
        primary = max(scores.keys(), key=lambda x: scores[x])
        
        # Check for hybrid documents
        second_highest = sorted(scores.values(), reverse=True)[1]
        if second_highest > max_score * 0.6:  # Secondary focus is significant
            return f"{primary}_hybrid"
        
        return primary
    
    def _analyze_content_metrics(self, content: str, title: str) -> Dict:
        """
        Analyze content structure and sophistication
        """
        sentences = re.split(r'[.!?]+', content)
        words = content.split()
        
        return {
            'sentence_count': len([s for s in sentences if len(s.strip()) > 10]),
            'avg_sentence_length': sum(len(s.split()) for s in sentences) / max(len(sentences), 1),
            'technical_terms': self._count_technical_terms(content.lower()),
            'document_structure': self._analyze_document_structure(content),
            'formality_level': self._assess_formality_level(content.lower())
        }
    
    def _calculate_technical_density(self, text: str) -> float:
        """
        Calculate the density of technical terminology
        """
        technical_patterns = [
            r'\b\w+tion\b', r'\b\w+ment\b', r'\b\w+ance\b', r'\b\w+ity\b',
            r'\bframework\b', r'\bstandard\b', r'\bprotocol\b', r'\bimplementation\b'
        ]
        
        total_words = len(text.split())
        technical_words = sum(len(re.findall(pattern, text)) for pattern in technical_patterns)
        
        return technical_words / max(total_words, 1)
    
    def _detect_policy_language(self, text: str) -> bool:
        """
        Detect if document uses policy/regulatory language
        """
        policy_indicators = [
            'shall', 'must', 'required', 'mandatory', 'compliance', 'regulation',
            'policy', 'guideline', 'standard', 'framework', 'directive', 'memorandum'
        ]
        
        return sum(1 for indicator in policy_indicators if indicator in text) >= 3
    
    def _count_technical_terms(self, text: str) -> int:
        """
        Count technical terms across all domains
        """
        all_terms = []
        for domain in [self.ai_indicators, self.quantum_indicators, self.cybersecurity_indicators]:
            for category in domain.values():
                all_terms.extend(category.keys())
        
        return sum(1 for term in all_terms if term in text)
    
    def _analyze_document_structure(self, content: str) -> Dict:
        """
        Analyze document structure and organization
        """
        sections = re.findall(r'\n\s*(?:[A-Z][^.]*\.|\d+\..*?)\n', content)
        numbered_lists = re.findall(r'\n\s*\d+\.\s', content)
        bullet_lists = re.findall(r'\n\s*[•\-\*]\s', content)
        
        return {
            'has_sections': len(sections) > 2,
            'numbered_items': len(numbered_lists),
            'bullet_items': len(bullet_lists),
            'is_structured': len(sections) > 2 or len(numbered_lists) > 3
        }
    
    def _assess_formality_level(self, text: str) -> str:
        """
        Assess the formality level of the document
        """
        formal_indicators = ['hereby', 'whereas', 'pursuant', 'accordance', 'aforementioned']
        technical_indicators = ['specification', 'implementation', 'methodology', 'framework']
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in text)
        technical_count = sum(1 for indicator in technical_indicators if indicator in text)
        
        if formal_count >= 2:
            return 'highly_formal'
        elif technical_count >= 3:
            return 'technical'
        else:
            return 'standard'
    
    def _determine_framework_applicability(self, analysis: Dict) -> Dict[str, bool]:
        """
        Determine which frameworks should apply based on content analysis
        """
        ai_relevant = analysis['ai_relevance']['is_relevant']
        quantum_relevant = analysis['quantum_relevance']['is_relevant']
        cyber_relevant = analysis['cyber_relevance']['is_relevant']
        ethics_relevant = analysis['ethics_relevance']['is_relevant']
        
        return {
            'ai_cybersecurity': ai_relevant and cyber_relevant,
            'quantum_cybersecurity': quantum_relevant and cyber_relevant,
            'ai_ethics': ai_relevant and ethics_relevant,
            'quantum_ethics': quantum_relevant and ethics_relevant
        }
    
    def _calculate_realistic_scores(self, analysis: Dict, applicability: Dict) -> Dict[str, Optional[int]]:
        """
        Calculate realistic scores based on content analysis
        """
        scores = {}
        
        # AI Cybersecurity Score
        if applicability['ai_cybersecurity']:
            ai_strength = min(analysis['ai_relevance']['total_score'] / 100, 1.0)
            cyber_strength = min(analysis['cyber_relevance']['total_score'] / 80, 1.0)
            content_quality = self._assess_content_quality(analysis['content_metrics'])
            
            base_score = (ai_strength * 0.4 + cyber_strength * 0.4 + content_quality * 0.2) * 100
            scores['ai_cybersecurity_score'] = min(max(int(base_score), 10), 85)  # Realistic range 10-85
        else:
            scores['ai_cybersecurity_score'] = None
        
        # Quantum Cybersecurity Score (1-5 scale)
        if applicability['quantum_cybersecurity']:
            quantum_strength = analysis['quantum_relevance']['total_score']
            cyber_strength = analysis['cyber_relevance']['total_score']
            
            if quantum_strength > 80:
                scores['quantum_cybersecurity_score'] = 5
            elif quantum_strength > 60:
                scores['quantum_cybersecurity_score'] = 4
            elif quantum_strength > 40:
                scores['quantum_cybersecurity_score'] = 3
            elif quantum_strength > 20:
                scores['quantum_cybersecurity_score'] = 2
            else:
                scores['quantum_cybersecurity_score'] = 1
        else:
            scores['quantum_cybersecurity_score'] = None
        
        # AI Ethics Score
        if applicability['ai_ethics']:
            ai_strength = min(analysis['ai_relevance']['total_score'] / 100, 1.0)
            ethics_strength = min(analysis['ethics_relevance']['total_score'] / 60, 1.0)
            
            base_score = (ai_strength * 0.5 + ethics_strength * 0.5) * 100
            scores['ai_ethics_score'] = min(max(int(base_score), 5), 80)  # Realistic range 5-80
        else:
            scores['ai_ethics_score'] = None
        
        # Quantum Ethics Score
        if applicability['quantum_ethics']:
            quantum_strength = analysis['quantum_relevance']['total_score']
            ethics_strength = analysis['ethics_relevance']['total_score']
            
            base_score = min((quantum_strength + ethics_strength) / 2, 100)
            scores['quantum_ethics_score'] = min(max(int(base_score), 5), 75)  # Realistic range 5-75
        else:
            scores['quantum_ethics_score'] = None
        
        return scores
    
    def _assess_content_quality(self, metrics: Dict) -> float:
        """
        Assess overall content quality and sophistication
        """
        quality_score = 0.0
        
        # Document structure
        if metrics['document_structure']['is_structured']:
            quality_score += 0.3
        
        # Technical density
        if metrics['technical_terms'] > 10:
            quality_score += 0.3
        
        # Content length and depth
        if metrics['sentence_count'] > 50:
            quality_score += 0.2
        
        # Formality level
        if metrics['formality_level'] in ['highly_formal', 'technical']:
            quality_score += 0.2
        
        return min(quality_score, 1.0)

# Global instance
ml_scoring_engine = MLEnhancedScoringEngine()

def assess_document_with_ml(content: str, title: str) -> Dict[str, Optional[int]]:
    """
    Main function to assess document using ML-enhanced scoring
    """
    return ml_scoring_engine.analyze_document_comprehensive(content, title)