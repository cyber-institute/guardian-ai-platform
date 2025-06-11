"""
Multi-LLM Benchmarking System for GUARDIAN
Provides before/after comparisons and quality metrics
"""

import json
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import sqlite3
import os
from datetime import datetime

@dataclass
class BenchmarkResult:
    """Individual benchmark result with detailed metrics"""
    document_title: str
    analysis_type: str  # 'standard' or 'multi_llm'
    processing_time: float
    confidence_score: float
    accuracy_metrics: Dict[str, float]
    detailed_scores: Dict[str, Any]
    timestamp: str
    services_used: Optional[int] = None
    consensus_strength: Optional[float] = None

class MultiLLMBenchmarker:
    """
    Comprehensive benchmarking system for Multi-LLM improvements
    Tracks quality metrics, processing times, and accuracy improvements
    """
    
    def __init__(self):
        self.db_path = "benchmarks.db"
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize SQLite database for benchmark storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benchmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_title TEXT NOT NULL,
                analysis_type TEXT NOT NULL,
                processing_time REAL,
                confidence_score REAL,
                accuracy_metrics TEXT,  -- JSON string
                detailed_scores TEXT,   -- JSON string
                services_used INTEGER,
                consensus_strength REAL,
                timestamp TEXT,
                content_hash TEXT  -- For identifying same documents
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_content_hash(self, content: str) -> str:
        """Generate hash for content identification"""
        import hashlib
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def store_benchmark_result(self, result: BenchmarkResult, content: str):
        """Store benchmark result in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        content_hash = self.generate_content_hash(content)
        
        cursor.execute('''
            INSERT INTO benchmarks 
            (document_title, analysis_type, processing_time, confidence_score, 
             accuracy_metrics, detailed_scores, services_used, consensus_strength, 
             timestamp, content_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.document_title,
            result.analysis_type,
            result.processing_time,
            result.confidence_score,
            json.dumps(result.accuracy_metrics),
            json.dumps(result.detailed_scores),
            result.services_used,
            result.consensus_strength,
            result.timestamp,
            content_hash
        ))
        
        conn.commit()
        conn.close()
    
    def get_benchmark_comparison(self, content_hash: str) -> Dict[str, Any]:
        """Get comparison between standard and Multi-LLM analysis for same content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM benchmarks 
            WHERE content_hash = ? 
            ORDER BY timestamp DESC
        ''', (content_hash,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return {"comparison_available": False}
        
        # Parse results
        standard_results = []
        multi_llm_results = []
        
        for row in results:
            result_data = {
                'document_title': row[1],
                'analysis_type': row[2],
                'processing_time': row[3],
                'confidence_score': row[4],
                'accuracy_metrics': json.loads(row[5]) if row[5] else {},
                'detailed_scores': json.loads(row[6]) if row[6] else {},
                'services_used': row[7],
                'consensus_strength': row[8],
                'timestamp': row[9]
            }
            
            if row[2] == 'standard':
                standard_results.append(result_data)
            else:
                multi_llm_results.append(result_data)
        
        if not standard_results or not multi_llm_results:
            return {"comparison_available": False, "single_analysis": True}
        
        # Calculate improvements
        latest_standard = standard_results[0]
        latest_multi_llm = multi_llm_results[0]
        
        improvements = self.calculate_improvements(latest_standard, latest_multi_llm)
        
        return {
            "comparison_available": True,
            "standard_analysis": latest_standard,
            "multi_llm_analysis": latest_multi_llm,
            "improvements": improvements,
            "total_analyses": len(results)
        }
    
    def calculate_improvements(self, standard: Dict, multi_llm: Dict) -> Dict[str, Any]:
        """Calculate specific improvements from Multi-LLM analysis"""
        improvements = {
            "confidence_improvement": 0,
            "processing_time_change": 0,
            "score_improvements": {},
            "quality_metrics": {},
            "overall_improvement": 0
        }
        
        # Confidence improvement
        if standard['confidence_score'] and multi_llm['confidence_score']:
            improvements["confidence_improvement"] = (
                multi_llm['confidence_score'] - standard['confidence_score']
            )
        
        # Processing time comparison
        if standard['processing_time'] and multi_llm['processing_time']:
            improvements["processing_time_change"] = (
                multi_llm['processing_time'] - standard['processing_time']
            )
        
        # Score comparisons
        standard_scores = standard.get('detailed_scores', {})
        multi_llm_scores = multi_llm.get('detailed_scores', {})
        
        for key in standard_scores:
            if key in multi_llm_scores:
                if isinstance(standard_scores[key], (int, float)) and isinstance(multi_llm_scores[key], (int, float)):
                    improvements["score_improvements"][key] = multi_llm_scores[key] - standard_scores[key]
        
        # Quality metrics specific to Multi-LLM
        improvements["quality_metrics"] = {
            "consensus_strength": multi_llm.get('consensus_strength', 0),
            "services_used": multi_llm.get('services_used', 0),
            "ensemble_advantage": multi_llm.get('services_used', 0) > 1
        }
        
        # Overall improvement score
        confidence_weight = improvements.get("confidence_improvement", 0) * 0.3
        score_weight = sum(improvements["score_improvements"].values()) * 0.5 if improvements["score_improvements"] else 0
        consensus_weight = improvements["quality_metrics"].get("consensus_strength", 0) * 0.2
        
        improvements["overall_improvement"] = confidence_weight + score_weight + consensus_weight
        
        return improvements
    
    def get_all_comparisons(self) -> List[Dict[str, Any]]:
        """Get all available benchmark comparisons"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get unique content hashes that have both analysis types
        cursor.execute('''
            SELECT content_hash, COUNT(DISTINCT analysis_type) as type_count
            FROM benchmarks 
            GROUP BY content_hash 
            HAVING type_count >= 2
        ''')
        
        content_hashes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        comparisons = []
        for content_hash in content_hashes:
            comparison = self.get_benchmark_comparison(content_hash)
            if comparison.get("comparison_available"):
                comparisons.append(comparison)
        
        return comparisons
    
    def generate_benchmark_report(self) -> Dict[str, Any]:
        """Generate comprehensive benchmark report"""
        comparisons = self.get_all_comparisons()
        
        if not comparisons:
            return {
                "total_comparisons": 0,
                "no_data": True,
                "recommendation": "Upload documents with both standard and Multi-LLM analysis to generate benchmarks"
            }
        
        # Aggregate improvements
        total_confidence_improvement = 0
        total_score_improvements = {}
        processing_time_changes = []
        consensus_strengths = []
        
        for comp in comparisons:
            improvements = comp["improvements"]
            
            total_confidence_improvement += improvements.get("confidence_improvement", 0)
            processing_time_changes.append(improvements.get("processing_time_change", 0))
            consensus_strengths.append(improvements["quality_metrics"].get("consensus_strength", 0))
            
            for key, value in improvements["score_improvements"].items():
                if key not in total_score_improvements:
                    total_score_improvements[key] = []
                total_score_improvements[key].append(value)
        
        # Calculate averages
        avg_confidence_improvement = total_confidence_improvement / len(comparisons)
        avg_processing_time_change = sum(processing_time_changes) / len(processing_time_changes)
        avg_consensus_strength = sum(consensus_strengths) / len(consensus_strengths)
        
        avg_score_improvements = {}
        for key, values in total_score_improvements.items():
            avg_score_improvements[key] = sum(values) / len(values)
        
        return {
            "total_comparisons": len(comparisons),
            "average_improvements": {
                "confidence_boost": round(avg_confidence_improvement, 2),
                "processing_time_change": round(avg_processing_time_change, 2),
                "consensus_strength": round(avg_consensus_strength, 2),
                "score_improvements": {k: round(v, 2) for k, v in avg_score_improvements.items()}
            },
            "quality_indicators": {
                "multi_llm_advantage": avg_confidence_improvement > 0,
                "consensus_reliability": avg_consensus_strength > 0.7,
                "improved_accuracy": len([v for v in avg_score_improvements.values() if v > 0]) > len([v for v in avg_score_improvements.values() if v <= 0])
            },
            "detailed_comparisons": comparisons[:5]  # Top 5 for display
        }

# Global benchmarker instance
multi_llm_benchmarker = MultiLLMBenchmarker()