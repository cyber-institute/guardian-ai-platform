"""
Comprehensive Patent-Based Document Scoring System
Applies all GUARDIAN patent formulas to documents and updates database scores
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.patent_scoring_engine import ComprehensivePatentScoringEngine
import logging

logger = logging.getLogger(__name__)

class DocumentScoringSystem:
    """
    System to apply comprehensive patent-based scoring to all documents.
    Updates database with scores from all four assessment frameworks.
    """
    
    def __init__(self):
        self.scoring_engine = ComprehensivePatentScoringEngine()
        
    def get_db_connection(self):
        """Get database connection."""
        return psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
    
    def score_all_documents(self):
        """
        Apply comprehensive patent-based scoring to all documents in database.
        Updates documents with scores from all four frameworks.
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Get all documents that need scoring
            cursor.execute("""
                SELECT id, title, text_content, content
                FROM documents 
                WHERE text_content IS NOT NULL 
                AND text_content != ''
                ORDER BY id
            """)
            
            documents = cursor.fetchall()
            total_docs = len(documents)
            processed = 0
            
            print(f"Starting comprehensive scoring for {total_docs} documents...")
            
            for doc in documents:
                try:
                    doc_id = doc['id']
                    title = doc.get('title', '')
                    content = doc.get('text_content', '') or doc.get('content', '')
                    
                    if not content:
                        continue
                    
                    # Apply comprehensive patent-based scoring
                    scores = self.scoring_engine.assess_document_comprehensive(content, title)
                    
                    # Update document with all four framework scores
                    cursor.execute("""
                        UPDATE documents 
                        SET ai_cybersecurity_score = %s,
                            quantum_cybersecurity_score = %s,
                            ai_ethics_score = %s,
                            quantum_ethics_score = %s,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (
                        scores['ai_cybersecurity_score'],
                        scores['quantum_cybersecurity_score'],
                        scores['ai_ethics_score'],
                        scores['quantum_ethics_score'],
                        doc_id
                    ))
                    
                    processed += 1
                    
                    if processed % 5 == 0:
                        print(f"Processed {processed}/{total_docs} documents...")
                        
                except Exception as e:
                    logger.error(f"Error scoring document {doc_id}: {e}")
                    continue
            
            conn.commit()
            cursor.close()
            
            print(f"Comprehensive scoring completed: {processed}/{total_docs} documents processed")
            return processed
            
        except Exception as e:
            logger.error(f"Error in comprehensive document scoring: {e}")
            if conn:
                conn.rollback()
            return 0
        finally:
            if conn:
                conn.close()
    
    def score_single_document(self, doc_id: int):
        """
        Score a single document with comprehensive patent formulas.
        
        Args:
            doc_id: Document ID to score
            
        Returns:
            Dictionary with all framework scores
        """
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Get document content
            cursor.execute("""
                SELECT id, title, text_content, content
                FROM documents 
                WHERE id = %s
            """, (doc_id,))
            
            doc = cursor.fetchone()
            if not doc:
                return None
            
            title = doc.get('title', '')
            content = doc.get('text_content', '') or doc.get('content', '')
            
            if not content:
                return None
            
            # Apply comprehensive scoring
            scores = self.scoring_engine.assess_document_comprehensive(content, title)
            
            # Update database
            cursor.execute("""
                UPDATE documents 
                SET ai_cybersecurity_score = %s,
                    quantum_cybersecurity_score = %s,
                    ai_ethics_score = %s,
                    quantum_ethics_score = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (
                scores['ai_cybersecurity_score'],
                scores['quantum_cybersecurity_score'],
                scores['ai_ethics_score'],
                scores['quantum_ethics_score'],
                doc_id
            ))
            
            conn.commit()
            cursor.close()
            
            return scores
            
        except Exception as e:
            logger.error(f"Error scoring document {doc_id}: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()
    
    def get_scoring_statistics(self):
        """Get statistics about document scoring coverage."""
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Get scoring statistics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_documents,
                    COUNT(CASE WHEN ai_cybersecurity_score IS NOT NULL THEN 1 END) as ai_cyber_scored,
                    COUNT(CASE WHEN quantum_cybersecurity_score IS NOT NULL THEN 1 END) as quantum_cyber_scored,
                    COUNT(CASE WHEN ai_ethics_score IS NOT NULL THEN 1 END) as ai_ethics_scored,
                    COUNT(CASE WHEN quantum_ethics_score IS NOT NULL THEN 1 END) as quantum_ethics_scored,
                    AVG(ai_cybersecurity_score) as avg_ai_cyber,
                    AVG(quantum_cybersecurity_score) as avg_quantum_cyber,
                    AVG(ai_ethics_score) as avg_ai_ethics,
                    AVG(quantum_ethics_score) as avg_quantum_ethics
                FROM documents 
                WHERE text_content IS NOT NULL AND text_content != ''
            """)
            
            stats = cursor.fetchone()
            cursor.close()
            
            return {
                'total_documents': stats['total_documents'],
                'scoring_coverage': {
                    'ai_cybersecurity': stats['ai_cyber_scored'],
                    'quantum_cybersecurity': stats['quantum_cyber_scored'],
                    'ai_ethics': stats['ai_ethics_scored'],
                    'quantum_ethics': stats['quantum_ethics_scored']
                },
                'average_scores': {
                    'ai_cybersecurity': round(stats['avg_ai_cyber'] or 0, 1),
                    'quantum_cybersecurity': round(stats['avg_quantum_cyber'] or 0, 1),
                    'ai_ethics': round(stats['avg_ai_ethics'] or 0, 1),
                    'quantum_ethics': round(stats['avg_quantum_ethics'] or 0, 1)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting scoring statistics: {e}")
            return None
        finally:
            if conn:
                conn.close()

def apply_comprehensive_patent_scoring():
    """
    Main function to apply comprehensive patent-based scoring to all documents.
    Called from the UI or as a standalone operation.
    """
    scoring_system = DocumentScoringSystem()
    return scoring_system.score_all_documents()

def get_document_scores_summary():
    """Get summary of document scoring statistics."""
    scoring_system = DocumentScoringSystem()
    return scoring_system.get_scoring_statistics()