"""
Multi-LLM Region Detection System
Automatically detects document origin regions using intelligent content analysis
"""

import os
import json
import re
from typing import Dict, Optional, List
from openai import OpenAI

def analyze_region_with_llm(title: str, content: str, organization: str) -> Dict[str, any]:
    """Use LLM to intelligently detect document region based on content analysis"""
    
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        prompt = f"""
        Analyze this document and determine its geographical/organizational origin region.
        
        Title: {title[:200]}
        Organization: {organization[:100]}
        Content Sample: {content[:500]}
        
        Based on:
        1. Organization name patterns and known entities
        2. Content references to specific regions/countries
        3. Regulatory frameworks mentioned
        4. Language patterns and terminology
        5. Government/institutional affiliations
        
        Classify into one of these regions:
        - US (United States - including federal agencies, US-based organizations)
        - EU (European Union - including EU institutions, European countries)
        - UK (United Kingdom - including UK government, British institutions)
        - Asia (Asian countries - China, Japan, Korea, Singapore, etc.)
        - International (UN, ISO, ITU, OECD, global standards bodies)
        - Other (Canada, Australia, New Zealand, other regions)
        
        Respond with JSON in this exact format:
        {{
            "region": "detected_region",
            "confidence": 0.85,
            "reasoning": "Brief explanation of detection logic",
            "indicators": ["key indicator 1", "key indicator 2"]
        }}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=300
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Validate and clean result
        valid_regions = ["US", "EU", "UK", "Asia", "International", "Other"]
        if result.get("region") not in valid_regions:
            result["region"] = "Unknown"
        
        return result
        
    except Exception as e:
        print(f"LLM region detection failed: {e}")
        return fallback_region_detection(organization, content)

def fallback_region_detection(organization: str, content: str) -> Dict[str, any]:
    """Fallback pattern-based region detection"""
    
    text = f"{organization} {content}".lower()
    
    # US indicators
    us_patterns = [
        r'\bnist\b', r'\bdhs\b', r'\bfederal\b', r'\busa\b', r'\bunited states\b',
        r'\bdod\b', r'\bnasa\b', r'\bcybersecurity.*infrastructure.*security.*agency\b',
        r'\bdepartment.*homeland.*security\b', r'\bwhite.*house\b'
    ]
    
    # EU indicators  
    eu_patterns = [
        r'\beuropean.*union\b', r'\benisa\b', r'\bgdpr\b', r'\beuropa\b',
        r'\beuropean.*commission\b', r'\beu\b.*regulation', r'\bbrussels\b'
    ]
    
    # UK indicators
    uk_patterns = [
        r'\buk\b', r'\bunited.*kingdom\b', r'\bbritish\b', r'\bncsc\b',
        r'\bgchq\b', r'\blondon\b', r'\bbritain\b'
    ]
    
    # International indicators
    intl_patterns = [
        r'\biso\b', r'\bitu\b', r'\boecd\b', r'\bunited.*nations\b',
        r'\bun\b.*charter', r'\bgeneva\b', r'\binternational.*standard\b'
    ]
    
    # Asia indicators
    asia_patterns = [
        r'\bchina\b', r'\bjapan\b', r'\bkorea\b', r'\bsingapore\b',
        r'\btokyo\b', r'\bbeijing\b', r'\bseoul\b'
    ]
    
    # Calculate confidence scores
    regions = {
        "US": sum(1 for pattern in us_patterns if re.search(pattern, text)),
        "EU": sum(1 for pattern in eu_patterns if re.search(pattern, text)),
        "UK": sum(1 for pattern in uk_patterns if re.search(pattern, text)),
        "International": sum(1 for pattern in intl_patterns if re.search(pattern, text)),
        "Asia": sum(1 for pattern in asia_patterns if re.search(pattern, text))
    }
    
    # Find highest scoring region
    best_region = max(regions.items(), key=lambda x: x[1])
    
    if best_region[1] > 0:
        confidence = min(0.7, best_region[1] * 0.2)  # Max 70% confidence for fallback
        return {
            "region": best_region[0],
            "confidence": confidence,
            "reasoning": f"Pattern-based detection found {best_region[1]} indicators",
            "indicators": ["Pattern-based fallback detection"]
        }
    
    return {
        "region": "Unknown",
        "confidence": 0.1,
        "reasoning": "No clear regional indicators found",
        "indicators": []
    }

def extract_enhanced_metadata_with_region(title: str, content: str, author_org: str) -> Dict[str, any]:
    """Extract comprehensive metadata including intelligent region detection"""
    
    # Perform region analysis
    region_analysis = analyze_region_with_llm(title, content, author_org)
    
    # Extract additional metadata patterns
    metadata = {
        "detected_region": region_analysis.get("region", "Unknown"),
        "region_confidence": region_analysis.get("confidence", 0.0),
        "region_reasoning": region_analysis.get("reasoning", ""),
        "region_indicators": region_analysis.get("indicators", [])
    }
    
    # Extract document type patterns
    doc_type_patterns = {
        "Policy": r'\b(policy|policies|governance|regulation|directive)\b',
        "Framework": r'\b(framework|standard|guideline|methodology)\b',
        "Research": r'\b(research|study|analysis|survey|investigation)\b',
        "Technical": r'\b(technical|specification|implementation|architecture)\b',
        "Report": r'\b(report|assessment|evaluation|review)\b'
    }
    
    content_lower = content.lower()
    for doc_type, pattern in doc_type_patterns.items():
        if re.search(pattern, content_lower):
            metadata["suggested_doc_type"] = doc_type
            break
    else:
        metadata["suggested_doc_type"] = "Document"
    
    return metadata