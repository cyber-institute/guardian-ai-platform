#!/usr/bin/env python3
"""
Record metadata extraction failure as ML training data
"""

from utils.ml_training_system import ml_training_system

def record_metadata_extraction_failure():
    """Record the NIST SP 800-218A metadata extraction failure for training"""
    
    failure_record = {
        "document_id": 30,
        "document_title": "NIST SP 800-218A Secure Software Development Practices for Generative AI and Dual-Use Foundation Models",
        "extraction_failures": {
            "topic": {
                "extracted": "General",
                "correct": "AI",
                "reason": "Content truncation prevented detection of AI keywords"
            },
            "organization": {
                "extracted": "Special", 
                "correct": "NIST",
                "reason": "Parser extracted wrong part of title instead of organization"
            },
            "date": {
                "extracted": None,
                "correct": "2024-05-01",
                "reason": "Date not found in truncated content"
            }
        },
        "content_issues": {
            "truncated_content": True,
            "content_length": 303,
            "expected_length": ">5000",
            "source_type": "PDF",
            "extraction_method": "trafilatura"
        },
        "learning_patterns": {
            "nist_sp_pattern": "Documents with 'NIST SP' should have organization=NIST",
            "ai_keywords": "Documents mentioning 'Generative AI', 'AI model' should be topic=AI",
            "secure_development": "Secure software development for AI should score AI Cybersecurity framework",
            "content_validation": "Validate content length before metadata extraction"
        }
    }
    
    # Add to training patterns
    if "metadata_extraction_improvements" not in ml_training_system.training_patterns:
        ml_training_system.training_patterns["metadata_extraction_improvements"] = []
    
    ml_training_system.training_patterns["metadata_extraction_improvements"].append(failure_record)
    ml_training_system._save_training_data()
    
    print("✓ Metadata extraction failure recorded for ML training")
    print("  System will now apply learned patterns to prevent similar issues")

if __name__ == "__main__":
    record_metadata_extraction_failure()