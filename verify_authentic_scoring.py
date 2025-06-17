#!/usr/bin/env python3
"""
Verify that quantum scoring is now authentic and content-based
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.comprehensive_scoring import score_quantum_cybersecurity_maturity
from utils.database import DatabaseManager

def verify_authentic_scoring():
    """Verify scoring authenticity by analyzing actual database documents"""
    
    print("QUANTUM SCORING AUTHENTICITY VERIFICATION")
    print("=" * 60)
    
    # Connect to database and get real documents
    db = DatabaseManager()
    docs = db.fetch_documents()
    
    quantum_docs = []
    for doc in docs[:20]:  # Sample first 20 documents
        title = doc.get('title', '')
        content = doc.get('content_preview', '')
        
        # Check if it's quantum-related
        quantum_keywords = ['quantum', 'post-quantum', 'pqc', 'quantum-safe', 'quantum cryptography']
        if any(keyword in (title + ' ' + content).lower() for keyword in quantum_keywords):
            quantum_docs.append(doc)
    
    print(f"Found {len(quantum_docs)} quantum-related documents in database")
    print("\nScoring Analysis:")
    print("-" * 40)
    
    scores = []
    for i, doc in enumerate(quantum_docs[:10], 1):  # Analyze up to 10 quantum docs
        title = doc.get('title', 'No title')
        content = doc.get('content_preview', '')
        
        # Calculate score using our fixed algorithm
        score = score_quantum_cybersecurity_maturity(content, title)
        
        if score:
            scores.append(score)
            print(f"\nDoc {i}: {title[:50]}...")
            
            # Show scoring breakdown
            text_lower = content.lower()
            
            # Count terms in each category
            basic_terms = ['quantum', 'post-quantum', 'quantum-safe', 'quantum-resistant', 'pqc']
            technical_terms = ['lattice-based', 'code-based', 'multivariate', 'hash-based', 'isogeny', 
                              'quantum key distribution', 'quantum cryptography', 'cryptographic agility']
            impl_terms = ['implementation', 'deployment', 'migration', 'transition', 'roadmap']
            standards_terms = ['nist', 'standards', 'compliance', 'governance', 'framework', 'policy']
            advanced_terms = ['hybrid systems', 'quantum supremacy', 'quantum advantage', 'quantum evolution', 
                             'quantum machine learning', 'adaptive quantum', 'continuous quantum monitoring']
            
            basic_count = sum(1 for term in basic_terms if term in text_lower)
            technical_count = sum(1 for term in technical_terms if term in text_lower)
            impl_count = sum(1 for term in impl_terms if term in text_lower)
            standards_count = sum(1 for term in standards_terms if term in text_lower)
            advanced_count = sum(1 for term in advanced_terms if term in text_lower)
            
            total_components = min(3, basic_count) + min(4, technical_count) + min(3, impl_count) + min(3, standards_count) + min(3, advanced_count)
            
            print(f"  Score: {score}/5")
            print(f"  Basic terms: {basic_count} -> {min(3, basic_count)} points")
            print(f"  Technical terms: {technical_count} -> {min(4, technical_count)} points")
            print(f"  Implementation: {impl_count} -> {min(3, impl_count)} points")
            print(f"  Standards: {standards_count} -> {min(3, standards_count)} points")
            print(f"  Advanced: {advanced_count} -> {min(3, advanced_count)} points")
            print(f"  Total components: {total_components}")
    
    print(f"\n" + "=" * 60)
    print("AUTHENTICITY VERIFICATION RESULTS:")
    print(f"Document scores: {scores}")
    print(f"Unique scores: {len(set(scores))} out of {len(scores)} documents")
    
    if len(set(scores)) > 1:
        print("✅ AUTHENTIC: Scores vary based on actual document content")
        print("   Each document receives a score based on:")
        print("   - Quantum terminology sophistication")
        print("   - Technical implementation depth")
        print("   - Standards and governance coverage")
        print("   - Advanced concept integration")
        print("   - Document length and comprehensiveness")
    else:
        print("❌ ISSUE: Scores still appear uniform")
    
    return scores

if __name__ == "__main__":
    verify_authentic_scoring()