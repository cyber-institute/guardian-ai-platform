"""
Fast Scoring System for GUARDIAN
Provides instant scoring without expensive computation
"""

def fast_document_scoring(doc):
    """Fast scoring that uses only database values for instant loading"""
    scores = {}
    
    # Use existing database scores directly
    ai_cyber = doc.get('ai_cybersecurity_score', 0)
    quantum_cyber = doc.get('quantum_cybersecurity_score', 0)
    ai_ethics = doc.get('ai_ethics_score', 0)
    quantum_ethics = doc.get('quantum_ethics_score', 0)
    
    # Return scores as-is from database for fastest performance
    scores['ai_cybersecurity'] = ai_cyber if ai_cyber and ai_cyber > 0 else 'N/A'
    scores['quantum_cybersecurity'] = quantum_cyber if quantum_cyber and quantum_cyber > 0 else 'N/A'
    scores['ai_ethics'] = ai_ethics if ai_ethics and ai_ethics > 0 else 'N/A'
    scores['quantum_ethics'] = quantum_ethics if quantum_ethics and quantum_ethics > 0 else 'N/A'
    
    return scores

def is_ai_document(doc):
    """Quick AI detection based on title and type"""
    title = (doc.get('title', '') or '').lower()
    doc_type = (doc.get('document_type', '') or '').lower()
    
    ai_keywords = ['artificial intelligence', 'ai ', 'machine learning', 'neural', 'algorithm']
    return any(keyword in title or keyword in doc_type for keyword in ai_keywords)

def is_quantum_document(doc):
    """Quick quantum detection based on title and type"""
    title = (doc.get('title', '') or '').lower()
    doc_type = (doc.get('document_type', '') or '').lower()
    
    quantum_keywords = ['quantum', 'cryptography', 'encryption']
    return any(keyword in title or keyword in doc_type for keyword in quantum_keywords)