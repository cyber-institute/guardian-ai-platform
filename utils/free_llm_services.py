"""
Free LLM Services Integration for GUARDIAN
Comprehensive list and integration for free/open-source LLM APIs that can enhance
GUARDIAN's AI ethics, quantum security, and cybersecurity intelligence
"""

import json
import os
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class FreeLLMService:
    """Configuration for free LLM services"""
    name: str
    api_endpoint: str
    model_name: str
    free_tier_limits: str
    requires_api_key: bool
    specialization: str
    documentation_url: str
    status: str  # "active", "limited", "beta"

class FreeLLMServiceManager:
    """
    Manager for free LLM services that can enhance GUARDIAN's intelligence
    without requiring paid API subscriptions
    """
    
    def __init__(self):
        self.services = self._configure_free_services()
        self.service_cache = {}
    
    def _configure_free_services(self) -> List[FreeLLMService]:
        """Configure available free LLM services"""
        return [
            # Hugging Face Inference API (Free tier)
            FreeLLMService(
                name="huggingface",
                api_endpoint="https://api-inference.huggingface.co/models",
                model_name="microsoft/DialoGPT-medium",
                free_tier_limits="1000 requests/month",
                requires_api_key=True,
                specialization="General conversation, code analysis",
                documentation_url="https://huggingface.co/docs/api-inference/index",
                status="active"
            ),
            
            # Ollama (Local deployment, completely free)
            FreeLLMService(
                name="ollama",
                api_endpoint="http://localhost:11434/api",
                model_name="llama3.2:3b",
                free_tier_limits="Unlimited (local)",
                requires_api_key=False,
                specialization="General purpose, privacy-focused",
                documentation_url="https://ollama.com/",
                status="active"
            ),
            
            # Together AI (Free tier)
            FreeLLMService(
                name="together_ai",
                api_endpoint="https://api.together.xyz/v1/chat/completions",
                model_name="meta-llama/Llama-2-7b-chat-hf",
                free_tier_limits="$5 free credits",
                requires_api_key=True,
                specialization="Open models, good for analysis",
                documentation_url="https://docs.together.ai/",
                status="active"
            ),
            
            # Groq (Free tier with fast inference)
            FreeLLMService(
                name="groq",
                api_endpoint="https://api.groq.com/openai/v1/chat/completions",
                model_name="llama3-8b-8192",
                free_tier_limits="14400 tokens/minute",
                requires_api_key=True,
                specialization="Fast inference, good for real-time analysis",
                documentation_url="https://console.groq.com/docs/quickstart",
                status="active"
            ),
            
            # Cohere (Free tier)
            FreeLLMService(
                name="cohere",
                api_endpoint="https://api.cohere.ai/v1/generate",
                model_name="command-light",
                free_tier_limits="100 requests/month",
                requires_api_key=True,
                specialization="Text generation, summarization",
                documentation_url="https://docs.cohere.com/",
                status="limited"
            ),
            
            # Replicate (Pay-per-use, very affordable)
            FreeLLMService(
                name="replicate",
                api_endpoint="https://api.replicate.com/v1/predictions",
                model_name="meta/llama-2-70b-chat",
                free_tier_limits="Pay per use (~$0.001/request)",
                requires_api_key=True,
                specialization="Large models, research-grade",
                documentation_url="https://replicate.com/docs",
                status="active"
            ),
            
            # Perplexity AI (Free tier)
            FreeLLMService(
                name="perplexity",
                api_endpoint="https://api.perplexity.ai/chat/completions",
                model_name="llama-3.1-sonar-small-128k-online",
                free_tier_limits="5 requests/hour",
                requires_api_key=True,
                specialization="Real-time web search + LLM",
                documentation_url="https://docs.perplexity.ai/",
                status="limited"
            ),
            
            # Fireworks AI (Free tier)
            FreeLLMService(
                name="fireworks",
                api_endpoint="https://api.fireworks.ai/inference/v1/chat/completions",
                model_name="accounts/fireworks/models/llama-v3p1-8b-instruct",
                free_tier_limits="Free tier available",
                requires_api_key=True,
                specialization="Open source models, fast inference",
                documentation_url="https://docs.fireworks.ai/",
                status="active"
            ),
            
            # Anyscale (Free tier)
            FreeLLMService(
                name="anyscale",
                api_endpoint="https://api.endpoints.anyscale.com/v1/chat/completions",
                model_name="meta-llama/Llama-2-7b-chat-hf",
                free_tier_limits="$1 free credits",
                requires_api_key=True,
                specialization="Scalable inference",
                documentation_url="https://docs.anyscale.com/",
                status="beta"
            ),
            
            # DeepInfra (Free tier)
            FreeLLMService(
                name="deepinfra",
                api_endpoint="https://api.deepinfra.com/v1/openai/chat/completions",
                model_name="meta-llama/Llama-2-7b-chat-hf",
                free_tier_limits="$5 free credits",
                requires_api_key=True,
                specialization="Variety of open models",
                documentation_url="https://deepinfra.com/docs",
                status="active"
            )
        ]
    
    async def test_service_availability(self, service_name: str) -> Dict[str, Any]:
        """Test if a specific service is available and working"""
        
        service = next((s for s in self.services if s.name == service_name), None)
        if not service:
            return {"error": f"Service {service_name} not found"}
        
        try:
            if service.name == "ollama":
                return await self._test_ollama()
            elif service.name == "huggingface":
                return await self._test_huggingface()
            elif service.name == "groq":
                return await self._test_groq()
            elif service.name == "together_ai":
                return await self._test_together_ai()
            elif service.name == "perplexity":
                return await self._test_perplexity()
            else:
                return await self._test_generic_openai_compatible(service)
                
        except Exception as e:
            return {"error": str(e), "service": service_name}
    
    async def _test_ollama(self) -> Dict[str, Any]:
        """Test Ollama local installation"""
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test if Ollama is running
                async with session.get("http://localhost:11434/api/tags") as response:
                    if response.status == 200:
                        models = await response.json()
                        return {
                            "status": "available",
                            "service": "ollama",
                            "models": models.get("models", []),
                            "cost": "free",
                            "setup_required": "Install Ollama locally"
                        }
                    else:
                        return {
                            "status": "unavailable",
                            "service": "ollama",
                            "error": "Ollama not running locally",
                            "setup_instructions": "Install Ollama from https://ollama.com/"
                        }
        except Exception as e:
            return {
                "status": "unavailable",
                "service": "ollama",
                "error": str(e),
                "setup_instructions": "Install Ollama from https://ollama.com/"
            }
    
    async def _test_huggingface(self) -> Dict[str, Any]:
        """Test Hugging Face Inference API"""
        
        api_key = os.environ.get("HUGGINGFACE_API_TOKEN")
        if not api_key:
            return {
                "status": "needs_key",
                "service": "huggingface",
                "error": "HUGGINGFACE_API_TOKEN environment variable required",
                "setup_instructions": "Get free API token from https://huggingface.co/settings/tokens"
            }
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            payload = {
                "inputs": "Test message for GUARDIAN system",
                "parameters": {"max_length": 50}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return {
                            "status": "available",
                            "service": "huggingface",
                            "cost": "free tier: 1000 requests/month",
                            "models": ["DialoGPT", "BERT variants", "T5", "GPT-2"]
                        }
                    else:
                        return {
                            "status": "error",
                            "service": "huggingface",
                            "error": f"HTTP {response.status}",
                            "response": await response.text()
                        }
        except Exception as e:
            return {"status": "error", "service": "huggingface", "error": str(e)}
    
    async def _test_groq(self) -> Dict[str, Any]:
        """Test Groq API"""
        
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return {
                "status": "needs_key",
                "service": "groq",
                "error": "GROQ_API_KEY environment variable required",
                "setup_instructions": "Get free API key from https://console.groq.com/"
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "user", "content": "Test message for GUARDIAN AI system"}
                ],
                "max_tokens": 50
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return {
                            "status": "available",
                            "service": "groq",
                            "cost": "free tier: 14400 tokens/minute",
                            "models": ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
                        }
                    else:
                        return {
                            "status": "error",
                            "service": "groq",
                            "error": f"HTTP {response.status}",
                            "response": await response.text()
                        }
        except Exception as e:
            return {"status": "error", "service": "groq", "error": str(e)}
    
    async def _test_together_ai(self) -> Dict[str, Any]:
        """Test Together AI"""
        
        api_key = os.environ.get("TOGETHER_API_KEY")
        if not api_key:
            return {
                "status": "needs_key",
                "service": "together_ai",
                "error": "TOGETHER_API_KEY environment variable required",
                "setup_instructions": "Get free credits from https://together.ai/"
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "meta-llama/Llama-2-7b-chat-hf",
                "messages": [
                    {"role": "user", "content": "Test message for GUARDIAN"}
                ],
                "max_tokens": 50
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.together.xyz/v1/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return {
                            "status": "available",
                            "service": "together_ai",
                            "cost": "$5 free credits",
                            "models": ["Llama-2 variants", "Code Llama", "Mistral models"]
                        }
                    else:
                        return {
                            "status": "error",
                            "service": "together_ai",
                            "error": f"HTTP {response.status}",
                            "response": await response.text()
                        }
        except Exception as e:
            return {"status": "error", "service": "together_ai", "error": str(e)}
    
    async def _test_perplexity(self) -> Dict[str, Any]:
        """Test Perplexity AI"""
        
        api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not api_key:
            return {
                "status": "needs_key",
                "service": "perplexity",
                "error": "PERPLEXITY_API_KEY environment variable required",
                "setup_instructions": "Get API key from https://perplexity.ai/"
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {"role": "user", "content": "What are current AI ethics best practices?"}
                ],
                "max_tokens": 100
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.perplexity.ai/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return {
                            "status": "available",
                            "service": "perplexity",
                            "cost": "free tier: 5 requests/hour",
                            "special_feature": "Real-time web search integration"
                        }
                    else:
                        return {
                            "status": "error",
                            "service": "perplexity",
                            "error": f"HTTP {response.status}",
                            "response": await response.text()
                        }
        except Exception as e:
            return {"status": "error", "service": "perplexity", "error": str(e)}
    
    async def _test_generic_openai_compatible(self, service: FreeLLMService) -> Dict[str, Any]:
        """Test generic OpenAI-compatible API"""
        
        api_key_var = f"{service.name.upper()}_API_KEY"
        api_key = os.environ.get(api_key_var)
        
        if service.requires_api_key and not api_key:
            return {
                "status": "needs_key",
                "service": service.name,
                "error": f"{api_key_var} environment variable required",
                "setup_instructions": f"Get API key from {service.documentation_url}"
            }
        
        try:
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            payload = {
                "model": service.model_name,
                "messages": [
                    {"role": "user", "content": "Test message"}
                ],
                "max_tokens": 50
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    service.api_endpoint,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        return {
                            "status": "available",
                            "service": service.name,
                            "cost": service.free_tier_limits,
                            "specialization": service.specialization
                        }
                    else:
                        return {
                            "status": "error",
                            "service": service.name,
                            "error": f"HTTP {response.status}",
                            "response": await response.text()
                        }
        except Exception as e:
            return {"status": "error", "service": service.name, "error": str(e)}
    
    async def test_all_services(self) -> Dict[str, Any]:
        """Test all configured free LLM services"""
        
        results = {
            "available_services": [],
            "needs_setup": [],
            "errors": [],
            "total_tested": len(self.services)
        }
        
        for service in self.services:
            test_result = await self.test_service_availability(service.name)
            
            if test_result.get("status") == "available":
                results["available_services"].append({
                    "name": service.name,
                    "cost": test_result.get("cost", "Unknown"),
                    "specialization": service.specialization,
                    "status": "ready"
                })
            elif test_result.get("status") == "needs_key":
                results["needs_setup"].append({
                    "name": service.name,
                    "setup_instructions": test_result.get("setup_instructions"),
                    "cost": service.free_tier_limits
                })
            else:
                results["errors"].append({
                    "name": service.name,
                    "error": test_result.get("error"),
                    "status": test_result.get("status")
                })
        
        return results
    
    def get_service_recommendations(self, use_case: str) -> List[Dict[str, Any]]:
        """Get service recommendations based on use case"""
        
        recommendations = []
        
        if use_case == "ai_ethics":
            recommendations = [
                {
                    "service": "perplexity",
                    "reason": "Real-time web search for latest AI ethics research",
                    "priority": 1
                },
                {
                    "service": "huggingface",
                    "reason": "Access to ethics-specific models",
                    "priority": 2
                },
                {
                    "service": "ollama",
                    "reason": "Privacy-focused local analysis",
                    "priority": 3
                }
            ]
        elif use_case == "quantum_security":
            recommendations = [
                {
                    "service": "groq",
                    "reason": "Fast inference for real-time security analysis",
                    "priority": 1
                },
                {
                    "service": "together_ai",
                    "reason": "Access to larger models for complex analysis",
                    "priority": 2
                },
                {
                    "service": "ollama",
                    "reason": "Secure local deployment",
                    "priority": 3
                }
            ]
        elif use_case == "cybersecurity":
            recommendations = [
                {
                    "service": "groq",
                    "reason": "Fast analysis for threat detection",
                    "priority": 1
                },
                {
                    "service": "ollama",
                    "reason": "Air-gapped security analysis",
                    "priority": 2
                },
                {
                    "service": "fireworks",
                    "reason": "Open source models for security research",
                    "priority": 3
                }
            ]
        else:
            # General purpose recommendations
            recommendations = [
                {
                    "service": "ollama",
                    "reason": "Completely free, privacy-focused",
                    "priority": 1
                },
                {
                    "service": "groq",
                    "reason": "Fast inference, good free tier",
                    "priority": 2
                },
                {
                    "service": "huggingface",
                    "reason": "Variety of specialized models",
                    "priority": 3
                }
            ]
        
        return recommendations
    
    def get_setup_instructions(self) -> Dict[str, str]:
        """Get setup instructions for all services"""
        
        instructions = {
            "ollama": """
1. Install Ollama from https://ollama.com/
2. Run: ollama pull llama3.2:3b
3. Start Ollama service
4. No API key required - completely local and free
            """,
            
            "huggingface": """
1. Create account at https://huggingface.co/
2. Go to https://huggingface.co/settings/tokens
3. Create new token with 'Read' permissions
4. Set environment variable: HUGGINGFACE_API_TOKEN=your_token
5. Free tier: 1000 requests/month
            """,
            
            "groq": """
1. Sign up at https://console.groq.com/
2. Create API key in dashboard
3. Set environment variable: GROQ_API_KEY=your_key
4. Free tier: 14400 tokens/minute
            """,
            
            "together_ai": """
1. Sign up at https://together.ai/
2. Get $5 free credits
3. Create API key
4. Set environment variable: TOGETHER_API_KEY=your_key
            """,
            
            "perplexity": """
1. Sign up at https://perplexity.ai/
2. Go to API settings
3. Create API key
4. Set environment variable: PERPLEXITY_API_KEY=your_key
5. Free tier: 5 requests/hour with web search
            """
        }
        
        return instructions

# Global instance
free_llm_manager = FreeLLMServiceManager()