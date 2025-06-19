#!/usr/bin/env python3
"""
Fix missing AI Ethics scores for AI-focused documents
"""

import os
import psycopg2
from datetime import datetime

def enhanced_ai_ethics_scoring(content, title):
    """Enhanced AI ethics scoring with comprehensive analysis"""
    if not content or len(content) < 100:
        return 0
        
    content_lower = content.lower()
    title_lower = title.lower() if title else ""
    
    # Core AI ethics indicators with weights
    ethics_indicators = {
        'ai ethics': 12,
        'artificial intelligence ethics': 12,
        'ethical ai': 10,
        'ai governance': 8,
        'ai fairness': 8,
        'algorithmic bias': 8,
        'ai transparency': 6,
        'ai accountability': 6,
        'responsible ai': 6,
        'ai human rights': 6,
        'ai dignity': 5,
        'ai justice': 5,
        'ai equity': 5,
        'ai inclusion': 5,
        'ai diversity': 4,
        'ai discrimination': 6,
        'ai privacy': 5,
        'ai autonomy': 4,
        'ai values': 4,
        'ai principles': 4,
        'bias detection': 5,
        'fairness testing': 5,
        'ethical considerations': 4,
        'responsible development': 4,
        'ai safety': 5,
        'trustworthy ai': 6
    }
    
    score = 0
    matched_terms = []
    
    # Check content for indicators
    for term, weight in ethics_indicators.items():
        count = content_lower.count(term)
        if count > 0:
            term_score = min(weight * count, weight * 2)  # Cap at 2x weight
            score += term_score
            matched_terms.append(f"{term}({count})")
    
    # Title boosts for AI-focused documents
    if any(term in title_lower for term in ['ai', 'artificial intelligence']):
        score += 8
        matched_terms.append("ai_title_boost")
    
    # Security-focused AI documents often have ethics components
    if any(term in title_lower for term in ['security', 'secure', 'cybersecurity']):
        score += 5
        matched_terms.append("security_ethics_boost")
    
    # Red teaming and evaluation documents
    if any(term in title_lower for term in ['red team', 'evaluation', 'testing']):
        score += 6
        matched_terms.append("evaluation_ethics_boost")
    
    # Deployment and guidance documents
    if any(term in title_lower for term in ['deploy', 'guidance', 'playbook', 'principles']):
        score += 5
        matched_terms.append("guidance_ethics_boost")
    
    # Cap at 100
    score = min(score, 100)
    
    return score, matched_terms

def fix_missing_ethics_scores():
    """Fix missing AI Ethics scores for AI documents"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        # Get documents missing AI Ethics scores but have AI Cybersecurity scores
        cursor.execute("""
            SELECT id, title, content, text_content, ai_cybersecurity_score
            FROM documents 
            WHERE ai_cybersecurity_score IS NOT NULL 
            AND ai_cybersecurity_score > 0
            AND (ai_ethics_score IS NULL OR ai_ethics_score = 0)
            ORDER BY id
        """)
        
        documents = cursor.fetchall()
        
        print(f"Found {len(documents)} documents missing AI Ethics scores")
        
        for doc_id, title, content, text_content, ai_cyber_score in documents:
            print(f"\nProcessing: {title[:60]}...")
            
            # Use text_content if available, otherwise content
            scoring_content = text_content if text_content else content
            
            if not scoring_content or len(scoring_content) < 100:
                print("  Insufficient content for scoring")
                continue
                
            # Calculate AI Ethics score
            ai_ethics_score, matched_terms = enhanced_ai_ethics_scoring(scoring_content, title)
            
            if ai_ethics_score > 0:
                # Update database
                cursor.execute("""
                    UPDATE documents 
                    SET ai_ethics_score = %s,
                        topic = 'AI',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (ai_ethics_score, doc_id))
                
                print(f"  Updated: AI Ethics Score = {ai_ethics_score}")
                print(f"  Matched terms: {matched_terms[:5]}...")  # Show first 5 terms
            else:
                print("  No significant ethics content found")
        
        conn.commit()
        print(f"\nSuccessfully processed {len(documents)} documents")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_missing_ethics_scores()