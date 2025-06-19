#!/usr/bin/env python3
"""
Fix UNESCO AI Ethics document scoring
Apply comprehensive AI scoring to the UNESCO document
"""

import os
import sys
import psycopg2
from datetime import datetime

# Add utils to path
sys.path.append('utils')

try:
    from multi_llm_scoring_engine import MultiLLMScoringEngine
    from comprehensive_scoring import comprehensive_document_scoring
except ImportError:
    print("Using fallback scoring methods...")
    
def enhanced_ai_cybersecurity_scoring(content, title):
    """Enhanced AI cybersecurity scoring with comprehensive analysis"""
    if not content or len(content) < 100:
        return 0
        
    content_lower = content.lower()
    title_lower = title.lower() if title else ""
    
    # Core AI cybersecurity indicators
    security_indicators = {
        'ai security': 15,
        'artificial intelligence security': 15,
        'ai governance': 12,
        'ai risk': 12,
        'algorithmic bias': 10,
        'ai ethics': 10,
        'ai safety': 10,
        'machine learning security': 8,
        'ai transparency': 8,
        'ai accountability': 8,
        'ai fairness': 8,
        'ai robustness': 6,
        'ai privacy': 6,
        'ai explainability': 6,
        'responsible ai': 6,
        'ai regulation': 5,
        'ai standards': 5,
        'ai compliance': 5
    }
    
    score = 0
    matched_terms = []
    
    # Check content for indicators
    for term, weight in security_indicators.items():
        count = content_lower.count(term)
        if count > 0:
            term_score = min(weight * count, weight * 3)  # Cap at 3x weight
            score += term_score
            matched_terms.append(f"{term}({count})")
    
    # Boost for ethics-focused AI documents
    if 'ethics' in title_lower and 'artificial intelligence' in title_lower:
        score += 20
        matched_terms.append("ethics_ai_title_boost")
    
    # UNESCO authoritative boost
    if 'unesco' in title_lower or 'unesco' in content_lower:
        score += 15
        matched_terms.append("unesco_authority_boost")
    
    # Cap at 100
    score = min(score, 100)
    
    print(f"AI Cybersecurity Score: {score}")
    print(f"Matched terms: {matched_terms}")
    
    return score

def enhanced_ai_ethics_scoring(content, title):
    """Enhanced AI ethics scoring with comprehensive analysis"""
    if not content or len(content) < 100:
        return 0
        
    content_lower = content.lower()
    title_lower = title.lower() if title else ""
    
    # Core AI ethics indicators
    ethics_indicators = {
        'ai ethics': 15,
        'artificial intelligence ethics': 15,
        'ethical ai': 12,
        'ai governance': 10,
        'ai fairness': 10,
        'algorithmic bias': 10,
        'ai transparency': 8,
        'ai accountability': 8,
        'responsible ai': 8,
        'ai human rights': 8,
        'ai dignity': 6,
        'ai justice': 6,
        'ai equity': 6,
        'ai inclusion': 6,
        'ai diversity': 5,
        'ai discrimination': 8,
        'ai privacy': 6,
        'ai autonomy': 5,
        'ai values': 5,
        'ai principles': 5
    }
    
    score = 0
    matched_terms = []
    
    # Check content for indicators
    for term, weight in ethics_indicators.items():
        count = content_lower.count(term)
        if count > 0:
            term_score = min(weight * count, weight * 3)  # Cap at 3x weight
            score += term_score
            matched_terms.append(f"{term}({count})")
    
    # Major boost for ethics-focused AI documents
    if 'ethics' in title_lower and 'artificial intelligence' in title_lower:
        score += 25
        matched_terms.append("ethics_ai_title_major_boost")
    
    # UNESCO authoritative boost for ethics
    if 'unesco' in title_lower or 'unesco' in content_lower:
        score += 20
        matched_terms.append("unesco_ethics_authority_boost")
    
    # Cap at 100
    score = min(score, 100)
    
    print(f"AI Ethics Score: {score}")
    print(f"Matched terms: {matched_terms}")
    
    return score

def fix_unesco_scoring():
    """Fix UNESCO document scoring"""
    
    # Connect to database
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        # Get UNESCO document
        cursor.execute("""
            SELECT id, title, content, text_content
            FROM documents 
            WHERE id = 63
        """)
        
        result = cursor.fetchone()
        if not result:
            print("UNESCO document not found")
            return
            
        doc_id, title, content, text_content = result
        
        print(f"Processing UNESCO document: {title}")
        print(f"Content length: {len(content) if content else 0}")
        print(f"Text content length: {len(text_content) if text_content else 0}")
        
        # Use text_content if available, otherwise content
        scoring_content = text_content if text_content else content
        
        if not scoring_content or len(scoring_content) < 100:
            print("Insufficient content for scoring")
            return
            
        # Calculate AI scores
        ai_cyber_score = enhanced_ai_cybersecurity_scoring(scoring_content, title)
        ai_ethics_score = enhanced_ai_ethics_scoring(scoring_content, title)
        
        # Update database
        cursor.execute("""
            UPDATE documents 
            SET ai_cybersecurity_score = %s,
                ai_ethics_score = %s,
                topic = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (ai_cyber_score, ai_ethics_score, 'AI', doc_id))
        
        conn.commit()
        
        print(f"\nSuccessfully updated UNESCO document:")
        print(f"AI Cybersecurity Score: {ai_cyber_score}")
        print(f"AI Ethics Score: {ai_ethics_score}")
        print(f"Topic: AI")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_unesco_scoring()