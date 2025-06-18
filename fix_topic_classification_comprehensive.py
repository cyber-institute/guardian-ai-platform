#!/usr/bin/env python3
"""
Comprehensive Topic Classification Fix
Fixes all documents with incorrect topic classification, especially those marked as "General"
"""

import os
import psycopg2
from datetime import datetime
import sys

def fix_topic_classification():
    """Fix topic classification for all documents in the database"""
    
    try:
        # Connect to database
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        print("🔍 Starting comprehensive topic classification fix...")
        
        # Get all documents that need topic reclassification
        cursor.execute("""
            SELECT id, title, content, topic, organization, document_type
            FROM documents 
            WHERE topic = 'General' OR topic IS NULL OR topic = '' OR topic = 'Both'
            ORDER BY id
        """)
        
        documents = cursor.fetchall()
        print(f"📊 Found {len(documents)} documents to reclassify")
        
        updated_count = 0
        
        for doc_id, title, content, current_topic, organization, doc_type in documents:
            try:
                # Enhanced AI detection - including UNESCO AI Ethics patterns
                combined_text = f"{title or ''} {content or ''} {organization or ''} {doc_type or ''}".lower()
                
                ai_indicators = [
                    'artificial intelligence', 'machine learning', 'ai policy', 'ai framework',
                    'ai strategy', 'ai governance', 'neural network', 'deep learning',
                    'ai ethics', 'ai safety', 'ai risk', 'generative ai', 'ai system',
                    'ethics of artificial intelligence', 'recommendation on the ethics',
                    'ai technologies', 'ethical ai', 'responsible ai', 'ai development',
                    'ai deployment', 'algorithmic', 'automated decision', 'intelligent system'
                ]
                
                # Enhanced quantum detection
                quantum_indicators = [
                    'quantum policy', 'quantum approach', 'quantum technology', 'quantum computing', 
                    'quantum cryptography', 'quantum security', 'post-quantum', 'quantum-safe',
                    'quantum initiative', 'quantum strategy', 'quantum framework', 'qkd',
                    'quantum key distribution', 'quantum resistant', 'quantum threat', 'quantum',
                    'qubit', 'quantum state', 'quantum mechanics', 'quantum information'
                ]
                
                ai_count = sum(1 for indicator in ai_indicators if indicator in combined_text)
                quantum_count = sum(1 for indicator in quantum_indicators if indicator in combined_text)
                
                # Determine new topic with improved sensitivity
                new_topic = current_topic
                if quantum_count >= 2 and quantum_count > ai_count:
                    new_topic = "Quantum"
                elif ai_count >= 1 and ai_count >= quantum_count:  # Lower threshold for AI detection
                    new_topic = "AI"
                elif quantum_count >= 1 and ai_count >= 1:
                    new_topic = "Both"
                else:
                    new_topic = "AI"  # Default to AI instead of General for policy documents
                
                # Update if topic changed
                if new_topic != current_topic:
                    cursor.execute("""
                        UPDATE documents 
                        SET topic = %s, 
                            updated_at = %s
                        WHERE id = %s
                    """, (new_topic, datetime.now(), doc_id))
                    
                    updated_count += 1
                    
                    print(f"✓ Updated document {doc_id}: '{title[:50]}...' from '{current_topic}' to '{new_topic}'")
                    print(f"  AI indicators: {ai_count}, Quantum indicators: {quantum_count}")
                
            except Exception as e:
                print(f"❌ Error processing document {doc_id}: {str(e)}")
                continue
        
        # Commit all changes
        conn.commit()
        print(f"\n🎉 Successfully updated {updated_count} documents!")
        
        # Show summary statistics
        cursor.execute("""
            SELECT topic, COUNT(*) as count
            FROM documents 
            GROUP BY topic
            ORDER BY count DESC
        """)
        
        topic_stats = cursor.fetchall()
        print("\n📊 Current topic distribution:")
        for topic, count in topic_stats:
            print(f"  {topic}: {count} documents")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return False

def main():
    """Main function"""
    print("🚀 GUARDIAN Topic Classification Fix")
    print("=" * 50)
    
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL environment variable not set")
        sys.exit(1)
    
    success = fix_topic_classification()
    
    if success:
        print("\n✅ Topic classification fix completed successfully!")
    else:
        print("\n❌ Topic classification fix failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()