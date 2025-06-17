import os
import json
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        self.engine = None
        self._connect()
    
    def _connect(self):
        """Initialize database connection with SSL and connection pooling."""
        try:
            if self.database_url:
                # Add SSL and connection pool settings for stability
                engine_args = {
                    'pool_size': 5,
                    'max_overflow': 10,
                    'pool_pre_ping': True,
                    'pool_recycle': 3600,
                    'connect_args': {
                        'sslmode': 'require',
                        'connect_timeout': 10
                    }
                }
                self.engine = create_engine(self.database_url, **engine_args)
                logger.info("Connected to PostgreSQL database")
            else:
                logger.warning("No DATABASE_URL found, database operations will fail")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            self.engine = None
    
    def execute_query(self, query, params=None):
        """Execute a query and return results with connection retry logic."""
        if not self.engine:
            return None
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with self.engine.begin() as conn:
                    result = conn.execute(text(query), params or {})
                    if result.returns_rows:
                        rows = result.fetchall()
                        return [dict(row._mapping) for row in rows]
                    else:
                        return result.rowcount
            except SQLAlchemyError as e:
                logger.error(f"Query execution failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    # Reconnect on connection errors
                    if "connection" in str(e).lower() or "ssl" in str(e).lower():
                        self._connect()
                    continue
                return []
    
    def fetch_documents(self):
        """Fetch documents from database - optimized for listing view."""
        query = """
        SELECT id, title, document_type, source, author_organization, publish_date, 
               COALESCE(content_preview, LEFT(content, 500), LEFT(text_content, 500), 'No preview available') as content_preview,
               ai_cybersecurity_score, quantum_cybersecurity_score, ai_ethics_score, quantum_ethics_score,
               detected_region, topic, url_valid, url_status, created_at, updated_at
        FROM documents 
        ORDER BY updated_at DESC, created_at DESC
        LIMIT 200
        """
        
        results = self.execute_query(query)
        if results is None:
            return []
        
        # Convert to lightweight format for fast loading
        documents = []
        if isinstance(results, list):
            for row in results:
                # Generate enhanced content preview from full content
                raw_preview = row.get('content_preview', '')
                full_content = row.get('content', '') or row.get('text_content', '')
                
                if full_content and len(full_content) > 200:
                    # Create preview from full content
                    import re
                    clean_preview = re.sub(r'<[^>]+>', '', full_content)  # Remove HTML
                    clean_preview = re.sub(r'\*+', '', clean_preview)     # Remove asterisks
                    clean_preview = re.sub(r'#+\s*', '', clean_preview)   # Remove headers
                    clean_preview = re.sub(r'[-_]{3,}', '', clean_preview) # Remove dividers
                    clean_preview = re.sub(r'\s+', ' ', clean_preview).strip()
                    
                    # Extract meaningful sentences
                    sentences = re.split(r'[.!?]+', clean_preview)
                    meaningful_text = []
                    for sentence in sentences[:3]:  # First 3 sentences
                        sentence = sentence.strip()
                        if len(sentence) > 30:  # Skip very short fragments
                            meaningful_text.append(sentence)
                    
                    if meaningful_text:
                        content_preview = '. '.join(meaningful_text) + '.'
                        if len(content_preview) > 350:
                            content_preview = content_preview[:350] + '...'
                    else:
                        content_preview = clean_preview[:350] + '...' if len(clean_preview) > 350 else clean_preview
                elif raw_preview:
                    # Clean existing preview
                    import re
                    clean_preview = re.sub(r'\*+', '', raw_preview)
                    clean_preview = re.sub(r'#+\s*', '', clean_preview)
                    clean_preview = re.sub(r'\s+', ' ', clean_preview).strip()
                    content_preview = clean_preview[:350] + '...' if len(clean_preview) > 350 else clean_preview
                else:
                    content_preview = 'Document content available - click to view details'

                doc = {
                    'id': row['id'],
                    'title': row['title'] or 'Untitled Document',
                    'document_type': row['document_type'] or 'Report',
                    'source': row['source'] or '',
                    'author_organization': row.get('author_organization', 'Unknown'),
                    'publish_date': str(row.get('publish_date')) if row.get('publish_date') else None,
                    'content_preview': content_preview,
                    'ai_cybersecurity_score': int(row.get('ai_cybersecurity_score', 0)) if row.get('ai_cybersecurity_score') else 0,
                    'quantum_cybersecurity_score': int(row.get('quantum_cybersecurity_score', 0)) if row.get('quantum_cybersecurity_score') else 0,
                    'ai_ethics_score': int(row.get('ai_ethics_score', 0)) if row.get('ai_ethics_score') else 0,
                    'quantum_ethics_score': int(row.get('quantum_ethics_score', 0)) if row.get('quantum_ethics_score') else 0,
                    'detected_region': row.get('detected_region', 'Unknown'),
                    'topic': row.get('topic', 'General'),
                    'url_valid': row.get('url_valid', False),
                    'url_status': row.get('url_status', 'unchecked'),
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                documents.append(doc)
        
        return documents
    
    def save_document(self, document):
        """Save a new document to the database with enhanced metadata support."""
        try:
            # Use verified metadata if available, otherwise extract metadata
            if document.get('metadata_verified'):
                # Use verified metadata directly
                final_title = document.get('title', 'Untitled')
                final_org = document.get('author_organization') or document.get('organization', 'Unknown')
                final_author = document.get('author', 'Unknown')
                final_doc_type = document.get('document_type', 'unknown')
                final_date = document.get('publish_date') or document.get('publication_date')
                final_topic = 'General'  # Will be determined by content analysis
            else:
                # Extract enhanced metadata during ingestion
                try:
                    from utils.fallback_analyzer import extract_metadata_fallback
                    text_content = document.get('text_content', '') or document.get('text', '')
                    source_hint = document.get('source', 'manual')
                    
                    # Extract intelligent metadata
                    enhanced_metadata = extract_metadata_fallback(text_content, source_hint)
                    
                    # Use enhanced metadata, fallback to provided values
                    final_title = enhanced_metadata.get('title') or document.get('title', 'Untitled')
                    final_org = enhanced_metadata.get('author_organization') or document.get('organization', 'Unknown')
                    final_author = document.get('author', 'Unknown')
                    final_doc_type = enhanced_metadata.get('document_type') or document.get('document_type', 'unknown')
                    final_date = enhanced_metadata.get('publish_date')
                    final_topic = enhanced_metadata.get('topic', 'General')
                except ImportError:
                    # Fallback if analyzer not available
                    final_title = document.get('title', 'Untitled')
                    final_org = document.get('author_organization') or document.get('organization', 'Unknown')
                    final_author = document.get('author', 'Unknown')
                    final_doc_type = document.get('document_type', 'unknown')
                    final_date = document.get('publish_date') or document.get('publication_date')
                    final_topic = 'General'
            
            text_content = document.get('text_content', '') or document.get('content', '')
            content_preview = document.get('content', text_content[:1000] if text_content else '')
            
            # Enhanced query to match existing schema
            query = """
            INSERT INTO documents (
                title, content, text_content, document_type, source,
                author_organization, publish_date, topic,
                ai_cybersecurity_score, quantum_cybersecurity_score, 
                ai_ethics_score, quantum_ethics_score, metadata
            )
            VALUES (
                :title, :content, :text_content, :document_type, :source,
                :author_organization, :publish_date, :topic,
                :ai_cybersecurity_score, :quantum_cybersecurity_score,
                :ai_ethics_score, :quantum_ethics_score, :metadata
            )
            RETURNING id
            """
            
            # Store additional metadata in JSONB field
            metadata_json = {
                'author': final_author,
                'source_url': document.get('source_url', ''),
                'verified': document.get('metadata_verified', False),
                'extraction_method': document.get('extraction_method', 'manual'),
                'verification_timestamp': document.get('verification_timestamp', ''),
                'document_id': document.get('id', '')
            }
            
            params = {
                'title': final_title,
                'content': content_preview,
                'text_content': text_content,
                'document_type': final_doc_type,
                'source': document.get('source', 'url'),
                'author_organization': final_org,
                'publish_date': final_date,
                'topic': final_topic,
                'ai_cybersecurity_score': document.get('ai_cybersecurity_score', 0),
                'quantum_cybersecurity_score': document.get('quantum_cybersecurity_score', 0),
                'ai_ethics_score': document.get('ai_ethics_score', 0),
                'quantum_ethics_score': document.get('quantum_ethics_score', 0),
                'metadata': json.dumps(metadata_json)
            }
            
            result = self.execute_query(query, params)
            return result is not None
            
        except Exception as e:
            logger.error(f"Error saving document: {e}")
            return False
    
    def save_assessment(self, document_id, assessment_data):
        """Save assessment results to the database."""
        query = """
        INSERT INTO assessments (document_id, assessment_type, score, confidence_scores, 
                               narrative, traits, raw_analysis)
        VALUES (:document_id, :assessment_type, :score, :confidence_scores, 
                :narrative, :traits, :raw_analysis)
        """
        
        params = {
            'document_id': document_id,
            'assessment_type': assessment_data.get('label', 'ai_analysis'),
            'score': assessment_data.get('patent_score', 0),
            'confidence_scores': json.dumps(assessment_data.get('raw', {})),
            'narrative': assessment_data.get('narrative', []),
            'traits': json.dumps(assessment_data.get('traits', {})),
            'raw_analysis': json.dumps(assessment_data)
        }
        
        result = self.execute_query(query, params)
        return result is not None
    
    def get_scoring_criteria(self):
        """Get all scoring criteria from the database."""
        query = "SELECT criterion_name, weight, category, description FROM scoring_criteria"
        return self.execute_query(query) or []
    
    def get_assessment_history(self, document_id):
        """Get assessment history for a specific document."""
        query = """
        SELECT assessment_type, score, confidence_scores, narrative, traits, 
               raw_analysis, created_at
        FROM assessments 
        WHERE document_id = :document_id 
        ORDER BY created_at DESC
        """
        
        return self.execute_query(query, {'document_id': document_id}) or []
    
    def update_document_score(self, document_id, new_score):
        """Update the quantum score for a document."""
        query = """
        UPDATE documents 
        SET quantum_score = :score, updated_at = CURRENT_TIMESTAMP 
        WHERE id = :document_id
        """
        
        params = {'score': new_score, 'document_id': document_id}
        result = self.execute_query(query, params)
        return result is not None

# Global database manager instance
db_manager = DatabaseManager()