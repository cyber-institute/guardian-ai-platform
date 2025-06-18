#!/usr/bin/env python3
"""
Apply Enhanced Scoring System to All Documents
Updates all documents to use content depth analysis instead of keyword matching
"""

import os
import psycopg2
from utils.comprehensive_scoring import comprehensive_document_scoring
from utils.metadata_integrity_validator import run_integrity_check

def rescore_all_documents():
    """Apply enhanced scoring to all documents in the database"""
    
    print("Starting enhanced scoring update for all documents...")
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Get all documents that need rescoring
        cursor.execute("""
            SELECT id, title, content 
            FROM documents 
            WHERE content IS NOT NULL AND content != ''
            ORDER BY id
        """)
        
        documents = cursor.fetchall()
        total_docs = len(documents)
        
        print(f"Found {total_docs} documents to rescore")
        
        updated_count = 0
        significant_changes = []
        
        for i, (doc_id, title, content) in enumerate(documents, 1):
            print(f"Processing {i}/{total_docs}: Document {doc_id}")
            
            try:
                # Get old scores for comparison
                cursor.execute("""
                    SELECT ai_cybersecurity_score, ai_ethics_score, 
                           quantum_cybersecurity_score, quantum_ethics_score
                    FROM documents WHERE id = %s
                """, (doc_id,))
                old_scores = cursor.fetchone()
                
                # Calculate new scores using enhanced system
                new_scores = comprehensive_document_scoring(content, title)
                
                # Update database with new scores
                cursor.execute("""
                    UPDATE documents 
                    SET ai_cybersecurity_score = %s,
                        ai_ethics_score = %s,
                        quantum_cybersecurity_score = %s,
                        quantum_ethics_score = %s
                    WHERE id = %s
                """, (
                    new_scores.get('ai_cybersecurity'),
                    new_scores.get('ai_ethics'), 
                    new_scores.get('quantum_cybersecurity'),
                    new_scores.get('quantum_ethics'),
                    doc_id
                ))
                
                # Track significant changes
                if old_scores:
                    old_ai_cyber, old_ai_ethics, old_q_cyber, old_q_ethics = old_scores
                    new_ai_cyber = new_scores.get('ai_cybersecurity')
                    new_ai_ethics = new_scores.get('ai_ethics')
                    
                    # Check for significant AI score reductions (keyword matching -> content analysis)
                    if old_ai_cyber and old_ai_cyber > 30 and (new_ai_cyber is None or new_ai_cyber < 15):
                        significant_changes.append({
                            'doc_id': doc_id,
                            'title': title[:50] + '...' if len(title) > 50 else title,
                            'change': f'AI Cyber: {old_ai_cyber} -> {new_ai_cyber or "N/A"}',
                            'reason': 'Content analysis detected AI mentioned only in passing'
                        })
                    
                    if old_ai_ethics and old_ai_ethics > 30 and (new_ai_ethics is None or new_ai_ethics < 15):
                        significant_changes.append({
                            'doc_id': doc_id,
                            'title': title[:50] + '...' if len(title) > 50 else title,
                            'change': f'AI Ethics: {old_ai_ethics} -> {new_ai_ethics or "N/A"}',
                            'reason': 'Content analysis detected AI mentioned only in passing'
                        })
                
                updated_count += 1
                
                if i % 10 == 0:
                    conn.commit()  # Commit every 10 documents
                    
            except Exception as e:
                print(f"Error processing document {doc_id}: {str(e)}")
                continue
        
        # Final commit
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\nCompleted rescoring {updated_count}/{total_docs} documents")
        
        # Show significant changes
        if significant_changes:
            print(f"\nSignificant scoring improvements detected ({len(significant_changes)} changes):")
            for change in significant_changes[:10]:  # Show first 10
                print(f"  Doc {change['doc_id']}: {change['title']}")
                print(f"    {change['change']}")
                print(f"    Reason: {change['reason']}")
            
            if len(significant_changes) > 10:
                print(f"    ... and {len(significant_changes) - 10} more")
        
        return True
        
    except Exception as e:
        print(f"Failed to rescore documents: {str(e)}")
        return False

def main():
    """Main function to apply enhanced scoring"""
    
    print("=" * 80)
    print("ENHANCED SCORING SYSTEM APPLICATION")
    print("=" * 80)
    
    # First, validate metadata integrity
    print("Step 1: Validating metadata integrity...")
    if not run_integrity_check():
        print("ERROR: Metadata integrity check failed. Aborting.")
        return
    
    print("✓ Metadata integrity validated")
    
    # Apply enhanced scoring
    print("\nStep 2: Applying enhanced content analysis scoring...")
    if rescore_all_documents():
        print("✓ Enhanced scoring applied successfully")
        
        # Final integrity check
        print("\nStep 3: Final metadata integrity validation...")
        if run_integrity_check():
            print("✓ All systems working correctly with enhanced scoring")
        else:
            print("WARNING: Metadata integrity issue detected after scoring update")
    else:
        print("ERROR: Failed to apply enhanced scoring")

if __name__ == "__main__":
    main()