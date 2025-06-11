"""
HTML Artifact Interceptor
Intercepts and cleans all metadata before any processing or display
"""

import re
from typing import Any, Dict, List, Union

class HTMLArtifactInterceptor:
    """Intercepts and eliminates HTML artifacts at the source"""
    
    @staticmethod
    def ultra_clean_any_field(value: Any) -> str:
        """Ultra-aggressive cleaning for any field type"""
        if not value or value in [None, 'None', 'null']:
            return 'Unknown'
        
        # Convert to string and initial cleaning
        text = str(value).strip()
        
        if not text or text.lower() in ['none', 'null', 'undefined']:
            return 'Unknown'
        
        # Remove ALL HTML tags and fragments - multiple passes
        for _ in range(3):  # Multiple cleaning passes
            text = re.sub(r'<[^>]*>', '', text)
            text = re.sub(r'</[^>]*>', '', text)
            text = re.sub(r'<[^>]*', '', text)
            text = re.sub(r'[^<]*>', '', text)
        
        # Remove HTML entities
        text = re.sub(r'&[#a-zA-Z0-9]+;?', '', text)
        
        # Remove specific problematic artifacts
        artifacts = [
            '</div>', '<div>', '<div', '</span>', '<span>', '<span',
            '</p>', '<p>', '<p', '</h1>', '<h1>', '</h2>', '<h2>',
            '</h3>', '<h3>', '</h4>', '<h4>', '</h5>', '<h5>',
            '</strong>', '<strong>', '</em>', '<em>', '</b>', '<b>',
            '</i>', '<i>', '</u>', '<u>', '</br>', '<br>', '<br/>',
            'style=', 'class=', 'id=', 'href=', 'src=', 'alt=',
            '&nbsp;', '&amp;', '&lt;', '&gt;', '&quot;', '&#39;',
            'div>', 'span>', '/div', '/span', 'div', 'span'
        ]
        
        for artifact in artifacts:
            text = text.replace(artifact, ' ')
        
        # Remove remaining brackets, quotes, and attribute patterns
        text = re.sub(r'[<>"\'`]', '', text)
        text = re.sub(r'\w+\s*=\s*["\'][^"\']*["\']', '', text)
        text = re.sub(r'\w+\s*=\s*\w+', '', text)
        
        # Remove common HTML words that leak through
        html_words = ['div', 'span', 'style', 'class', 'href', 'src', 'alt']
        for word in html_words:
            text = re.sub(rf'\b{word}\b', '', text, flags=re.IGNORECASE)
        
        # Normalize whitespace
        text = ' '.join(text.split()).strip()
        
        # Final validation - if still contains artifacts, return Unknown
        if re.search(r'[<>]|&\w+;|\w+=|/>', text) or len(text) < 2:
            return 'Unknown'
        
        return text
    
    @staticmethod
    def clean_document_dict(doc: Dict[str, Any]) -> Dict[str, Any]:
        """Clean all fields in a document dictionary"""
        if not doc:
            return {}
        
        cleaned = {}
        
        # Fields that need cleaning
        fields_to_clean = [
            'title', 'author_organization', 'publish_date', 
            'document_type', 'content_preview'
        ]
        
        for key, value in doc.items():
            if key in fields_to_clean:
                cleaned[key] = HTMLArtifactInterceptor.ultra_clean_any_field(value)
            else:
                cleaned[key] = value
        
        return cleaned
    
    @staticmethod
    def clean_document_list(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Clean all documents in a list"""
        return [HTMLArtifactInterceptor.clean_document_dict(doc) for doc in docs]

# Global interceptor instance
interceptor = HTMLArtifactInterceptor()

def clean_field(value: Any) -> str:
    """Quick access function for cleaning any field"""
    return interceptor.ultra_clean_any_field(value)

def clean_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Quick access function for cleaning a document"""
    return interceptor.clean_document_dict(doc)

def clean_documents(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Quick access function for cleaning document list"""
    return interceptor.clean_document_list(docs)