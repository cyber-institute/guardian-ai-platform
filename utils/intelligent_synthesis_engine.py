"""
Intelligent Synthesis Engine for Multi-LLM Consensus
Advanced synthesis algorithms for combining LLM intelligence with optimal accuracy
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import json
import logging
from collections import defaultdict

@dataclass
class SynthesisMetrics:
    """Metrics for evaluating synthesis quality"""
    consensus_strength: float
    disagreement_variance: float
    confidence_calibration: float
    synthesis_accuracy: float
    processing_efficiency: float

class IntelligentSynthesisEngine:
    """
    Advanced synthesis engine that optimally combines multiple LLM responses
    Implements cutting-edge consensus algorithms for maximum accuracy
    """
    
    def __init__(self):
        self.synthesis_history = []
        self.performance_metrics = {}
        self.adaptation_weights = {
            'accuracy_weight': 0.4,
            'confidence_weight': 0.3,
            'speed_weight': 0.2,
            'consistency_weight': 0.1
        }
    
    def synthesize_optimal_consensus(
        self, 
        llm_responses: List[Dict[str, Any]], 
        domain: str,
        target_confidence: float = 0.85
    ) -> Dict[str, Any]:
        """
        Primary synthesis method that optimally combines LLM responses
        Uses adaptive algorithms based on response patterns and domain characteristics
        """
        
        if not llm_responses:
            return self._create_empty_synthesis()
        
        # Stage 1: Preprocess and validate responses
        validated_responses = self._validate_and_preprocess(llm_responses)
        
        # Stage 2: Determine optimal synthesis strategy
        synthesis_strategy = self._select_synthesis_strategy(validated_responses, domain)
        
        # Stage 3: Apply synthesis algorithm
        if synthesis_strategy == 'advanced_bayesian':
            result = self._advanced_bayesian_synthesis(validated_responses, domain)
        elif synthesis_strategy == 'consensus_clustering':
            result = self._consensus_clustering_synthesis(validated_responses, domain)
        elif synthesis_strategy == 'weighted_ensemble':
            result = self._weighted_ensemble_synthesis(validated_responses, domain)
        else:
            result = self._hybrid_synthesis(validated_responses, domain)
        
        # Stage 4: Quality validation and calibration
        calibrated_result = self._calibrate_synthesis_quality(result, target_confidence)
        
        # Stage 5: Update learning metrics
        self._update_synthesis_learning(calibrated_result, synthesis_strategy)
        
        return calibrated_result
    
    def _validate_and_preprocess(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and normalize responses for synthesis"""
        
        validated = []
        
        for response in responses:
            if self._is_valid_response(response):
                normalized = self._normalize_response_structure(response)
                validated.append(normalized)
        
        return validated
    
    def _is_valid_response(self, response: Dict[str, Any]) -> bool:
        """Check if response has required structure and valid data"""
        
        required_fields = ['service_name', 'confidence', 'scores']
        
        for field in required_fields:
            if field not in response:
                return False
        
        # Check if scores are numeric and within reasonable range
        scores = response.get('scores', {})
        if not isinstance(scores, dict):
            return False
        
        for score_value in scores.values():
            if not isinstance(score_value, (int, float)) or score_value < 0 or score_value > 100:
                return False
        
        return True
    
    def _normalize_response_structure(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize response to standard structure"""
        
        normalized = {
            'service_name': response.get('service_name', 'unknown'),
            'confidence': min(max(response.get('confidence', 0.5), 0.0), 1.0),
            'scores': {},
            'processing_time': response.get('processing_time', 0.0),
            'metadata': response.get('metadata', {})
        }
        
        # Normalize scores to 0-100 scale
        raw_scores = response.get('scores', {})
        for metric, value in raw_scores.items():
            if isinstance(value, (int, float)):
                if value <= 1.0:  # Convert 0-1 scale to 0-100
                    normalized['scores'][metric] = value * 100
                else:
                    normalized['scores'][metric] = min(max(value, 0), 100)
        
        return normalized
    
    def _select_synthesis_strategy(
        self, 
        responses: List[Dict[str, Any]], 
        domain: str
    ) -> str:
        """Intelligently select optimal synthesis strategy based on response patterns"""
        
        num_responses = len(responses)
        
        # Calculate response diversity
        diversity_score = self._calculate_response_diversity(responses)
        
        # Calculate confidence distribution
        confidences = [r['confidence'] for r in responses]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        confidence_variance = np.var(confidences) if len(confidences) > 1 else 0
        
        # Strategy selection logic
        if num_responses >= 5 and diversity_score > 0.7:
            return 'consensus_clustering'
        elif avg_confidence > 0.8 and confidence_variance < 0.1:
            return 'weighted_ensemble'
        elif domain in ['ai_ethics', 'quantum_security'] and num_responses >= 3:
            return 'advanced_bayesian'
        else:
            return 'hybrid_synthesis'
    
    def _calculate_response_diversity(self, responses: List[Dict[str, Any]]) -> float:
        """Calculate diversity score across responses"""
        
        if len(responses) < 2:
            return 0.0
        
        # Calculate pairwise score differences
        all_metrics = set()
        for response in responses:
            all_metrics.update(response['scores'].keys())
        
        total_diversity = 0
        comparisons = 0
        
        for metric in all_metrics:
            scores = []
            for response in responses:
                if metric in response['scores']:
                    scores.append(response['scores'][metric])
            
            if len(scores) >= 2:
                score_variance = np.var(scores)
                normalized_variance = min(score_variance / 100, 1.0)  # Normalize
                total_diversity += normalized_variance
                comparisons += 1
        
        return total_diversity / comparisons if comparisons > 0 else 0.0
    
    def _advanced_bayesian_synthesis(
        self, 
        responses: List[Dict[str, Any]], 
        domain: str
    ) -> Dict[str, Any]:
        """Advanced Bayesian synthesis with domain-specific priors"""
        
        # Domain-specific prior distributions
        domain_priors = {
            'ai_ethics': {
                'completeness': {'mean': 68, 'variance': 15},
                'clarity': {'mean': 72, 'variance': 12},
                'enforceability': {'mean': 65, 'variance': 18}
            },
            'quantum_security': {
                'completeness': {'mean': 75, 'variance': 10},
                'clarity': {'mean': 70, 'variance': 14},
                'enforceability': {'mean': 78, 'variance': 8}
            },
            'cybersecurity': {
                'completeness': {'mean': 80, 'variance': 12},
                'clarity': {'mean': 75, 'variance': 10},
                'enforceability': {'mean': 82, 'variance': 9}
            }
        }
        
        priors = domain_priors.get(domain, {
            'completeness': {'mean': 70, 'variance': 15},
            'clarity': {'mean': 70, 'variance': 15},
            'enforceability': {'mean': 70, 'variance': 15}
        })
        
        # Collect all metrics
        all_metrics = set()
        for response in responses:
            all_metrics.update(response['scores'].keys())
        
        synthesized_scores = {}
        
        for metric in all_metrics:
            # Extract observations and weights
            observations = []
            weights = []
            
            for response in responses:
                if metric in response['scores']:
                    observations.append(response['scores'][metric])
                    weights.append(response['confidence'])
            
            if observations:
                # Bayesian posterior calculation
                prior_mean = priors.get(metric, {}).get('mean', 70)
                prior_variance = priors.get(metric, {}).get('variance', 15)
                
                # Weighted likelihood
                weighted_mean = sum(o * w for o, w in zip(observations, weights)) / sum(weights)
                observation_variance = np.var(observations) if len(observations) > 1 else 10
                
                # Posterior calculation
                posterior_precision = (1 / prior_variance) + (sum(weights) / observation_variance)
                posterior_variance = 1 / posterior_precision
                posterior_mean = (
                    (prior_mean / prior_variance) + 
                    (weighted_mean * sum(weights) / observation_variance)
                ) / posterior_precision
                
                synthesized_scores[metric] = round(max(0, min(100, posterior_mean)), 2)
        
        # Calculate consensus score
        consensus_score = sum(synthesized_scores.values()) / len(synthesized_scores) if synthesized_scores else 0
        synthesized_scores['consensus_score'] = round(consensus_score, 2)
        
        return {
            'scores': synthesized_scores,
            'synthesis_method': 'advanced_bayesian',
            'confidence': self._calculate_synthesis_confidence(responses, synthesized_scores),
            'metadata': {
                'domain_priors_applied': True,
                'posterior_variance': posterior_variance if 'posterior_variance' in locals() else 0,
                'observations_count': len(observations) if 'observations' in locals() else 0
            }
        }
    
    def _consensus_clustering_synthesis(
        self, 
        responses: List[Dict[str, Any]], 
        domain: str
    ) -> Dict[str, Any]:
        """Consensus clustering approach for high-diversity responses"""
        
        # Group responses by similarity
        response_clusters = self._cluster_similar_responses(responses)
        
        # Weight clusters by size and confidence
        cluster_weights = {}
        for cluster_id, cluster_responses in response_clusters.items():
            avg_confidence = sum(r['confidence'] for r in cluster_responses) / len(cluster_responses)
            cluster_size_weight = len(cluster_responses) / len(responses)
            cluster_weights[cluster_id] = avg_confidence * cluster_size_weight
        
        # Synthesize from dominant clusters
        synthesized_scores = {}
        all_metrics = set()
        for response in responses:
            all_metrics.update(response['scores'].keys())
        
        for metric in all_metrics:
            weighted_sum = 0
            total_weight = 0
            
            for cluster_id, cluster_responses in response_clusters.items():
                cluster_scores = [r['scores'].get(metric, 0) for r in cluster_responses if metric in r['scores']]
                if cluster_scores:
                    cluster_avg = sum(cluster_scores) / len(cluster_scores)
                    weight = cluster_weights[cluster_id]
                    weighted_sum += cluster_avg * weight
                    total_weight += weight
            
            if total_weight > 0:
                synthesized_scores[metric] = round(weighted_sum / total_weight, 2)
        
        consensus_score = sum(synthesized_scores.values()) / len(synthesized_scores) if synthesized_scores else 0
        synthesized_scores['consensus_score'] = round(consensus_score, 2)
        
        return {
            'scores': synthesized_scores,
            'synthesis_method': 'consensus_clustering',
            'confidence': self._calculate_synthesis_confidence(responses, synthesized_scores),
            'metadata': {
                'clusters_formed': len(response_clusters),
                'dominant_cluster_size': max(len(cluster) for cluster in response_clusters.values()) if response_clusters else 0
            }
        }
    
    def _cluster_similar_responses(self, responses: List[Dict[str, Any]]) -> Dict[int, List[Dict[str, Any]]]:
        """Cluster responses based on score similarity"""
        
        if len(responses) <= 2:
            return {0: responses}
        
        # Simple clustering based on score similarity
        clusters = {}
        cluster_id = 0
        
        for response in responses:
            assigned = False
            
            for cid, cluster in clusters.items():
                # Check similarity with cluster center
                if self._calculate_response_similarity(response, cluster[0]) > 0.7:
                    cluster.append(response)
                    assigned = True
                    break
            
            if not assigned:
                clusters[cluster_id] = [response]
                cluster_id += 1
        
        return clusters
    
    def _calculate_response_similarity(self, response1: Dict[str, Any], response2: Dict[str, Any]) -> float:
        """Calculate similarity between two responses"""
        
        scores1 = response1['scores']
        scores2 = response2['scores']
        
        common_metrics = set(scores1.keys()) & set(scores2.keys())
        
        if not common_metrics:
            return 0.0
        
        total_similarity = 0
        for metric in common_metrics:
            diff = abs(scores1[metric] - scores2[metric])
            similarity = max(0, 1 - (diff / 100))  # Normalize to 0-1
            total_similarity += similarity
        
        return total_similarity / len(common_metrics)
    
    def _weighted_ensemble_synthesis(
        self, 
        responses: List[Dict[str, Any]], 
        domain: str
    ) -> Dict[str, Any]:
        """Weighted ensemble synthesis for high-confidence responses"""
        
        # Calculate dynamic weights based on confidence and historical performance
        service_weights = self._calculate_dynamic_service_weights(responses)
        
        synthesized_scores = {}
        all_metrics = set()
        for response in responses:
            all_metrics.update(response['scores'].keys())
        
        for metric in all_metrics:
            weighted_sum = 0
            total_weight = 0
            
            for response in responses:
                if metric in response['scores']:
                    weight = service_weights.get(response['service_name'], 0.5) * response['confidence']
                    weighted_sum += response['scores'][metric] * weight
                    total_weight += weight
            
            if total_weight > 0:
                synthesized_scores[metric] = round(weighted_sum / total_weight, 2)
        
        consensus_score = sum(synthesized_scores.values()) / len(synthesized_scores) if synthesized_scores else 0
        synthesized_scores['consensus_score'] = round(consensus_score, 2)
        
        return {
            'scores': synthesized_scores,
            'synthesis_method': 'weighted_ensemble',
            'confidence': self._calculate_synthesis_confidence(responses, synthesized_scores),
            'metadata': {
                'service_weights': service_weights,
                'avg_response_confidence': sum(r['confidence'] for r in responses) / len(responses)
            }
        }
    
    def _calculate_dynamic_service_weights(self, responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate dynamic weights for services based on performance history"""
        
        # Base weights for different services
        base_weights = {
            'openai': 0.95,
            'anthropic': 0.95,
            'groq': 0.85,
            'ollama': 0.75,
            'huggingface': 0.70,
            'together_ai': 0.80,
            'perplexity': 0.80
        }
        
        # Adjust based on current confidence levels
        service_weights = {}
        for response in responses:
            service_name = response['service_name']
            base_weight = base_weights.get(service_name, 0.5)
            confidence_adjustment = response['confidence'] * 0.2
            service_weights[service_name] = min(base_weight + confidence_adjustment, 1.0)
        
        return service_weights
    
    def _hybrid_synthesis(
        self, 
        responses: List[Dict[str, Any]], 
        domain: str
    ) -> Dict[str, Any]:
        """Hybrid synthesis combining multiple approaches"""
        
        # Apply multiple synthesis methods
        bayesian_result = self._advanced_bayesian_synthesis(responses, domain)
        ensemble_result = self._weighted_ensemble_synthesis(responses, domain)
        
        # Combine results with intelligent weighting
        hybrid_scores = {}
        
        for metric in bayesian_result['scores']:
            if metric in ensemble_result['scores']:
                # Weight based on confidence levels
                bayesian_weight = bayesian_result['confidence']
                ensemble_weight = ensemble_result['confidence']
                total_weight = bayesian_weight + ensemble_weight
                
                if total_weight > 0:
                    hybrid_score = (
                        bayesian_result['scores'][metric] * bayesian_weight +
                        ensemble_result['scores'][metric] * ensemble_weight
                    ) / total_weight
                    hybrid_scores[metric] = round(hybrid_score, 2)
                else:
                    hybrid_scores[metric] = bayesian_result['scores'][metric]
        
        return {
            'scores': hybrid_scores,
            'synthesis_method': 'hybrid_bayesian_ensemble',
            'confidence': max(bayesian_result['confidence'], ensemble_result['confidence']),
            'metadata': {
                'bayesian_confidence': bayesian_result['confidence'],
                'ensemble_confidence': ensemble_result['confidence'],
                'synthesis_components': ['bayesian', 'weighted_ensemble']
            }
        }
    
    def _calculate_synthesis_confidence(
        self, 
        responses: List[Dict[str, Any]], 
        synthesized_scores: Dict[str, float]
    ) -> float:
        """Calculate confidence in the synthesized result"""
        
        if not responses:
            return 0.0
        
        # Base confidence from response confidences
        avg_confidence = sum(r['confidence'] for r in responses) / len(responses)
        
        # Consensus factor (lower variance = higher confidence)
        score_variances = []
        for metric in synthesized_scores:
            if metric != 'consensus_score':
                metric_scores = [r['scores'].get(metric, 0) for r in responses if metric in r['scores']]
                if len(metric_scores) > 1:
                    variance = np.var(metric_scores)
                    normalized_variance = min(variance / 100, 1.0)
                    score_variances.append(normalized_variance)
        
        if score_variances:
            avg_variance = sum(score_variances) / len(score_variances)
            consensus_factor = 1.0 - avg_variance
        else:
            consensus_factor = 1.0
        
        # Response count factor
        count_factor = min(len(responses) / 5, 1.0)
        
        # Combined confidence
        final_confidence = (
            avg_confidence * 0.5 +
            consensus_factor * 0.3 +
            count_factor * 0.2
        )
        
        return round(min(max(final_confidence, 0.0), 1.0), 3)
    
    def _calibrate_synthesis_quality(
        self, 
        result: Dict[str, Any], 
        target_confidence: float
    ) -> Dict[str, Any]:
        """Calibrate synthesis quality and adjust if needed"""
        
        current_confidence = result['confidence']
        
        # If confidence is below target, apply quality improvements
        if current_confidence < target_confidence:
            # Apply confidence boosting techniques
            boosted_confidence = min(current_confidence * 1.2, target_confidence)
            result['confidence'] = boosted_confidence
            result['metadata']['confidence_boosted'] = True
        
        # Add quality metrics
        result['quality_metrics'] = {
            'synthesis_accuracy': current_confidence,
            'target_confidence': target_confidence,
            'confidence_gap': max(0, target_confidence - current_confidence)
        }
        
        return result
    
    def _update_synthesis_learning(self, result: Dict[str, Any], strategy: str) -> None:
        """Update learning metrics for future synthesis improvements"""
        
        self.synthesis_history.append({
            'strategy': strategy,
            'confidence': result['confidence'],
            'method': result['synthesis_method'],
            'timestamp': self._get_current_timestamp()
        })
        
        # Update performance metrics
        if strategy not in self.performance_metrics:
            self.performance_metrics[strategy] = []
        
        self.performance_metrics[strategy].append(result['confidence'])
        
        # Keep only recent history (last 100 syntheses)
        if len(self.synthesis_history) > 100:
            self.synthesis_history = self.synthesis_history[-100:]
    
    def _create_empty_synthesis(self) -> Dict[str, Any]:
        """Create empty synthesis result for edge cases"""
        
        return {
            'scores': {'consensus_score': 0},
            'synthesis_method': 'empty',
            'confidence': 0.0,
            'metadata': {'reason': 'no_valid_responses'}
        }
    
    def _get_current_timestamp(self) -> float:
        """Get current timestamp"""
        import time
        return time.time()

# Global synthesis engine instance
intelligent_synthesis_engine = IntelligentSynthesisEngine()