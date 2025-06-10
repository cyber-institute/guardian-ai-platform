"""
Anthropic-based document analysis as alternative to OpenAI when quota exceeded
Uses Claude for intelligent metadata extraction when OpenAI is unavailable
"""

import os
import sys
import re
from typing import Dict, Optional
import anthropic
from anthropic import Anthropic

def analyze_document_with_anthropic(content: str, filename: str = "") -> Optional[Dict[str, Optional[str]]]:
    """
    Extract document metadata using Anthropic Claude when OpenAI is unavailable.
    
    Args:
        content: Full document text content
        filename: Original filename for context
        
    Returns:
        Dict with extracted metadata or None if analysis fails
    """
    
    try:
        # Initialize Anthropic client
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        if not anthropic_key:
            return None
            
        client = Anthropic(api_key=anthropic_key)
        
        # Create analysis prompt for document metadata extraction
        prompt = f"""Analyze this document and extract metadata in JSON format. Focus on identifying:

1. **Title**: The actual document title/publication name (not website names or navigation text)
2. **Organization**: The publishing organization/agency
3. **Publication Date**: When this document was published
4. **Document Type**: Choose from: Standard, Framework, Guideline, Policy, Report, Research, Whitepaper, Advisory, Regulation
5. **Content Preview**: A brief 2-3 sentence description of what this document covers

For government documents like NIST Special Publications, extract the formal publication title (e.g., "NIST Special Publication 800-63-3 Digital Identity Guidelines").

Document content:
{content[:2000]}

Filename context: {filename}

Return ONLY a JSON object with these exact keys: title, author_organization, publish_date, document_type, content_preview"""

        # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{
                "role": "user", 
                "content": prompt
            }]
        )
        
        # Parse the response
        if hasattr(response.content[0], 'text'):
            response_text = response.content[0].text.strip()
        else:
            response_text = str(response.content[0]).strip()
        
        # Extract JSON from response
        import json
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                metadata = json.loads(json_match.group())
                
                # Validate and clean the metadata
                return {
                    'title': validate_title(metadata.get('title', '')),
                    'author_organization': validate_organization(metadata.get('author_organization', '')),
                    'publish_date': validate_date(metadata.get('publish_date', '')),
                    'document_type': validate_document_type(metadata.get('document_type', 'Report')),
                    'content_preview': validate_preview(metadata.get('content_preview', ''))
                }
        except json.JSONDecodeError:
            pass
            
    except Exception as e:
        print(f"Anthropic analysis failed: {e}")
        
    return None

def validate_title(title: str) -> str:
    """Validate and clean extracted title."""
    if not title or len(title) < 5:
        return ""
    
    # Clean the title
    title = title.strip().strip('"').strip("'")
    title = re.sub(r'\s+', ' ', title)
    
    # Avoid generic titles
    if any(bad in title.lower() for bad in ['document', 'webpage', 'website', 'page', 'untitled']):
        return ""
        
    return title[:100]

def validate_organization(org: str) -> str:
    """Validate and clean organization name."""
    if not org or len(org) < 2:
        return "Unknown"
    
    org = org.strip().strip('"').strip("'")
    org = re.sub(r'\s+', ' ', org)
    
    return org[:80]

def validate_date(date_str: str) -> Optional[str]:
    """Validate and normalize date string."""
    if not date_str:
        return None
    
    date_str = date_str.strip().strip('"').strip("'")
    
    # Try to extract year and format consistently
    year_match = re.search(r'(\d{4})', date_str)
    if year_match:
        year = int(year_match.group(1))
        if 2000 <= year <= 2025:
            return f"{year}-01-01"
    
    return None

def validate_document_type(doc_type: str) -> str:
    """Validate document type against allowed values."""
    if not doc_type:
        return 'Report'
    
    doc_type = doc_type.strip().strip('"').strip("'")
    
    valid_types = [
        'Standard', 'Framework', 'Guideline', 'Policy', 'Report', 
        'Research', 'Whitepaper', 'Advisory', 'Regulation'
    ]
    
    # Check for exact match
    if doc_type in valid_types:
        return doc_type
    
    # Check for case-insensitive match
    for valid_type in valid_types:
        if doc_type.lower() == valid_type.lower():
            return valid_type
    
    return 'Report'

def validate_preview(preview: str) -> str:
    """Validate and clean content preview."""
    if not preview:
        return ""
    
    preview = preview.strip().strip('"').strip("'")
    preview = re.sub(r'\s+', ' ', preview)
    
    return preview[:300]