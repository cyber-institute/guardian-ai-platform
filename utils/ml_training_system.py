"""
ML Training System for GUARDIAN
Learns from scoring corrections and user feedback to improve future assessments
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from utils.ml_enhanced_scoring import MLEnhancedScoringEngine

class MLTrainingSystem:
    """
    Captures scoring patterns and user corrections to improve future document analysis
    """
    
    def __init__(self):
        self.training_data_path = "ml_training_data.json"
        self.scoring_engine = MLEnhancedScoringEngine()
        self.training_patterns = self._load_training_data()
    
    def _load_training_data(self) -> Dict:
        """Load existing training data"""
        if os.path.exists(self.training_data_path):
            try:
                with open(self.training_data_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "scoring_corrections": [],
            "content_patterns": {},
            "framework_applicability": {},
            "realistic_score_ranges": {
                "ai_cybersecurity": {"min": 10, "max": 85, "typical": 45},
                "quantum_cybersecurity": {"min": 1, "max": 5, "typical": 3},
                "ai_ethics": {"min": 5, "max": 80, "typical": 35},
                "quantum_ethics": {"min": 5, "max": 75, "typical": 30}
            },
            "topic_classification_rules": [],
            "metadata_extraction_improvements": []
        }
    
    def _save_training_data(self):
        """Save training data to file"""
        with open(self.training_data_path, 'w') as f:
            json.dump(self.training_patterns, f, indent=2, default=str)
    
    def record_scoring_correction(self, document_id: int, original_scores: Dict, 
                                corrected_scores: Dict, content: str, title: str):
        """Record when scores are corrected for learning"""
        
        correction_record = {
            "timestamp": datetime.now().isoformat(),
            "document_id": document_id,
            "title": title[:100],
            "content_snippet": content[:500],
            "original_scores": original_scores,
            "corrected_scores": corrected_scores,
            "correction_type": self._classify_correction_type(original_scores, corrected_scores),
            "content_features": self._extract_content_features(content, title)
        }
        
        self.training_patterns["scoring_corrections"].append(correction_record)
        self._update_scoring_patterns(correction_record)
        self._save_training_data()
    
    def _classify_correction_type(self, original: Dict, corrected: Dict) -> str:
        """Classify the type of correction made"""
        
        corrections = []
        
        for framework in ['ai_cybersecurity_score', 'quantum_cybersecurity_score', 
                         'ai_ethics_score', 'quantum_ethics_score']:
            orig_val = original.get(framework)
            corr_val = corrected.get(framework)
            
            if orig_val is not None and corr_val is None:
                corrections.append(f"removed_{framework}")
            elif orig_val is None and corr_val is not None:
                corrections.append(f"added_{framework}")
            elif orig_val != corr_val:
                if isinstance(orig_val, (int, float)) and isinstance(corr_val, (int, float)):
                    if orig_val > corr_val:
                        corrections.append(f"reduced_{framework}")
                    else:
                        corrections.append(f"increased_{framework}")
        
        return "|".join(corrections) if corrections else "no_change"
    
    def _extract_content_features(self, content: str, title: str) -> Dict:
        """Extract features from content for pattern learning"""
        
        content_lower = content.lower()
        title_lower = title.lower()
        combined = content_lower + " " + title_lower
        
        # Keyword density analysis
        ai_keywords = ['artificial intelligence', 'machine learning', 'ai ', 'neural network']
        quantum_keywords = ['quantum', 'post-quantum', 'quantum computing', 'quantum cryptography']
        cyber_keywords = ['cybersecurity', 'security', 'encryption', 'vulnerability']
        ethics_keywords = ['ethics', 'bias', 'fairness', 'transparency']
        
        return {
            "word_count": len(content.split()),
            "ai_keyword_density": sum(1 for kw in ai_keywords if kw in combined) / len(ai_keywords),
            "quantum_keyword_density": sum(1 for kw in quantum_keywords if kw in combined) / len(quantum_keywords),
            "cyber_keyword_density": sum(1 for kw in cyber_keywords if kw in combined) / len(cyber_keywords),
            "ethics_keyword_density": sum(1 for kw in ethics_keywords if kw in combined) / len(ethics_keywords),
            "has_technical_structure": "framework" in combined or "standard" in combined,
            "document_formality": "shall" in combined or "must" in combined,
            "title_indicates_topic": any(kw in title_lower for kw in ai_keywords + quantum_keywords)
        }
    
    def _update_scoring_patterns(self, correction: Dict):
        """Update scoring patterns based on corrections"""
        
        content_features = correction["content_features"]
        corrected_scores = correction["corrected_scores"]
        correction_type = correction["correction_type"]
        
        # Learn patterns for when frameworks should/shouldn't apply
        for framework in ['ai_cybersecurity_score', 'quantum_cybersecurity_score', 
                         'ai_ethics_score', 'quantum_ethics_score']:
            
            score = corrected_scores.get(framework)
            framework_key = framework.replace('_score', '')
            
            if framework_key not in self.training_patterns["framework_applicability"]:
                self.training_patterns["framework_applicability"][framework_key] = {
                    "should_apply_patterns": [],
                    "should_not_apply_patterns": []
                }
            
            # Learn when framework should apply
            if score is not None and score > 0:
                self.training_patterns["framework_applicability"][framework_key]["should_apply_patterns"].append({
                    "features": content_features,
                    "score": score,
                    "confidence": 0.8
                })
            
            # Learn when framework should NOT apply
            if score is None and f"removed_{framework}" in correction_type:
                self.training_patterns["framework_applicability"][framework_key]["should_not_apply_patterns"].append({
                    "features": content_features,
                    "reason": "topic_mismatch",
                    "confidence": 0.9
                })
    
    def predict_framework_applicability(self, content: str, title: str) -> Dict[str, bool]:
        """Predict which frameworks should apply based on learned patterns"""
        
        content_features = self._extract_content_features(content, title)
        predictions = {}
        
        for framework, patterns in self.training_patterns["framework_applicability"].items():
            should_apply_score = 0
            should_not_apply_score = 0
            
            # Check positive patterns
            for pattern in patterns.get("should_apply_patterns", []):
                similarity = self._calculate_feature_similarity(content_features, pattern["features"])
                should_apply_score += similarity * pattern["confidence"]
            
            # Check negative patterns
            for pattern in patterns.get("should_not_apply_patterns", []):
                similarity = self._calculate_feature_similarity(content_features, pattern["features"])
                should_not_apply_score += similarity * pattern["confidence"]
            
            # Make prediction
            predictions[framework] = should_apply_score > should_not_apply_score
        
        return predictions
    
    def _calculate_feature_similarity(self, features1: Dict, features2: Dict) -> float:
        """Calculate similarity between two feature sets"""
        
        similarity_scores = []
        
        for key in features1:
            if key in features2:
                val1, val2 = features1[key], features2[key]
                
                if isinstance(val1, bool) and isinstance(val2, bool):
                    similarity_scores.append(1.0 if val1 == val2 else 0.0)
                elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                    max_val = max(abs(val1), abs(val2), 1)
                    similarity_scores.append(1.0 - abs(val1 - val2) / max_val)
        
        return sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
    
    def get_recommended_score_range(self, framework: str, content_features: Dict) -> Dict:
        """Get recommended score range based on similar documents"""
        
        base_range = self.training_patterns["realistic_score_ranges"].get(framework, {})
        
        # Find similar documents in training data
        similar_corrections = []
        for correction in self.training_patterns["scoring_corrections"]:
            if framework in correction["corrected_scores"]:
                similarity = self._calculate_feature_similarity(
                    content_features, correction["content_features"]
                )
                if similarity > 0.7:  # High similarity threshold
                    similar_corrections.append({
                        "score": correction["corrected_scores"][framework],
                        "similarity": similarity
                    })
        
        if similar_corrections:
            # Weight scores by similarity
            weighted_scores = [
                corr["score"] * corr["similarity"] 
                for corr in similar_corrections 
                if corr["score"] is not None
            ]
            
            if weighted_scores:
                avg_score = sum(weighted_scores) / len(weighted_scores)
                return {
                    "recommended": int(avg_score),
                    "min": max(int(avg_score * 0.8), base_range.get("min", 0)),
                    "max": min(int(avg_score * 1.2), base_range.get("max", 100)),
                    "confidence": min(len(similar_corrections) / 5, 1.0)
                }
        
        return base_range
    
    def enhance_scoring_with_ml(self, content: str, title: str) -> Dict:
        """Enhance scoring using ML training patterns"""
        
        # Get base ML scores
        base_scores = self.scoring_engine.analyze_document_comprehensive(content, title)
        
        # Apply training improvements
        content_features = self._extract_content_features(content, title)
        applicability_predictions = self.predict_framework_applicability(content, title)
        
        enhanced_scores = {}
        for framework, score in base_scores.items():
            framework_key = framework.replace('_score', '')
            
            # Check if framework should apply based on training
            if not applicability_predictions.get(framework_key, True):
                enhanced_scores[framework] = None
                continue
            
            # Adjust score based on training patterns
            if score is not None:
                score_range = self.get_recommended_score_range(framework, content_features)
                if score_range.get("confidence", 0) > 0.5:
                    # Adjust score within learned range
                    recommended = score_range.get("recommended", score)
                    min_score = score_range.get("min", 0)
                    max_score = score_range.get("max", 100)
                    
                    adjusted_score = max(min_score, min(score, max_score))
                    # Blend with recommendation
                    enhanced_scores[framework] = int(0.7 * adjusted_score + 0.3 * recommended)
                else:
                    enhanced_scores[framework] = score
            else:
                enhanced_scores[framework] = None
        
        return enhanced_scores

# Global training system instance
ml_training_system = MLTrainingSystem()

def train_from_corrections(doc_id: int, original_scores: Dict, corrected_scores: Dict, 
                          content: str, title: str):
    """Record scoring corrections for training"""
    ml_training_system.record_scoring_correction(doc_id, original_scores, corrected_scores, content, title)

def get_ml_enhanced_scores(content: str, title: str) -> Dict:
    """Get ML-enhanced scores using training patterns"""
    return ml_training_system.enhance_scoring_with_ml(content, title)