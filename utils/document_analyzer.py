"""
Intelligent Document Analysis System for GUARDIAN
Uses OpenAI LLM with Anthropic fallback to extract metadata and generate meaningful content previews
"""

import json
import os
import re
from typing import Dict, Optional, Tuple, Union
from openai import OpenAI
from utils.anthropic_analyzer import analyze_document_with_anthropic
from utils.fallback_analyzer import extract_metadata_fallback

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_document_metadata(content: str, filename: str = "") -> Dict[str, Optional[str]]:
    """
    Extract comprehensive metadata from document content using OpenAI.
    
    Args:
        content: Full document text content
        filename: Original filename for context
        
    Returns:
        Dict with extracted metadata: title, author_organization, publish_date, document_type, content_preview
    """
    if not content or len(content.strip()) < 50:
        return {
            'title': filename or 'Untitled Document',
            'author_organization': 'Unknown',
            'publish_date': None,
            'document_type': 'Unknown',
            'content_preview': 'Insufficient content for analysis'
        }
    
    try:
        prompt = f"""
        You are an expert document analyst specializing in government, academic, and policy documents. 
        Analyze the following document and extract key metadata. Focus on accuracy and intelligently 
        interpreting the document structure regardless of formatting.

        Document content:
        {content[:4000]}  # Limit to first 4000 chars for API efficiency

        Extract the following information and respond with ONLY valid JSON:
        {{
            "title": "The actual document title (not filename or first sentence)",
            "author_organization": "Primary organization/agency (e.g., NIST, NSA, NASA, White House, EU, etc.)",
            "publish_date": "Publication date in YYYY-MM-DD format or null if not found",
            "document_type": "One of: Policy, Standard, Strategy, Framework, Guideline, Report, Research, Whitepaper, Regulation, Directive",
            "content_preview": "Intelligent 2-3 sentence summary of key content and purpose"
        }}

        Guidelines:
        - For title: Look for actual document titles in headers, not filenames
        - For author_organization: Focus on institutional authors, not individual names
        - For publish_date: Look for publication dates, not revision dates
        - For document_type: Classify based on content purpose and structure
        - For content_preview: Provide substantive summary, not just introduction text
        """

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=500
        )
        
        content_result = response.choices[0].message.content
        if not content_result:
            raise ValueError("Empty response from OpenAI")
        result = json.loads(content_result)
        
        # Validate and clean results
        validated_result = {
            'title': result.get('title', filename or 'Untitled Document')[:200],
            'author_organization': result.get('author_organization', 'Unknown')[:100],
            'publish_date': validate_date(result.get('publish_date')),
            'document_type': validate_document_type(result.get('document_type', 'Unknown')),
            'content_preview': result.get('content_preview', 'Analysis not available')[:500]
        }
        
        return validated_result
        
    except Exception as e:
        print(f"Error in document analysis: {e}")
        return {
            'title': filename or 'Analysis Error',
            'author_organization': 'Unknown',
            'publish_date': None,
            'document_type': 'Unknown',
            'content_preview': f'Error analyzing document: {str(e)[:100]}'
        }

def validate_date(date_str: Optional[str]) -> Optional[str]:
    """Validate and format date string."""
    if not date_str or date_str.lower() == 'null':
        return None
    
    # Basic date validation
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(date_pattern, date_str):
        return date_str
    
    return None

def validate_document_type(doc_type: str) -> str:
    """Validate document type against allowed values."""
    valid_types = [
        'Policy', 'Standard', 'Strategy', 'Framework', 'Guideline', 
        'Report', 'Research', 'Whitepaper', 'Regulation', 'Directive'
    ]
    
    if doc_type in valid_types:
        return doc_type
    
    # Try to match partial or case-insensitive
    doc_type_lower = doc_type.lower()
    for valid_type in valid_types:
        if doc_type_lower in valid_type.lower() or valid_type.lower() in doc_type_lower:
            return valid_type
    
    return 'Unknown'

def extract_document_summary(content: str, title: str = "") -> str:
    """
    Generate intelligent document summary for preview purposes.
    
    Args:
        content: Document content
        title: Document title for context
        
    Returns:
        Meaningful summary string
    """
    if not content or len(content.strip()) < 50:
        return "Insufficient content for summary generation"
    
    try:
        prompt = f"""
        Create a concise, informative summary of this document's key points and purpose.
        Focus on the substantive content rather than introductory material.
        
        Document title: {title}
        Content: {content[:3000]}
        
        Provide a 2-3 sentence summary that captures:
        1. The document's main purpose or objective
        2. Key findings, recommendations, or requirements
        3. Target audience or scope
        
        Keep it professional and factual.
        """
        
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=200
        )
        
        result_content = response.choices[0].message.content
        if result_content:
            return result_content.strip()
        else:
            return "Summary generation failed"
        
    except Exception as e:
        return f"Summary generation error: {str(e)[:100]}"

def batch_analyze_documents(documents: list) -> list:
    """
    Analyze multiple documents efficiently.
    
    Args:
        documents: List of document dicts with 'content' and optional 'filename'
        
    Returns:
        List of documents with added metadata
    """
    analyzed_docs = []
    
    for doc in documents:
        content = doc.get('content', '') or doc.get('text_content', '')
        filename = doc.get('filename', doc.get('title', ''))
        
        metadata = analyze_document_metadata(content, filename)
        
        # Update document with analyzed metadata
        updated_doc = doc.copy()
        updated_doc.update({
            'analyzed_title': metadata['title'],
            'analyzed_author': metadata['author_organization'],
            'analyzed_date': metadata['publish_date'],
            'analyzed_type': metadata['document_type'],
            'analyzed_preview': metadata['content_preview']
        })
        
        analyzed_docs.append(updated_doc)
    
    return analyzed_docs