"""
Duplicate Document Cleanup Utility
Identifies and manages duplicate documents in the repository
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

def identify_duplicate_groups() -> List[Dict]:
    """Identify groups of duplicate documents in the repository."""
    
    documents = fetch_documents()
    if not documents:
        return []
    
    # Group documents by content hash
    content_groups = {}
    title_groups = {}
    
    for doc in documents:
        doc_id = doc.get('id')
        title = doc.get('title', '').strip().lower()
        content = doc.get('text', '') or doc.get('content', '')
        
        # Create content hash
        if content:
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            if content_hash not in content_groups:
                content_groups[content_hash] = []
            content_groups[content_hash].append(doc)
        
        # Group by similar titles
        if title:
            if title not in title_groups:
                title_groups[title] = []
            title_groups[title].append(doc)
    
    # Identify duplicate groups
    duplicate_groups = []
    
    # Content-based duplicates (exact matches)
    for content_hash, docs in content_groups.items():
        if len(docs) > 1:
            duplicate_groups.append({
                'type': 'exact_content',
                'hash': content_hash,
                'documents': docs,
                'count': len(docs),
                'confidence': 1.0
            })
    
    # Title-based duplicates
    for title, docs in title_groups.items():
        if len(docs) > 1:
            # Check if not already in content duplicates
            existing_content_group = False
            for group in duplicate_groups:
                if group['type'] == 'exact_content':
                    group_ids = [d.get('id') for d in group['documents']]
                    doc_ids = [d.get('id') for d in docs]
                    if any(doc_id in group_ids for doc_id in doc_ids):
                        existing_content_group = True
                        break
            
            if not existing_content_group:
                duplicate_groups.append({
                    'type': 'similar_title',
                    'title': title,
                    'documents': docs,
                    'count': len(docs),
                    'confidence': 0.8
                })
    
    return duplicate_groups

def remove_duplicates(duplicate_group: Dict, keep_document_id: str) -> bool:
    """Remove duplicate documents, keeping only the specified document."""
    
    try:
        conn = get_db_connection()
        if not conn:
            print("Failed to establish database connection")
            return False
            
        with conn.cursor() as cursor:
            # Get IDs of documents to remove
            docs_to_remove = [
                doc.get('id') for doc in duplicate_group['documents'] 
                if doc.get('id') != keep_document_id
            ]
            
            if not docs_to_remove:
                return False
            
            # Remove duplicate documents
            for doc_id in docs_to_remove:
                cursor.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
            
            conn.commit()
        
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error removing duplicates: {e}")
        return False

def get_duplicate_summary() -> Dict:
    """Get summary of duplicate issues in the repository."""
    
    duplicate_groups = identify_duplicate_groups()
    
    total_duplicates = sum(group['count'] - 1 for group in duplicate_groups)
    exact_content_groups = [g for g in duplicate_groups if g['type'] == 'exact_content']
    similar_title_groups = [g for g in duplicate_groups if g['type'] == 'similar_title']
    
    return {
        'total_duplicate_groups': len(duplicate_groups),
        'total_duplicate_documents': total_duplicates,
        'exact_content_groups': len(exact_content_groups),
        'similar_title_groups': len(similar_title_groups),
        'groups': duplicate_groups
    }

def auto_cleanup_exact_duplicates() -> Dict:
    """Automatically remove exact content duplicates, keeping the most recent."""
    
    duplicate_groups = identify_duplicate_groups()
    exact_groups = [g for g in duplicate_groups if g['type'] == 'exact_content']
    
    cleaned_count = 0
    
    for group in exact_groups:
        docs = group['documents']
        
        # Sort by upload date or ID to keep the most recent
        sorted_docs = sorted(docs, key=lambda x: x.get('upload_date', ''), reverse=True)
        keep_doc = sorted_docs[0]
        
        if remove_duplicates(group, keep_doc.get('id')):
            cleaned_count += len(docs) - 1
    
    return {
        'groups_processed': len(exact_groups),
        'documents_removed': cleaned_count
    }