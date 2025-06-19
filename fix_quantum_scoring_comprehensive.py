#!/usr/bin/env python3
"""
Comprehensive Quantum Scoring System Fix
Apply enhanced quantum scoring to all relevant documents
"""

import os
import psycopg2
from datetime import datetime

def enhanced_quantum_cybersecurity_scoring(content, title):
    """Enhanced quantum cybersecurity scoring with comprehensive analysis"""
    if not content or len(content) < 100:
        return 0
        
    content_lower = content.lower()
    title_lower = title.lower() if title else ""
    
    # Core quantum cybersecurity indicators
    quantum_security_indicators = {
        'quantum cryptography': 15,
        'quantum security': 15,
        'quantum-safe': 12,
        'post-quantum cryptography': 12,
        'quantum key distribution': 10,
        'quantum-resistant': 10,
        'quantum computing security': 10,
        'quantum threat': 8,
        'quantum-proof': 8,
        'quantum encryption': 8,
        'quantum vulnerability': 6,
        'quantum attack': 6,
        'quantum algorithm': 5,
        'quantum supremacy': 5,
        'quantum advantage': 5,
        'shor algorithm': 8,
        'grover algorithm': 6,
        'quantum entanglement': 4,
        'quantum superposition': 4,
        'qubits': 3
    }
    
    score = 0
    matched_terms = []
    
    # Check content for quantum security indicators
    for term, weight in quantum_security_indicators.items():
        count = content_lower.count(term)
        if count > 0:
            term_score = min(weight * count, weight * 2)  # Cap at 2x weight
            score += term_score
            matched_terms.append(f"{term}({count})")
    
    # Title boosts for quantum-focused documents
    if any(term in title_lower for term in ['quantum', 'post-quantum']):
        score += 10
        matched_terms.append("quantum_title_boost")
    
    # National security context boost
    if any(term in content_lower for term in ['national security', 'nsm-', 'national security memorandum']):
        score += 8
        matched_terms.append("national_security_boost")
    
    # Technology regulation context
    if any(term in title_lower for term in ['regulating', 'transformative technology', 'intellectual property']):
        score += 12
        matched_terms.append("regulation_tech_boost")
    
    # Cap at 100
    score = min(score, 100)
    
    return score, matched_terms

def enhanced_quantum_ethics_scoring(content, title):
    """Enhanced quantum ethics scoring with comprehensive analysis"""
    if not content or len(content) < 100:
        return 0
        
    content_lower = content.lower()
    title_lower = title.lower() if title else ""
    
    # Core quantum ethics indicators
    quantum_ethics_indicators = {
        'quantum ethics': 15,
        'quantum governance': 12,
        'quantum regulation': 10,
        'quantum policy': 8,
        'quantum responsibility': 8,
        'quantum oversight': 6,
        'quantum standards': 6,
        'quantum fairness': 8,
        'quantum access': 6,
        'quantum equity': 6,
        'quantum inclusion': 8,
        'quantum sustainability': 8,
        'quantum implications': 5,
        'quantum impact': 5,
        'ethical quantum': 10,
        'responsible quantum': 8,
        'quantum development': 4,
        'quantum future': 4,
        'quantum society': 6
    }
    
    score = 0
    matched_terms = []
    
    # Check content for quantum ethics indicators
    for term, weight in quantum_ethics_indicators.items():
        count = content_lower.count(term)
        if count > 0:
            term_score = min(weight * count, weight * 2)  # Cap at 2x weight
            score += term_score
            matched_terms.append(f"{term}({count})")
    
    # Title boosts for quantum ethics documents
    if 'quantum' in title_lower and any(term in title_lower for term in ['ethics', 'inclusion', 'sustainability', 'governance']):
        score += 15
        matched_terms.append("quantum_ethics_title_boost")
    
    # Transformative technology ethics boost
    if any(term in title_lower for term in ['transformative technology', 'intellectual property', 'sustainable innovation']):
        score += 10
        matched_terms.append("transformative_ethics_boost")
    
    # Cap at 100
    score = min(score, 100)
    
    return score, matched_terms

def fix_comprehensive_quantum_scoring():
    """Apply comprehensive quantum scoring to all relevant documents"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        # Get all documents that might have quantum content
        cursor.execute("""
            SELECT id, title, content, text_content, quantum_cybersecurity_score, quantum_ethics_score
            FROM documents 
            WHERE (title ILIKE '%quantum%' 
                   OR title ILIKE '%post-quantum%'
                   OR title ILIKE '%transformative technology%'
                   OR content ILIKE '%quantum%'
                   OR quantum_cybersecurity_score IS NOT NULL
                   OR quantum_ethics_score IS NOT NULL)
            ORDER BY id
        """)
        
        documents = cursor.fetchall()
        
        print(f"Found {len(documents)} documents with potential quantum content")
        
        for doc_id, title, content, text_content, existing_q_cyber, existing_q_ethics in documents:
            print(f"\nProcessing: {title[:60]}...")
            
            # Use text_content if available, otherwise content
            scoring_content = text_content if text_content else content
            
            if not scoring_content or len(scoring_content) < 100:
                print("  Insufficient content for scoring")
                continue
            
            # Calculate quantum scores
            q_cyber_score, q_cyber_terms = enhanced_quantum_cybersecurity_scoring(scoring_content, title)
            q_ethics_score, q_ethics_terms = enhanced_quantum_ethics_scoring(scoring_content, title)
            
            # Determine if we should update scores
            should_update = False
            updates = {}
            
            if q_cyber_score > 0 and (existing_q_cyber is None or existing_q_cyber < q_cyber_score):
                updates['quantum_cybersecurity_score'] = q_cyber_score
                should_update = True
                print(f"  Updated Quantum Cybersecurity: {q_cyber_score} (was {existing_q_cyber})")
                print(f"  Q Cyber terms: {q_cyber_terms[:3]}...")
            
            if q_ethics_score > 0 and (existing_q_ethics is None or existing_q_ethics < q_ethics_score):
                updates['quantum_ethics_score'] = q_ethics_score
                should_update = True
                print(f"  Updated Quantum Ethics: {q_ethics_score} (was {existing_q_ethics})")
                print(f"  Q Ethics terms: {q_ethics_terms[:3]}...")
            
            # Set topic to Quantum if significant quantum scores
            if q_cyber_score > 20 or q_ethics_score > 15:
                updates['topic'] = 'Quantum'
                should_update = True
                print(f"  Set topic to Quantum")
            elif q_cyber_score > 10 or q_ethics_score > 10:
                updates['topic'] = 'Both'  # Mixed AI/Quantum content
                should_update = True
                print(f"  Set topic to Both (mixed content)")
            
            if should_update:
                # Build update query dynamically
                set_clauses = []
                values = []
                for field, value in updates.items():
                    set_clauses.append(f"{field} = %s")
                    values.append(value)
                
                set_clauses.append("updated_at = CURRENT_TIMESTAMP")
                values.append(doc_id)
                
                update_query = f"""
                    UPDATE documents 
                    SET {', '.join(set_clauses)}
                    WHERE id = %s
                """
                
                cursor.execute(update_query, values)
            else:
                print("  No significant quantum content found")
        
        conn.commit()
        print(f"\nSuccessfully processed {len(documents)} documents for quantum scoring")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_comprehensive_quantum_scoring()