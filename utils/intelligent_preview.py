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
            Create an extensive, detailed preview summary for this document. Provide comprehensive analysis covering all key aspects, insights, and strategic implications.
            
            Title: {title}
            Content: {content_excerpt}
            
            Generate a thorough 6-8 sentence preview that includes:
            1. Document's main purpose, scope, strategic importance, and organizational context
            2. Detailed overview of key topics, frameworks, standards, methodologies, and technical approaches covered
            3. Specific practical applications, implementation strategies, deployment considerations, and target audience
            4. Critical recommendations, best practices, risk assessments, and compliance requirements
            5. Relevance to cybersecurity, AI governance, quantum technologies, or related emerging technologies
            6. Authority and credibility indicators (source organization, standards body, expert authorship)
            7. Unique insights, innovative approaches, or distinguishing features of the document
            8. Strategic value for different stakeholder groups (practitioners, policymakers, researchers, executives)
            
            Make the summary comprehensive and detailed (300-450 words) while maintaining excellent clarity, flow, and professional readability. Include specific technical details and actionable insights where relevant.
            """
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
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
                
                return f"{base_description} {content_insights}{practical_context} This resource serves as a valuable reference for stakeholders, practitioners, and decision-makers seeking comprehensive understanding and actionable implementation strategies. The document offers strategic insights that support informed decision-making and effective governance approaches in complex technological environments."
            else:
                return f"{base_description} The document provides detailed analysis, strategic recommendations, and comprehensive implementation guidance across multiple domains. It serves as an authoritative resource for understanding key concepts, advanced methodologies, and industry best practices. This material delivers particular value for practitioners, policymakers, researchers, and stakeholders seeking authoritative guidance, practical insights, and strategic direction. The content supports evidence-based decision-making and facilitates effective governance frameworks for emerging technologies and complex organizational challenges."
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
                base_text = f"This comprehensive document presents detailed analysis and extensive guidance on {title.lower()}. {preview_text} The resource provides valuable insights, practical recommendations, strategic frameworks, and actionable implementation guidance. It addresses critical considerations for stakeholders across technical, operational, and governance domains, offering evidence-based approaches to complex challenges and emerging opportunities in the field."
                return base_text[:500] + '...' if len(base_text) > 500 else base_text
            else:
                return f"This comprehensive document provides extensive analysis and detailed guidance on {title.lower()}, addressing key concepts, advanced methodologies, and strategic implementation approaches. The resource covers practical recommendations for stakeholders, offering authoritative insights across technical, operational, and governance domains. It serves as a definitive reference for practitioners, policymakers, researchers, and decision-makers seeking evidence-based guidance and strategic direction. The document facilitates informed decision-making through comprehensive coverage of best practices, risk considerations, and emerging trends, supporting effective implementation of complex initiatives and organizational transformation efforts."

# Global instance
preview_generator = IntelligentPreviewGenerator()

def generate_intelligent_preview(title: str, content: str) -> str:
    """Generate intelligent preview summary for document"""
    return preview_generator.generate_intelligent_preview(title, content)