"""
Enhanced Metadata Extraction System for GUARDIAN
Fixes metadata parsing issues and improves accuracy for AI/Quantum documents
"""

import re
from datetime import datetime
from typing import Dict, Optional, List
import json
from utils.organization_acronym_converter import convert_org_to_acronym

class EnhancedMetadataExtractor:
    """
    Advanced metadata extraction with specialized patterns for technical documents
    """
    
    def __init__(self):
        self.ai_indicators = [
            'artificial intelligence', 'machine learning', 'ai model', 'neural network',
            'generative ai', 'foundation model', 'large language model', 'deep learning',
            'ai risk', 'ai governance', 'ai ethics', 'ai safety', 'responsible ai'
        ]
        
        self.quantum_indicators = [
            'quantum computing', 'quantum cryptography', 'post-quantum', 'quantum-safe',
            'quantum key distribution', 'quantum algorithm', 'quantum security',
            'quantum resistant', 'quantum threat', 'qkd'
        ]
        
        self.cybersecurity_indicators = [
            'cybersecurity', 'information security', 'cyber security', 'security framework',
            'vulnerability', 'threat', 'risk management', 'secure development'
        ]
        
        self.ethics_indicators = [
            'ethics', 'bias', 'fairness', 'transparency', 'accountability',
            'responsible', 'trustworthy', 'governance', 'compliance'
        ]
    
    def extract_comprehensive_metadata(self, content: str, title: str = "", url: str = "") -> Dict:
        """Extract comprehensive metadata from document content"""
        
        content_clean = self._clean_content(content)
        
        metadata = {
            'title': self._extract_title(content_clean, title),
            'topic': self._determine_topic(content_clean, title),
            'document_type': self._determine_document_type(content_clean, title),
            'author_organization': self._extract_organization(content_clean, url),
            'publish_date': self._extract_date(content_clean),
            'content_summary': self._generate_summary(content_clean),
            'framework_applicability': self._assess_framework_applicability(content_clean, title)
        }
        
        return metadata
    
    def _clean_content(self, content: str) -> str:
        """Clean and normalize content for better parsing"""
        # Remove extra whitespace and normalize
        content = re.sub(r'\s+', ' ', content.strip())
        # Remove common PDF artifacts
        content = re.sub(r'This publication is available free of charge from.*?(?=\n|\s{10})', '', content)
        return content
    
    def _extract_title(self, content: str, existing_title: str = "") -> str:
        """Extract proper document title using multiple strategies"""
        
        content_lower = content.lower()
        
        # Strategy 1: Look for NIST publication patterns
        nist_patterns = [
            r'nist\s+special\s+publication\s+(\d+[-\w]*)\s+(.+?)(?=\n|author|this publication)',
            r'nist\s+sp\s+(\d+[-\w]*)\s+(.+?)(?=\n|author|this publication)',
            r'(nist\s+sp\s+\d+[-\w]*[^.]*?)(?=\s+author|\s+this\s+publication|\s+\w+\s+\w+\s+\w+\s+\w+)',
        ]
        
        for pattern in nist_patterns:
            match = re.search(pattern, content_lower, re.IGNORECASE | re.DOTALL)
            if match:
                if len(match.groups()) == 2:
                    pub_num, title_part = match.groups()
                    return f"NIST SP {pub_num.upper()} {title_part.strip()}".title()
                else:
                    return match.group(1).strip().title()
        
        # Strategy 2: Look for document headers
        header_patterns = [
            r'^(.+?)(?=\n.*?author|\n.*?published|\n.*?date)',
            r'(?:^|\n)([A-Z][^.\n]{10,100})(?=\n|\s+version|\s+draft)',
        ]
        
        for pattern in header_patterns:
            match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
            if match:
                potential_title = match.group(1).strip()
                if len(potential_title) > 10 and not any(word in potential_title.lower() for word in ['page', 'section', 'chapter']):
                    return potential_title.title()
        
        # Strategy 3: Use existing title if available
        if existing_title and len(existing_title) > 5:
            return existing_title
        
        # Strategy 4: Extract from first meaningful line
        lines = content.split('\n')[:10]
        for line in lines:
            line = line.strip()
            if len(line) > 15 and not line.lower().startswith(('page', 'section', 'chapter')):
                return line.title()
        
        return "Untitled Document"
    
    def _determine_topic(self, content: str, title: str = "") -> str:
        """Determine document topic with enhanced accuracy"""
        
        combined_text = (content + " " + title).lower()
        
        ai_score = sum(1 for indicator in self.ai_indicators if indicator in combined_text)
        quantum_score = sum(1 for indicator in self.quantum_indicators if indicator in combined_text)
        
        # Weighted scoring based on context
        if 'generative ai' in combined_text or 'ai model' in combined_text:
            ai_score += 3
        if 'quantum computing' in combined_text or 'post-quantum' in combined_text:
            quantum_score += 3
        
        # Determine primary topic
        if ai_score > quantum_score and ai_score >= 2:
            return "AI"
        elif quantum_score > ai_score and quantum_score >= 2:
            return "Quantum"
        elif ai_score > 0 and quantum_score > 0:
            return "Both"
        else:
            return "General"
    
    def _determine_document_type(self, content: str, title: str = "") -> str:
        """Determine document type with better accuracy"""
        
        combined_text = (content + " " + title).lower()
        
        type_indicators = {
            'Standard': ['nist sp', 'special publication', 'standard', 'specification', 'guideline'],
            'Policy': ['policy', 'memorandum', 'directive', 'executive order', 'strategy'],
            'Research': ['research', 'study', 'analysis', 'evaluation', 'assessment'],
            'Report': ['report', 'findings', 'results', 'survey'],
            'Framework': ['framework', 'model', 'methodology'],
            'Draft': ['draft', 'preliminary', 'working paper']
        }
        
        scores = {}
        for doc_type, indicators in type_indicators.items():
            scores[doc_type] = sum(1 for indicator in indicators if indicator in combined_text)
        
        # Return the type with highest score
        best_type = max(scores.items(), key=lambda x: x[1])
        return best_type[0] if best_type[1] > 0 else "General"
    
    def _extract_organization(self, content: str, url: str = "") -> str:
        """Extract organization with enhanced patterns"""
        
        # Strategy 1: URL-based detection
        if url:
            if 'nist.gov' in url or 'doi.org/10.6028/NIST' in url:
                return "NIST"
            elif 'nasa.gov' in url:
                return "NASA"
            elif 'whitehouse.gov' in url:
                return "White House"
            elif 'cisa.gov' in url:
                return "CISA"
        
        # Strategy 2: Content-based patterns
        content_lower = content.lower()
        
        org_patterns = {
            'NIST': [r'nist\s+special\s+publication', r'national\s+institute\s+of\s+standards', r'nist\.gov'],
            'NASA': [r'nasa', r'national\s+aeronautics'],
            'White House': [r'white\s+house', r'executive\s+office', r'president'],
            'CISA': [r'cisa', r'cybersecurity\s+and\s+infrastructure'],
            'DOD': [r'department\s+of\s+defense', r'dod'],
            'NSF': [r'national\s+science\s+foundation', r'nsf']
        }
        
        for org, patterns in org_patterns.items():
            if any(re.search(pattern, content_lower) for pattern in patterns):
                return convert_org_to_acronym(org)
        
        # Strategy 3: Look for author affiliations
        affiliation_match = re.search(r'(?:affiliation|organization|institution)[:]\s*([^.\n]+)', content_lower)
        if affiliation_match:
            extracted_org = affiliation_match.group(1).strip().title()
            return convert_org_to_acronym(extracted_org)
        
        # Convert to acronym before returning
        extracted_org = "Unknown"
        return convert_org_to_acronym(extracted_org)
    
    def _extract_date(self, content: str) -> Optional[str]:
        """Extract publication date with comprehensive patterns"""
        
        content_lower = content.lower()
        
        # Date patterns (most specific to least specific)
        date_patterns = [
            # Full dates
            r'(?:published|date|issued)[:]\s*(\w+\s+\d{1,2},?\s+\d{4})',
            r'(\w+\s+\d{4})',  # Month Year
            r'(\d{1,2}/\d{4})',  # MM/YYYY
            r'(\d{4}-\d{2})',  # YYYY-MM
            r'(\d{4})',  # Just year
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, content_lower)
            for match in matches:
                try:
                    # Try to parse and standardize the date
                    normalized_date = self._normalize_date(match)
                    if normalized_date:
                        return normalized_date
                except:
                    continue
        
        return None
    
    def _normalize_date(self, date_str: str) -> Optional[str]:
        """Normalize date string to YYYY-MM-DD format"""
        
        date_str = date_str.strip()
        
        # Handle different date formats
        try:
            # Try common formats
            for fmt in ['%B %d, %Y', '%B %Y', '%m/%Y', '%Y-%m', '%Y']:
                try:
                    parsed = datetime.strptime(date_str, fmt)
                    return parsed.strftime('%Y-%m-%d')
                except ValueError:
                    continue
            
            # Handle "May 2024" style
            if re.match(r'\w+\s+\d{4}', date_str):
                parts = date_str.split()
                if len(parts) == 2:
                    month_name, year = parts
                    month_num = {
                        'january': 1, 'february': 2, 'march': 3, 'april': 4,
                        'may': 5, 'june': 6, 'july': 7, 'august': 8,
                        'september': 9, 'october': 10, 'november': 11, 'december': 12
                    }.get(month_name.lower())
                    
                    if month_num:
                        return f"{year}-{month_num:02d}-01"
        
        except Exception:
            pass
        
        return None
    
    def _generate_summary(self, content: str) -> str:
        """Generate intelligent summary of document content"""
        
        # Extract first meaningful paragraph
        paragraphs = [p.strip() for p in content.split('\n') if len(p.strip()) > 50]
        
        if paragraphs:
            first_para = paragraphs[0]
            # Truncate to reasonable length
            if len(first_para) > 200:
                sentences = first_para.split('.')
                summary = sentences[0] + '.'
                if len(summary) < 100 and len(sentences) > 1:
                    summary += ' ' + sentences[1] + '.'
                return summary[:200] + '...' if len(summary) > 200 else summary
            return first_para
        
        return "No summary available"
    
    def _assess_framework_applicability(self, content: str, title: str = "") -> Dict[str, bool]:
        """Assess which scoring frameworks should apply to this document"""
        
        combined_text = (content + " " + title).lower()
        
        # AI frameworks
        ai_relevant = any(indicator in combined_text for indicator in self.ai_indicators)
        ai_cyber_relevant = ai_relevant and any(indicator in combined_text for indicator in self.cybersecurity_indicators)
        ai_ethics_relevant = ai_relevant and any(indicator in combined_text for indicator in self.ethics_indicators)
        
        # Quantum frameworks  
        quantum_relevant = any(indicator in combined_text for indicator in self.quantum_indicators)
        quantum_cyber_relevant = quantum_relevant and any(indicator in combined_text for indicator in self.cybersecurity_indicators)
        quantum_ethics_relevant = quantum_relevant and any(indicator in combined_text for indicator in self.ethics_indicators)
        
        return {
            'ai_cybersecurity': ai_cyber_relevant,
            'ai_ethics': ai_ethics_relevant,
            'quantum_cybersecurity': quantum_cyber_relevant,
            'quantum_ethics': quantum_ethics_relevant
        }

# Global instance
enhanced_extractor = EnhancedMetadataExtractor()

def extract_enhanced_metadata(content: str, title: str = "", url: str = "") -> Dict:
    """Extract enhanced metadata from document content"""
    return enhanced_extractor.extract_comprehensive_metadata(content, title, url)