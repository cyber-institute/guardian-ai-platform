"""
Direct database operations with robust transaction handling
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json

def get_db_connection():
    """Get a direct PostgreSQL connection."""
    return psycopg2.connect(
        os.getenv('DATABASE_URL'),
        cursor_factory=RealDictCursor
    )

def save_document_direct(document):
    """Save document using direct PostgreSQL connection with explicit commit."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Prepare the insert statement
        insert_query = """
        INSERT INTO documents (title, content, text_content, quantum_score, document_type, source)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        values = (
            document.get('title', 'Untitled'),
            document.get('content', ''),
            document.get('text_content', ''),
            float(document.get('quantum_score', 0)),
            document.get('document_type', 'Unknown'),
            document.get('source', 'manual')
        )
        
        # Execute and commit
        cursor.execute(insert_query, values)
        result = cursor.fetchone()
        document_id = result['id'] if result else None
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print(f"Successfully saved document ID: {document_id}")
        return True
        
    except Exception as e:
        print(f"Direct database save failed: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def fetch_documents_direct():
    """Fetch documents using direct connection."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT id, title, content, text_content as text, quantum_score as quantum_q,
               document_type, source, created_at, updated_at
        FROM documents 
        ORDER BY created_at DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Convert to expected format
        documents = []
        for row in results:
            doc = dict(row)
            doc['quantum_q'] = float(doc['quantum_q']) if doc['quantum_q'] else 0
            documents.append(doc)
        
        cursor.close()
        conn.close()
        
        return documents
        
    except Exception as e:
        print(f"Direct database fetch failed: {e}")
        return []