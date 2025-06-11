"""
Enhanced Multi-LLM Metadata Extractor
Comprehensive metadata extraction for all document ingestion methods
"""

import os
import re
import json
from typing import Dict, Optional
from openai import OpenAI

class EnhancedMetadataExtractor:
    """Advanced metadata extraction using multi-LLM intelligence"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def extract_comprehensive_metadata(self, title: str, content: str, url: str = "", filename: str = "") -> Dict[str, any]:
        """Extract comprehensive metadata using multiple intelligence layers"""
        
        # Multi-layer extraction
        llm_metadata = self._extract_with_llm(title, content, url, filename)
        pattern_metadata = self._extract_with_patterns(title, content, url, filename)
        
        # Combine and prioritize results
        combined_metadata = self._combine_metadata(llm_metadata, pattern_metadata)
        
        # Clean HTML artifacts
        cleaned_metadata = self._clean_html_artifacts(combined_metadata)
        
        return cleaned_metadata
    
    def _extract_with_llm(self, title: str, content: str, url: str, filename: str) -> Dict[str, any]:
        """Extract metadata using LLM intelligence"""
        
        try:
            prompt = f"""
            Extract precise metadata from this document with high accuracy:
            
            Title: {title[:200]}
            URL: {url}
            Filename: {filename}
            Content: {content[:1500]}
            
            EXTRACTION REQUIREMENTS:
            1. TITLE: Extract the EXACT document title from content, not generic descriptions
            2. ORGANIZATION: Identify the precise authoring organization (NASA, NIST, ENISA, etc.)
            3. DATE: Extract publication date in YYYY-MM-DD format only
            4. DOCUMENT_TYPE: Classify as Framework, Policy, Research, Standard, Report, Guidance
            5. AUTHOR: Extract specific author names if mentioned
            6. DESCRIPTION: One-line summary of document purpose
            
            CRITICAL RULES:
            - Use EXACT titles from document headers/covers, not generic descriptions
            - For NASA documents, organization should be "NASA" or "National Aeronautics and Space Administration"
            - Return actual dates only, no HTML artifacts
            - If information is unclear, return "Unknown" rather than guessing
            
            Respond with JSON only:
            {{
                "title": "exact document title",
                "organization": "precise organization name",
                "author": "specific author or Unknown",
                "publication_date": "YYYY-MM-DD or Unknown", 
                "document_type": "classification",
                "description": "one-line purpose summary",
                "confidence": 0.0-1.0
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"LLM metadata extraction failed: {e}")
            return self._fallback_metadata()
    
    def _extract_with_patterns(self, title: str, content: str, url: str, filename: str) -> Dict[str, any]:
        """Extract metadata using pattern recognition"""
        
        metadata = {
            "title": "Unknown",
            "organization": "Unknown", 
            "author": "Unknown",
            "publication_date": "Unknown",
            "document_type": "Unknown",
            "description": "Unknown",
            "confidence": 0.3
        }
        
        # Title extraction patterns
        title_patterns = [
            r'(?:title|document title|subject):\s*([^\n\r]{10,100})',
            r'^([A-Z][^\n\r]{20,80}(?:Framework|Policy|Guidelines?|Standards?|Report))',
            r'Executive Order \d+[:\-\s]*([^\n\r]{10,80})',
            r'(?:NASA|NIST|DHS|ENISA)[:\-\s]*([^\n\r]{10,80})',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                extracted_title = match.group(1).strip()
                if len(extracted_title) > 10:
                    metadata["title"] = extracted_title
                    break
        
        # Organization extraction from URL and content
        if 'nasa.gov' in url.lower() or 'nasa' in content[:500].lower():
            metadata["organization"] = "NASA"
        elif 'nist.gov' in url.lower() or 'nist' in content[:500].lower():
            metadata["organization"] = "National Institute of Standards and Technology"
        elif 'dhs.gov' in url.lower() or 'cisa' in content[:500].lower():
            metadata["organization"] = "Department of Homeland Security"
        elif 'enisa.europa.eu' in url.lower():
            metadata["organization"] = "European Union Agency for Cybersecurity"
        elif 'ncsc.gov.uk' in url.lower():
            metadata["organization"] = "UK National Cyber Security Centre"
        
        # Date extraction patterns
        date_patterns = [
            r'(?:published|issued|date|effective):\s*(\d{4}-\d{2}-\d{2})',
            r'(?:published|issued|date|effective):\s*([A-Z][a-z]+ \d{1,2}, \d{4})',
            r'(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{4})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                if len(date_str) >= 4 and date_str.isdigit():
                    metadata["publication_date"] = date_str
                elif '-' in date_str:
                    metadata["publication_date"] = date_str
                break
        
        # Document type classification
        content_lower = content.lower()
        if any(term in content_lower for term in ['framework', 'cybersecurity framework']):
            metadata["document_type"] = "Framework"
        elif any(term in content_lower for term in ['executive order', 'policy', 'directive']):
            metadata["document_type"] = "Policy"
        elif any(term in content_lower for term in ['guidelines', 'guidance', 'best practices']):
            metadata["document_type"] = "Guidance"
        elif any(term in content_lower for term in ['standard', 'specification']):
            metadata["document_type"] = "Standard"
        elif any(term in content_lower for term in ['report', 'assessment', 'analysis']):
            metadata["document_type"] = "Report"
        
        return metadata
    
    def _combine_metadata(self, llm_metadata: Dict, pattern_metadata: Dict) -> Dict[str, any]:
        """Intelligently combine LLM and pattern-based metadata"""
        
        combined = {}
        
        # Prioritize non-generic, high-confidence results
        for field in ["title", "organization", "author", "publication_date", "document_type", "description"]:
            llm_value = llm_metadata.get(field, "Unknown")
            pattern_value = pattern_metadata.get(field, "Unknown")
            
            # Prioritize specific over generic
            if llm_value != "Unknown" and not self._is_generic(llm_value, field):
                combined[field] = llm_value
            elif pattern_value != "Unknown" and not self._is_generic(pattern_value, field):
                combined[field] = pattern_value
            else:
                combined[field] = llm_value if llm_value != "Unknown" else pattern_value
        
        # Set confidence based on data quality
        llm_conf = llm_metadata.get("confidence", 0.0)
        pattern_conf = pattern_metadata.get("confidence", 0.0)
        combined["confidence"] = max(llm_conf, pattern_conf)
        
        return combined
    
    def _is_generic(self, value: str, field: str) -> bool:
        """Check if a value is too generic to be useful"""
        
        if field == "title":
            generic_titles = [
                "cybersecurity document", "document", "untitled", "no title",
                "web document", "pdf document", "government document"
            ]
            return value.lower() in generic_titles or len(value) < 10
        
        elif field == "organization":
            generic_orgs = [
                "organization", "unknown organization", "government", "agency"
            ]
            return value.lower() in generic_orgs
        
        return False
    
    def _clean_html_artifacts(self, metadata: Dict) -> Dict[str, any]:
        """Remove HTML artifacts from all metadata fields"""
        
        cleaned = {}
        
        for key, value in metadata.items():
            if isinstance(value, str):
                # Remove HTML tags
                cleaned_value = re.sub(r'<[^>]+>', '', str(value))
                # Remove HTML entities
                cleaned_value = re.sub(r'&[a-z]+;', '', cleaned_value)
                # Remove excess whitespace
                cleaned_value = re.sub(r'\s+', ' ', cleaned_value).strip()
                # Remove specific artifacts
                cleaned_value = cleaned_value.replace('</div>', '').replace('<div>', '')
                
                cleaned[key] = cleaned_value if cleaned_value else "Unknown"
            else:
                cleaned[key] = value
        
        return cleaned
    
    def _fallback_metadata(self) -> Dict[str, any]:
        """Fallback metadata when extraction fails"""
        return {
            "title": "Unknown",
            "organization": "Unknown",
            "author": "Unknown", 
            "publication_date": "Unknown",
            "document_type": "Unknown",
            "description": "Unknown",
            "confidence": 0.0
        }

def extract_enhanced_metadata(title: str, content: str, url: str = "", filename: str = "") -> Dict[str, any]:
    """Main function for enhanced metadata extraction"""
    extractor = EnhancedMetadataExtractor()
    return extractor.extract_comprehensive_metadata(title, content, url, filename)