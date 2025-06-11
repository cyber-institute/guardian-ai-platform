"""
LLM Intelligence Enhancement System for GUARDIAN
Integrates multiple AI APIs and knowledge sources to enhance GUARDIAN's understanding
of AI Ethics, Quantum Security, and Cybersecurity Best Practices
"""

import json
import os
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from openai import OpenAI
# Anthropic import made optional to prevent deployment issues
try:
    import anthropic
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

@dataclass
class KnowledgeSource:
    """Configuration for external knowledge sources"""
    name: str
    api_endpoint: str
    requires_auth: bool
    knowledge_domain: str
    priority: int

class LLMIntelligenceEnhancer:
    """
    Multi-LLM intelligence system that aggregates knowledge from various AI sources
    to enhance GUARDIAN's understanding of AI/Quantum ethics and security
    """
    
    def __init__(self):
        self.openai_client = self._init_openai()
        self.anthropic_client = self._init_anthropic()
        self.knowledge_sources = self._configure_knowledge_sources()
        self.knowledge_cache = {}
        
    def _init_openai(self) -> Optional[OpenAI]:
        """Initialize OpenAI client if available"""
        api_key = os.environ.get("OPENAI_API_KEY")
        return OpenAI(api_key=api_key) if api_key else None
    
    def _init_anthropic(self) -> Optional[Any]:
        """Initialize Anthropic client if available"""
        if not ANTHROPIC_AVAILABLE:
            return None
        try:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            return Anthropic(api_key=api_key) if api_key else None
        except:
            return None
    
    def _configure_knowledge_sources(self) -> List[KnowledgeSource]:
        """Configure external knowledge sources for AI/Quantum intelligence"""
        return [
            # Hugging Face Inference API (Free tier available)
            KnowledgeSource(
                name="huggingface_ethics",
                api_endpoint="https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                requires_auth=True,
                knowledge_domain="ai_ethics",
                priority=1
            ),
            
            # Ollama Local Models (Free, self-hosted)
            KnowledgeSource(
                name="ollama_local",
                api_endpoint="http://localhost:11434/api/generate",
                requires_auth=False,
                knowledge_domain="general_ai",
                priority=2
            ),
            
            # Groq API (Fast inference, free tier)
            KnowledgeSource(
                name="groq_fast",
                api_endpoint="https://api.groq.com/openai/v1/chat/completions",
                requires_auth=True,
                knowledge_domain="quantum_security",
                priority=3
            ),
            
            # Together AI (Various open models)
            KnowledgeSource(
                name="together_ai",
                api_endpoint="https://api.together.xyz/inference",
                requires_auth=True,
                knowledge_domain="cybersecurity",
                priority=4
            )
        ]
    
    async def enhance_document_analysis(self, content: str, domain: str) -> Dict[str, Any]:
        """
        Enhance document analysis using multiple LLM sources for domain-specific knowledge
        """
        
        # Primary analysis with available LLMs
        primary_analysis = await self._get_primary_analysis(content, domain)
        
        # Cross-reference with domain-specific knowledge sources
        domain_insights = await self._get_domain_insights(content, domain)
        
        # Synthesize enhanced analysis
        enhanced_analysis = self._synthesize_analysis(primary_analysis, domain_insights)
        
        return enhanced_analysis
    
    async def _get_primary_analysis(self, content: str, domain: str) -> Dict[str, Any]:
        """Get primary analysis from OpenAI/Anthropic"""
        
        prompt = self._create_domain_prompt(content, domain)
        
        # Try OpenAI first
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",  # Latest model
                    messages=[
                        {"role": "system", "content": self._get_system_prompt(domain)},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return json.loads(response.choices[0].message.content)
            except Exception as e:
                print(f"OpenAI analysis failed: {e}")
        
        # Fallback to Anthropic
        if self.anthropic_client:
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",  # Latest Claude model
                    max_tokens=2000,
                    messages=[
                        {"role": "user", "content": f"{self._get_system_prompt(domain)}\n\n{prompt}"}
                    ]
                )
                return {"analysis": response.content[0].text, "source": "anthropic"}
            except Exception as e:
                print(f"Anthropic analysis failed: {e}")
        
        return {"error": "No LLM available for primary analysis"}
    
    async def _get_domain_insights(self, content: str, domain: str) -> List[Dict[str, Any]]:
        """Get insights from domain-specific knowledge sources"""
        
        insights = []
        relevant_sources = [s for s in self.knowledge_sources if s.knowledge_domain == domain or s.knowledge_domain == "general_ai"]
        
        for source in sorted(relevant_sources, key=lambda x: x.priority):
            try:
                insight = await self._query_knowledge_source(source, content, domain)
                if insight:
                    insights.append(insight)
            except Exception as e:
                print(f"Failed to query {source.name}: {e}")
                continue
        
        return insights
    
    async def _query_knowledge_source(self, source: KnowledgeSource, content: str, domain: str) -> Optional[Dict[str, Any]]:
        """Query a specific knowledge source"""
        
        if source.name == "huggingface_ethics":
            return await self._query_huggingface(content, domain)
        elif source.name == "ollama_local":
            return await self._query_ollama(content, domain)
        elif source.name == "groq_fast":
            return await self._query_groq(content, domain)
        elif source.name == "together_ai":
            return await self._query_together_ai(content, domain)
        
        return None
    
    async def _query_huggingface(self, content: str, domain: str) -> Optional[Dict[str, Any]]:
        """Query Hugging Face Inference API for ethics-focused analysis"""
        
        hf_token = os.environ.get("HUGGINGFACE_API_TOKEN")
        if not hf_token:
            return None
        
        # Use a model specifically trained on ethics/safety
        model_endpoint = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        
        headers = {"Authorization": f"Bearer {hf_token}"}
        payload = {
            "inputs": f"Analyze this document for AI ethics implications: {content[:500]}",
            "parameters": {"max_length": 200}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(model_endpoint, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "source": "huggingface_ethics",
                            "analysis": result,
                            "domain": "ai_ethics"
                        }
        except Exception as e:
            print(f"Hugging Face query failed: {e}")
        
        return None
    
    async def _query_ollama(self, content: str, domain: str) -> Optional[Dict[str, Any]]:
        """Query local Ollama models if available"""
        
        payload = {
            "model": "llama2",  # Can be configured
            "prompt": f"Analyze this {domain} document and provide insights: {content[:500]}",
            "stream": False
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost:11434/api/generate", json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "source": "ollama_local",
                            "analysis": result.get("response", ""),
                            "domain": domain
                        }
        except Exception:
            # Ollama not available, skip silently
            pass
        
        return None
    
    async def _query_groq(self, content: str, domain: str) -> Optional[Dict[str, Any]]:
        """Query Groq API for fast inference"""
        
        groq_key = os.environ.get("GROQ_API_KEY")
        if not groq_key:
            return None
        
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mixtral-8x7b-32768",  # Fast Groq model
            "messages": [
                {
                    "role": "user",
                    "content": f"Analyze this {domain} document for security and compliance insights: {content[:1000]}"
                }
            ],
            "max_tokens": 500
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.groq.com/openai/v1/chat/completions", 
                                      headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "source": "groq_fast",
                            "analysis": result["choices"][0]["message"]["content"],
                            "domain": domain
                        }
        except Exception as e:
            print(f"Groq query failed: {e}")
        
        return None
    
    async def _query_together_ai(self, content: str, domain: str) -> Optional[Dict[str, Any]]:
        """Query Together AI for open model insights"""
        
        together_key = os.environ.get("TOGETHER_API_KEY")
        if not together_key:
            return None
        
        headers = {
            "Authorization": f"Bearer {together_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": f"<s>[INST] Analyze this {domain} document for best practices and compliance: {content[:800]} [/INST]",
            "max_tokens": 400
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.together.xyz/inference", 
                                      headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        return {
                            "source": "together_ai",
                            "analysis": result["output"]["choices"][0]["text"],
                            "domain": domain
                        }
        except Exception as e:
            print(f"Together AI query failed: {e}")
        
        return None
    
    def _create_domain_prompt(self, content: str, domain: str) -> str:
        """Create domain-specific analysis prompt"""
        
        domain_contexts = {
            "ai_ethics": """
            Analyze this document for AI ethics implications including:
            - Fairness and bias considerations
            - Transparency and explainability requirements
            - Privacy and data protection measures
            - Accountability frameworks
            - Human oversight mechanisms
            """,
            "quantum_security": """
            Analyze this document for quantum security implications including:
            - Post-quantum cryptography readiness
            - Quantum key distribution protocols
            - Quantum-resistant algorithms
            - Quantum threat mitigation strategies
            - Future quantum computing impacts
            """,
            "cybersecurity": """
            Analyze this document for cybersecurity frameworks including:
            - Risk assessment methodologies
            - Security control implementations
            - Incident response procedures
            - Compliance requirements
            - Threat intelligence integration
            """
        }
        
        context = domain_contexts.get(domain, "Analyze this document for general technology governance.")
        
        return f"""
        {context}
        
        Document content:
        {content[:2000]}
        
        Provide analysis in JSON format with these fields:
        - domain_relevance: How relevant is this to {domain} (0-100)
        - key_insights: List of key insights specific to {domain}
        - compliance_frameworks: Relevant standards/frameworks mentioned
        - risk_factors: Identified risks or concerns
        - best_practices: Recommended best practices
        - maturity_indicators: Signs of organizational maturity in this domain
        """
    
    def _get_system_prompt(self, domain: str) -> str:
        """Get system prompt for domain-specific analysis"""
        
        return f"""You are an expert in {domain} with deep knowledge of:
        - Current industry standards and best practices
        - Regulatory frameworks and compliance requirements  
        - Emerging threats and risk mitigation strategies
        - Organizational maturity models
        - Technology implementation guidelines
        
        Provide detailed, actionable analysis that helps organizations improve their {domain} posture.
        Always respond in valid JSON format."""
    
    def _synthesize_analysis(self, primary: Dict[str, Any], insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize multiple analysis sources into comprehensive result"""
        
        synthesis = {
            "primary_analysis": primary,
            "supporting_insights": insights,
            "confidence_score": self._calculate_confidence(primary, insights),
            "knowledge_sources_used": [insight.get("source") for insight in insights],
            "enhanced_metadata": self._extract_enhanced_metadata(primary, insights)
        }
        
        return synthesis
    
    def _calculate_confidence(self, primary: Dict[str, Any], insights: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on source agreement"""
        
        base_confidence = 0.5 if primary else 0.1
        
        # Increase confidence with more sources
        source_bonus = min(len(insights) * 0.1, 0.4)
        
        # Check for consistency across sources
        consistency_bonus = 0.1 if len(insights) > 1 else 0.0
        
        return min(base_confidence + source_bonus + consistency_bonus, 1.0)
    
    def _extract_enhanced_metadata(self, primary: Dict[str, Any], insights: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract enhanced metadata from multi-source analysis"""
        
        enhanced = {
            "ai_ethics_score": 0,
            "quantum_security_score": 0,
            "cybersecurity_score": 0,
            "compliance_frameworks": [],
            "risk_level": "unknown",
            "maturity_indicators": []
        }
        
        # Extract scores and metadata from insights
        for insight in insights:
            domain = insight.get("domain", "")
            if "ai_ethics" in domain:
                enhanced["ai_ethics_score"] = min(enhanced["ai_ethics_score"] + 20, 100)
            elif "quantum" in domain:
                enhanced["quantum_security_score"] = min(enhanced["quantum_security_score"] + 20, 100)
            elif "cyber" in domain:
                enhanced["cybersecurity_score"] = min(enhanced["cybersecurity_score"] + 20, 100)
        
        return enhanced

# Global instance
llm_enhancer = LLMIntelligenceEnhancer()