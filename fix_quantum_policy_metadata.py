#!/usr/bin/env python3
"""
Fix metadata extraction for the quantum policy document
Apply comprehensive scoring and correct metadata
"""

import os
import psycopg2
from datetime import datetime

def fix_quantum_policy_document():
    """Fix the quantum policy document metadata and scoring"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        # Get the document content for analysis
        cursor.execute("""
            SELECT id, title, content, text_content, author_organization, document_type, publish_date
            FROM documents 
            WHERE id = 64
        """)
        
        result = cursor.fetchone()
        if not result:
            print("Document ID 64 not found")
            return
            
        doc_id, title, content, text_content, org, doc_type, pub_date = result
        
        print(f"Current metadata for document {doc_id}:")
        print(f"Title: {title}")
        print(f"Organization: {org}")
        print(f"Document Type: {doc_type}")
        print(f"Publish Date: {pub_date}")
        
        # Use text_content if available, otherwise content
        scoring_content = text_content if text_content else content
        
        if not scoring_content:
            print("No content available for analysis")
            return
            
        # Extract better metadata from content
        content_sample = scoring_content[:2000].lower()
        
        # Fix the title to include the full name
        full_title = "Regulating Transformative Technology in The Quantum Age: Intellectual Property, Standardization & Sustainable Innovation"
        
        # Determine organization from content analysis
        organization = "Unknown"
        if "european" in content_sample or "eu " in content_sample:
            organization = "European Union"
        elif "united nations" in content_sample or "un " in content_sample:
            organization = "United Nations"
        elif "ieee" in content_sample:
            organization = "IEEE"
        elif "wipo" in content_sample:
            organization = "WIPO"
        elif "oecd" in content_sample:
            organization = "OECD"
        
        # Better document type classification
        doc_type_new = "Policy Framework"
        if "regulation" in content_sample and "policy" in content_sample:
            doc_type_new = "Regulatory Policy"
        elif "framework" in content_sample:
            doc_type_new = "Policy Framework"
        elif "standard" in content_sample:
            doc_type_new = "Technical Standard"
        
        # Calculate comprehensive scores
        ai_cyber_score = calculate_ai_cybersecurity_score(scoring_content, full_title)
        ai_ethics_score = calculate_ai_ethics_score(scoring_content, full_title)
        q_cyber_score = calculate_quantum_cybersecurity_score(scoring_content, full_title)
        q_ethics_score = calculate_quantum_ethics_score(scoring_content, full_title)
        
        # Determine topic based on scores and content
        topic = "Quantum"
        if ai_cyber_score > 30 or ai_ethics_score > 25:
            if q_cyber_score > 30 or q_ethics_score > 20:
                topic = "Both"
            else:
                topic = "AI"
        elif q_cyber_score > 20 or q_ethics_score > 15:
            topic = "Quantum"
        else:
            topic = "General"
        
        # Update the document with corrected metadata and scores
        cursor.execute("""
            UPDATE documents 
            SET title = %s,
                author_organization = %s,
                document_type = %s,
                ai_cybersecurity_score = %s,
                ai_ethics_score = %s,
                quantum_cybersecurity_score = %s,
                quantum_ethics_score = %s,
                topic = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (full_title, organization, doc_type_new, ai_cyber_score, ai_ethics_score, 
              q_cyber_score, q_ethics_score, topic, doc_id))
        
        conn.commit()
        
        print(f"\nDocument updated successfully:")
        print(f"New Title: {full_title}")
        print(f"Organization: {organization}")
        print(f"Document Type: {doc_type_new}")
        print(f"AI Cybersecurity Score: {ai_cyber_score}")
        print(f"AI Ethics Score: {ai_ethics_score}")
        print(f"Quantum Cybersecurity Score: {q_cyber_score}")
        print(f"Quantum Ethics Score: {q_ethics_score}")
        print(f"Topic: {topic}")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def calculate_ai_cybersecurity_score(content, title):
    """Calculate AI cybersecurity score for the document"""
    content_lower = content.lower()
    title_lower = title.lower()
    
    indicators = {
        'artificial intelligence': 10,
        'ai governance': 8,
        'ai regulation': 8,
        'ai security': 10,
        'ai risk': 6,
        'ai standardization': 8,
        'ai compliance': 6,
        'ai oversight': 6,
        'algorithmic': 5,
        'machine learning': 4,
        'transformative technology': 8
    }
    
    score = 0
    for term, weight in indicators.items():
        count = content_lower.count(term)
        if count > 0:
            score += min(weight * count, weight * 2)
    
    # Title boost for transformative technology
    if 'transformative technology' in title_lower:
        score += 15
    
    return min(score, 100)

def calculate_ai_ethics_score(content, title):
    """Calculate AI ethics score for the document"""
    content_lower = content.lower()
    title_lower = title.lower()
    
    indicators = {
        'ai ethics': 12,
        'ai governance': 8,
        'ai regulation': 8,
        'ethical ai': 10,
        'responsible ai': 8,
        'ai transparency': 6,
        'ai accountability': 6,
        'ai fairness': 6,
        'sustainable innovation': 8,
        'standardization': 6,
        'intellectual property': 5
    }
    
    score = 0
    for term, weight in indicators.items():
        count = content_lower.count(term)
        if count > 0:
            score += min(weight * count, weight * 2)
    
    # Title boost for sustainable innovation
    if 'sustainable innovation' in title_lower:
        score += 10
    
    return min(score, 100)

def calculate_quantum_cybersecurity_score(content, title):
    """Calculate quantum cybersecurity score for the document"""
    content_lower = content.lower()
    title_lower = title.lower()
    
    indicators = {
        'quantum technology': 12,
        'quantum computing': 10,
        'quantum cryptography': 15,
        'quantum security': 12,
        'post-quantum': 12,
        'quantum-safe': 10,
        'quantum threat': 8,
        'quantum algorithm': 6,
        'quantum supremacy': 8,
        'quantum age': 10,
        'quantum regulation': 10,
        'quantum standardization': 8
    }
    
    score = 0
    for term, weight in indicators.items():
        count = content_lower.count(term)
        if count > 0:
            score += min(weight * count, weight * 2)
    
    # Major title boost for quantum age
    if 'quantum age' in title_lower:
        score += 20
    
    return min(score, 100)

def calculate_quantum_ethics_score(content, title):
    """Calculate quantum ethics score for the document"""
    content_lower = content.lower()
    title_lower = title.lower()
    
    indicators = {
        'quantum ethics': 15,
        'quantum governance': 12,
        'quantum policy': 10,
        'quantum regulation': 10,
        'quantum standardization': 8,
        'sustainable innovation': 8,
        'intellectual property': 6,
        'quantum development': 6,
        'quantum future': 6,
        'quantum society': 8,
        'responsible quantum': 10,
        'quantum age': 8
    }
    
    score = 0
    for term, weight in indicators.items():
        count = content_lower.count(term)
        if count > 0:
            score += min(weight * count, weight * 2)
    
    # Title boost for sustainable innovation in quantum context
    if 'quantum age' in title_lower and 'sustainable innovation' in title_lower:
        score += 15
    
    return min(score, 100)

if __name__ == "__main__":
    fix_quantum_policy_document()