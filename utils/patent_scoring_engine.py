"""
Patent-Based Scoring Engine for GUARDIAN System
Implements all mathematical formulations from the patent application
"""

import numpy as np
import json
from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime
import math

class PatentScoringEngine:
    """
    Comprehensive scoring engine implementing patent formulations for:
    - Bayesian inference for dynamic maturity updates
    - Reinforcement learning policy optimization
    - Cybersecurity and ethics risk assessment
    - Policy effectiveness and gap analysis
    """
    
    def __init__(self):
        """Initialize the patent-based scoring engine."""
        # Bayesian prior probabilities for maturity levels
        self.maturity_priors = {
            'initial': 0.4,
            'basic': 0.3,
            'intermediate': 0.2,
            'advanced': 0.08,
            'dynamic': 0.02
        }
        
        # Q-learning parameters
        self.q_learning_alpha = 0.1  # Learning rate
        self.q_learning_gamma = 0.9  # Discount factor
        self.q_table = {}  # State-action value table
        
        # Risk assessment weights (from patent specifications)
        self.cyber_weights = {
            'authentication': 0.3,
            'encryption': 0.25,
            'access_control': 0.25,
            'monitoring': 0.2
        }
        
        self.ethics_weights = {
            'fairness': 0.3,
            'transparency': 0.25,
            'accountability': 0.25,
            'privacy': 0.2
        }
    
    def bayesian_maturity_update(self, observed_data: Dict, current_maturity: str) -> Dict[str, float]:
        """
        Patent Formula: P(M|D) = P(D|M)P(M) / P(D)
        Dynamically updates maturity levels as new data is received.
        
        Args:
            observed_data: Dictionary with query outcomes, policy adoption rates
            current_maturity: Current assessed maturity level
            
        Returns:
            Updated probability distribution over maturity levels
        """
        # Extract likelihood factors from observed data
        query_success_rate = observed_data.get('query_success_rate', 0.5)
        policy_adoption_rate = observed_data.get('policy_adoption_rate', 0.3)
        compliance_score = observed_data.get('compliance_score', 0.4)
        
        # Calculate likelihood P(D|M) for each maturity level
        likelihoods = {
            'initial': max(0.1, 1.0 - query_success_rate),
            'basic': max(0.1, 0.7 - abs(query_success_rate - 0.4)),
            'intermediate': max(0.1, 0.8 - abs(query_success_rate - 0.6)),
            'advanced': max(0.1, 0.9 - abs(query_success_rate - 0.8)),
            'dynamic': max(0.1, query_success_rate * policy_adoption_rate * compliance_score)
        }
        
        # Apply Bayes' theorem
        posteriors = {}
        normalizer = 0
        
        for maturity in self.maturity_priors:
            posterior = likelihoods[maturity] * self.maturity_priors[maturity]
            posteriors[maturity] = posterior
            normalizer += posterior
        
        # Normalize to get probability distribution
        for maturity in posteriors:
            posteriors[maturity] = posteriors[maturity] / normalizer if normalizer > 0 else 0.2
        
        return posteriors
    
    def q_learning_policy_optimization(self, state: str, action: str, reward: float, 
                                     next_state: str) -> float:
        """
        Patent Formula: Q(s,a) = Q(s,a) + α[R(s,a) + γ max Q(s',a') - Q(s,a)]
        Continuously refines policy recommendations using Q-learning.
        
        Args:
            state: Current policy state
            action: Action taken (policy recommendation)
            reward: Immediate reward (reduced vulnerabilities)
            next_state: Resulting state after action
            
        Returns:
            Updated Q-value for the state-action pair
        """
        # Initialize Q-table entries if not present
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0.0
        
        if next_state not in self.q_table:
            self.q_table[next_state] = {}
        
        # Find maximum Q-value for next state
        max_q_next = 0.0
        if self.q_table[next_state]:
            max_q_next = max(self.q_table[next_state].values())
        
        # Apply Q-learning update formula
        current_q = self.q_table[state][action]
        updated_q = current_q + self.q_learning_alpha * (
            reward + self.q_learning_gamma * max_q_next - current_q
        )
        
        self.q_table[state][action] = updated_q
        return updated_q
    
    def cybersecurity_risk_assessment(self, vulnerability_data: Dict) -> float:
        """
        Patent Formula: Risk_cyber = Σ(Wi × Vi × Ci)
        Compliance metrics using NIST RMF, ISO 27001, and GDPR frameworks.
        
        Args:
            vulnerability_data: Dictionary with vulnerability assessments
            
        Returns:
            Cybersecurity risk score (0-100, lower is better)
        """
        total_risk = 0.0
        
        for vuln_type, weight in self.cyber_weights.items():
            vulnerability_score = vulnerability_data.get(f'{vuln_type}_vulnerability', 3.0)  # 0-5 scale
            likelihood = vulnerability_data.get(f'{vuln_type}_likelihood', 0.5)  # 0-1 scale
            impact = vulnerability_data.get(f'{vuln_type}_impact', 0.7)  # 0-1 scale
            
            # Normalize vulnerability score to 0-1 range
            normalized_vuln = vulnerability_score / 5.0
            
            # Apply patent formula
            risk_component = weight * normalized_vuln * likelihood * impact
            total_risk += risk_component
        
        # Convert to 0-100 scale (higher means more risk)
        return min(100.0, total_risk * 100.0)
    
    def ethics_risk_assessment(self, ethics_data: Dict) -> float:
        """
        Patent Formula: Risk_ethics = (1 - T) × B × A
        Bias, fairness, transparency, and human autonomy evaluation.
        
        Args:
            ethics_data: Dictionary with ethics assessment data
            
        Returns:
            Ethics risk score (0-100, lower is better)
        """
        transparency_score = ethics_data.get('transparency', 0.5)  # 0-1 scale
        bias_factor = ethics_data.get('bias_factor', 0.5)  # 0-1 scale  
        autonomy_risk = ethics_data.get('autonomy_risk', 0.5)  # 0-1 scale
        
        # Apply patent formula
        ethics_risk = (1 - transparency_score) * bias_factor * autonomy_risk
        
        # Convert to 0-100 scale
        return min(100.0, ethics_risk * 100.0)
    
    def similarity_detection(self, vector_a: List[float], vector_b: List[float]) -> float:
        """
        Patent Formula: Similarity = A·B / (||A|| ||B||)
        Cosine similarity for detecting semantic drift in policy vectors.
        
        Args:
            vector_a: First vector representation
            vector_b: Second vector representation
            
        Returns:
            Similarity score (0-1, higher means more similar)
        """
        if not vector_a or not vector_b or len(vector_a) != len(vector_b):
            return 0.0
        
        # Convert to numpy arrays for easier computation
        a = np.array(vector_a)
        b = np.array(vector_b)
        
        # Calculate dot product
        dot_product = np.dot(a, b)
        
        # Calculate magnitudes (Euclidean norms)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        # Avoid division by zero
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        # Apply patent formula
        similarity = dot_product / (norm_a * norm_b)
        return max(0.0, similarity)  # Ensure non-negative
    
    def policy_gap_score(self, found_provisions: Dict, expected_provisions: Dict) -> float:
        """
        Patent Formula: G_policy = 1 - (C_match + E_match) / (C_total + E_total)
        Comprehensive compliance gap analysis and reporting.
        
        Args:
            found_provisions: Dictionary with counts of found provisions
            expected_provisions: Dictionary with expected provision counts
            
        Returns:
            Gap score (0-1, lower means better compliance)
        """
        c_match = found_provisions.get('cybersecurity', 0)
        e_match = found_provisions.get('ethics', 0)
        c_total = expected_provisions.get('cybersecurity', 1)
        e_total = expected_provisions.get('ethics', 1)
        
        # Avoid division by zero
        if (c_total + e_total) == 0:
            return 1.0  # Maximum gap if no expectations set
        
        # Apply patent formula
        gap_score = 1 - (c_match + e_match) / (c_total + e_total)
        return max(0.0, min(1.0, gap_score))
    
    def policy_effectiveness_score(self, success_probability: float, 
                                 regulatory_influence: float,
                                 ethical_compliance: float) -> float:
        """
        Patent Formula: E_policy = P_success × Rf × Ec
        Probabilistic reinforcement learning for policy synthesis.
        
        Args:
            success_probability: Probability of policy adoption (0-1)
            regulatory_influence: Regulatory influence factor (0-1)
            ethical_compliance: Ethical compliance coefficient (0-1)
            
        Returns:
            Policy effectiveness score (0-100)
        """
        # Apply patent formula
        effectiveness = success_probability * regulatory_influence * ethical_compliance
        return min(100.0, effectiveness * 100.0)
    
    def probability_based_optimization(self, component_scores: List[float], 
                                     weights: List[float]) -> float:
        """
        Patent Formula: P_success = Σ(wi × Si)
        Success probability calculation for policy adoption.
        
        Args:
            component_scores: List of success scores for each component
            weights: List of weights based on geographical, ethical, regulatory constraints
            
        Returns:
            Success probability (0-1)
        """
        if len(component_scores) != len(weights):
            return 0.0
        
        # Apply patent formula
        success_probability = sum(w * s for w, s in zip(weights, component_scores))
        return max(0.0, min(1.0, success_probability))
    
    def stress_testing_score(self, ecs: float, adaptability: float, 
                           legal_alignment: float, implementation_feasibility: float) -> float:
        """
        Patent Formula: S_final = (ECS + AS + LAS + IFS) / 4
        Four-criteria assessment for AI policy sandbox stress-testing.
        
        Args:
            ecs: Ethical Compliance Score (0-100)
            adaptability: Adaptability Score (0-100)
            legal_alignment: Legal Alignment Score (0-100)
            implementation_feasibility: Implementation Feasibility Score (0-100)
            
        Returns:
            Final stress-testing score (0-100)
        """
        # Apply patent formula
        final_score = (ecs + adaptability + legal_alignment + implementation_feasibility) / 4
        return max(0.0, min(100.0, final_score))
    
    def comprehensive_document_assessment(self, document_text: str, 
                                        document_metadata: Dict) -> Dict[str, float]:
        """
        Perform comprehensive assessment using all patent formulations.
        
        Args:
            document_text: Full document content
            document_metadata: Document metadata and context
            
        Returns:
            Dictionary with all assessment scores
        """
        # Extract features from document for assessment
        features = self._extract_document_features(document_text)
        
        # Bayesian maturity assessment
        observed_data = {
            'query_success_rate': features.get('technical_complexity', 0.5),
            'policy_adoption_rate': features.get('policy_relevance', 0.3),
            'compliance_score': features.get('compliance_indicators', 0.4)
        }
        maturity_distribution = self.bayesian_maturity_update(observed_data, 'intermediate')
        
        # Risk assessments
        vulnerability_data = {
            'authentication_vulnerability': features.get('auth_weakness', 2.0),
            'authentication_likelihood': features.get('auth_likelihood', 0.3),
            'authentication_impact': features.get('auth_impact', 0.7),
            'encryption_vulnerability': features.get('encryption_gaps', 1.5),
            'encryption_likelihood': features.get('encryption_likelihood', 0.2),
            'encryption_impact': features.get('encryption_impact', 0.8),
            'access_control_vulnerability': features.get('access_weakness', 1.8),
            'access_control_likelihood': features.get('access_likelihood', 0.25),
            'access_control_impact': features.get('access_impact', 0.6),
            'monitoring_vulnerability': features.get('monitoring_gaps', 2.2),
            'monitoring_likelihood': features.get('monitoring_likelihood', 0.4),
            'monitoring_impact': features.get('monitoring_impact', 0.5)
        }
        
        ethics_data = {
            'transparency': features.get('transparency_score', 0.6),
            'bias_factor': features.get('bias_indicators', 0.4),
            'autonomy_risk': features.get('autonomy_concerns', 0.3)
        }
        
        cyber_risk = self.cybersecurity_risk_assessment(vulnerability_data)
        ethics_risk = self.ethics_risk_assessment(ethics_data)
        
        # Policy gap analysis
        found_provisions = {
            'cybersecurity': features.get('cyber_provisions_found', 0),
            'ethics': features.get('ethics_provisions_found', 0)
        }
        expected_provisions = {
            'cybersecurity': features.get('expected_cyber_provisions', 5),
            'ethics': features.get('expected_ethics_provisions', 4)
        }
        gap_score = self.policy_gap_score(found_provisions, expected_provisions)
        
        # Policy effectiveness
        effectiveness = self.policy_effectiveness_score(
            features.get('adoption_probability', 0.6),
            features.get('regulatory_strength', 0.7),
            features.get('ethical_compliance', 0.8)
        )
        
        # Stress testing score
        stress_score = self.stress_testing_score(
            features.get('ethical_compliance_score', 75),
            features.get('adaptability_score', 70),
            features.get('legal_alignment_score', 80),
            features.get('implementation_score', 65)
        )
        
        return {
            'maturity_distribution': maturity_distribution,
            'cybersecurity_risk': cyber_risk,
            'ethics_risk': ethics_risk,
            'policy_gap': gap_score,
            'policy_effectiveness': effectiveness,
            'stress_testing_score': stress_score,
            'overall_score': (100 - cyber_risk + 100 - ethics_risk + effectiveness + stress_score) / 4
        }
    
    def _extract_document_features(self, text: str) -> Dict[str, float]:
        """
        Extract numerical features from document text for scoring.
        
        Args:
            text: Document content
            
        Returns:
            Dictionary of extracted features
        """
        text_lower = text.lower()
        
        # Technical complexity indicators
        technical_terms = ['algorithm', 'framework', 'protocol', 'architecture', 'implementation']
        technical_complexity = sum(1 for term in technical_terms if term in text_lower) / len(technical_terms)
        
        # Policy relevance indicators
        policy_terms = ['policy', 'regulation', 'compliance', 'governance', 'standard']
        policy_relevance = sum(1 for term in policy_terms if term in text_lower) / len(policy_terms)
        
        # Compliance indicators
        compliance_terms = ['nist', 'iso', 'gdpr', 'sox', 'hipaa', 'compliance']
        compliance_indicators = sum(1 for term in compliance_terms if term in text_lower) / len(compliance_terms)
        
        # Cybersecurity indicators
        cyber_terms = ['security', 'encryption', 'authentication', 'authorization', 'firewall']
        cyber_strength = sum(1 for term in cyber_terms if term in text_lower) / len(cyber_terms)
        
        # Ethics indicators  
        ethics_terms = ['ethics', 'bias', 'fairness', 'transparency', 'accountability']
        ethics_strength = sum(1 for term in ethics_terms if term in text_lower) / len(ethics_terms)
        
        return {
            'technical_complexity': technical_complexity,
            'policy_relevance': policy_relevance,
            'compliance_indicators': compliance_indicators,
            'auth_weakness': max(0.5, 3.0 - cyber_strength * 2),
            'auth_likelihood': max(0.1, 0.5 - cyber_strength * 0.3),
            'auth_impact': 0.7,
            'encryption_gaps': max(0.5, 2.5 - cyber_strength * 1.5),
            'encryption_likelihood': max(0.1, 0.4 - cyber_strength * 0.2),
            'encryption_impact': 0.8,
            'access_weakness': max(0.5, 2.8 - cyber_strength * 1.8),
            'access_likelihood': max(0.1, 0.45 - cyber_strength * 0.25),
            'access_impact': 0.6,
            'monitoring_gaps': max(0.5, 3.2 - cyber_strength * 2.2),
            'monitoring_likelihood': max(0.1, 0.6 - cyber_strength * 0.4),
            'monitoring_impact': 0.5,
            'transparency_score': min(0.9, 0.3 + ethics_strength * 0.6),
            'bias_indicators': max(0.1, 0.6 - ethics_strength * 0.5),
            'autonomy_concerns': max(0.1, 0.5 - ethics_strength * 0.4),
            'cyber_provisions_found': int(cyber_strength * 8),
            'ethics_provisions_found': int(ethics_strength * 6),
            'expected_cyber_provisions': 8,
            'expected_ethics_provisions': 6,
            'adoption_probability': min(0.9, 0.4 + policy_relevance * 0.5),
            'regulatory_strength': min(0.9, 0.5 + compliance_indicators * 0.4),
            'ethical_compliance': min(0.9, 0.4 + ethics_strength * 0.5),
            'ethical_compliance_score': min(95, 60 + ethics_strength * 35),
            'adaptability_score': min(90, 50 + technical_complexity * 40),
            'legal_alignment_score': min(95, 65 + compliance_indicators * 30),
            'implementation_score': min(85, 45 + (technical_complexity + policy_relevance) * 20)
        }

# Global instance for use across the application
patent_scoring_engine = PatentScoringEngine()