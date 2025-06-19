#!/usr/bin/env python3
"""
Add Cybersecurity as a standalone topic category
Enhances the classification system to identify pure cybersecurity documents
"""

import os
import sys
sys.path.append('.')
import psycopg2
import re

def add_cybersecurity_topic():
    """Add Cybersecurity as a new topic category for documents"""
    
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    try:
        # Create cybersecurity content detector
        def is_cybersecurity_focused(content, title):
            """Detect if document is focused on cybersecurity without AI/quantum"""
            
            if not content:
                return False
                
            content_lower = content.lower()
            title_lower = title.lower()
            combined_text = f"{title_lower} {content_lower}"
            
            # Cybersecurity indicators
            cybersec_indicators = [
                'digital identity', 'authentication', 'authorization', 'access control',
                'identity management', 'credential', 'verification', 'digital certificates',
                'password', 'multifactor', 'biometric', 'encryption', 'cryptography',
                'security controls', 'threat assessment', 'vulnerability', 'risk management',
                'incident response', 'security framework', 'cybersecurity', 'information security',
                'network security', 'data protection', 'privacy', 'security policy',
                'security standards', 'compliance', 'audit', 'penetration testing',
                'intrusion detection', 'firewall', 'security monitoring'
            ]
            
            # AI indicators (should be minimal for pure cybersecurity)
            ai_indicators = [
                'artificial intelligence', 'machine learning', 'neural network',
                'deep learning', 'ai model', 'algorithm training', 'predictive analytics',
                'natural language processing', 'computer vision', 'ai system'
            ]
            
            # Quantum indicators (should be minimal for pure cybersecurity)
            quantum_indicators = [
                'quantum computing', 'quantum cryptography', 'quantum key',
                'post-quantum', 'quantum resistant', 'quantum algorithm',
                'quantum supremacy', 'qubit', 'quantum entanglement'
            ]
            
            # Count occurrences
            cybersec_count = sum(1 for indicator in cybersec_indicators if indicator in combined_text)
            ai_count = sum(1 for indicator in ai_indicators if indicator in combined_text)
            quantum_count = sum(1 for indicator in quantum_indicators if indicator in combined_text)
            
            # Classify as Cybersecurity if:
            # 1. Strong cybersecurity focus (5+ indicators)
            # 2. Minimal AI/quantum content (less than 3 indicators each)
            return cybersec_count >= 5 and ai_count < 3 and quantum_count < 3
        
        # Update documents that should be classified as Cybersecurity
        cursor.execute("""
            SELECT id, title, content, topic 
            FROM documents 
            WHERE topic IS NULL OR topic = 'AI' OR topic = 'General'
        """)
        
        documents = cursor.fetchall()
        updated_count = 0
        
        for doc_id, title, content, current_topic in documents:
            if is_cybersecurity_focused(content, title):
                cursor.execute("""
                    UPDATE documents 
                    SET topic = 'Cybersecurity',
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (doc_id,))
                
                print(f"Updated Document {doc_id}: {title[:50]}... -> Cybersecurity")
                updated_count += 1
        
        conn.commit()
        print(f"\nUpdated {updated_count} documents to Cybersecurity topic")
        
        # Verify the updates
        cursor.execute("""
            SELECT id, title, topic 
            FROM documents 
            WHERE topic = 'Cybersecurity'
            ORDER BY id
        """)
        
        cybersec_docs = cursor.fetchall()
        print(f"\nDocuments now classified as Cybersecurity:")
        for doc_id, title, topic in cybersec_docs:
            print(f"  {doc_id}: {title[:60]}...")
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    add_cybersecurity_topic()