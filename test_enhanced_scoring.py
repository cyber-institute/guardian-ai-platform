#!/usr/bin/env python3
"""
Test Enhanced Scoring System
Verify that content depth analysis properly scores the Quantum Science document
"""

import os
import psycopg2
from utils.enhanced_content_analyzer import analyze_document_content_depth
from utils.comprehensive_scoring import comprehensive_document_scoring

def test_quantum_science_document():
    """Test scoring on the actual Quantum Science for Inclusion and Sustainability document"""
    
    try:
        # Get the actual document content from database
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, content 
            FROM documents 
            WHERE title ILIKE '%quantum science for inclusion%'
            LIMIT 1
        """)
        
        row = cursor.fetchone()
        if not row:
            print("❌ Quantum Science document not found")
            return False
        
        doc_id, title, content = row
        cursor.close()
        conn.close()
        
        print(f"📄 Testing Document ID {doc_id}: {title}")
        print("=" * 80)
        
        # Analyze content depth
        content_analysis = analyze_document_content_depth(content, title)
        
        print("🔍 CONTENT DEPTH ANALYSIS:")
        print(f"AI Analysis:")
        ai_analysis = content_analysis['ai_analysis']
        print(f"  - Substantive terms: {ai_analysis['substantive_terms']}")
        print(f"  - Shallow mentions: {ai_analysis['shallow_mentions']}")
        print(f"  - Is primary focus: {ai_analysis['is_primary_focus']}")
        print(f"  - Should score: {ai_analysis['recommendation']['should_score']}")
        print(f"  - Reason: {ai_analysis['recommendation']['reason']}")
        
        print(f"\nQuantum Analysis:")
        quantum_analysis = content_analysis['quantum_analysis']
        print(f"  - Substantive terms: {quantum_analysis['substantive_terms']}")
        print(f"  - Is primary focus: {quantum_analysis['is_primary_focus']}")
        print(f"  - Should score: {quantum_analysis['recommendation']['should_score']}")
        print(f"  - Reason: {quantum_analysis['recommendation']['reason']}")
        
        # Test comprehensive scoring
        print("\n🎯 COMPREHENSIVE SCORING RESULTS:")
        scores = comprehensive_document_scoring(content, title)
        
        print(f"AI Cybersecurity: {scores.get('ai_cybersecurity', 'N/A')}")
        print(f"AI Ethics: {scores.get('ai_ethics', 'N/A')}")
        print(f"Quantum Cybersecurity: {scores.get('quantum_cybersecurity', 'N/A')}")
        print(f"Quantum Ethics: {scores.get('quantum_ethics', 'N/A')}")
        
        # Validate expected behavior
        print("\n✅ VALIDATION RESULTS:")
        
        # AI scores should be None or very low for this document
        ai_cyber_score = scores.get('ai_cybersecurity')
        ai_ethics_score = scores.get('ai_ethics')
        
        if ai_cyber_score is None:
            print("✅ AI Cybersecurity: Correctly not scored (N/A)")
        elif ai_cyber_score <= 15:
            print(f"✅ AI Cybersecurity: Low score ({ai_cyber_score}) - appropriate for minimal AI content")
        else:
            print(f"❌ AI Cybersecurity: Score too high ({ai_cyber_score}) for document with minimal AI content")
        
        if ai_ethics_score is None:
            print("✅ AI Ethics: Correctly not scored (N/A)")
        elif ai_ethics_score <= 15:
            print(f"✅ AI Ethics: Low score ({ai_ethics_score}) - appropriate for minimal AI content")
        else:
            print(f"❌ AI Ethics: Score too high ({ai_ethics_score}) for document with minimal AI content")
        
        # Quantum scores should be present and reasonable
        quantum_cyber_score = scores.get('quantum_cybersecurity')
        quantum_ethics_score = scores.get('quantum_ethics')
        
        if quantum_ethics_score is not None and quantum_ethics_score > 0:
            print(f"✅ Quantum Ethics: Appropriate score ({quantum_ethics_score}) for quantum-focused document")
        else:
            print(f"❌ Quantum Ethics: Should have a score for quantum-focused document")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_ai_content_examples():
    """Test with some example AI content to verify scoring logic"""
    
    print("\n" + "=" * 80)
    print("🧪 TESTING AI CONTENT EXAMPLES")
    print("=" * 80)
    
    # Test 1: Document with AI mentioned only in passing
    test1_title = "Investment Challenges in Emerging Technologies"
    test1_content = """
    Many organizations have faced similar investment decisions with AI as they now face with quantum computing.
    The quantum technology sector requires significant capital investment and long-term commitment.
    Like AI, quantum computing represents a paradigm shift that organizations must carefully evaluate.
    """
    
    print("\n📄 Test 1: AI mentioned in passing comparison")
    content_analysis = analyze_document_content_depth(test1_content, test1_title)
    ai_analysis = content_analysis['ai_analysis']
    print(f"Should score AI: {ai_analysis['recommendation']['should_score']}")
    print(f"Reason: {ai_analysis['recommendation']['reason']}")
    
    scores = comprehensive_document_scoring(test1_content, test1_title)
    print(f"AI Cybersecurity score: {scores.get('ai_cybersecurity', 'N/A')}")
    print(f"AI Ethics score: {scores.get('ai_ethics', 'N/A')}")
    
    # Test 2: Document with substantial AI policy content
    test2_title = "AI Risk Management Framework Implementation"
    test2_content = """
    This document outlines comprehensive AI governance model for responsible AI deployment.
    The AI risk management framework includes AI system lifecycle management, AI bias mitigation,
    AI transparency requirements, and AI accountability measures. Organizations must implement
    AI oversight mechanisms and AI safety protocols to ensure trustworthy AI systems.
    """
    
    print("\n📄 Test 2: Substantial AI policy content")
    content_analysis = analyze_document_content_depth(test2_content, test2_title)
    ai_analysis = content_analysis['ai_analysis']
    print(f"Should score AI: {ai_analysis['recommendation']['should_score']}")
    print(f"Reason: {ai_analysis['recommendation']['reason']}")
    print(f"Recommended score level: {ai_analysis['recommendation']['recommended_score']}")
    
    scores = comprehensive_document_scoring(test2_content, test2_title)
    print(f"AI Cybersecurity score: {scores.get('ai_cybersecurity', 'N/A')}")
    print(f"AI Ethics score: {scores.get('ai_ethics', 'N/A')}")

if __name__ == "__main__":
    print("🔬 ENHANCED SCORING SYSTEM TEST")
    print("Testing content depth analysis vs keyword matching")
    print("=" * 80)
    
    # Test the actual Quantum Science document
    success = test_quantum_science_document()
    
    # Test AI content examples
    test_ai_content_examples()
    
    print("\n" + "=" * 80)
    if success:
        print("✅ Enhanced scoring system test completed")
    else:
        print("❌ Enhanced scoring system test had issues")