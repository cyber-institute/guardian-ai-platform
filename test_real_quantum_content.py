#!/usr/bin/env python3
"""
Test scoring with the actual NSM-10 quantum document content
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.comprehensive_scoring import score_quantum_cybersecurity_maturity

def test_nsm10_scoring():
    """Test scoring with the actual NSM-10 quantum content"""
    
    # Extract key quantum content from NSM-10
    nsm10_content = """
    National Security Memorandum on Promoting United States Leadership in Quantum Computing While Mitigating Risks to Vulnerable Cryptographic Systems.
    
    A cryptanalytically relevant quantum computer (CRQC) will be capable of breaking much of the public-key cryptography used on digital systems. 
    When available, a CRQC could jeopardize civilian and military communications, undermine supervisory and control systems for critical infrastructure, 
    and defeat security protocols for most Internet-based financial transactions.
    
    The United States must mitigate the threat of CRQCs through a timely and equitable transition of the Nation's cryptographic systems to 
    interoperable quantum-resistant cryptography. The goal is mitigating quantum risk by 2035.
    
    NIST and NSA are developing technical standards for quantum-resistant cryptography. The first sets of standards are expected by 2024.
    
    Central to this migration effort will be cryptographic agility, both to reduce transition time and allow seamless updates for future 
    cryptographic standards. This effort spans government, critical infrastructure, commercial services, cloud providers, and everywhere 
    vulnerable public-key cryptography is used.
    
    NIST shall establish a Migration to Post-Quantum Cryptography Project at the National Cybersecurity Center of Excellence to work with 
    the private sector on cybersecurity challenges posed by the transition to quantum-resistant cryptography. This project shall develop 
    programs for discovery and remediation of systems that do not use quantum-resistant cryptography.
    
    Federal agencies must deliver inventories of IT systems vulnerable to CRQCs, focusing on High Value Assets and High Impact Systems. 
    Inventories should include current cryptographic methods, system administrator protocols, non-security software and firmware requiring 
    upgraded digital signatures.
    
    NIST shall release a proposed timeline for deprecation of quantum-vulnerable cryptography in standards, with the goal of moving the 
    maximum number of systems off quantum-vulnerable cryptography within a decade of initial standards publication.
    
    Federal agencies must develop plans to upgrade non-NSS IT systems to quantum-resistant cryptography, designed to address the most 
    significant risks first, with cost estimates for upgrading vulnerable systems.
    """
    
    title = "NSM-10: Promoting US Leadership in Quantum Computing While Mitigating Cryptographic Risks"
    
    print("Testing NSM-10 Quantum Document Scoring")
    print("=" * 50)
    
    # Score the document
    score = score_quantum_cybersecurity_maturity(nsm10_content, title)
    
    # Analyze scoring components
    text_lower = nsm10_content.lower()
    
    basic_terms = ['quantum', 'post-quantum', 'quantum-safe', 'quantum-resistant', 'pqc']
    technical_terms = ['lattice-based', 'code-based', 'multivariate', 'hash-based', 'isogeny', 
                      'quantum key distribution', 'quantum cryptography', 'cryptographic agility']
    impl_terms = ['implementation', 'deployment', 'migration', 'transition', 'roadmap']
    standards_terms = ['nist', 'standards', 'compliance', 'governance', 'framework', 'policy']
    advanced_terms = ['hybrid systems', 'quantum supremacy', 'quantum advantage', 'quantum evolution', 
                     'quantum machine learning', 'adaptive quantum', 'continuous quantum monitoring']
    
    basic_count = sum(1 for term in basic_terms if term in text_lower)
    technical_count = sum(1 for term in technical_terms if term in text_lower)
    impl_count = sum(1 for term in impl_terms if term in text_lower)
    standards_count = sum(1 for term in standards_terms if term in text_lower)
    advanced_count = sum(1 for term in advanced_terms if term in text_lower)
    
    total_components = min(3, basic_count) + min(4, technical_count) + min(3, impl_count) + min(3, standards_count) + min(3, advanced_count)
    length_factor = 1.2 if len(nsm10_content) > 5000 else 1.1 if len(nsm10_content) > 2000 else 1.0
    final_score = int(total_components * length_factor)
    
    print(f"Document: {title}")
    print(f"Content length: {len(nsm10_content)} characters")
    print(f"\nScoring Breakdown:")
    print(f"Basic quantum terms found: {basic_count} -> {min(3, basic_count)} points")
    print(f"Technical terms found: {technical_count} -> {min(4, technical_count)} points") 
    print(f"Implementation terms found: {impl_count} -> {min(3, impl_count)} points")
    print(f"Standards terms found: {standards_count} -> {min(3, standards_count)} points")
    print(f"Advanced terms found: {advanced_count} -> {min(3, advanced_count)} points")
    print(f"Total component score: {total_components}")
    print(f"Length factor: {length_factor}")
    print(f"Final weighted score: {final_score}")
    print(f"Maturity level: {score}/5")
    
    # Show which specific terms were found
    print(f"\nSpecific terms found:")
    found_basic = [term for term in basic_terms if term in text_lower]
    found_technical = [term for term in technical_terms if term in text_lower]
    found_impl = [term for term in impl_terms if term in text_lower]
    found_standards = [term for term in standards_terms if term in text_lower]
    found_advanced = [term for term in advanced_terms if term in text_lower]
    
    print(f"Basic: {found_basic}")
    print(f"Technical: {found_technical}")
    print(f"Implementation: {found_impl}")
    print(f"Standards: {found_standards}")
    print(f"Advanced: {found_advanced}")
    
    print(f"\nScoring Authenticity:")
    if score >= 3:
        print("✅ AUTHENTIC: High score reflects substantial quantum content")
    elif score >= 2:
        print("✅ AUTHENTIC: Medium score reflects moderate quantum content")
    else:
        print("⚠️  Score reflects limited quantum sophistication in content")
    
    return score

if __name__ == "__main__":
    test_nsm10_scoring()