"""
Clean content preview generator - completely isolated from scoring system
"""

import re
from typing import Dict

def generate_clean_preview(raw_content: str) -> str:
    """
    Generate a clean content preview completely isolated from any HTML generation.
    
    Args:
        raw_content: Raw document content
        
    Returns:
        Clean text preview without any HTML artifacts
    """
    if not raw_content or len(raw_content.strip()) < 20:
        return "Insufficient content for preview"
    
    # Step 1: Aggressive HTML/CSS cleaning
    content = raw_content
    
    # Remove all HTML tags and script/style blocks
    content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<[^>]*>', '', content)
    
    # Remove CSS properties and styling artifacts
    css_patterns = [
        r'style\s*=\s*["\'][^"\']*["\']',
        r'background[^;]*;',
        r'color[^;]*;',
        r'margin[^;]*;',
        r'padding[^;]*;',
        r'font[^;]*;',
        r'border[^;]*;',
        r'display[^;]*;',
        r'width[^;]*;',
        r'height[^;]*;'
    ]
    
    for pattern in css_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # Remove HTML entities
    content = re.sub(r'&[a-zA-Z]+;', ' ', content)
    content = re.sub(r'&#\d+;', ' ', content)
    
    # Remove any remaining brackets and artifacts
    content = re.sub(r'[<>{}]', '', content)
    content = re.sub(r'["\']', '', content)
    
    # Step 2: Clean up whitespace and normalize
    content = re.sub(r'\s+', ' ', content).strip()
    
    # Step 3: Extract meaningful sentences
    sentences = re.split(r'[.!?]\s+', content)
    clean_sentences = []
    
    for sentence in sentences[:10]:  # Check first 10 sentences
        sentence = sentence.strip()
        
        # Filter criteria for meaningful content
        if (20 <= len(sentence) <= 400 and  # Reasonable length
            sentence.count(' ') >= 4 and    # At least 5 words
            not re.search(r'^\d+\s*$|^[A-Z]\s*$', sentence) and  # Not just numbers/letters
            not sentence.lower().startswith(('ai cyber', 'q cyber', 'ai ethics', 'q ethics')) and  # Not scoring artifacts
            not re.search(r'score|rating|assessment|badge', sentence.lower()) and  # Not scoring references
            any(char.isalpha() for char in sentence)):  # Contains actual letters
            
            clean_sentences.append(sentence)
            if len(clean_sentences) >= 2:
                break
    
    # Step 4: Build preview
    if clean_sentences:
        preview = '. '.join(clean_sentences)
        if not preview.endswith('.'):
            preview += '.'
        
        # Final length check
        if len(preview) > 300:
            preview = preview[:297] + '...'
        
        return preview
    
    # Fallback: Extract first coherent text block
    words = content.split()
    meaningful_words = []
    
    for word in words[:100]:
        if (len(word) > 1 and 
            word.isalnum() and 
            not re.search(r'score|rating|cyber|ethics', word.lower())):
            meaningful_words.append(word)
            if len(meaningful_words) >= 25:
                break
    
    if len(meaningful_words) >= 10:
        return ' '.join(meaningful_words) + '...'
    
    return "Content preview not available"

def extract_clean_metadata(content: str, filename: str = "") -> dict:
    """
    Extract basic metadata without any HTML generation or scoring involvement.
    
    Args:
        content: Clean document content
        filename: Original filename
        
    Returns:
        Dictionary with clean metadata
    """
    if not content or len(content.strip()) < 20:
        return {
            'clean_title': filename or 'Untitled Document',
            'clean_preview': 'Insufficient content'
        }
    
    # Clean content first
    clean_content = re.sub(r'[<>]', '', content)
    clean_content = re.sub(r'\s+', ' ', clean_content).strip()
    
    # Extract title (first meaningful line)
    lines = clean_content.split('\n')
    title = filename or 'Untitled Document'
    
    for line in lines[:5]:
        line = line.strip()
        if 10 <= len(line) <= 100 and not re.search(r'^\d+|page|section', line.lower()):
            title = line
            break
    
    # Generate clean preview
    preview = generate_clean_preview(clean_content)
    
    return {
        'clean_title': title,
        'clean_preview': preview
    }