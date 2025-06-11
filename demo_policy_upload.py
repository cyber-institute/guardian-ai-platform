"""
Demonstration of Enhanced AI Policy Analyzer with Gap Analysis
"""

from utils.policy_gap_analyzer import policy_gap_analyzer
from utils.document_recommendation_engine import recommendation_engine
from utils.db import save_document
import time

def demo_policy_analysis():
    """Demonstrate the complete AI policy analysis workflow."""
    
    # Sample policy content for demonstration
    sample_policy = """
    Federal AI Safety and Security Policy

    Section 1: Risk Management Framework
    All federal AI systems must implement comprehensive risk assessment including:
    - Security vulnerability testing
    - Algorithmic bias evaluation
    - Privacy impact assessment
    - Ethical compliance review

    Section 2: Technical Requirements
    AI systems shall maintain:
    - End-to-end encryption for data transmission
    - Multi-factor authentication protocols
    - Regular security audits and monitoring
    - Incident response procedures

    Section 3: Governance Structure
    Establish AI oversight committee with:
    - Technical expertise in AI/ML systems
    - Ethics and compliance oversight
    - Legal and regulatory knowledge
    - Stakeholder representation

    Section 4: Compliance Requirements
    Systems must comply with:
    - NIST AI Risk Management Framework
    - Federal privacy regulations
    - Cybersecurity standards
    - Ethical AI principles
    """
    
    print("Analyzing Federal AI Safety Policy...")
    
    # Perform gap analysis
    report = policy_gap_analyzer.analyze_policy_document(
        sample_policy,
        "Federal AI Safety and Security Policy",
        "policy"
    )
    
    print(f"Analysis Results:")
    print(f"- Overall Maturity: {report.overall_maturity_score}/100")
    print(f"- AI Cybersecurity: {report.framework_scores['ai_cybersecurity_score']}/100")
    print(f"- Quantum Security: Tier {report.framework_scores['quantum_cybersecurity_score']}/5")
    print(f"- AI Ethics: {report.framework_scores['ai_ethics_score']}/100")
    print(f"- Gaps Identified: {len(report.identified_gaps)}")
    print(f"- Recommendations: {len(report.strategic_recommendations)}")
    
    # Save to database with enhanced metadata
    document_data = {
        'title': "Federal AI Safety and Security Policy",
        'content': sample_policy[:200] + "...",
        'text': sample_policy,
        'document_type': "Policy",
        'source': 'demo_upload',
        'ai_cybersecurity_score': report.framework_scores['ai_cybersecurity_score'],
        'quantum_cybersecurity_score': report.framework_scores['quantum_cybersecurity_score'],
        'ai_ethics_score': report.framework_scores['ai_ethics_score'],
        'quantum_ethics_score': report.framework_scores['quantum_ethics_score']
    }
    
    # Save document
    success = save_document(document_data)
    if success:
        print("Document saved successfully with comprehensive scoring")
        
        # Test recommendation engine
        print("\nTesting recommendation engine...")
        documents = recommendation_engine.load_documents()
        print(f"Total documents available: {len(documents)}")
        
        # Get recommendations for newly added document
        if documents:
            latest_doc_id = max([doc[0] for doc in documents if isinstance(doc, tuple)])
            recommendations = recommendation_engine.get_comprehensive_recommendations(
                target_doc_id=latest_doc_id,
                max_recommendations=3
            )
            
            print(f"Recommendation categories available:")
            for category, items in recommendations.items():
                print(f"- {category}: {len(items)} items")
    
    return report

if __name__ == "__main__":
    demo_policy_analysis()