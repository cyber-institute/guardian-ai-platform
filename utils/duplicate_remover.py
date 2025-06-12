"""
Duplicate Document Removal System
Actually removes duplicate documents from the database
"""

import hashlib
import psycopg2
import os
from typing import List, Dict, Tuple
from utils.db import fetch_documents

def get_db_connection():
    """Get database connection using environment variables."""
    try:
        return psycopg2.connect(
            host=os.getenv('PGHOST'),
            database=os.getenv('PGDATABASE'),
            user=os.getenv('PGUSER'),
            password=os.getenv('PGPASSWORD'),
            port=os.getenv('PGPORT')
        )
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def find_and_remove_duplicates() -> Dict:
    """Find and remove duplicate documents, keeping the most recent."""
    
    try:
        documents = fetch_documents()
        if not documents:
            return {'removed': 0, 'groups': 0}
        
        print(f"Analyzing {len(documents)} documents for duplicates...")
        
        # Group by exact title matches (most common duplicate type)
        title_groups = {}
        for doc in documents:
            title = doc.get('title', '').strip()
            if title and len(title) > 20:  # Only meaningful titles
                clean_title = title.lower()
                if clean_title not in title_groups:
                    title_groups[clean_title] = []
                title_groups[clean_title].append(doc)
        
        # Group by content hash for exact content duplicates
        content_groups = {}
        for doc in documents:
            content = doc.get('content', '') or doc.get('text', '')
            if content and len(content) > 1000:  # Only substantial content
                # Use first 5000 chars for hash to avoid memory issues
                content_hash = hashlib.md5(content[:5000].encode('utf-8')).hexdigest()
                if content_hash not in content_groups:
                    content_groups[content_hash] = []
                content_groups[content_hash].append(doc)
        
        # Remove duplicates
        removed_count = 0
        groups_processed = 0
        
        conn = get_db_connection()
        if not conn:
            return {'removed': 0, 'groups': 0}
        
        with conn.cursor() as cursor:
            # Remove title-based duplicates
            for title, docs in title_groups.items():
                if len(docs) > 1:
                    groups_processed += 1
                    # Keep the document with the highest ID (most recent)
                    sorted_docs = sorted(docs, key=lambda x: int(x.get('id', 0)), reverse=True)
                    keep_doc = sorted_docs[0]
                    
                    for doc in sorted_docs[1:]:
                        doc_id = doc.get('id')
                        try:
                            cursor.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
                            removed_count += 1
                            print(f"Removed duplicate document ID {doc_id}: {title[:50]}...")
                        except Exception as e:
                            print(f"Error removing document {doc_id}: {e}")
            
            # Remove content-based duplicates (not already removed by title)
            for content_hash, docs in content_groups.items():
                if len(docs) > 1:
                    # Check if these weren't already removed by title matching
                    remaining_docs = []
                    for doc in docs:
                        try:
                            cursor.execute("SELECT id FROM documents WHERE id = %s", (doc.get('id'),))
                            if cursor.fetchone():
                                remaining_docs.append(doc)
                        except:
                            continue
                    
                    if len(remaining_docs) > 1:
                        groups_processed += 1
                        # Keep the document with the highest ID (most recent)
                        sorted_docs = sorted(remaining_docs, key=lambda x: int(x.get('id', 0)), reverse=True)
                        keep_doc = sorted_docs[0]
                        
                        for doc in sorted_docs[1:]:
                            doc_id = doc.get('id')
                            try:
                                cursor.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
                                removed_count += 1
                                print(f"Removed duplicate content ID {doc_id}")
                            except Exception as e:
                                print(f"Error removing document {doc_id}: {e}")
            
            conn.commit()
        
        conn.close()
        
        return {
            'removed': removed_count,
            'groups': groups_processed
        }
        
    except Exception as e:
        print(f"Error in duplicate removal: {e}")
        return {'removed': 0, 'groups': 0}

def get_duplicate_count() -> int:
    """Get quick count of potential duplicates."""
    try:
        documents = fetch_documents()
        if not documents:
            return 0
        
        # Quick title-based duplicate count
        titles = {}
        for doc in documents:
            title = doc.get('title', '').strip().lower()
            if title and len(title) > 20:
                titles[title] = titles.get(title, 0) + 1
        
        duplicates = sum(1 for count in titles.values() if count > 1)
        return duplicates
        
    except Exception as e:
        print(f"Error counting duplicates: {e}")
        return 0