"""
Intelligent Content Preview Generator
Creates AI-powered summaries for document previews using OpenAI
"""

import os
import json
import re
from typing import Optional
from openai import OpenAI

class IntelligentPreviewGenerator:
    def __init__(self):
        self.client = None
        self._initialize_openai()
    
    def _initialize_openai(self):
        """Initialize OpenAI client with API key"""
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
            except Exception as e:
                print(f"OpenAI initialization failed: {e}")
                self.client = None
    
    def generate_intelligent_preview(self, title: str, content: str) -> str:
        """Generate an intelligent summary preview of document content"""
        
        # Clean content first
        clean_content = self._clean_content(content)
        
        # If OpenAI is available, generate AI summary
        if self.client and len(clean_content) > 200:
            ai_summary = self._generate_ai_summary(title, clean_content)
            if ai_summary:
                return ai_summary
        
        # Fallback to intelligent extraction
        return self._generate_intelligent_fallback(title, clean_content)
    
    def _clean_content(self, content: str) -> str:
        """Clean content of formatting artifacts"""
        if not content:
            return ""
        
        # Remove HTML tags and formatting
        clean = re.sub(r'<[^>]+>', '', content)
        clean = re.sub(r'\*+', '', clean)
        clean = re.sub(r'#+\s*', '', clean)
        clean = re.sub(r'[-_]{3,}', '', clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        return clean
    
    def _generate_ai_summary(self, title: str, content: str) -> Optional[str]:
        """Generate AI-powered summary using OpenAI"""
        if not self.client:
            return None
            
        try:
            # Truncate content for API efficiency
            content_excerpt = content[:2000] if len(content) > 2000 else content
            
            prompt = f"""
            Create a concise, intelligent preview summary for this document. Focus on key insights, main topics, and practical implications. 
            
            Title: {title}
            Content: {content_excerpt}
            
            Generate a 2-3 sentence preview that:
            1. Identifies the document's main purpose and scope
            2. Highlights key topics or frameworks covered
            3. Mentions practical applications or target audience
            
            Keep the summary informative but concise (under 200 words).
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            
            if response and response.choices and len(response.choices) > 0:
                summary = response.choices[0].message.content
                if summary:
                    return summary.strip()
            
            return None
            
        except Exception as e:
            print(f"AI summary generation failed: {e}")
            return None
    
    def _generate_intelligent_fallback(self, title: str, content: str) -> str:
        """Generate intelligent preview without AI when API unavailable"""
        
        if not content or len(content) < 50:
            return f"Document outlining {title.lower()} with comprehensive coverage of key topics and implementation guidance."
        
        # Extract key topics based on document type
        content_lower = content.lower()
        
        # Identify document type and key themes
        themes = []
        
        # AI/ML themes
        if any(term in content_lower for term in ['artificial intelligence', 'machine learning', 'ai system', 'neural network']):
            themes.append("AI/ML technologies")
        
        # Cybersecurity themes  
        if any(term in content_lower for term in ['cybersecurity', 'security framework', 'threat', 'risk management']):
            themes.append("cybersecurity frameworks")
        
        # Quantum themes
        if any(term in content_lower for term in ['quantum', 'post-quantum', 'quantum computing']):
            themes.append("quantum technologies")
        
        # Policy/governance themes
        if any(term in content_lower for term in ['policy', 'governance', 'compliance', 'regulation']):
            themes.append("governance and policy")
        
        # Standards themes
        if any(term in content_lower for term in ['nist', 'standard', 'guideline', 'best practice']):
            themes.append("standards and guidelines")
        
        # Implementation themes
        if any(term in content_lower for term in ['implementation', 'deployment', 'migration', 'adoption']):
            themes.append("implementation strategies")
        
        # Create intelligent summary
        if themes:
            theme_text = ", ".join(themes[:3])
            # Extract first meaningful sentence
            sentences = re.split(r'[.!?]+', content)
            first_sentence = ""
            for sentence in sentences[:3]:
                sentence = sentence.strip()
                if len(sentence) > 40 and not sentence.lower().startswith(('table', 'figure', 'page')):
                    first_sentence = sentence + "."
                    break
            
            if first_sentence:
                return f"Comprehensive document covering {theme_text}. {first_sentence} Provides detailed guidance for practitioners and stakeholders."
            else:
                return f"Comprehensive document addressing {theme_text} with practical implementation guidance and strategic recommendations."
        else:
            # Generic intelligent preview
            sentences = re.split(r'[.!?]+', content)
            meaningful_sentences = []
            for sentence in sentences[:3]:
                sentence = sentence.strip()
                if len(sentence) > 30:
                    meaningful_sentences.append(sentence)
            
            if meaningful_sentences:
                preview_text = '. '.join(meaningful_sentences[:2]) + '.'
                return preview_text[:250] + '...' if len(preview_text) > 250 else preview_text
            else:
                return f"Document providing comprehensive analysis and guidance on {title.lower()} with detailed recommendations and best practices."

# Global instance
preview_generator = IntelligentPreviewGenerator()

def generate_intelligent_preview(title: str, content: str) -> str:
    """Generate intelligent preview summary for document"""
    return preview_generator.generate_intelligent_preview(title, content)