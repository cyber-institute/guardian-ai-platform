"""
Multi-LLM Duplicate Detection System
Prevents ingestion of duplicate documents across all input methods
"""

import os
import hashlib
import json
from typing import Dict, List, Tuple, Optional
from openai import OpenAI
from utils.db import fetch_documents

class DuplicateDetector:
    """Advanced duplicate detection using content similarity and metadata analysis"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def check_for_duplicates(self, title: str, content: str, url: str = "", filename: str = "") -> Dict[str, any]:
        """Comprehensive duplicate detection across all existing documents"""
        
        # Get all existing documents
        existing_docs = fetch_documents()
        if not existing_docs:
            return {"is_duplicate": False, "confidence": 0.0, "matches": []}
        
        # Multi-layer duplicate detection
        exact_match = self._check_exact_duplicates(content, existing_docs)
        if exact_match["is_duplicate"]:
            return exact_match
        
        content_similarity = self._check_content_similarity(title, content, existing_docs)
        if content_similarity["is_duplicate"]:
            return content_similarity
        
        metadata_similarity = self._check_metadata_similarity(title, url, filename, existing_docs)
        
        return metadata_similarity
    
    def _check_exact_duplicates(self, content: str, existing_docs: List[Dict]) -> Dict[str, any]:
        """Check for exact content matches using hashing"""
        
        # Create content hash
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        for doc in existing_docs:
            existing_content = doc.get('text', '') or doc.get('content', '')
            existing_hash = hashlib.sha256(existing_content.encode('utf-8')).hexdigest()
            
            if content_hash == existing_hash:
                return {
                    "is_duplicate": True,
                    "confidence": 1.0,
                    "match_type": "exact_content",
                    "matches": [{
                        "id": doc.get('id'),
                        "title": doc.get('title', 'Unknown'),
                        "reason": "Identical content hash"
                    }]
                }
        
        return {"is_duplicate": False, "confidence": 0.0, "matches": []}
    
    def _check_content_similarity(self, title: str, content: str, existing_docs: List[Dict]) -> Dict[str, any]:
        """Check for content similarity using LLM analysis"""
        
        # Check against each existing document
        high_similarity_matches = []
        
        for doc in existing_docs:
            existing_title = doc.get('title', '')
            existing_content = doc.get('text', '') or doc.get('content', '')
            
            if not existing_content or len(existing_content) < 100:
                continue
            
            similarity_result = self._analyze_content_similarity(
                title, content[:2000], existing_title, existing_content[:2000]
            )
            
            if similarity_result["similarity"] > 0.8:
                high_similarity_matches.append({
                    "id": doc.get('id'),
                    "title": existing_title,
                    "similarity": similarity_result["similarity"],
                    "reason": similarity_result["reasoning"]
                })
        
        if high_similarity_matches:
            # Sort by similarity score
            high_similarity_matches.sort(key=lambda x: x["similarity"], reverse=True)
            best_match = high_similarity_matches[0]
            
            return {
                "is_duplicate": best_match["similarity"] > 0.85,
                "confidence": best_match["similarity"],
                "match_type": "content_similarity",
                "matches": high_similarity_matches[:3]  # Top 3 matches
            }
        
        return {"is_duplicate": False, "confidence": 0.0, "matches": []}
    
    def _analyze_content_similarity(self, title1: str, content1: str, title2: str, content2: str) -> Dict[str, any]:
        """Use LLM to analyze content similarity"""
        
        try:
            prompt = f"""
            Compare these two documents for similarity and determine if they are the same document:
            
            DOCUMENT 1:
            Title: {title1}
            Content: {content1}
            
            DOCUMENT 2:
            Title: {title2}
            Content: {content2}
            
            Analyze for:
            1. Content overlap and similarity
            2. Same underlying document with different formatting
            3. Different versions of the same document
            4. Same executive orders, policies, or reports
            
            Consider documents duplicates if they:
            - Have identical or very similar content structure
            - Are the same policy/order with minor formatting differences
            - Cover identical topics with same key points
            
            Respond with JSON:
            {{
                "similarity": 0.0-1.0,
                "reasoning": "explanation of similarity assessment",
                "same_document": true/false
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content)
            return {
                "similarity": float(result.get("similarity", 0.0)),
                "reasoning": result.get("reasoning", ""),
                "same_document": result.get("same_document", False)
            }
            
        except Exception as e:
            print(f"LLM similarity analysis failed: {e}")
            return {"similarity": 0.0, "reasoning": "Analysis failed", "same_document": False}
    
    def _check_metadata_similarity(self, title: str, url: str, filename: str, existing_docs: List[Dict]) -> Dict[str, any]:
        """Check for metadata-based duplicates"""
        
        metadata_matches = []
        
        for doc in existing_docs:
            similarity_score = 0.0
            reasons = []
            
            # Title similarity
            existing_title = doc.get('title', '').lower()
            if title.lower() == existing_title:
                similarity_score += 0.4
                reasons.append("Identical titles")
            elif title.lower() in existing_title or existing_title in title.lower():
                similarity_score += 0.2
                reasons.append("Similar titles")
            
            # URL similarity
            existing_url = doc.get('url', '') or doc.get('source_url', '')
            if url and existing_url and url.lower() == existing_url.lower():
                similarity_score += 0.3
                reasons.append("Identical URLs")
            
            # Filename similarity
            existing_filename = doc.get('filename', '')
            if filename and existing_filename:
                if filename.lower() == existing_filename.lower():
                    similarity_score += 0.3
                    reasons.append("Identical filenames")
                elif filename.lower().replace('.pdf', '') == existing_filename.lower().replace('.pdf', ''):
                    similarity_score += 0.2
                    reasons.append("Similar filenames")
            
            if similarity_score > 0.5:
                metadata_matches.append({
                    "id": doc.get('id'),
                    "title": doc.get('title', 'Unknown'),
                    "similarity": similarity_score,
                    "reason": "; ".join(reasons)
                })
        
        if metadata_matches:
            metadata_matches.sort(key=lambda x: x["similarity"], reverse=True)
            best_match = metadata_matches[0]
            
            return {
                "is_duplicate": best_match["similarity"] > 0.7,
                "confidence": best_match["similarity"],
                "match_type": "metadata_similarity",
                "matches": metadata_matches[:2]
            }
        
        return {"is_duplicate": False, "confidence": 0.0, "matches": []}

def check_document_duplicates(title: str, content: str, url: str = "", filename: str = "") -> Dict[str, any]:
    """Main function for duplicate detection"""
    detector = DuplicateDetector()
    return detector.check_for_duplicates(title, content, url, filename)