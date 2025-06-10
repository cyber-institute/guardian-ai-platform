"""
Content cleaning utilities for removing HTML, CSS, and other markup artifacts
"""

import re
from typing import Dict

def clean_html_content(content: str) -> str:
    """
    Comprehensively clean HTML and CSS artifacts from content.
    
    Args:
        content: Raw content that may contain HTML/CSS
        
    Returns:
        Cleaned text content
    """
    if not content:
        return ""
    
    # Remove HTML tags completely
    content = re.sub(r'<[^>]+>', '', content)
    
    # Remove CSS style attributes
    content = re.sub(r"style\s*=\s*['\"][^'\"]*['\"]", '', content)
    
    # Remove CSS style blocks
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove script blocks
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML entities
    content = re.sub(r'&[a-zA-Z][a-zA-Z0-9]*;', ' ', content)
    content = re.sub(r'&#[0-9]+;', ' ', content)
    content = re.sub(r'&#x[0-9a-fA-F]+;', ' ', content)
    
    # Remove CSS properties that might appear as text
    css_properties = [
        r'margin-[a-z-]*:\s*[^;]+;?',
        r'padding-[a-z-]*:\s*[^;]+;?',
        r'background-[a-z-]*:\s*[^;]+;?',
        r'color:\s*[^;]+;?',
        r'font-[a-z-]*:\s*[^;]+;?',
        r'border-[a-z-]*:\s*[^;]+;?',
        r'display:\s*[^;]+;?',
        r'position:\s*[^;]+;?',
        r'width:\s*[^;]+;?',
        r'height:\s*[^;]+;?',
        r'box-shadow:\s*[^;]+;?',
        r'text-align:\s*[^;]+;?',
        r'line-height:\s*[^;]+;?',
        r'overflow:\s*[^;]+;?',
        r'transform:\s*[^;]+;?',
        r'transition:\s*[^;]+;?'
    ]
    
    for pattern in css_properties:
        content = re.sub(pattern, ' ', content, flags=re.IGNORECASE)
    
    # Remove div tags and common HTML structure elements
    content = re.sub(r'</?div[^>]*>', ' ', content, flags=re.IGNORECASE)
    content = re.sub(r'</?span[^>]*>', ' ', content, flags=re.IGNORECASE)
    content = re.sub(r'</?p[^>]*>', ' ', content, flags=re.IGNORECASE)
    content = re.sub(r'</?strong[^>]*>', ' ', content, flags=re.IGNORECASE)
    content = re.sub(r'</?em[^>]*>', ' ', content, flags=re.IGNORECASE)
    
    # Remove any remaining angle brackets that might be artifacts
    content = re.sub(r'[<>]', ' ', content)
    
    # Remove excessive whitespace and normalize
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()
    
    return content

def extract_clean_text(content: str) -> str:
    """
    Extract clean, meaningful text from potentially messy content.
    
    Args:
        content: Raw content
        
    Returns:
        Clean text suitable for analysis and display
    """
    if not content:
        return ""
    
    # First pass: HTML cleaning
    cleaned = clean_html_content(content)
    
    # Remove common document artifacts
    cleaned = re.sub(r'(?i)page\s+\d+', '', cleaned)
    cleaned = re.sub(r'(?i)draft|confidential|proprietary', '', cleaned)
    
    # Remove lines that are mostly CSS or technical markup
    lines = cleaned.split('\n')
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        # Skip lines that are mostly technical artifacts
        if (len(line) > 10 and 
            not re.search(r'^\d+\s*$|^[A-Z]\s*$', line) and
            not line.startswith(('margin-', 'padding-', 'background-', 'color:', 'font-')) and
            line.count(' ') > 2):  # At least 3 words
            clean_lines.append(line)
    
    # Rejoin and final cleanup
    result = ' '.join(clean_lines)
    result = re.sub(r'\s+', ' ', result).strip()
    
    return result

def clean_document_content(doc: dict) -> dict:
    """
    Clean all content fields in a document dictionary.
    
    Args:
        doc: Document dictionary
        
    Returns:
        Document with cleaned content
    """
    cleaned_doc = doc.copy()
    
    # Clean main content fields
    if 'content' in cleaned_doc and cleaned_doc['content']:
        cleaned_doc['content'] = extract_clean_text(cleaned_doc['content'])
    
    if 'text_content' in cleaned_doc and cleaned_doc['text_content']:
        cleaned_doc['text_content'] = extract_clean_text(cleaned_doc['text_content'])
    
    # Use the cleaner content for analysis
    if cleaned_doc.get('content'):
        cleaned_doc['clean_content'] = cleaned_doc['content']
    elif cleaned_doc.get('text_content'):
        cleaned_doc['clean_content'] = cleaned_doc['text_content']
    else:
        cleaned_doc['clean_content'] = ""
    
    return cleaned_doc