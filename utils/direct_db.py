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
    """Save document using direct PostgreSQL connection with enhanced metadata extraction."""
    conn = None
    try:
        # Extract enhanced metadata during ingestion
        from utils.fallback_analyzer import extract_metadata_fallback
        
        text_content = document.get('text_content', '') or document.get('text', '')
        source_hint = document.get('source', 'manual')
        
        # Extract intelligent metadata
        enhanced_metadata = extract_metadata_fallback(text_content, source_hint)
        
        # Use enhanced metadata, fallback to provided values
        final_title = enhanced_metadata.get('title') or document.get('title', 'Untitled')
        final_org = enhanced_metadata.get('author_organization', 'Unknown')
        final_doc_type = enhanced_metadata.get('document_type') or document.get('document_type', 'Unknown')
        final_preview = enhanced_metadata.get('content_preview', document.get('content', ''))
        final_date = enhanced_metadata.get('publish_date')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Enhanced insert statement with all metadata fields including scoring and URL validation
        scores = document.get('comprehensive_scores', {})
        
        # Determine topic based on content analysis
        content_lower = text_content.lower()
        quantum_keywords = ['quantum', 'post-quantum', 'quantum-safe', 'qkd', 'quantum computing', 'quantum cryptography']
        ai_keywords = ['artificial intelligence', 'machine learning', 'ai ', ' ai', 'neural network']
        
        if any(keyword in content_lower for keyword in quantum_keywords):
            topic = 'Quantum'
        elif any(keyword in content_lower for keyword in ai_keywords):
            topic = 'AI'
        else:
            topic = 'General'
        
        # Set URL validation for URL-ingested documents
        is_url_source = source_hint and source_hint.startswith(('http://', 'https://'))
        
        import datetime
        
        insert_query = """
        INSERT INTO documents (title, content, text_content, quantum_score, document_type, source, 
                             author_organization, publish_date, ai_cybersecurity_score, 
                             quantum_cybersecurity_score, ai_ethics_score, quantum_ethics_score,
                             topic, url_valid, url_status, url_checked)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """
        
        values = (
            final_title,
            final_preview,
            text_content,
            float(document.get('quantum_score', 0)),
            final_doc_type,
            source_hint,
            final_org,
            final_date,
            scores.get('ai_cybersecurity_score', 0),
            scores.get('quantum_cybersecurity_score', 0),
            scores.get('ai_ethics_score', 0),
            scores.get('quantum_ethics_score', 0),
            topic,
            is_url_source,  # URL validation status
            'verified' if is_url_source else None,  # URL status
            datetime.datetime.now() if is_url_source else None  # URL check timestamp
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