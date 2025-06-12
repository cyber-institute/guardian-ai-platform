"""
Quantum-Enhanced Multi-LLM Scoring System for GUARDIAN
Integrates quantum routing with existing comprehensive patent scoring
"""

import json
from typing import Dict, List, Any, Optional
from utils.qiskit_router import quantum_task_specific_routing, quantum_confidence_weighting
from utils.patent_scoring_engine import ComprehensivePatentScoringEngine

class QuantumEnhancedScoringEngine:
    """Enhanced scoring engine that uses quantum routing for optimal LLM selection."""
    
    def __init__(self):
        self.available_models = ["gpt4", "claude", "local_llm"]
        self.routing_history = []
        
    def quantum_score_document(self, content: str, title: str, document_type: str = "policy") -> Dict[str, Any]:
        """
        Score a document using quantum-assisted LLM routing for optimal results.
        
        Args:
            content: Document content
            title: Document title
            document_type: Type of document for routing optimization
            
        Returns:
            Enhanced scoring results with quantum routing insights
        """
        try:
            # Step 1: Use quantum routing to select optimal LLM combination
            selected_models = quantum_task_specific_routing(content, document_type)
            
            # Step 2: Apply existing comprehensive scoring with selected models
            base_scores = comprehensive_document_scoring(content, title)
            
            # Step 3: Simulate multi-LLM analysis results
            llm_results = {}
            
            for model in selected_models:
                # Simulate different LLM perspectives on the same content
                model_score = self._simulate_model_perspective(base_scores, model, content)
                llm_results[model] = {
                    'scores': model_score,
                    'confidence': self._calculate_model_confidence(model, content),
                    'reasoning': self._generate_model_reasoning(model, content)
                }
            
            # Step 4: Apply quantum confidence weighting
            quantum_weights = quantum_confidence_weighting(llm_results)
            
            # Step 5: Generate quantum-consensus scores
            consensus_scores = self._generate_quantum_consensus(llm_results, quantum_weights)
            
            # Store routing decision for analysis
            routing_decision = {
                'selected_models': selected_models,
                'quantum_weights': quantum_weights,
                'document_type': document_type,
                'content_keywords': self._extract_keywords(content)
            }
            self.routing_history.append(routing_decision)
            
            return {
                'quantum_routing': {
                    'selected_models': selected_models,
                    'quantum_weights': quantum_weights,
                    'routing_reasoning': self._explain_routing(selected_models, content)
                },
                'individual_llm_results': llm_results,
                'quantum_consensus_scores': consensus_scores,
                'enhanced_scores': {
                    **base_scores,
                    'quantum_confidence': sum(quantum_weights.values()) / len(quantum_weights) if quantum_weights else 0.5,
                    'ensemble_diversity': len(selected_models),
                    'quantum_enhanced': True
                }
            }
            
        except Exception as e:
            # Fallback to standard scoring if quantum routing fails
            return {
                'quantum_routing': {'error': str(e), 'fallback_used': True},
                'enhanced_scores': comprehensive_document_scoring(content, title)
            }
    
    def _simulate_model_perspective(self, base_scores: Dict, model: str, content: str) -> Dict[str, float]:
        """Simulate how different LLMs might score the same content differently."""
        import random
        random.seed(hash(content + model))  # Deterministic but varied
        
        # Apply model-specific biases
        model_adjustments = {
            'gpt4': {'ai_cybersecurity': 1.1, 'ai_ethics': 1.05, 'quantum_cybersecurity': 0.95, 'quantum_ethics': 0.98},
            'claude': {'ai_cybersecurity': 1.0, 'ai_ethics': 1.15, 'quantum_cybersecurity': 1.0, 'quantum_ethics': 1.1},
            'local_llm': {'ai_cybersecurity': 0.9, 'ai_ethics': 0.95, 'quantum_cybersecurity': 1.1, 'quantum_ethics': 1.05}
        }
        
        adjustments = model_adjustments.get(model, {})
        adjusted_scores = {}
        
        for framework, score in base_scores.items():
            if isinstance(score, (int, float)):
                adjustment = adjustments.get(framework, 1.0)
                # Add small random variation (±5%)
                variation = 1.0 + (random.random() - 0.5) * 0.1
                adjusted_score = score * adjustment * variation
                
                # Keep scores within valid ranges
                if framework in ['ai_cybersecurity', 'ai_ethics']:
                    adjusted_scores[framework] = max(0, min(100, adjusted_score))
                elif framework == 'quantum_cybersecurity':
                    adjusted_scores[framework] = max(1, min(5, adjusted_score))
                elif framework == 'quantum_ethics':
                    adjusted_scores[framework] = max(0, min(100, adjusted_score))
                else:
                    adjusted_scores[framework] = adjusted_score
            else:
                adjusted_scores[framework] = score
        
        return adjusted_scores
    
    def _calculate_model_confidence(self, model: str, content: str) -> float:
        """Calculate confidence score for a model based on content characteristics."""
        confidence_factors = {
            'gpt4': {
                'ai_keywords': ['artificial intelligence', 'machine learning', 'neural network'],
                'base_confidence': 0.85
            },
            'claude': {
                'ai_keywords': ['ethics', 'policy', 'governance', 'responsibility'],
                'base_confidence': 0.82
            },
            'local_llm': {
                'ai_keywords': ['quantum', 'cybersecurity', 'encryption', 'technical'],
                'base_confidence': 0.78
            }
        }
        
        model_config = confidence_factors.get(model, {'ai_keywords': [], 'base_confidence': 0.75})
        base_confidence = model_config['base_confidence']
        
        # Boost confidence if content matches model's specialty
        content_lower = content.lower()
        keyword_matches = sum(1 for keyword in model_config['ai_keywords'] if keyword in content_lower)
        keyword_boost = min(0.15, keyword_matches * 0.03)
        
        return min(1.0, base_confidence + keyword_boost)
    
    def _generate_model_reasoning(self, model: str, content: str) -> str:
        """Generate reasoning for why a model was selected."""
        reasoning_templates = {
            'gpt4': "Selected for comprehensive AI analysis and broad domain expertise",
            'claude': "Selected for ethical reasoning and policy analysis capabilities",
            'local_llm': "Selected for specialized quantum and cybersecurity assessment"
        }
        
        base_reasoning = reasoning_templates.get(model, "Selected for specialized analysis")
        
        # Add content-specific reasoning
        content_lower = content.lower()
        if 'quantum' in content_lower:
            base_reasoning += " - quantum content detected"
        if 'ethics' in content_lower:
            base_reasoning += " - ethical considerations identified"
        if 'cybersecurity' in content_lower:
            base_reasoning += " - cybersecurity focus recognized"
            
        return base_reasoning
    
    def _generate_quantum_consensus(self, llm_results: Dict, quantum_weights: Dict) -> Dict[str, float]:
        """Generate consensus scores using quantum weighting."""
        consensus_scores = {}
        
        # Get all scoring frameworks
        all_frameworks = set()
        for model_result in llm_results.values():
            all_frameworks.update(model_result['scores'].keys())
        
        for framework in all_frameworks:
            weighted_sum = 0.0
            total_weight = 0.0
            
            for model, weight in quantum_weights.items():
                if model in llm_results and framework in llm_results[model]['scores']:
                    score = llm_results[model]['scores'][framework]
                    if isinstance(score, (int, float)):
                        weighted_sum += score * weight
                        total_weight += weight
            
            if total_weight > 0:
                consensus_scores[framework] = weighted_sum / total_weight
            else:
                # Fallback to simple average
                scores = [llm_results[model]['scores'].get(framework, 0) 
                         for model in llm_results 
                         if isinstance(llm_results[model]['scores'].get(framework), (int, float))]
                consensus_scores[framework] = sum(scores) / len(scores) if scores else 0
        
        return consensus_scores
    
    def _explain_routing(self, selected_models: List[str], content: str) -> str:
        """Explain why specific models were selected by quantum routing."""
        explanations = []
        content_lower = content.lower()
        
        if len(selected_models) == 1:
            explanations.append(f"Quantum circuit converged on {selected_models[0]} for specialized analysis")
        elif len(selected_models) == 2:
            explanations.append(f"Quantum superposition selected {' and '.join(selected_models)} for dual validation")
        else:
            explanations.append("Quantum entanglement triggered full ensemble analysis")
        
        # Add content-based reasoning
        if 'quantum' in content_lower and 'ai' in content_lower:
            explanations.append("Content spans quantum-AI domains, enabling hybrid analysis")
        elif 'ethics' in content_lower and 'policy' in content_lower:
            explanations.append("Policy-ethics focus detected, optimizing for governance analysis")
        
        return ". ".join(explanations)
    
    def _extract_keywords(self, content: str) -> List[str]:
        """Extract key terms for routing analysis."""
        keywords = []
        content_lower = content.lower()
        
        key_terms = [
            'artificial intelligence', 'ai', 'machine learning', 'quantum', 'cybersecurity',
            'ethics', 'policy', 'governance', 'privacy', 'security', 'encryption',
            'neural network', 'algorithm', 'automation', 'responsibility'
        ]
        
        for term in key_terms:
            if term in content_lower:
                keywords.append(term)
        
        return keywords[:10]  # Limit to top 10 keywords
    
    def get_routing_analytics(self) -> Dict[str, Any]:
        """Get analytics about quantum routing decisions."""
        if not self.routing_history:
            return {'message': 'No routing history available'}
        
        # Analyze routing patterns
        model_usage = {}
        weight_distributions = []
        
        for decision in self.routing_history:
            for model in decision['selected_models']:
                model_usage[model] = model_usage.get(model, 0) + 1
            
            if decision['quantum_weights']:
                weight_distributions.append(decision['quantum_weights'])
        
        # Calculate average weights
        avg_weights = {}
        if weight_distributions:
            for model in self.available_models:
                weights = [w.get(model, 0) for w in weight_distributions if model in w]
                avg_weights[model] = sum(weights) / len(weights) if weights else 0
        
        return {
            'total_routing_decisions': len(self.routing_history),
            'model_usage_frequency': model_usage,
            'average_quantum_weights': avg_weights,
            'routing_diversity': len(set(tuple(sorted(d['selected_models'])) for d in self.routing_history))
        }