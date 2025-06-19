"""
Smart LLM Caching System with Multiple Provider Support
Implements intelligent caching and load balancing across multiple LLM providers
"""

import os
import json
import hashlib
import sqlite3
from typing import Dict, Optional, List
from datetime import datetime, timedelta

class SmartLLMCache:
    def __init__(self, cache_db_path="llm_cache.db"):
        self.cache_db_path = cache_db_path
        self.init_cache_db()
        
    def init_cache_db(self):
        """Initialize cache database"""
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS llm_cache (
                content_hash TEXT PRIMARY KEY,
                title TEXT,
                content_preview TEXT,
                ai_cybersecurity INTEGER,
                ai_ethics INTEGER,
                quantum_cybersecurity INTEGER,
                quantum_ethics INTEGER,
                provider TEXT,
                created_at TIMESTAMP,
                last_used TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_content_hash(self, text: str, title: str) -> str:
        """Generate hash for content caching"""
        combined = f"{title}|||{text[:2000]}"  # Use first 2000 chars for consistency
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get_cached_scores(self, text: str, title: str) -> Optional[Dict[str, Optional[int]]]:
        """Retrieve cached scores if available"""
        content_hash = self.get_content_hash(text, title)
        
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT ai_cybersecurity, ai_ethics, quantum_cybersecurity, quantum_ethics, provider
            FROM llm_cache 
            WHERE content_hash = ?
        ''', (content_hash,))
        
        result = cursor.fetchone()
        
        if result:
            # Update last_used timestamp
            cursor.execute('''
                UPDATE llm_cache 
                SET last_used = ? 
                WHERE content_hash = ?
            ''', (datetime.now(), content_hash))
            conn.commit()
            
            scores = {
                'ai_cybersecurity': result[0],
                'ai_ethics': result[1], 
                'quantum_cybersecurity': result[2],
                'quantum_ethics': result[3]
            }
            
            print(f"Cache HIT: Retrieved scores from {result[4]} provider")
            conn.close()
            return scores
        
        conn.close()
        return None
    
    def cache_scores(self, text: str, title: str, scores: Dict[str, Optional[int]], provider: str):
        """Cache computed scores"""
        content_hash = self.get_content_hash(text, title)
        
        conn = sqlite3.connect(self.cache_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO llm_cache 
            (content_hash, title, content_preview, ai_cybersecurity, ai_ethics, 
             quantum_cybersecurity, quantum_ethics, provider, created_at, last_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            content_hash,
            title[:100],
            text[:200],
            scores.get('ai_cybersecurity'),
            scores.get('ai_ethics'),
            scores.get('quantum_cybersecurity'),
            scores.get('quantum_ethics'),
            provider,
            datetime.now(),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
        print(f"Cache STORE: Saved scores from {provider} provider")

def analyze_with_groq(text: str, title: str) -> Dict[str, Optional[int]]:
    """Use Groq API for fast, free LLM analysis"""
    try:
        import requests
        
        # Groq provides free tier with good performance
        groq_api_key = os.getenv('GROQ_API_KEY')
        if not groq_api_key:
            return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}
        
        headers = {
            'Authorization': f'Bearer {groq_api_key}',
            'Content-Type': 'application/json'
        }
        
        prompt = f"""
Analyze this document for AI/quantum cybersecurity and ethics maturity (0-100 scale):

Title: {title}
Content: {text[:3000]}...

Score each applicable area 0-100 or null if not relevant:
- AI Cybersecurity: AI system security, threats, governance, secure deployment
- AI Ethics: Responsible AI, fairness, transparency, accountability, governance  
- Quantum Cybersecurity: Post-quantum cryptography, quantum-safe security
- Quantum Ethics: Quantum access, inclusion, sustainability, governance

Return JSON: {{"ai_cybersecurity": score_or_null, "ai_ethics": score_or_null, "quantum_cybersecurity": score_or_null, "quantum_ethics": score_or_null}}
"""
        
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "mixtral-8x7b-32768",
            "temperature": 0.1,
            "max_tokens": 500
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
                
                # Validate scores
                validated_scores = {}
                for key in ['ai_cybersecurity', 'ai_ethics', 'quantum_cybersecurity', 'quantum_ethics']:
                    score = scores.get(key)
                    if score is not None and isinstance(score, (int, float)) and 0 <= score <= 100:
                        validated_scores[key] = int(score)
                    else:
                        validated_scores[key] = None
                
                return validated_scores
        
    except Exception as e:
        print(f"Groq analysis failed: {e}")
    
    return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}

def analyze_with_ollama(text: str, title: str) -> Dict[str, Optional[int]]:
    """Use local Ollama for free LLM analysis"""
    try:
        import requests
        
        # Check if Ollama is running locally
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            if response.status_code != 200:
                return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}
        except:
            return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}
        
        prompt = f"""
You are an AI/cybersecurity expert. Analyze this document and provide maturity scores (0-100):

Title: {title}
Content: {text[:2000]}...

Score each applicable framework 0-100 or respond with null if not relevant:

AI Cybersecurity: How well does this address AI system security, threat management, secure deployment, governance?
AI Ethics: How well does this address responsible AI, fairness, transparency, accountability?
Quantum Cybersecurity: How well does this address post-quantum cryptography, quantum-safe security?
Quantum Ethics: How well does this address quantum inclusion, access, sustainability?

Respond with JSON only: {{"ai_cybersecurity": score_or_null, "ai_ethics": score_or_null, "quantum_cybersecurity": score_or_null, "quantum_ethics": score_or_null}}
"""
        
        data = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.1}
        }
        
        response = requests.post(
            'http://localhost:11434/api/generate',
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result.get('response', '')
            
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
                
                # Validate scores
                validated_scores = {}
                for key in ['ai_cybersecurity', 'ai_ethics', 'quantum_cybersecurity', 'quantum_ethics']:
                    score = scores.get(key)
                    if score is not None and isinstance(score, (int, float)) and 0 <= score <= 100:
                        validated_scores[key] = int(score)
                    else:
                        validated_scores[key] = None
                
                return validated_scores
        
    except Exception as e:
        print(f"Ollama analysis failed: {e}")
    
    return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}

def smart_multi_llm_scoring(text: str, title: str) -> Dict[str, Optional[int]]:
    """
    Smart multi-LLM scoring with caching and load balancing
    """
    cache = SmartLLMCache()
    
    # Try cache first
    cached_scores = cache.get_cached_scores(text, title)
    if cached_scores:
        return cached_scores
    
    # Try free/local providers first
    providers = [
        ('groq', analyze_with_groq),
        ('ollama', analyze_with_ollama),
    ]
    
    # Try Anthropic as premium option (with rate limiting awareness)
    if os.getenv('ANTHROPIC_API_KEY'):
        from utils.multi_llm_scoring_engine import analyze_document_with_anthropic
        providers.append(('anthropic', analyze_document_with_anthropic))
    
    # Enhanced pattern scoring as reliable fallback
    from utils.enhanced_pattern_scoring import enhanced_pattern_scoring
    providers.append(('enhanced_patterns', enhanced_pattern_scoring))
    
    for provider_name, provider_func in providers:
        try:
            scores = provider_func(text, title)
            
            # Check if we got valid scores
            if any(score is not None and score > 0 for score in scores.values()):
                # Cache the results
                cache.cache_scores(text, title, scores, provider_name)
                return scores
                
        except Exception as e:
            print(f"{provider_name} provider failed: {e}")
            continue
    
    # Ultimate fallback - return None scores
    return {'ai_cybersecurity': None, 'ai_ethics': None, 'quantum_cybersecurity': None, 'quantum_ethics': None}