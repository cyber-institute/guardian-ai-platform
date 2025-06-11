#!/usr/bin/env python3
"""
Trigger Multi-LLM comprehensive scoring for documents
"""

import sys
import os
sys.path.append('.')

from utils.comprehensive_scoring import comprehensive_document_scoring
from utils.db import fetch_documents
from utils.database import db_manager

def rescore_documents_with_multi_llm():
    """Re-score documents using the new Multi-LLM integration"""
    
    print("Fetching documents for Multi-LLM re-scoring...")
    documents = fetch_documents()
    
    # Focus on documents with cleared scores
    target_docs = [doc for doc in documents if doc['id'] in [10, 12, 13]]
    
    print(f"Re-scoring {len(target_docs)} documents with Multi-LLM ensemble...")
    
    for doc in target_docs:
        print(f"\nProcessing document {doc['id']}: {doc['title'][:50]}...")
        
        # Get document content
        text_content = doc.get('text', '') or doc.get('content', '')
        title = doc.get('title', '')
        
        if not text_content:
            print(f"  Skipping - no content available")
            continue
            
        # Score with new Multi-LLM system
        scores = comprehensive_document_scoring(text_content, title)
        
        print(f"  New scores: {scores}")
        
        # Update database with new scores using direct SQL execution
        from utils.database import db_manager
        
        update_query = """
        UPDATE documents 
        SET ai_cybersecurity_score = %s,
            quantum_cybersecurity_score = %s,
            ai_ethics_score = %s,
            quantum_ethics_score = %s
        WHERE id = %s
        """
        
        result = db_manager.execute_query(update_query, (
            scores.get('ai_cybersecurity'),
            scores.get('quantum_cybersecurity'),
            scores.get('ai_ethics'),
            scores.get('quantum_ethics'),
            doc['id']
        ))
        
        if result:
            print(f"  Updated database successfully")
        else:
            print(f"  Database update failed")
    
    print("\nMulti-LLM re-scoring completed!")

if __name__ == "__main__":
    rescore_documents_with_multi_llm()