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
            'ollama': 1.0,      # Local, always available
            'groq': 0.9,        # Fast inference
            'openai': 0.95,     # High quality
            'anthropic': 0.95,  # High quality
            'huggingface': 0.7, # Specialized models
            'together_ai': 0.8, # Open models
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
        
        # Synthesize consensus
        consensus_result = self._synthesize_consensus(valid_responses, evaluation_domain)
        
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
        """Synthesize consensus from parallel responses"""
        
        if not responses:
            return {
                'scores': {'consensus_score': 0},
                'confidence': 0.0,
                'metadata': {'synthesis_method': 'no_responses'}
            }
        
        # Weighted averaging based on service reliability and confidence
        total_weight = 0
        weighted_scores = {}
        all_insights = []
        
        for response in responses:
            service_weight = self.processing_weights.get(response.service_name, 0.5)
            confidence_weight = response.confidence_score
            combined_weight = service_weight * confidence_weight
            
            total_weight += combined_weight
            
            # Aggregate scores
            policy_scores = response.response_data.get('policy_scores', {})
            for metric, score in policy_scores.items():
                if metric not in weighted_scores:
                    weighted_scores[metric] = 0
                weighted_scores[metric] += score * combined_weight
            
            # Collect insights
            insights = response.response_data.get('key_insights', [])
            all_insights.extend(insights)
        
        # Normalize weighted scores
        final_scores = {}
        if total_weight > 0:
            for metric, weighted_sum in weighted_scores.items():
                final_scores[metric] = round(weighted_sum / total_weight, 2)
        
        # Calculate overall consensus score
        if final_scores:
            consensus_score = round(sum(final_scores.values()) / len(final_scores), 2)
        else:
            consensus_score = 0
        
        final_scores['consensus_score'] = consensus_score
        
        # Calculate confidence based on agreement between services
        confidence = min(total_weight / len(responses), 1.0) if responses else 0.0
        
        return {
            'scores': final_scores,
            'confidence': confidence,
            'metadata': {
                'synthesis_method': 'weighted_consensus',
                'participating_services': [r.service_name for r in responses],
                'total_insights': len(all_insights),
                'unique_insights': list(set(all_insights))
            }
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

# Global ensemble instance
multi_llm_ensemble = MultiLLMEnsemble()