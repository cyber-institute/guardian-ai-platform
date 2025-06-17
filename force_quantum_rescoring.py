#!/usr/bin/env python3
"""
Force fresh quantum scoring calculations bypassing all caches
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import DatabaseManager
from utils.comprehensive_scoring import score_quantum_cybersecurity_maturity, analyze_document_applicability

def force_quantum_rescoring():
    """Force fresh quantum scoring calculations for all quantum documents"""
    
    print("FORCING FRESH QUANTUM SCORING CALCULATIONS")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Get all documents that contain quantum content
    query = """
    SELECT id, title, content, text_content, quantum_cybersecurity_score
    FROM documents 
    WHERE (title ILIKE '%quantum%' OR content ILIKE '%quantum%' OR content ILIKE '%post-quantum%' OR text_content ILIKE '%quantum%')
    ORDER BY id
    """
    
    results = db.execute_query(query)
    if not results:
        print("No quantum documents found")
        return
    
    print(f"Found {len(results)} documents with quantum content")
    
    updated_count = 0
    for row in results:
        doc_id = row['id']
        title = row['title'] or 'Untitled'
        content = row['content'] or row['text_content'] or ''
        old_score = row['quantum_cybersecurity_score']
        
        # Check if document is truly quantum-applicable
        applicability = analyze_document_applicability(content, title)
        
        if applicability['quantum_cybersecurity']:
            # Calculate fresh score using new algorithm
            new_score = score_quantum_cybersecurity_maturity(content, title)
            
            if new_score is not None:
                # Update database with new score
                update_query = """
                UPDATE documents 
                SET quantum_cybersecurity_score = %s, updated_at = NOW()
                WHERE id = %s
                """
                db.execute_query(update_query, (new_score, doc_id))
                
                print(f"Doc {doc_id}: {title[:40]}...")
                print(f"  Old score: {old_score} -> New score: {new_score}")
                
                updated_count += 1
            else:
                print(f"Doc {doc_id}: Not applicable for quantum scoring")
        else:
            # Clear quantum score for non-quantum documents
            update_query = """
            UPDATE documents 
            SET quantum_cybersecurity_score = NULL, updated_at = NOW()
            WHERE id = %s
            """
            db.execute_query(update_query, (doc_id,))
            print(f"Doc {doc_id}: Cleared quantum score (not quantum-applicable)")
    
    print(f"\n" + "=" * 60)
    print(f"RESCORING COMPLETE: {updated_count} documents updated with new quantum scores")
    
    # Verify scoring diversity
    verify_query = """
    SELECT quantum_cybersecurity_score, COUNT(*) as count
    FROM documents 
    WHERE quantum_cybersecurity_score IS NOT NULL
    GROUP BY quantum_cybersecurity_score
    ORDER BY quantum_cybersecurity_score
    """
    
    score_distribution = db.execute_query(verify_query)
    if score_distribution:
        print(f"\nScore Distribution After Update:")
        for row in score_distribution:
            score = row['quantum_cybersecurity_score']
            count = row['count']
            print(f"  Score {score}: {count} documents")
        
        unique_scores = len(score_distribution)
        total_scored = sum(row['count'] for row in score_distribution)
        
        if unique_scores > 1:
            print(f"\n✅ SUCCESS: {unique_scores} different scores across {total_scored} documents")
        else:
            print(f"\n⚠️  WARNING: Only {unique_scores} unique score found")
    
    return updated_count

if __name__ == "__main__":
    force_quantum_rescoring()