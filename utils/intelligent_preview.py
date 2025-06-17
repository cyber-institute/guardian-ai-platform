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
            Create a comprehensive, intelligent preview summary for this document. Focus on key insights, main topics, practical implications, and strategic value.
            
            Title: {title}
            Content: {content_excerpt}
            
            Generate a detailed 4-6 sentence preview that:
            1. Identifies the document's main purpose, scope, and strategic importance
            2. Highlights key topics, frameworks, standards, or methodologies covered
            3. Describes practical applications, implementation guidance, or target audience
            4. Mentions any specific recommendations, best practices, or critical insights
            5. Notes the document's relevance to cybersecurity, AI governance, or quantum technologies if applicable
            6. Provides context about the document's authority or organizational source
            
            Make the summary comprehensive and informative (200-300 words) while maintaining clarity and readability.
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
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
        
        # Create comprehensive intelligent summary
        if themes:
            theme_text = ", ".join(themes[:4])
            
            # Extract multiple meaningful sentences for detailed preview
            sentences = re.split(r'[.!?]+', content)
            meaningful_sentences = []
            for sentence in sentences[:8]:  # Look at more sentences
                sentence = sentence.strip()
                if (len(sentence) > 40 and 
                    not sentence.lower().startswith(('table', 'figure', 'page', 'abstract', 'keywords')) and
                    not re.match(r'^\d+\.', sentence.strip())):  # Skip numbered lists
                    meaningful_sentences.append(sentence)
                    if len(meaningful_sentences) >= 4:  # Get up to 4 good sentences
                        break
            
            # Build comprehensive preview
            base_description = f"This comprehensive document addresses {theme_text}, providing strategic guidance and practical implementation frameworks."
            
            if meaningful_sentences:
                # Add key insights from content
                content_insights = '. '.join(meaningful_sentences[:3]) + '.'
                if len(content_insights) > 300:
                    content_insights = content_insights[:300] + '...'
                
                # Add practical applications context
                practical_context = ""
                if 'implementation' in content_lower:
                    practical_context = " The document includes specific implementation strategies and deployment considerations."
                elif 'guidance' in content_lower or 'recommendation' in content_lower:
                    practical_context = " It offers detailed recommendations and best practice guidance for practitioners."
                elif 'framework' in content_lower or 'standard' in content_lower:
                    practical_context = " The framework provides structured approaches and standardized methodologies."
                
                return f"{base_description} {content_insights}{practical_context} This resource serves as a valuable reference for stakeholders, practitioners, and decision-makers in the field."
            else:
                return f"{base_description} The document provides detailed analysis, strategic recommendations, and implementation guidance. It serves as a comprehensive resource for understanding key concepts, methodologies, and best practices. This material is particularly valuable for practitioners, policymakers, and stakeholders seeking authoritative guidance and practical insights."
        else:
            # Enhanced generic intelligent preview
            sentences = re.split(r'[.!?]+', content)
            meaningful_sentences = []
            for sentence in sentences[:6]:
                sentence = sentence.strip()
                if (len(sentence) > 30 and 
                    not sentence.lower().startswith(('table', 'figure', 'page', 'abstract'))):
                    meaningful_sentences.append(sentence)
                    if len(meaningful_sentences) >= 3:
                        break
            
            if meaningful_sentences:
                preview_text = '. '.join(meaningful_sentences) + '.'
                base_text = f"This document presents comprehensive analysis and guidance on {title.lower()}. {preview_text} It provides valuable insights, practical recommendations, and strategic frameworks for implementation."
                return base_text[:400] + '...' if len(base_text) > 400 else base_text
            else:
                return f"This comprehensive document provides detailed analysis and guidance on {title.lower()}. It covers key concepts, methodologies, and implementation strategies with practical recommendations for stakeholders. The document serves as an authoritative resource offering strategic insights, best practices, and actionable guidance for practitioners and decision-makers in the field."

# Global instance
preview_generator = IntelligentPreviewGenerator()

def generate_intelligent_preview(title: str, content: str) -> str:
    """Generate intelligent preview summary for document"""
    return preview_generator.generate_intelligent_preview(title, content)