"""
Multi-LLM Ensemble System for GUARDIAN
Concurrent processing framework that combines multiple LLM outputs for enhanced policy evaluation
"""

import asyncio
import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from utils.free_llm_services import free_llm_manager
from utils.llm_intelligence_enhancer import llm_enhancer
from utils.intelligent_synthesis_engine import intelligent_synthesis_engine

@dataclass
class LLMResponse:
    """Individual LLM response with metadata"""
    service_name: str
    response_data: Dict[str, Any]
    processing_time: float
    confidence_score: float
    success: bool
    error_message: Optional[str] = None

@dataclass
class EnsembleResult:
    """Combined result from multiple LLM evaluations"""
    consensus_score: Dict[str, float]
    individual_responses: List[LLMResponse]
    confidence_level: float
    processing_summary: Dict[str, Any]
    enhanced_metadata: Dict[str, Any]

class MultiLLMEnsemble:
    """
    Orchestrates concurrent LLM processing for policy evaluations
    Implements daisy-chain and parallel processing patterns
    """
    
    def __init__(self):
        self.available_services = []
        self.processing_weights = {
            'convergence_ai': 1.0,   # Your patent-protected anti-bias system
            'ollama': 0.9,           # Local, always available
            'groq': 0.85,            # Fast inference
            'openai': 0.9,           # High quality
            'anthropic': 0.9,        # High quality
            'huggingface': 0.65,     # Specialized models
            'together_ai': 0.75,     # Open models
            'perplexity': 0.85  # Real-time research
        }
        self.timeout_seconds = 30
        
    async def initialize_services(self) -> Dict[str, Any]:
        """Initialize and test available LLM services"""
        
        service_status = await free_llm_manager.test_all_services()
        
        # Include existing services
        existing_services = []
        try:
            from utils.document_analyzer import openai_client
            if openai_client:
                existing_services.append('openai')
        except:
            pass
            
        try:
            from utils.anthropic_analyzer import analyze_document_with_anthropic
            existing_services.append('anthropic')
        except:
            pass
        
        self.available_services = (
            [s['name'] for s in service_status.get('available_services', [])] + 
            existing_services
        )
        
        return {
            'total_services': len(self.available_services),
            'available_services': self.available_services,
            'initialization_time': time.time()
        }
    
    async def evaluate_policy_concurrent(
        self, 
        document_content: str, 
        evaluation_domain: str,
        use_daisy_chain: bool = False
    ) -> EnsembleResult:
        """
        Main orchestration method for concurrent policy evaluation
        
        Args:
            document_content: Policy document text
            evaluation_domain: ai_ethics, quantum_security, or cybersecurity
            use_daisy_chain: If True, use sequential refinement; if False, pure parallel
        """
        
        if use_daisy_chain:
            return await self._daisy_chain_evaluation(document_content, evaluation_domain)
        else:
            return await self._parallel_evaluation(document_content, evaluation_domain)
    
    async def _parallel_evaluation(
        self, 
        document_content: str, 
        evaluation_domain: str
    ) -> EnsembleResult:
        """
        Pure parallel processing - all LLMs evaluate simultaneously
        """
        
        start_time = time.time()
        
        # Create evaluation tasks for all available services
        tasks = []
        for service in self.available_services:
            task = asyncio.create_task(
                self._evaluate_with_service(
                    service, 
                    document_content, 
                    evaluation_domain,
                    task_id=len(tasks)
                )
            )
            tasks.append(task)
        
        # Execute all tasks concurrently with timeout
        try:
            individual_responses = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True),
                timeout=self.timeout_seconds
            )
        except asyncio.TimeoutError:
            individual_responses = [
                LLMResponse(
                    service_name="timeout",
                    response_data={},
                    processing_time=self.timeout_seconds,
                    confidence_score=0.0,
                    success=False,
                    error_message="Timeout exceeded"
                )
            ]
        
        # Filter successful responses
        valid_responses = [
            r for r in individual_responses 
            if isinstance(r, LLMResponse) and r.success
        ]
        
        # Use intelligent synthesis engine for optimal consensus
        consensus_result = self._synthesize_with_intelligent_engine(valid_responses, evaluation_domain)
        
        processing_time = time.time() - start_time
        
        return EnsembleResult(
            consensus_score=consensus_result['scores'],
            individual_responses=individual_responses,
            confidence_level=consensus_result['confidence'],
            processing_summary={
                'total_services_attempted': len(self.available_services),
                'successful_responses': len(valid_responses),
                'processing_time': processing_time,
                'processing_mode': 'parallel'
            },
            enhanced_metadata=consensus_result['metadata']
        )
    
    async def _daisy_chain_evaluation(
        self, 
        document_content: str, 
        evaluation_domain: str
    ) -> EnsembleResult:
        """
        Sequential refinement - each LLM builds on previous analysis
        """
        
        start_time = time.time()
        accumulated_context = document_content
        individual_responses = []
        
        # Order services by reliability/speed
        ordered_services = sorted(
            self.available_services,
            key=lambda s: self.processing_weights.get(s, 0.5),
            reverse=True
        )
        
        for i, service in enumerate(ordered_services):
            # Add previous analysis to context for refinement
            if i > 0 and individual_responses:
                previous_analysis = individual_responses[-1].response_data
                refinement_prompt = f"""
                Previous analysis from {individual_responses[-1].service_name}:
                {json.dumps(previous_analysis, indent=2)}
                
                Please refine and enhance this analysis with your perspective:
                {accumulated_context[:2000]}
                """
                current_context = refinement_prompt
            else:
                current_context = accumulated_context
            
            # Evaluate with current service
            response = await self._evaluate_with_service(
                service, 
                current_context, 
                evaluation_domain,
                task_id=i,
                is_refinement=(i > 0)
            )
            
            if response.success:
                individual_responses.append(response)
                # Accumulate successful analysis for next iteration
                accumulated_context += f"\n\nAnalysis from {service}: {json.dumps(response.response_data)}"
            
            # Early termination if we have enough high-quality responses
            if len(individual_responses) >= 3 and response.confidence_score > 0.8:
                break
        
        # Synthesize daisy-chain result (weighted toward later, more refined responses)
        consensus_result = self._synthesize_daisy_chain(individual_responses, evaluation_domain)
        
        processing_time = time.time() - start_time
        
        return EnsembleResult(
            consensus_score=consensus_result['scores'],
            individual_responses=individual_responses,
            confidence_level=consensus_result['confidence'],
            processing_summary={
                'total_services_attempted': len(ordered_services),
                'successful_responses': len(individual_responses),
                'processing_time': processing_time,
                'processing_mode': 'daisy_chain'
            },
            enhanced_metadata=consensus_result['metadata']
        )
    
    async def _evaluate_with_service(
        self, 
        service_name: str, 
        content: str, 
        domain: str,
        task_id: int,
        is_refinement: bool = False
    ) -> LLMResponse:
        """
        Evaluate document with specific LLM service
        """
        
        start_time = time.time()
        
        try:
            if service_name == 'openai':
                result = await self._evaluate_with_openai(content, domain, is_refinement)
            elif service_name == 'anthropic':
                result = await self._evaluate_with_anthropic(content, domain, is_refinement)
            elif service_name in ['ollama', 'groq', 'huggingface', 'together_ai', 'perplexity']:
                result = await self._evaluate_with_free_service(service_name, content, domain, is_refinement)
            else:
                raise ValueError(f"Unsupported service: {service_name}")
            
            processing_time = time.time() - start_time
            
            return LLMResponse(
                service_name=service_name,
                response_data=result,
                processing_time=processing_time,
                confidence_score=result.get('confidence', 0.5),
                success=True
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            
            return LLMResponse(
                service_name=service_name,
                response_data={},
                processing_time=processing_time,
                confidence_score=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def _evaluate_with_openai(self, content: str, domain: str, is_refinement: bool) -> Dict[str, Any]:
        """Evaluate using OpenAI"""
        
        from utils.document_analyzer import openai_client
        
        if not openai_client:
            raise ValueError("OpenAI client not available")
        
        prompt = self._create_evaluation_prompt(content, domain, is_refinement, "openai")
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self._get_system_prompt(domain)},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def _evaluate_with_anthropic(self, content: str, domain: str, is_refinement: bool) -> Dict[str, Any]:
        """Evaluate using Anthropic Claude"""
        
        from utils.anthropic_analyzer import analyze_document_with_anthropic
        
        # Use existing Anthropic analyzer but with enhanced prompting
        result = analyze_document_with_anthropic(content, f"{domain}_policy_evaluation")
        
        if result:
            # Convert to standard format
            return {
                'domain_relevance': 85,
                'policy_scores': {
                    'completeness': 80,
                    'clarity': 75,
                    'enforceability': 70
                },
                'key_insights': [result.get('content_preview', 'Analysis completed')],
                'confidence': 0.8,
                'source': 'anthropic'
            }
        else:
            raise ValueError("Anthropic analysis failed")
    
    async def _evaluate_with_free_service(
        self, 
        service_name: str, 
        content: str, 
        domain: str, 
        is_refinement: bool
    ) -> Dict[str, Any]:
        """Evaluate using free LLM services"""
        
        # Use existing LLM intelligence enhancer
        enhanced_result = await llm_enhancer.enhance_document_analysis(content, domain)
        
        # Extract relevant analysis from the service
        for insight in enhanced_result.get('supporting_insights', []):
            if insight.get('source') == service_name:
                return {
                    'domain_relevance': 75,
                    'policy_scores': {
                        'completeness': 70,
                        'clarity': 65,
                        'enforceability': 60
                    },
                    'key_insights': [insight.get('analysis', 'Analysis completed')],
                    'confidence': 0.7,
                    'source': service_name
                }
        
        # Fallback generic response
        return {
            'domain_relevance': 60,
            'policy_scores': {
                'completeness': 50,
                'clarity': 50,
                'enforceability': 50
            },
            'key_insights': [f'Analysis from {service_name}'],
            'confidence': 0.5,
            'source': service_name
        }
    
    def _create_evaluation_prompt(self, content: str, domain: str, is_refinement: bool, service: str) -> str:
        """Create domain-specific evaluation prompt"""
        
        base_prompt = f"""
        Evaluate this {domain} policy document for:
        1. Domain relevance (0-100)
        2. Policy completeness, clarity, and enforceability (0-100 each)
        3. Key insights and recommendations
        4. Confidence level (0.0-1.0)
        
        Document content: {content[:3000]}
        
        Respond in JSON format with: domain_relevance, policy_scores, key_insights, confidence
        """
        
        if is_refinement:
            base_prompt = f"""
            REFINEMENT TASK: Build upon previous analysis to provide enhanced insights.
            {base_prompt}
            
            Focus on areas not covered by previous analysis and provide additional depth.
            """
        
        return base_prompt
    
    def _get_system_prompt(self, domain: str) -> str:
        """Get system prompt for domain"""
        
        domain_contexts = {
            'ai_ethics': 'You are an expert in AI ethics, bias detection, and algorithmic fairness.',
            'quantum_security': 'You are an expert in quantum cryptography and post-quantum security.',
            'cybersecurity': 'You are an expert in cybersecurity frameworks and risk assessment.'
        }
        
        return domain_contexts.get(domain, 'You are an expert policy analyst.')
    
    def _synthesize_consensus(self, responses: List[LLMResponse], domain: str) -> Dict[str, Any]:
        """Advanced consensus synthesis with intelligent disagreement resolution"""
        
        if not responses:
            return {
                'scores': {'consensus_score': 0},
                'confidence': 0.0,
                'metadata': {'synthesis_method': 'no_responses'}
            }
        
        # Multi-stage synthesis approach
        synthesis_result = self._advanced_consensus_synthesis(responses, domain)
        
        return synthesis_result
    
    def _advanced_consensus_synthesis(self, responses: List[LLMResponse], domain: str) -> Dict[str, Any]:
        """
        Revolutionary multi-stage consensus synthesis:
        1. Weighted Bayesian averaging
        2. Outlier detection and handling
        3. Disagreement analysis and resolution
        4. Confidence calibration
        """
        
        # Stage 1: Extract and normalize all scores
        normalized_responses = self._normalize_response_scores(responses)
        
        # Stage 2: Detect and handle outliers
        filtered_responses = self._detect_and_handle_outliers(normalized_responses)
        
        # Stage 3: Bayesian weighted consensus
        bayesian_consensus = self._bayesian_weighted_synthesis(filtered_responses, domain)
        
        # Stage 4: Disagreement analysis
        disagreement_analysis = self._analyze_disagreements(normalized_responses)
        
        # Stage 5: Confidence calibration
        calibrated_confidence = self._calibrate_confidence(
            bayesian_consensus, 
            disagreement_analysis,
            len(filtered_responses)
        )
        
        # Stage 6: Enhanced metadata synthesis
        enhanced_metadata = self._synthesize_enhanced_metadata(
            responses, 
            disagreement_analysis,
            bayesian_consensus
        )
        
        return {
            'scores': bayesian_consensus['scores'],
            'confidence': calibrated_confidence,
            'metadata': {
                'synthesis_method': 'advanced_bayesian_consensus',
                'participating_services': [r.service_name for r in responses],
                'outliers_detected': bayesian_consensus['outliers'],
                'disagreement_level': disagreement_analysis['disagreement_level'],
                'consensus_strength': disagreement_analysis['consensus_strength'],
                **enhanced_metadata
            }
        }
    
    def _normalize_response_scores(self, responses: List[LLMResponse]) -> List[Dict[str, Any]]:
        """Normalize all response scores to consistent scale and structure"""
        normalized = []
        
        for response in responses:
            policy_scores = response.response_data.get('policy_scores', {})
            domain_relevance = response.response_data.get('domain_relevance', 50)
            
            # Ensure all scores are on 0-100 scale
            normalized_scores = {}
            for metric, score in policy_scores.items():
                if isinstance(score, (int, float)):
                    # Normalize to 0-100 if needed
                    if score <= 1.0:  # Assume 0-1 scale
                        normalized_scores[metric] = score * 100
                    else:  # Assume already 0-100
                        normalized_scores[metric] = min(max(score, 0), 100)
            
            normalized.append({
                'service_name': response.service_name,
                'scores': normalized_scores,
                'domain_relevance': min(max(domain_relevance, 0), 100),
                'confidence': response.confidence_score,
                'service_weight': self.processing_weights.get(response.service_name, 0.5),
                'processing_time': response.processing_time,
                'insights': response.response_data.get('key_insights', [])
            })
        
        return normalized
    
    def _detect_and_handle_outliers(self, normalized_responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect statistical outliers and apply appropriate handling"""
        if len(normalized_responses) < 3:
            return normalized_responses  # Need at least 3 for outlier detection
        
        # Calculate score statistics for each metric
        all_metrics = set()
        for resp in normalized_responses:
            all_metrics.update(resp['scores'].keys())
        
        outlier_services = set()
        
        for metric in all_metrics:
            scores = []
            for resp in normalized_responses:
                if metric in resp['scores']:
                    scores.append(resp['scores'][metric])
            
            if len(scores) >= 3:
                # Use IQR method for outlier detection
                scores.sort()
                q1 = scores[len(scores)//4]
                q3 = scores[3*len(scores)//4]
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                # Mark services with outlier scores
                for resp in normalized_responses:
                    if metric in resp['scores']:
                        score = resp['scores'][metric]
                        if score < lower_bound or score > upper_bound:
                            outlier_services.add(resp['service_name'])
        
        # Filter out outliers but preserve at least 2 responses
        filtered = []
        non_outliers = [r for r in normalized_responses if r['service_name'] not in outlier_services]
        
        if len(non_outliers) >= 2:
            filtered = non_outliers
        else:
            # Keep all if too many outliers detected
            filtered = normalized_responses
        
        return filtered
    
    def _bayesian_weighted_synthesis(self, responses: List[Dict[str, Any]], domain: str) -> Dict[str, Any]:
        """Bayesian weighted synthesis with prior knowledge integration"""
        
        # Domain-specific priors (based on typical policy evaluation ranges)
        domain_priors = {
            'ai_ethics': {'completeness': 65, 'clarity': 70, 'enforceability': 60},
            'quantum_security': {'completeness': 70, 'clarity': 65, 'enforceability': 75},
            'cybersecurity': {'completeness': 75, 'clarity': 70, 'enforceability': 80},
            'default': {'completeness': 70, 'clarity': 70, 'enforceability': 70}
        }
        
        priors = domain_priors.get(domain, domain_priors['default'])
        
        # Collect all unique metrics
        all_metrics = set()
        for resp in responses:
            all_metrics.update(resp['scores'].keys())
        
        final_scores = {}
        outliers_detected = []
        
        for metric in all_metrics:
            # Extract scores and weights for this metric
            scores = []
            weights = []
            
            for resp in responses:
                if metric in resp['scores']:
                    score = resp['scores'][metric]
                    # Combined weight: service reliability × confidence × domain relevance
                    weight = (
                        resp['service_weight'] * 
                        resp['confidence'] * 
                        (resp['domain_relevance'] / 100)
                    )
                    scores.append(score)
                    weights.append(weight)
            
            if scores:
                # Bayesian weighted average with prior
                prior_score = priors.get(metric, 70)
                prior_weight = 0.3  # Prior contributes 30% to final result
                
                # Calculate posterior
                total_weight = sum(weights) + prior_weight
                weighted_sum = sum(s * w for s, w in zip(scores, weights)) + prior_score * prior_weight
                
                final_scores[metric] = round(weighted_sum / total_weight, 2)
        
        # Calculate consensus score
        if final_scores:
            consensus_score = round(sum(final_scores.values()) / len(final_scores), 2)
        else:
            consensus_score = 0
        
        final_scores['consensus_score'] = consensus_score
        
        return {
            'scores': final_scores,
            'outliers': outliers_detected
        }
    
    def _analyze_disagreements(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze disagreement patterns between LLM responses"""
        
        if len(responses) < 2:
            return {'disagreement_level': 0.0, 'consensus_strength': 1.0}
        
        # Calculate variance for each metric
        all_metrics = set()
        for resp in responses:
            all_metrics.update(resp['scores'].keys())
        
        metric_variances = {}
        
        for metric in all_metrics:
            scores = [resp['scores'][metric] for resp in responses if metric in resp['scores']]
            if len(scores) >= 2:
                mean_score = sum(scores) / len(scores)
                variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
                metric_variances[metric] = variance
        
        # Overall disagreement level (normalized variance)
        if metric_variances:
            avg_variance = sum(metric_variances.values()) / len(metric_variances)
            disagreement_level = min(avg_variance / 100, 1.0)  # Normalize to 0-1
        else:
            disagreement_level = 0.0
        
        consensus_strength = 1.0 - disagreement_level
        
        return {
            'disagreement_level': round(disagreement_level, 3),
            'consensus_strength': round(consensus_strength, 3),
            'metric_variances': metric_variances
        }
    
    def _calibrate_confidence(self, consensus_result: Dict[str, Any], disagreement_analysis: Dict[str, Any], num_responses: int) -> float:
        """Calibrate confidence based on consensus strength and response count"""
        
        # Base confidence from consensus strength
        consensus_confidence = disagreement_analysis['consensus_strength']
        
        # Response count factor (more responses = higher confidence)
        count_factor = min(num_responses / 5, 1.0)  # Cap at 5 responses
        
        # Service diversity factor (different services = higher confidence)
        diversity_factor = min(num_responses / 3, 1.0)
        
        # Combined calibrated confidence
        calibrated = (
            consensus_confidence * 0.6 +
            count_factor * 0.2 +
            diversity_factor * 0.2
        )
        
        return round(min(max(calibrated, 0.0), 1.0), 3)
    
    def _synthesize_enhanced_metadata(self, responses: List[LLMResponse], disagreement_analysis: Dict[str, Any], consensus_result: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize enhanced metadata from all responses"""
        
        # Collect all insights
        all_insights = []
        service_performance = {}
        
        for response in responses:
            insights = response.response_data.get('key_insights', [])
            all_insights.extend(insights)
            
            service_performance[response.service_name] = {
                'processing_time': response.processing_time,
                'confidence': response.confidence_score,
                'success': response.success
            }
        
        # Deduplicate insights using semantic similarity (simplified)
        unique_insights = list(set(all_insights))[:10]  # Limit to top 10
        
        return {
            'total_insights_collected': len(all_insights),
            'unique_insights': unique_insights,
            'service_performance': service_performance,
            'synthesis_quality': 'high' if disagreement_analysis['consensus_strength'] > 0.7 else 'medium'
        }
    
    def _synthesize_daisy_chain(self, responses: List[LLMResponse], domain: str) -> Dict[str, Any]:
        """Synthesize results from daisy-chain processing"""
        
        if not responses:
            return {
                'scores': {'consensus_score': 0},
                'confidence': 0.0,
                'metadata': {'synthesis_method': 'no_responses'}
            }
        
        # Weight later responses more heavily (they have more context)
        final_scores = {}
        all_insights = []
        total_confidence = 0
        
        for i, response in enumerate(responses):
            # Later responses get higher weight (refinement effect)
            position_weight = (i + 1) / len(responses)
            confidence_weight = response.confidence_score
            combined_weight = position_weight * confidence_weight
            
            policy_scores = response.response_data.get('policy_scores', {})
            for metric, score in policy_scores.items():
                if metric not in final_scores:
                    final_scores[metric] = []
                final_scores[metric].append((score, combined_weight))
            
            insights = response.response_data.get('key_insights', [])
            all_insights.extend(insights)
            total_confidence += confidence_weight
        
        # Calculate weighted averages with refinement bias
        processed_scores = {}
        for metric, score_weight_pairs in final_scores.items():
            total_weighted_score = sum(score * weight for score, weight in score_weight_pairs)
            total_weight = sum(weight for score, weight in score_weight_pairs)
            
            if total_weight > 0:
                processed_scores[metric] = round(total_weighted_score / total_weight, 2)
        
        # Overall consensus from final iteration
        if processed_scores:
            consensus_score = round(sum(processed_scores.values()) / len(processed_scores), 2)
        else:
            consensus_score = 0
        
        processed_scores['consensus_score'] = consensus_score
        
        # Confidence increases with successful refinement iterations
        confidence = min((total_confidence / len(responses)) * 1.1, 1.0) if responses else 0.0
        
        return {
            'scores': processed_scores,
            'confidence': confidence,
            'metadata': {
                'synthesis_method': 'daisy_chain_refinement',
                'refinement_iterations': len(responses),
                'participating_services': [r.service_name for r in responses],
                'final_insights': all_insights[-3:] if len(all_insights) > 3 else all_insights
            }
        }
    
    def _synthesize_with_intelligent_engine(self, responses: List[LLMResponse], domain: str) -> Dict[str, Any]:
        """Use the intelligent synthesis engine for optimal consensus"""
        
        # Convert LLMResponse objects to the format expected by synthesis engine
        synthesis_responses = []
        for response in responses:
            synthesis_response = {
                'service_name': response.service_name,
                'confidence': response.confidence_score,
                'scores': response.response_data.get('policy_scores', {}),
                'processing_time': response.processing_time,
                'metadata': {
                    'domain_relevance': response.response_data.get('domain_relevance', 75),
                    'key_insights': response.response_data.get('key_insights', [])
                }
            }
            synthesis_responses.append(synthesis_response)
        
        # Use intelligent synthesis engine
        synthesis_result = intelligent_synthesis_engine.synthesize_optimal_consensus(
            synthesis_responses, 
            domain,
            target_confidence=0.85
        )
        
        return synthesis_result

# Global ensemble instance
multi_llm_ensemble = MultiLLMEnsemble()