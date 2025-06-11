"""
Comprehensive Metadata Cleaner
Ensures all document metadata is completely free of HTML artifacts
"""

import re
from typing import Dict, Any, List

def clean_metadata_field(value: Any) -> str:
    """Clean any metadata field of HTML artifacts completely"""
    if not value or value in [None, 'None', 'null']:
        return 'Unknown'
    
    text = str(value).strip()
    
    if not text or text.lower() in ['none', 'null', 'undefined', '']:
        return 'Unknown'
    
    # Multiple aggressive cleaning passes
    for _ in range(5):
        # Remove all HTML tags
        text = re.sub(r'<[^>]*>', '', text)
        text = re.sub(r'</[^>]*>', '', text)
        text = re.sub(r'<[^>]*', '', text)
        text = re.sub(r'[^<]*>', '', text)
    
    # Remove HTML entities
    text = re.sub(r'&[#a-zA-Z0-9]+;?', '', text)
    
    # Remove specific artifacts
    artifacts = [
        '</div>', '<div>', 'div>', '/div>', 'div', '</span>', '<span>', 
        'span>', '/span/', 'span', '</p>', '<p>', 'p>', '/p/', 
        '&nbsp;', '&amp;', '&lt;', '&gt;', '&quot;', '&#39;'
    ]
    
    for artifact in artifacts:
        text = text.replace(artifact, ' ')
    
    # Remove any remaining HTML-like patterns
    text = re.sub(r'[<>"\'`]', '', text)
    text = re.sub(r'[/\\]', ' ', text)
    
    # Clean whitespace
    text = ' '.join(text.split()).strip()
    
    if not text or len(text) < 2:
        return 'Unknown'
    
    return text

def clean_all_document_fields(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Clean all string fields in a document dictionary"""
    cleaned_doc = doc.copy()
    
    # Fields that need cleaning
    metadata_fields = [
        'title', 'author_organization', 'document_type', 'source',
        'content_preview', 'organization'
    ]
    
    for field in metadata_fields:
        if field in cleaned_doc:
            cleaned_doc[field] = clean_metadata_field(cleaned_doc[field])
    
    # Handle publish_date specially
    if 'publish_date' in cleaned_doc:
        raw_date = cleaned_doc['publish_date']
        if raw_date and str(raw_date).strip():
            cleaned_date = clean_metadata_field(raw_date)
            if cleaned_date != 'Unknown' and len(cleaned_date) > 3:
                cleaned_doc['publish_date'] = cleaned_date
            else:
                cleaned_doc['publish_date'] = 'Date not available'
        else:
            cleaned_doc['publish_date'] = 'Date not available'
    
    return cleaned_doc

def clean_document_list(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Clean all documents in a list"""
    return [clean_all_document_fields(doc) for doc in documents]