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
        """Initialize database connection."""
        try:
            if self.database_url:
                self.engine = create_engine(self.database_url)
                logger.info("Connected to PostgreSQL database")
            else:
                logger.warning("No DATABASE_URL found, database operations will fail")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            self.engine = None
    
    def execute_query(self, query, params=None):
        """Execute a query and return results."""
        if not self.engine:
            return None
        
        try:
            with self.engine.begin() as conn:  # Use begin() for auto-commit transaction
                result = conn.execute(text(query), params or {})
                if result.returns_rows:
                    rows = result.fetchall()
                    return [dict(row._mapping) for row in rows]
                else:
                    return result.rowcount
        except SQLAlchemyError as e:
            logger.error(f"Query execution failed: {e}")
            return []
    
    def fetch_documents(self):
        """Fetch all documents from the database."""
        query = """
        SELECT id, title, content, text_content as text, quantum_score as quantum_q,
               document_type, source, created_at, updated_at
        FROM documents 
        ORDER BY created_at DESC
        """
        
        results = self.execute_query(query)
        if results is None:
            return []
        
        # Convert to format expected by the application
        documents = []
        if isinstance(results, list):
            for row in results:
                doc = {
                    'id': row['id'],
                    'title': row['title'],
                    'content': row['content'],
                    'text': row['text'],
                    'quantum_q': float(row['quantum_q']) if row['quantum_q'] else 0,
                    'document_type': row['document_type'],
                    'source': row['source'],
                    'created_at': row['created_at'],
                    'updated_at': row['updated_at']
                }
                documents.append(doc)
        
        return documents
    
    def save_document(self, document):
        """Save a new document to the database."""
        query = """
        INSERT INTO documents (title, content, text_content, quantum_score, document_type, source)
        VALUES (:title, :content, :text_content, :quantum_score, :document_type, :source)
        RETURNING id
        """
        
        params = {
            'title': document.get('title', 'Untitled'),
            'content': document.get('content', ''),
            'text_content': document.get('text_content', '') or document.get('text', ''),
            'quantum_score': document.get('quantum_score', 0) or document.get('quantum_q', 0),
            'document_type': document.get('document_type', 'unknown'),
            'source': document.get('source', 'manual')
        }
        
        result = self.execute_query(query, params)
        return result is not None
    
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