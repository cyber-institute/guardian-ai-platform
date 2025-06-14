"""
Organization Acronym Converter for GUARDIAN
Converts full organization names to standard acronyms using built-in library and web lookup
"""

import re
import requests
from typing import Dict, Optional
import json
import os

class OrganizationAcronymConverter:
    """
    Converts organization names to their standard acronyms
    """
    
    def __init__(self):
        # Built-in acronym library for common organizations
        self.acronym_library = {
            # US Government Agencies
            "cybersecurity and infrastructure security agency": "CISA",
            "national security agency": "NSA", 
            "central intelligence agency": "CIA",
            "federal bureau of investigation": "FBI",
            "department of homeland security": "DHS",
            "department of defense": "DOD",
            "department of energy": "DOE",
            "national institute of standards and technology": "NIST",
            "national aeronautics and space administration": "NASA",
            "national science foundation": "NSF",
            "office of management and budget": "OMB",
            "government accountability office": "GAO",
            "office of the director of national intelligence": "ODNI",
            
            # Standards Organizations
            "institute of electrical and electronics engineers": "IEEE",
            "international organization for standardization": "ISO",
            "internet engineering task force": "IETF",
            "world wide web consortium": "W3C",
            "international electrotechnical commission": "IEC",
            "american national standards institute": "ANSI",
            
            # Academic/Research
            "massachusetts institute of technology": "MIT",
            "california institute of technology": "Caltech",
            "stanford research institute": "SRI",
            "carnegie mellon university": "CMU",
            "georgia institute of technology": "Georgia Tech",
            
            # International Organizations
            "european union": "EU",
            "united nations": "UN",
            "north atlantic treaty organization": "NATO",
            "organization for economic cooperation and development": "OECD",
            
            # Technology Companies (when acting as standards bodies)
            "international business machines": "IBM",
            "american telephone and telegraph": "AT&T",
            
            # Other Common Organizations
            "american civil liberties union": "ACLU",
            "electronic frontier foundation": "EFF",
            "information technology industry council": "ITI"
        }
        
        # Cache for web-looked-up acronyms
        self.web_lookup_cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load cached web lookups"""
        cache_file = "organization_acronym_cache.json"
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_cache(self):
        """Save web lookup cache"""
        cache_file = "organization_acronym_cache.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(self.web_lookup_cache, f, indent=2)
        except:
            pass
    
    def convert_to_acronym(self, organization_name: str) -> str:
        """Convert organization name to acronym using multiple strategies"""
        
        if not organization_name or len(organization_name.strip()) < 3:
            return organization_name
        
        org_clean = organization_name.strip()
        org_lower = org_clean.lower()
        
        # Strategy 0: Return acronyms unchanged (already acronyms)
        if self._is_already_acronym(org_clean):
            return org_clean
        
        # Strategy 1: Direct lookup in built-in library
        if org_lower in self.acronym_library:
            return self.acronym_library[org_lower]
        
        # Strategy 2: Partial matching for variations
        acronym = self._partial_match_lookup(org_lower)
        if acronym:
            return acronym
        
        # Strategy 3: Pattern-based acronym generation (only for long names)
        if len(org_clean) > 15:  # Only generate for clearly long organization names
            generated_acronym = self._generate_acronym_from_pattern(org_clean)
            if generated_acronym and len(generated_acronym) <= 6:
                return generated_acronym
        
        # Strategy 4: Web lookup (if enabled and reasonable length)
        if len(org_clean) > 10 and len(org_clean) < 100:
            web_acronym = self._web_lookup_acronym(org_clean)
            if web_acronym:
                return web_acronym
        
        # Strategy 5: Return original if no conversion found
        return org_clean
    
    def _partial_match_lookup(self, org_lower: str) -> Optional[str]:
        """Find partial matches in the acronym library"""
        
        # Look for partial matches (organization name contains known org)
        for known_org, acronym in self.acronym_library.items():
            if known_org in org_lower or org_lower in known_org:
                # Check if it's a meaningful match (not just a common word)
                if len(known_org) > 10:  # Avoid matching short common words
                    return acronym
        
        return None
    
    def _is_already_acronym(self, org_name: str) -> bool:
        """Check if the organization name is already an acronym"""
        
        # Common patterns for acronyms
        if len(org_name) <= 6 and org_name.isupper():
            return True
        
        # Check if it's a known acronym
        known_acronyms = set(self.acronym_library.values())
        if org_name in known_acronyms:
            return True
        
        # Check if it looks like an acronym (mostly capitals, few vowels)
        if len(org_name) <= 8:
            upper_count = sum(1 for c in org_name if c.isupper())
            if upper_count / len(org_name) > 0.7:  # More than 70% uppercase
                return True
        
        return False
    
    def _generate_acronym_from_pattern(self, org_name: str) -> Optional[str]:
        """Generate acronym from organization name patterns"""
        
        # Clean up the name
        org_clean = re.sub(r'\b(the|of|and|for|in|on|at|to|a|an)\b', '', org_name, flags=re.IGNORECASE)
        org_clean = re.sub(r'[^\w\s]', '', org_clean)
        
        # Split into significant words
        words = [word.strip() for word in org_clean.split() if len(word.strip()) > 2]
        
        if len(words) >= 2 and len(words) <= 6:
            # Generate acronym from first letters
            acronym = ''.join(word[0].upper() for word in words)
            
            # Validate the acronym makes sense
            if len(acronym) >= 2 and len(acronym) <= 6:
                return acronym
        
        return None
    
    def _web_lookup_acronym(self, organization_name: str) -> Optional[str]:
        """Look up acronym using web search (with caching)"""
        
        # Check cache first
        cache_key = organization_name.lower().strip()
        if cache_key in self.web_lookup_cache:
            return self.web_lookup_cache[cache_key]
        
        try:
            # Use a simple strategy to find acronyms from organization websites
            # Look for patterns like "ORG_NAME (ACRONYM)" or "ACRONYM - ORG_NAME"
            
            # Strategy: Search for the organization's official website
            search_patterns = [
                f'"{organization_name}" acronym',
                f'"{organization_name}" abbreviation',
                f'"{organization_name}" official website'
            ]
            
            for pattern in search_patterns:
                acronym = self._extract_acronym_from_search(pattern, organization_name)
                if acronym:
                    # Cache the result
                    self.web_lookup_cache[cache_key] = acronym
                    self._save_cache()
                    return acronym
        
        except Exception as e:
            # Don't fail on web lookup errors
            pass
        
        return None
    
    def _extract_acronym_from_search(self, search_pattern: str, org_name: str) -> Optional[str]:
        """Extract acronym from search results (placeholder for actual implementation)"""
        
        # This is a simplified implementation
        # In a full implementation, you would use a search API or web scraping
        
        # For now, we'll use some heuristic patterns based on common formats
        org_words = org_name.split()
        
        # Look for patterns in the organization name itself
        # E.g., "National Security Agency (NSA)" -> extract NSA
        paren_match = re.search(r'\(([A-Z]{2,6})\)', org_name)
        if paren_match:
            return paren_match.group(1)
        
        # Look for acronyms at the end: "Something - ABC"
        dash_match = re.search(r'-\s*([A-Z]{2,6})\s*$', org_name)
        if dash_match:
            return dash_match.group(1)
        
        return None
    
    def add_to_library(self, organization_name: str, acronym: str):
        """Add a new organization-acronym pair to the library"""
        org_lower = organization_name.lower().strip()
        self.acronym_library[org_lower] = acronym.upper().strip()
    
    def bulk_convert_organizations(self, organizations: list) -> Dict[str, str]:
        """Convert multiple organizations to acronyms"""
        results = {}
        for org in organizations:
            results[org] = self.convert_to_acronym(org)
        return results

# Global instance
org_converter = OrganizationAcronymConverter()

def convert_org_to_acronym(organization_name: str) -> str:
    """Convert organization name to acronym"""
    return org_converter.convert_to_acronym(organization_name)

def add_organization_mapping(full_name: str, acronym: str):
    """Add a new organization mapping"""
    org_converter.add_to_library(full_name, acronym)