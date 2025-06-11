"""
AI-Powered Document Recommendation Engine for GUARDIAN
Provides intelligent document suggestions based on content analysis, scoring patterns, and user context
"""

import os
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

class DocumentRecommendationEngine:
    """
    AI-powered recommendation system that suggests relevant documents based on:
    - Content similarity using TF-IDF and cosine similarity
    - Patent scoring patterns and framework alignment
    - Document type and organizational context
    - User interaction patterns
    """
    
    def __init__(self):
        self.vectorizer = None
        self.document_vectors = None
        self.documents_cache = None
        self.logger = logging.getLogger(__name__)
        
    def get_db_connection(self):
        """Get database connection."""
        return psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
    
    def load_documents(self, force_refresh=False):
        """Load all documents from database for analysis."""
        if self.documents_cache is not None and not force_refresh:
            return self.documents_cache
            
        conn = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, title, content, text_content, document_type, author_organization,
                       ai_cybersecurity_score, quantum_cybersecurity_score, 
                       ai_ethics_score, quantum_ethics_score,
                       created_at, source
                FROM documents 
                WHERE text_content IS NOT NULL 
                AND text_content != ''
                ORDER BY id
            """)
            
            self.documents_cache = cursor.fetchall()
            return self.documents_cache
            
        except Exception as e:
            self.logger.error(f"Error loading documents: {e}")
            return []
        finally:
            if conn:
                conn.close()
    
    def build_content_vectors(self, documents=None):
        """Build TF-IDF vectors for document content similarity analysis."""
        if documents is None:
            documents = self.load_documents()
        
        if not documents:
            return
        
        # Prepare document texts for vectorization
        doc_texts = []
        for doc in documents:
            # Handle database tuple format: (id, title, content, text_content, document_type, author_organization, ...)
            if isinstance(doc, tuple):
                title = doc[1] or ''
                content = doc[2] or ''
                text_content = doc[3] or ''
            else:
                # Handle dictionary format for compatibility
                title = doc.get('title', '')
                content = doc.get('content', '')
                text_content = doc.get('text_content', '') or doc.get('content', '')
            
            combined_text = f"{title} {content} {text_content[:1000]}"
            doc_texts.append(combined_text.lower())
        
        # Create TF-IDF vectors
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.8
        )
        
        self.document_vectors = self.vectorizer.fit_transform(doc_texts)
        
    def calculate_content_similarity(self, target_doc_id: int, top_k: int = 5) -> List[Tuple[int, float]]:
        """Calculate content similarity between target document and all others."""
        documents = self.load_documents()
        
        if not documents or self.document_vectors is None:
            return []
        
        # Find target document index
        target_idx = None
        for idx, doc in enumerate(documents):
            if doc['id'] == target_doc_id:
                target_idx = idx
                break
        
        if target_idx is None:
            return []
        
        # Calculate cosine similarities
        target_vector = self.document_vectors[target_idx]
        similarities = cosine_similarity(target_vector, self.document_vectors).flatten()
        
        # Get top similar documents (excluding self)
        similar_indices = similarities.argsort()[::-1]
        results = []
        
        for idx in similar_indices:
            if idx != target_idx and len(results) < top_k:
                doc_id = documents[idx]['id']
                similarity_score = similarities[idx]
                if similarity_score > 0.1:  # Minimum similarity threshold
                    results.append((doc_id, similarity_score))
        
        return results
    
    def calculate_scoring_similarity(self, target_doc_id: int, top_k: int = 5) -> List[Tuple[int, float]]:
        """Find documents with similar patent scoring patterns."""
        documents = self.load_documents()
        
        if not documents:
            return []
        
        # Find target document
        target_doc = None
        for doc in documents:
            if doc['id'] == target_doc_id:
                target_doc = doc
                break
        
        if not target_doc:
            return []
        
        # Extract target scores
        target_scores = np.array([
            target_doc.get('ai_cybersecurity_score', 0) or 0,
            target_doc.get('quantum_cybersecurity_score', 0) or 0,
            target_doc.get('ai_ethics_score', 0) or 0,
            target_doc.get('quantum_ethics_score', 0) or 0
        ])
        
        # Calculate scoring pattern similarities
        similarities = []
        for doc in documents:
            if doc['id'] == target_doc_id:
                continue
                
            doc_scores = np.array([
                doc.get('ai_cybersecurity_score', 0) or 0,
                doc.get('quantum_cybersecurity_score', 0) or 0,
                doc.get('ai_ethics_score', 0) or 0,
                doc.get('quantum_ethics_score', 0) or 0
            ])
            
            # Calculate normalized similarity
            if np.linalg.norm(target_scores) > 0 and np.linalg.norm(doc_scores) > 0:
                similarity = np.dot(target_scores, doc_scores) / (
                    np.linalg.norm(target_scores) * np.linalg.norm(doc_scores)
                )
                similarities.append((doc['id'], similarity))
        
        # Sort by similarity and return top_k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def get_context_recommendations(self, document_type: str = None, organization: str = None, 
                                  framework_focus: str = None, top_k: int = 5) -> List[Dict]:
        """Get recommendations based on contextual criteria."""
        documents = self.load_documents()
        
        if not documents:
            return []
        
        scored_docs = []
        
        for doc in documents:
            score = 0
            
            # Document type matching
            if document_type and doc.get('document_type', '').lower() == document_type.lower():
                score += 3
            
            # Organization matching
            if organization and organization.lower() in (doc.get('organization', '') or '').lower():
                score += 2
            
            # Framework focus scoring
            if framework_focus:
                if framework_focus == 'ai_cybersecurity':
                    score += (doc.get('ai_cybersecurity_score', 0) or 0) / 20
                elif framework_focus == 'quantum_cybersecurity':
                    score += (doc.get('quantum_cybersecurity_score', 0) or 0) * 2
                elif framework_focus == 'ai_ethics':
                    score += (doc.get('ai_ethics_score', 0) or 0) / 20
                elif framework_focus == 'quantum_ethics':
                    score += (doc.get('quantum_ethics_score', 0) or 0) / 20
            
            if score > 0:
                scored_docs.append((doc, score))
        
        # Sort by score and return top documents
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in scored_docs[:top_k]]
    
    def get_comprehensive_recommendations(self, target_doc_id: int, 
                                        include_content_similarity: bool = True,
                                        include_scoring_similarity: bool = True,
                                        include_context: bool = True,
                                        max_recommendations: int = 10) -> Dict[str, List]:
        """
        Get comprehensive recommendations using multiple approaches.
        
        Returns:
            Dict with recommendation categories and their results
        """
        # Initialize content vectors if needed
        if self.document_vectors is None:
            self.build_content_vectors()
        
        recommendations = {
            'content_similar': [],
            'scoring_similar': [],
            'contextual': [],
            'combined': []
        }
        
        documents = self.load_documents()
        target_doc = None
        
        for doc in documents:
            if doc['id'] == target_doc_id:
                target_doc = doc
                break
        
        if not target_doc:
            return recommendations
        
        # Content-based recommendations
        if include_content_similarity:
            content_similar = self.calculate_content_similarity(target_doc_id, top_k=5)
            recommendations['content_similar'] = [
                self._get_document_info(doc_id, similarity) 
                for doc_id, similarity in content_similar
            ]
        
        # Scoring pattern recommendations
        if include_scoring_similarity:
            scoring_similar = self.calculate_scoring_similarity(target_doc_id, top_k=5)
            recommendations['scoring_similar'] = [
                self._get_document_info(doc_id, similarity) 
                for doc_id, similarity in scoring_similar
            ]
        
        # Contextual recommendations
        if include_context:
            contextual_docs = self.get_context_recommendations(
                document_type=target_doc.get('document_type'),
                organization=target_doc.get('organization'),
                top_k=5
            )
            recommendations['contextual'] = [
                self._format_document_info(doc) for doc in contextual_docs
            ]
        
        # Combined recommendations with weighted scoring
        all_recommended_ids = set()
        weighted_scores = defaultdict(float)
        
        # Weight content similarity
        for doc_id, similarity in content_similar if include_content_similarity else []:
            weighted_scores[doc_id] += similarity * 0.4
            all_recommended_ids.add(doc_id)
        
        # Weight scoring similarity
        for doc_id, similarity in scoring_similar if include_scoring_similarity else []:
            weighted_scores[doc_id] += similarity * 0.3
            all_recommended_ids.add(doc_id)
        
        # Weight contextual relevance
        for doc in contextual_docs if include_context else []:
            doc_id = doc['id']
            weighted_scores[doc_id] += 0.3
            all_recommended_ids.add(doc_id)
        
        # Sort by combined weighted score
        combined_recommendations = sorted(
            [(doc_id, weighted_scores[doc_id]) for doc_id in all_recommended_ids],
            key=lambda x: x[1],
            reverse=True
        )
        
        recommendations['combined'] = [
            self._get_document_info(doc_id, score) 
            for doc_id, score in combined_recommendations[:max_recommendations]
        ]
        
        return recommendations
    
    def _get_document_info(self, doc_id: int, score: float) -> Dict:
        """Get formatted document information with recommendation score."""
        documents = self.load_documents()
        
        for doc in documents:
            if doc['id'] == doc_id:
                return self._format_document_info(doc, score)
        
        return {}
    
    def _format_document_info(self, doc: dict, score: float = None) -> Dict:
        """Format document information for recommendations."""
        return {
            'id': doc['id'],
            'title': doc.get('title', 'Unknown Title'),
            'document_type': doc.get('document_type', 'Unknown'),
            'organization': doc.get('organization', 'Unknown'),
            'ai_cybersecurity_score': doc.get('ai_cybersecurity_score', 0),
            'quantum_cybersecurity_score': doc.get('quantum_cybersecurity_score', 0),
            'ai_ethics_score': doc.get('ai_ethics_score', 0),
            'quantum_ethics_score': doc.get('quantum_ethics_score', 0),
            'content_preview': (doc.get('content', '') or '')[:200] + "..." if doc.get('content') else '',
            'recommendation_score': round(score, 3) if score is not None else None,
            'date': doc.get('date'),
            'source': doc.get('source')
        }
    
    def get_trending_documents(self, framework: str = None, top_k: int = 10) -> List[Dict]:
        """Get trending documents based on scoring patterns and recent activity."""
        documents = self.load_documents()
        
        if not documents:
            return []
        
        scored_docs = []
        
        for doc in documents:
            # Calculate trending score based on multiple factors
            trend_score = 0
            
            # High scores in specific frameworks indicate relevance
            if framework:
                if framework == 'ai_cybersecurity':
                    trend_score = doc.get('ai_cybersecurity_score', 0) or 0
                elif framework == 'quantum_cybersecurity':
                    trend_score = (doc.get('quantum_cybersecurity_score', 0) or 0) * 20
                elif framework == 'ai_ethics':
                    trend_score = doc.get('ai_ethics_score', 0) or 0
                elif framework == 'quantum_ethics':
                    trend_score = doc.get('quantum_ethics_score', 0) or 0
            else:
                # Overall relevance score
                trend_score = (
                    (doc.get('ai_cybersecurity_score', 0) or 0) +
                    (doc.get('quantum_cybersecurity_score', 0) or 0) * 20 +
                    (doc.get('ai_ethics_score', 0) or 0) +
                    (doc.get('quantum_ethics_score', 0) or 0)
                ) / 4
            
            if trend_score > 0:
                scored_docs.append((doc, trend_score))
        
        # Sort by trend score
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        return [self._format_document_info(doc, score) for doc, score in scored_docs[:top_k]]

# Global instance for use across the application
recommendation_engine = DocumentRecommendationEngine()