"""
Enhanced Multi-LLM Region Detection System
Comprehensive geographical intelligence for document classification
"""

import os
import json
import re
from typing import Dict, Optional, List
from openai import OpenAI

class EnhancedRegionDetector:
    """Advanced region detection using multi-layered intelligence"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Comprehensive mapping of organizations to regions
        self.org_patterns = {
            'US': [
                'nasa', 'nist', 'dhs', 'dod', 'nsa', 'cia', 'fbi', 'doe', 'epa',
                'federal', 'united states', 'us government', '.gov', 'washington dc',
                'pentagon', 'white house', 'congress', 'senate', 'fema', 'cisa',
                'cybersecurity and infrastructure security agency'
            ],
            'Europe': [
                'enisa', 'european union', 'eu commission', 'gdpr', 'anssi', 'bsi',
                'netherlands', 'france', 'germany', 'italy', 'spain', 'estonia',
                'finland', 'sweden', 'denmark', 'belgium', 'austria', 'poland',
                'european cybersecurity agency', 'cert-eu', 'europol'
            ],
            'UK': [
                'ncsc', 'gchq', 'cabinet office', 'uk government', 'british',
                'united kingdom', 'england', 'scotland', 'wales', 'northern ireland',
                'crown', 'her majesty', 'his majesty', 'ministry of defence'
            ],
            'Canada': [
                'cse', 'canadian', 'canada', 'government of canada', 'rcmp',
                'communications security establishment', 'public safety canada'
            ],
            'Australia': [
                'asd', 'australian', 'australia', 'acsc', 'asio', 'asis',
                'australian signals directorate', 'australian cyber security centre'
            ],
            'Asia-Pacific': [
                'nisc', 'japan', 'japanese', 'singapore', 'csa singapore', 'china',
                'chinese', 'korea', 'korean', 'taiwan', 'hong kong', 'thailand',
                'malaysia', 'indonesia', 'philippines', 'vietnam', 'india'
            ],
            'International': [
                'iso', 'itu', 'oecd', 'united nations', 'un ', 'nato', 'interpol',
                'world bank', 'imf', 'wto', 'ieee', 'ietf', 'w3c'
            ]
        }
        
        # Address and location patterns
        self.location_patterns = {
            'US': [
                r'\b\d{5}(-\d{4})?\b',  # US ZIP codes
                r'washington,?\s*d\.?c\.?', r'virginia', r'maryland', r'california',
                r'new york', r'texas', r'florida', r'illinois', r'ohio'
            ],
            'Europe': [
                r'\d{5}\s+[a-zA-Z]+,?\s*(germany|france|netherlands|belgium)',
                r'brussels', r'paris', r'berlin', r'amsterdam', r'rome', r'madrid',
                r'helsinki', r'stockholm', r'copenhagen', r'vienna', r'tallinn'
            ],
            'UK': [
                r'[a-zA-Z]{1,2}\d{1,2}[a-zA-Z]?\s*\d[a-zA-Z]{2}',  # UK postcodes
                r'london', r'manchester', r'birmingham', r'glasgow', r'edinburgh',
                r'cardiff', r'belfast', r'liverpool', r'leeds', r'sheffield'
            ]
        }
    
    def detect_region_comprehensive(self, title: str, content: str, organization: str, url: str = "") -> Dict[str, any]:
        """Comprehensive region detection using multiple intelligence sources"""
        
        # Multi-layer detection
        llm_result = self._llm_analysis(title, content, organization, url)
        pattern_result = self._pattern_analysis(title, content, organization, url)
        address_result = self._address_analysis(content + " " + organization)
        
        # Confidence-weighted combination
        results = [llm_result, pattern_result, address_result]
        valid_results = [r for r in results if r['confidence'] > 0.3]
        
        if not valid_results:
            return self._unknown_result()
        
        # Find consensus or highest confidence
        if len(valid_results) == 1:
            return valid_results[0]
        
        # Check for consensus
        regions = [r['region'] for r in valid_results]
        if len(set(regions)) == 1:
            # All agree - boost confidence
            best = max(valid_results, key=lambda x: x['confidence'])
            best['confidence'] = min(0.95, best['confidence'] + 0.1)
            return best
        
        # Return highest confidence
        return max(valid_results, key=lambda x: x['confidence'])
    
    def _llm_analysis(self, title: str, content: str, organization: str, url: str) -> Dict[str, any]:
        """Advanced LLM-based region detection"""
        
        try:
            prompt = f"""
            Analyze this document for geographical/organizational origin with advanced intelligence:
            
            Title: {title[:300]}
            Organization: {organization[:200]}
            URL: {url[:100]}
            Content: {content[:800]}
            
            INTELLIGENCE CRITERIA:
            
            1. ORGANIZATIONAL INTELLIGENCE:
            - NASA, NIST, DHS, DoD, NSA, CISA → US (very high confidence)
            - ENISA, ANSSI, BSI, national EU agencies → Europe
            - NCSC, GCHQ, Cabinet Office → UK
            - CSE, RCMP → Canada
            - ASD, ACSC → Australia
            - NISC Japan, CSA Singapore → Asia-Pacific
            
            2. ADDRESS INTELLIGENCE:
            - Detect specific addresses, postal codes, city names
            - Washington DC, Virginia → US
            - Brussels, Paris, Berlin → Europe
            - London, Manchester → UK
            
            3. REGULATORY INTELLIGENCE:
            - GDPR, AI Act, DSA → Europe
            - NIST Cybersecurity Framework → US
            - Essential Eight → Australia
            - PCI DSS (global but often US-centric)
            
            4. LINGUISTIC INTELLIGENCE:
            - "Federal government" → typically US
            - "Crown" references → UK/Commonwealth
            - "Ministry" vs "Department" patterns
            
            Available regions: US, Europe, UK, Canada, Australia, Asia-Pacific, International, Unknown
            
            Respond with JSON:
            {{
                "region": "detected_region",
                "confidence": 0.0-1.0,
                "reasoning": "specific evidence found",
                "indicators": ["evidence1", "evidence2"],
                "sub_location": "specific country/state if identifiable"
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.05,
                max_tokens=400
            )
            
            result = json.loads(response.choices[0].message.content)
            
            return {
                'region': result.get('region', 'Unknown'),
                'confidence': float(result.get('confidence', 0.0)),
                'reasoning': f"LLM Analysis: {result.get('reasoning', '')}",
                'indicators': result.get('indicators', []),
                'sub_location': result.get('sub_location', ''),
                'method': 'llm'
            }
            
        except Exception as e:
            print(f"LLM region analysis failed: {e}")
            return self._unknown_result()
    
    def _pattern_analysis(self, title: str, content: str, organization: str, url: str) -> Dict[str, any]:
        """Pattern-based region detection using comprehensive mappings"""
        
        text_to_analyze = f"{title} {organization} {content} {url}".lower()
        
        region_scores = {}
        matched_indicators = {}
        
        for region, patterns in self.org_patterns.items():
            score = 0
            indicators = []
            
            for pattern in patterns:
                if pattern in text_to_analyze:
                    score += 1
                    indicators.append(pattern)
            
            if score > 0:
                region_scores[region] = score / len(patterns)
                matched_indicators[region] = indicators
        
        if not region_scores:
            return self._unknown_result()
        
        best_region = max(region_scores, key=region_scores.get)
        confidence = min(0.9, region_scores[best_region] * 2)  # Scale to reasonable confidence
        
        return {
            'region': best_region,
            'confidence': confidence,
            'reasoning': f"Pattern matching found {len(matched_indicators[best_region])} indicators",
            'indicators': matched_indicators[best_region][:5],
            'method': 'pattern'
        }
    
    def _address_analysis(self, text: str) -> Dict[str, any]:
        """Address and location-based region detection"""
        
        text_lower = text.lower()
        
        for region, patterns in self.location_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return {
                        'region': region,
                        'confidence': 0.8,
                        'reasoning': f"Address pattern detected: {pattern}",
                        'indicators': [pattern],
                        'method': 'address'
                    }
        
        return self._unknown_result()
    
    def _unknown_result(self):
        """Return unknown result structure"""
        return {
            'region': 'Unknown',
            'confidence': 0.0,
            'reasoning': 'No reliable region indicators found',
            'indicators': [],
            'method': 'none'
        }

# Main function for integration
def enhanced_region_detection(title: str, content: str, organization: str, url: str = "") -> Dict[str, any]:
    """Enhanced region detection with comprehensive intelligence"""
    
    detector = EnhancedRegionDetector()
    return detector.detect_region_comprehensive(title, content, organization, url)