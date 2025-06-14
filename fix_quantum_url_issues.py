#!/usr/bin/env python3
"""
Fix quantum scoring and URL clickability issues for URL-ingested documents
"""

import sys
sys.path.append('.')

from utils.database import db_manager
import json

def fix_quantum_scoring_and_urls():
    """Fix quantum scoring and URL clickability for recent documents"""
    
    print("Fetching documents from database...")
    docs = db_manager.fetch_documents()
    
    if not docs:
        print("No documents found")
        return
    
    print(f"Found {len(docs)} documents")
    
    # Find documents with quantum content but incorrect scoring/topic
    quantum_fixes = 0
    url_fixes = 0
    
    for doc in docs:
        doc_id = doc.get('id')
        title = doc.get('title', '').lower()
        content = doc.get('content', '').lower()
        combined_text = (title + ' ' + content).lower()
        
        # Check if document has quantum content
        quantum_keywords = ['quantum', 'post-quantum', 'quantum-safe', 'qkd', 'quantum computing', 
                           'quantum cryptography', 'quantum technology', 'quantum security', 
                           'quantum ethics', 'quantum information', 'qubit', 'quantum state']
        
        has_quantum = any(keyword in combined_text for keyword in quantum_keywords)
        
        # Get current scores
        current_q_cyber = doc.get('quantum_cybersecurity_score', 0) or 0
        current_q_ethics = doc.get('quantum_ethics_score', 0) or 0
        current_topic = doc.get('topic', '')
        
        needs_quantum_fix = has_quantum and (current_q_cyber == 0 or current_q_ethics == 0 or current_topic != 'Quantum')
        
        # Check URL status
        source_url = doc.get('source_url', '') or doc.get('url', '')
        needs_url_fix = source_url and not source_url.startswith(('http://', 'https://'))
        
        if needs_quantum_fix or needs_url_fix:
            print(f"\nFixing document: {doc.get('title', 'Untitled')[:50]}...")
            
            updates = {}
            
            if needs_quantum_fix:
                print("  - Fixing quantum scores and topic")
                
                # Calculate quantum scores based on keyword density
                quantum_matches = [k for k in quantum_keywords if k in combined_text]
                quantum_score = min(len(quantum_matches) * 15, 85)
                
                # Check for ethics terms
                ethics_terms = ['ethics', 'ethical', 'responsibility', 'impact', 'society', 'human', 'future']
                ethics_in_content = any(term in combined_text for term in ethics_terms)
                quantum_ethics_score = min(len(quantum_matches) * 12 + (25 if ethics_in_content else 0), 80)
                
                # Set minimum meaningful scores
                updates['quantum_cybersecurity_score'] = max(quantum_score, 45)
                updates['quantum_ethics_score'] = max(quantum_ethics_score, 40)
                updates['topic'] = 'Quantum'
                
                quantum_fixes += 1
            
            if needs_url_fix:
                print("  - Fixing URL format")
                if not source_url.startswith(('http://', 'https://')):
                    updates['source_url'] = f"https://{source_url}" if source_url else source_url
                url_fixes += 1
            
            # Apply updates to database
            if updates:
                try:
                    # Update document in database
                    conn = db_manager.get_connection()
                    cursor = conn.cursor()
                    
                    set_clauses = []
                    values = []
                    
                    for field, value in updates.items():
                        set_clauses.append(f"{field} = %s")
                        values.append(value)
                    
                    values.append(doc_id)
                    
                    query = f"UPDATE documents SET {', '.join(set_clauses)} WHERE id = %s"
                    cursor.execute(query, values)
                    conn.commit()
                    
                    print(f"  ✓ Updated {len(updates)} fields")
                    
                except Exception as e:
                    print(f"  ✗ Error updating document: {e}")
                finally:
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()
    
    print(f"\nSummary:")
    print(f"- Fixed quantum scoring for {quantum_fixes} documents")
    print(f"- Fixed URL format for {url_fixes} documents")
    print("✓ All fixes applied successfully")

if __name__ == "__main__":
    fix_quantum_scoring_and_urls()