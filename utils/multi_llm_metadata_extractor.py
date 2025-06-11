"""
Multi-LLM Enhanced Metadata Extraction System
Uses AI to intelligently extract clean metadata without HTML artifacts
"""

import re
import os
from typing import Dict, Optional, Any
from openai import OpenAI

class MultiLLMMetadataExtractor:
    """Enhanced metadata extraction using LLM intelligence"""
    
    def __init__(self):
        self.openai_key = os.environ.get('OPENAI_API_KEY')
        if self.openai_key:
            self.client = OpenAI(api_key=self.openai_key)
        else:
            self.client = None

    def extract_metadata_with_llm(self, content: str, filename: str = "") -> Dict[str, Optional[str]]:
        """
        Extract metadata using LLM intelligence for superior accuracy
        Falls back to pattern matching if LLM is unavailable
        """
        if self.client:
            try:
                return self._llm_extract_metadata(content, filename)
            except Exception as e:
                print(f"LLM extraction failed, using fallback: {e}")
                return self._fallback_extract_metadata(content, filename)
        else:
            return self._fallback_extract_metadata(content, filename)

    def _llm_extract_metadata(self, content: str, filename: str = "") -> Dict[str, Optional[str]]:
        """Use LLM to extract clean metadata"""
        
        # Prepare content - take first 3000 chars for LLM processing
        sample_content = self._clean_content_for_llm(content[:3000])
        
        prompt = f"""
Extract metadata from this document content. Return ONLY clean text without any HTML tags, styling, or formatting artifacts.

Document filename: {filename}
Content: {sample_content}

Extract and return in this exact JSON format:
{{
    "title": "document title (plain text only)",
    "author_organization": "organization name (plain text only)", 
    "publish_date": "date in YYYY-MM-DD format or null",
    "document_type": "document type (Policy/Standard/Framework/etc)",
    "content_preview": "clean preview of main content (no HTML)"
}}

Rules:
- Return ONLY valid JSON
- NO HTML tags, styling, or markup of any kind
- Dates must be YYYY-MM-DD format or null
- Keep text clean and readable
- If unsure about any field, use "Unknown" or null
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
                messages=[
                    {"role": "system", "content": "You are an expert document metadata extractor. Return only clean, HTML-free text in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Additional cleaning to ensure no artifacts
            return self._post_process_llm_result(result)
            
        except Exception as e:
            print(f"LLM processing error: {e}")
            return self._fallback_extract_metadata(content, filename)

    def _clean_content_for_llm(self, content: str) -> str:
        """Pre-clean content before sending to LLM"""
        # Remove obvious HTML artifacts
        content = re.sub(r'<[^>]+>', ' ', content)
        content = re.sub(r'&[#a-zA-Z0-9]+;', ' ', content)
        content = re.sub(r'\s+', ' ', content).strip()
        return content

    def _post_process_llm_result(self, result: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """Final cleaning of LLM extracted metadata"""
        cleaned = {}
        
        for key, value in result.items():
            if value and isinstance(value, str):
                # Aggressive HTML cleaning
                clean_value = self._ultra_clean_text(value)
                cleaned[key] = clean_value if clean_value and clean_value != "Unknown" else None
            else:
                cleaned[key] = None
                
        return cleaned

    def _ultra_clean_text(self, text: str) -> Optional[str]:
        """Ultra-aggressive text cleaning to remove all HTML artifacts"""
        if not text:
            return None
            
        # Convert to string and initial cleaning
        clean_text = str(text).strip()
        
        # Remove all HTML tags and fragments
        clean_text = re.sub(r'<[^>]*>', '', clean_text)
        clean_text = re.sub(r'</[^>]*>', '', clean_text)
        clean_text = re.sub(r'<[^>]*', '', clean_text)
        clean_text = re.sub(r'[^<]*>', '', clean_text)
        
        # Remove HTML entities
        clean_text = re.sub(r'&[#a-zA-Z0-9]+;?', '', clean_text)
        
        # Remove specific artifacts
        artifacts = [
            '</div>', '<div>', '<div', '</span>', '<span>', '<span',
            '</p>', '<p>', '<p', 'style=', 'class=', 'id=',
            '&nbsp;', '&amp;', '&lt;', '&gt;', '&quot;'
        ]
        
        for artifact in artifacts:
            clean_text = clean_text.replace(artifact, ' ')
        
        # Remove remaining brackets and quotes
        clean_text = re.sub(r'[<>"\'`]', '', clean_text)
        
        # Remove attribute patterns
        clean_text = re.sub(r'\w+\s*=\s*["\'][^"\']*["\']', '', clean_text)
        
        # Normalize whitespace
        clean_text = ' '.join(clean_text.split()).strip()
        
        # Validate result
        if len(clean_text) < 2 or re.search(r'[<>]|&\w+;|\w+=', clean_text):
            return None
            
        return clean_text

    def _fallback_extract_metadata(self, content: str, filename: str = "") -> Dict[str, Optional[str]]:
        """Fallback pattern-based extraction with enhanced cleaning"""
        from utils.document_metadata_extractor import extract_document_metadata
        
        # Use existing extraction but apply ultra cleaning
        metadata = extract_document_metadata(content, filename)
        
        # Apply ultra cleaning to all fields
        cleaned_metadata = {}
        for key, value in metadata.items():
            cleaned_metadata[key] = self._ultra_clean_text(value) if value else None
            
        return cleaned_metadata

# Global instance
multi_llm_extractor = MultiLLMMetadataExtractor()

def extract_clean_metadata(content: str, filename: str = "") -> Dict[str, Optional[str]]:
    """Main function to extract completely clean metadata"""
    return multi_llm_extractor.extract_metadata_with_llm(content, filename)