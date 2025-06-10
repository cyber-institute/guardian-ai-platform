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
    if not raw_content or len(raw_content.strip()) < 10:
        return "Content not available"
    
    # Step 1: Ultra-aggressive HTML removal
    content = str(raw_content)
    
    # Remove everything between angle brackets (including incomplete tags)
    content = re.sub(r'<[^<>]*/?>', '', content)  # Complete tags
    content = re.sub(r'<[^<>]*$', '', content)    # Incomplete opening tags
    content = re.sub(r'^[^<>]*>', '', content)    # Incomplete closing tags
    content = re.sub(r'</[^<>]*>', '', content)   # Any remaining closing tags
    
    # Remove any remaining angle brackets and fragments
    content = re.sub(r'[<>]', '', content)
    
    # Remove HTML entities completely
    content = re.sub(r'&[#a-zA-Z0-9]+;?', ' ', content)
    
    # Remove CSS/style attributes and values
    content = re.sub(r'style\s*=\s*["\'][^"\']*["\']', '', content, flags=re.IGNORECASE)
    content = re.sub(r'class\s*=\s*["\'][^"\']*["\']', '', content, flags=re.IGNORECASE)
    content = re.sub(r'id\s*=\s*["\'][^"\']*["\']', '', content, flags=re.IGNORECASE)
    
    # Remove common CSS properties that might leak through
    css_remnants = [
        r'background[^;]*;?', r'color[^;]*;?', r'margin[^;]*;?', r'padding[^;]*;?',
        r'font[^;]*;?', r'border[^;]*;?', r'display[^;]*;?', r'width[^;]*;?',
        r'height[^;]*;?', r'text-align[^;]*;?', r'position[^;]*;?'
    ]
    
    for pattern in css_remnants:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)
    
    # Remove quotes and brackets that might contain artifacts
    content = re.sub(r'["\'{}\[\]]', '', content)
    
    # Remove div, span, and other common HTML terms that might leak
    html_terms = ['div', 'span', 'p', 'h1', 'h2', 'h3', 'ul', 'li', 'br', 'hr']
    for term in html_terms:
        content = re.sub(rf'\b{term}\b', '', content, flags=re.IGNORECASE)
    
    # Normalize whitespace
    content = re.sub(r'\s+', ' ', content).strip()
    
    # Step 2: Extract clean meaningful text
    # Split into potential sentences
    parts = re.split(r'[.!?]\s+', content)
    clean_parts = []
    
    for part in parts[:20]:  # Check more parts
        part = part.strip()
        
        # Very strict filtering
        if (15 <= len(part) <= 500 and  # Reasonable length
            part.count(' ') >= 3 and     # At least 4 words
            not re.match(r'^[^a-zA-Z]*$', part) and  # Contains letters
            not re.search(r'\b(score|rating|cyber|ethics|assessment|badge|n/a)\b', part.lower()) and
            not re.search(r'^\d+$|^[A-Z]+$', part.strip()) and  # Not just numbers or caps
            any(c.islower() for c in part)):  # Contains lowercase letters
            
            clean_parts.append(part)
            if len(clean_parts) >= 2:  # Get 2 good sentences
                break
    
    # Step 3: Build final preview
    if clean_parts:
        result = '. '.join(clean_parts)
        if not result.endswith('.'):
            result += '.'
        
        # Truncate if too long
        if len(result) > 250:
            result = result[:247] + '...'
            
        return result
    
    # Ultimate fallback: word-by-word extraction
    words = content.split()
    good_words = []
    
    for word in words[:50]:
        # Only keep clearly readable words
        if (2 <= len(word) <= 20 and 
            word.isalpha() and 
            not re.search(r'^(div|span|style|class|score|rating)$', word.lower())):
            good_words.append(word)
            if len(good_words) >= 15:
                break
    
    if len(good_words) >= 8:
        return ' '.join(good_words) + '.'
    
    return "Preview unavailable"

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