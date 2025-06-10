#!/usr/bin/env python3
"""
Test script to verify enhanced metadata extraction functionality
"""

from utils.document_metadata_extractor import extract_document_metadata

# Test sample content that simulates real documents
test_samples = [
    {
        "name": "NIST Post-Quantum Cryptography",
        "content": """
        Post-Quantum Cryptography Implementation Guide
        
        National Institute of Standards and Technology
        Special Publication 800-208
        
        Published: August 2023
        
        This document outlines the implementation of post-quantum cryptographic 
        algorithms in enterprise systems to prepare for the quantum computing era.
        
        NIST, Gaithersburg, MD
        """
    },
    {
        "name": "MIT Research Paper",
        "content": """
        Quantum Risk Assessment Framework
        
        Massachusetts Institute of Technology
        Computer Science and Artificial Intelligence Laboratory
        
        Authors: John Smith (jsmith@mit.edu), Jane Doe
        Publication Date: March 15, 2024
        
        This research presents a comprehensive framework for assessing 
        quantum computing risks in organizational security systems.
        """
    },
    {
        "name": "Microsoft Technical Report",
        "content": """
        AI Ethics in Cybersecurity Applications
        
        Microsoft Corporation
        Redmond, WA
        
        Version 2.1 - December 2023
        Copyright © 2023 Microsoft Corporation
        
        This technical report examines ethical considerations when 
        implementing AI-powered cybersecurity solutions.
        """
    }
]

def test_metadata_extraction():
    """Test the enhanced metadata extraction on sample documents."""
    print("Testing Enhanced Metadata Extraction System")
    print("=" * 60)
    
    for sample in test_samples:
        print(f"\nTesting: {sample['name']}")
        print("-" * 40)
        
        metadata = extract_document_metadata(sample['content'])
        
        print(f"Title: {metadata.get('title', 'N/A')}")
        print(f"Organization: {metadata.get('author_organization', 'N/A')}")
        print(f"Date: {metadata.get('publish_date', 'N/A')}")
        print(f"Type: {metadata.get('document_type', 'N/A')}")
        
        print()

if __name__ == "__main__":
    test_metadata_extraction()