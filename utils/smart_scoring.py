"""
Smart Scoring System with Caching
Combines database scores with intelligent caching for maximum performance
"""

import streamlit as st
from typing import Dict, Optional
from utils.score_cache import score_cache

def get_smart_scores(doc: Dict) -> Dict:
    """Get scores using cache-first strategy for maximum performance"""
    doc_id = doc.get('id', '')
    title = doc.get('title', '')
    content_preview = doc.get('content_preview', '')
    
    # First, try to get cached scores
    cached_scores = score_cache.get_cached_scores(doc_id, title, content_preview)
    if cached_scores:
        return cached_scores
    
    # If not cached, use database scores directly for speed
    scores = {
        'ai_cybersecurity': doc.get('ai_cybersecurity_score') or 'N/A',
        'quantum_cybersecurity': doc.get('quantum_cybersecurity_score') or 'N/A', 
        'ai_ethics': doc.get('ai_ethics_score') or 'N/A',
        'quantum_ethics': doc.get('quantum_ethics_score') or 'N/A'
    }
    
    # Cache the scores for next time
    score_cache.cache_scores(doc_id, title, content_preview, scores)
    
    return scores

def is_ai_related_fast(doc: Dict) -> bool:
    """Fast AI detection based on title and metadata only"""
    title = (doc.get('title', '') or '').lower()
    doc_type = (doc.get('document_type', '') or '').lower()
    
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'neural', 'algorithm']
    return any(keyword in title or keyword in doc_type for keyword in ai_keywords)

def is_quantum_related_fast(doc: Dict) -> bool:
    """Fast quantum detection based on title and metadata only"""
    title = (doc.get('title', '') or '').lower()
    doc_type = (doc.get('document_type', '') or '').lower()
    
    quantum_keywords = ['quantum', 'cryptography', 'encryption']
    return any(keyword in title or keyword in doc_type for keyword in quantum_keywords)

def apply_topic_filtering(scores: Dict, doc: Dict) -> Dict:
    """Apply N/A logic based on document relevance"""
    is_ai = is_ai_related_fast(doc)
    is_quantum = is_quantum_related_fast(doc)
    
    # Only show scores for relevant topics
    if not is_ai:
        scores['ai_cybersecurity'] = 'N/A'
        scores['ai_ethics'] = 'N/A'
    
    if not is_quantum:
        scores['quantum_cybersecurity'] = 'N/A'
        scores['quantum_ethics'] = 'N/A'
    
    return scores