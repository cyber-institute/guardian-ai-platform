"""
Test the updated scoring system for AI documents with enhanced metadata
"""

from utils.comprehensive_scoring import comprehensive_document_scoring, analyze_document_applicability

def test_nasa_ai_scoring():
    """Test scoring for NASA AI Plan document"""
    title = "NASA'S RESPONSIBLE AI PLAN"
    content = """
    NASA's Response Plan: Executive Order 13960 - Promoting the Use of Trustworthy Artificial Intelligence (AI) in the Federal Government
    
    Artificial intelligence systems require responsible governance, security measures, and ethical oversight.
    This plan outlines NASA's approach to implementing trustworthy AI systems with proper safeguards,
    risk management, and compliance frameworks for responsible AI deployment across federal operations.
    
    Key areas include:
    - AI security and protection measures
    - Ethical AI principles and governance
    - Risk assessment and mitigation strategies
    - Trustworthy AI implementation guidelines
    """
    
    print(f"Testing document: {title}")
    print("-" * 50)
    
    # Test applicability detection
    applicability = analyze_document_applicability(content, title)
    print("Applicability Analysis:")
    for framework, applies in applicability.items():
        print(f"  {framework}: {applies}")
    
    # Test comprehensive scoring
    scores = comprehensive_document_scoring(content, title)
    print("\nComprehensive Scores:")
    for framework, score in scores.items():
        if score is not None:
            print(f"  {framework}: {score}")
        else:
            print(f"  {framework}: Not applicable")
    
    print("\nExpected behavior:")
    print("- AI Cybersecurity: Should have score (AI + security keywords)")
    print("- AI Ethics: Should have score (AI + ethics/governance keywords)")
    print("- Quantum scores: Should be None (no quantum keywords)")

if __name__ == "__main__":
    test_nasa_ai_scoring()