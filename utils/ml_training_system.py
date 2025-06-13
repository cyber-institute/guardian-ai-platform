"""
Machine Learning Training System for GUARDIAN
Captures verification patterns and builds training datasets for continuous improvement
"""

import json
import sqlite3
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class VerificationPattern:
    """Single verification event for training"""
    document_id: str
    original_extraction: Dict[str, Any]
    verified_extraction: Dict[str, Any]
    user_corrections: Dict[str, Any]
    content_sample: str
    extraction_confidence: Dict[str, float]
    timestamp: str
    document_type: str
    source_type: str  # 'url', 'upload', 'manual'
    content_hash: str

@dataclass
class LearningPattern:
    """Identified pattern from multiple verifications"""
    pattern_id: str
    pattern_type: str  # 'title', 'author', 'organization', 'topic'
    trigger_conditions: List[str]
    correction_rule: str
    confidence_score: float
    usage_count: int
    success_rate: float
    created_at: str
    last_updated: str

class MLTrainingSystem:
    """
    Advanced machine learning training system that learns from user verifications
    and builds patterns for improved automatic extraction
    """
    
    def __init__(self, db_path: str = "ml_training.db"):
        self.db_path = db_path
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.logger = logging.getLogger(__name__)
        self._initialize_database()
        self.learned_patterns = self._load_learned_patterns()
        
    def _initialize_database(self):
        """Initialize SQLite database for training data storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verification patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT,
                original_extraction TEXT,
                verified_extraction TEXT,
                user_corrections TEXT,
                content_sample TEXT,
                extraction_confidence TEXT,
                timestamp TEXT,
                document_type TEXT,
                source_type TEXT,
                content_hash TEXT UNIQUE
            )
        """)
        
        # Learned patterns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_id TEXT UNIQUE,
                pattern_type TEXT,
                trigger_conditions TEXT,
                correction_rule TEXT,
                confidence_score REAL,
                usage_count INTEGER,
                success_rate REAL,
                created_at TEXT,
                last_updated TEXT
            )
        """)
        
        # Performance metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ml_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_type TEXT,
                metric_value REAL,
                document_count INTEGER,
                timestamp TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def capture_verification_event(
        self,
        document_id: str,
        original_extraction: Dict[str, Any],
        verified_extraction: Dict[str, Any],
        content: str,
        document_type: str = "unknown",
        source_type: str = "url"
    ) -> str:
        """
        Capture a verification event for training
        Returns the pattern ID for tracking
        """
        
        # Calculate content hash for deduplication
        content_hash = hashlib.md5(content.encode()).hexdigest()
        
        # Extract user corrections
        user_corrections = self._identify_corrections(original_extraction, verified_extraction)
        
        # Calculate extraction confidence
        extraction_confidence = self._calculate_extraction_confidence(
            original_extraction, verified_extraction
        )
        
        # Create verification pattern
        pattern = VerificationPattern(
            document_id=document_id,
            original_extraction=original_extraction,
            verified_extraction=verified_extraction,
            user_corrections=user_corrections,
            content_sample=content[:2000],  # First 2000 chars for analysis
            extraction_confidence=extraction_confidence,
            timestamp=datetime.now().isoformat(),
            document_type=document_type,
            source_type=source_type,
            content_hash=content_hash
        )
        
        # Store in database
        pattern_id = self._store_verification_pattern(pattern)
        
        # Analyze for new learning patterns
        self._analyze_for_new_patterns(pattern)
        
        # Update existing pattern performance
        self._update_pattern_performance()
        
        self.logger.info(f"Captured verification pattern: {pattern_id}")
        return pattern_id
    
    def _identify_corrections(
        self, 
        original: Dict[str, Any], 
        verified: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Identify what the user corrected"""
        corrections = {}
        
        for key in verified.keys():
            original_val = original.get(key, "")
            verified_val = verified.get(key, "")
            
            if original_val != verified_val:
                corrections[key] = {
                    'original': original_val,
                    'corrected': verified_val,
                    'correction_type': self._classify_correction_type(key, original_val, verified_val)
                }
        
        return corrections
    
    def _classify_correction_type(self, field: str, original: str, corrected: str) -> str:
        """Classify the type of correction made"""
        if not original and corrected:
            return "missing_field_added"
        elif original and not corrected:
            return "incorrect_field_removed"
        elif len(corrected) > len(original):
            return "field_expanded"
        elif len(corrected) < len(original):
            return "field_truncated"
        elif original.lower() != corrected.lower():
            return "field_reformatted"
        else:
            return "field_replaced"
    
    def _calculate_extraction_confidence(
        self, 
        original: Dict[str, Any], 
        verified: Dict[str, Any]
    ) -> Dict[str, float]:
        """Calculate confidence scores for each extracted field"""
        confidence = {}
        
        for key in verified.keys():
            original_val = str(original.get(key, ""))
            verified_val = str(verified.get(key, ""))
            
            if original_val == verified_val:
                confidence[key] = 1.0  # Perfect extraction
            elif not original_val:
                confidence[key] = 0.0  # Missed extraction
            else:
                # Calculate similarity using character overlap
                similarity = self._calculate_string_similarity(original_val, verified_val)
                confidence[key] = similarity
        
        return confidence
    
    def _calculate_string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings"""
        if not str1 or not str2:
            return 0.0
        
        # Simple character-based similarity
        longer = str1 if len(str1) > len(str2) else str2
        shorter = str1 if len(str1) <= len(str2) else str2
        
        if len(longer) == 0:
            return 1.0
        
        # Calculate edit distance approximation
        matches = sum(1 for i, char in enumerate(shorter) if i < len(longer) and char == longer[i])
        return matches / len(longer)
    
    def _store_verification_pattern(self, pattern: VerificationPattern) -> str:
        """Store verification pattern in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO verification_patterns 
                (document_id, original_extraction, verified_extraction, user_corrections,
                 content_sample, extraction_confidence, timestamp, document_type, 
                 source_type, content_hash)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern.document_id,
                json.dumps(pattern.original_extraction),
                json.dumps(pattern.verified_extraction),
                json.dumps(pattern.user_corrections),
                pattern.content_sample,
                json.dumps(pattern.extraction_confidence),
                pattern.timestamp,
                pattern.document_type,
                pattern.source_type,
                pattern.content_hash
            ))
            
            pattern_id = cursor.lastrowid
            conn.commit()
            return str(pattern_id)
            
        except Exception as e:
            self.logger.error(f"Error storing verification pattern: {e}")
            return ""
        finally:
            conn.close()
    
    def _analyze_for_new_patterns(self, pattern: VerificationPattern):
        """Analyze verification event for new learning patterns"""
        
        # Analyze title extraction patterns
        if 'title' in pattern.user_corrections:
            self._learn_title_pattern(pattern)
        
        # Analyze author extraction patterns
        if 'author' in pattern.user_corrections:
            self._learn_author_pattern(pattern)
        
        # Analyze organization extraction patterns
        if 'organization' in pattern.user_corrections:
            self._learn_organization_pattern(pattern)
        
        # Analyze topic classification patterns
        if 'topic' in pattern.user_corrections:
            self._learn_topic_pattern(pattern)
    
    def _learn_title_pattern(self, pattern: VerificationPattern):
        """Learn patterns for title extraction"""
        correction = pattern.user_corrections['title']
        original_title = correction['original']
        corrected_title = correction['corrected']
        content = pattern.content_sample
        
        # Identify content patterns that indicate the correct title
        title_indicators = self._extract_title_indicators(content, corrected_title)
        
        if title_indicators:
            # Create or update learning pattern
            pattern_rule = {
                'indicators': title_indicators,
                'extraction_rule': self._create_title_extraction_rule(title_indicators, corrected_title),
                'confidence_threshold': 0.8
            }
            
            self._store_learned_pattern(
                pattern_type='title',
                trigger_conditions=title_indicators,
                correction_rule=json.dumps(pattern_rule),
                confidence_score=0.8
            )
    
    def _extract_title_indicators(self, content: str, correct_title: str) -> List[str]:
        """Extract indicators that point to the correct title"""
        indicators = []
        
        # Look for title in first 500 characters
        if correct_title.lower() in content[:500].lower():
            indicators.append("title_in_first_500_chars")
        
        # Check for specific patterns
        if "policy" in correct_title.lower() and "policy" in content[:200].lower():
            indicators.append("policy_document_pattern")
        
        if "quantum" in correct_title.lower() and "quantum" in content[:300].lower():
            indicators.append("quantum_document_pattern")
        
        if "approach to" in correct_title.lower():
            indicators.append("approach_document_pattern")
        
        # Check for author attribution patterns
        if "by " in content[:400].lower():
            indicators.append("author_attribution_present")
        
        return indicators
    
    def _create_title_extraction_rule(self, indicators: List[str], correct_title: str) -> str:
        """Create extraction rule based on indicators"""
        rule_components = []
        
        if "quantum_document_pattern" in indicators:
            rule_components.append("Look for quantum-related titles in first 300 characters")
        
        if "policy_document_pattern" in indicators:
            rule_components.append("Extract policy document titles with 'Policy' keyword")
        
        if "approach_document_pattern" in indicators:
            rule_components.append("Extract titles containing 'Approach to' pattern")
        
        return "; ".join(rule_components)
    
    def _learn_author_pattern(self, pattern: VerificationPattern):
        """Learn patterns for author extraction"""
        correction = pattern.user_corrections['author']
        corrected_author = correction['corrected']
        content = pattern.content_sample
        
        # Look for author patterns in content
        author_indicators = []
        
        if f"by {corrected_author.lower()}" in content.lower():
            author_indicators.append("by_author_pattern")
        
        if corrected_author.lower() in content[:500].lower():
            author_indicators.append("author_in_first_500_chars")
        
        if author_indicators:
            pattern_rule = {
                'indicators': author_indicators,
                'extraction_pattern': f"Extract author near 'by' keyword: {corrected_author}"
            }
            
            self._store_learned_pattern(
                pattern_type='author',
                trigger_conditions=author_indicators,
                correction_rule=json.dumps(pattern_rule),
                confidence_score=0.75
            )
    
    def _learn_organization_pattern(self, pattern: VerificationPattern):
        """Learn patterns for organization extraction"""
        # Similar to author pattern learning but for organizations
        pass
    
    def _learn_topic_pattern(self, pattern: VerificationPattern):
        """Learn patterns for topic classification"""
        correction = pattern.user_corrections['topic']
        corrected_topic = correction['corrected']
        content = pattern.content_sample
        
        # Analyze content for topic indicators
        topic_keywords = self._extract_topic_keywords(content, corrected_topic)
        
        if topic_keywords:
            pattern_rule = {
                'topic': corrected_topic,
                'keywords': topic_keywords,
                'classification_rule': f"Classify as {corrected_topic} when keywords present: {', '.join(topic_keywords)}"
            }
            
            self._store_learned_pattern(
                pattern_type='topic',
                trigger_conditions=topic_keywords,
                correction_rule=json.dumps(pattern_rule),
                confidence_score=0.85
            )
    
    def _extract_topic_keywords(self, content: str, topic: str) -> List[str]:
        """Extract keywords that indicate the correct topic"""
        content_lower = content.lower()
        keywords = []
        
        if topic.lower() == "quantum":
            quantum_keywords = ["quantum", "quantum policy", "quantum approach", "quantum technology"]
            keywords = [kw for kw in quantum_keywords if kw in content_lower]
        elif topic.lower() == "ai":
            ai_keywords = ["artificial intelligence", "ai policy", "machine learning", "ai framework"]
            keywords = [kw for kw in ai_keywords if kw in content_lower]
        
        return keywords
    
    def _store_learned_pattern(
        self,
        pattern_type: str,
        trigger_conditions: List[str],
        correction_rule: str,
        confidence_score: float
    ):
        """Store a learned pattern in the database"""
        
        # Generate pattern ID
        pattern_id = hashlib.md5(
            (pattern_type + str(trigger_conditions) + correction_rule).encode()
        ).hexdigest()[:12]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if pattern exists
            cursor.execute(
                "SELECT id, usage_count FROM learned_patterns WHERE pattern_id = ?",
                (pattern_id,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing pattern
                cursor.execute("""
                    UPDATE learned_patterns 
                    SET usage_count = usage_count + 1, last_updated = ?
                    WHERE pattern_id = ?
                """, (datetime.now().isoformat(), pattern_id))
            else:
                # Insert new pattern
                cursor.execute("""
                    INSERT INTO learned_patterns 
                    (pattern_id, pattern_type, trigger_conditions, correction_rule,
                     confidence_score, usage_count, success_rate, created_at, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    pattern_id,
                    pattern_type,
                    json.dumps(trigger_conditions),
                    correction_rule,
                    confidence_score,
                    1,
                    0.0,  # Will be calculated later
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            
        except Exception as e:
            self.logger.error(f"Error storing learned pattern: {e}")
        finally:
            conn.close()
    
    def _load_learned_patterns(self) -> List[LearningPattern]:
        """Load learned patterns from database"""
        patterns = []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM learned_patterns")
            rows = cursor.fetchall()
            
            for row in rows:
                pattern = LearningPattern(
                    pattern_id=row[1],
                    pattern_type=row[2],
                    trigger_conditions=json.loads(row[3]),
                    correction_rule=row[4],
                    confidence_score=row[5],
                    usage_count=row[6],
                    success_rate=row[7],
                    created_at=row[8],
                    last_updated=row[9]
                )
                patterns.append(pattern)
                
        except Exception as e:
            self.logger.error(f"Error loading learned patterns: {e}")
        finally:
            conn.close()
        
        return patterns
    
    def apply_learned_patterns(
        self,
        content: str,
        extracted_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply learned patterns to improve extraction"""
        
        improved_metadata = extracted_metadata.copy()
        
        for pattern in self.learned_patterns:
            if pattern.confidence_score < 0.7:  # Skip low-confidence patterns
                continue
            
            # Check if trigger conditions are met
            if self._pattern_applies(pattern, content):
                # Apply the pattern
                improved_metadata = self._apply_pattern(pattern, content, improved_metadata)
        
        return improved_metadata
    
    def _pattern_applies(self, pattern: LearningPattern, content: str) -> bool:
        """Check if a learned pattern applies to the given content"""
        content_lower = content.lower()
        
        # Check if trigger conditions are present
        triggers_met = 0
        for condition in pattern.trigger_conditions:
            if condition.replace("_", " ") in content_lower:
                triggers_met += 1
        
        # Pattern applies if majority of conditions are met
        return triggers_met >= len(pattern.trigger_conditions) * 0.6
    
    def _apply_pattern(
        self,
        pattern: LearningPattern,
        content: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a specific learned pattern to improve metadata"""
        
        try:
            rule_data = json.loads(pattern.correction_rule)
            
            if pattern.pattern_type == 'title' and 'extraction_rule' in rule_data:
                # Apply title extraction improvements
                if "quantum_document_pattern" in pattern.trigger_conditions:
                    improved_title = self._extract_quantum_title(content)
                    if improved_title:
                        metadata['title'] = improved_title
            
            elif pattern.pattern_type == 'topic' and 'topic' in rule_data:
                # Apply topic classification improvements
                metadata['topic'] = rule_data['topic']
            
        except Exception as e:
            self.logger.error(f"Error applying pattern {pattern.pattern_id}: {e}")
        
        return metadata
    
    def _extract_quantum_title(self, content: str) -> Optional[str]:
        """Extract quantum document title using learned patterns"""
        
        # Look for quantum-specific title patterns
        quantum_title_patterns = [
            r'(The\s+U\.?S\.?\s+Approach\s+to\s+Quantum\s+Policy)',
            r'(Quantum\s+[^.\n]{10,80}(?:Policy|Framework|Strategy))',
            r'(National\s+Quantum\s+Initiative[^.\n]*)'
        ]
        
        import re
        for pattern in quantum_title_patterns:
            match = re.search(pattern, content[:500], re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _update_pattern_performance(self):
        """Update performance metrics for learned patterns"""
        # This would analyze recent verification events to calculate success rates
        # Implementation would track how often patterns lead to correct extractions
        pass
    
    def get_training_statistics(self) -> Dict[str, Any]:
        """Get statistics about the training system"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        try:
            # Count verification events
            cursor.execute("SELECT COUNT(*) FROM verification_patterns")
            stats['total_verifications'] = cursor.fetchone()[0]
            
            # Count learned patterns
            cursor.execute("SELECT COUNT(*) FROM learned_patterns")
            stats['learned_patterns'] = cursor.fetchone()[0]
            
            # Pattern breakdown by type
            cursor.execute("""
                SELECT pattern_type, COUNT(*) 
                FROM learned_patterns 
                GROUP BY pattern_type
            """)
            stats['patterns_by_type'] = dict(cursor.fetchall())
            
            # Average confidence scores
            cursor.execute("SELECT AVG(confidence_score) FROM learned_patterns")
            avg_confidence = cursor.fetchone()[0]
            stats['average_pattern_confidence'] = avg_confidence if avg_confidence else 0.0
            
        except Exception as e:
            self.logger.error(f"Error getting training statistics: {e}")
        finally:
            conn.close()
        
        return stats

# Global instance
ml_training_system = MLTrainingSystem()