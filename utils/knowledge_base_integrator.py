"""
Knowledge Base Integration System for GUARDIAN
Connects to external knowledge sources for AI/Quantum best practices and standards
"""

import json
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import requests
from datetime import datetime, timedelta

@dataclass
class KnowledgeSource:
    """External knowledge source configuration"""
    name: str
    base_url: str
    api_type: str  # "rest", "graphql", "rss", "scrape"
    update_frequency: str  # "daily", "weekly", "monthly"
    knowledge_domains: List[str]
    requires_auth: bool = False
    last_updated: Optional[datetime] = None

class KnowledgeBaseIntegrator:
    """
    Integrates external knowledge sources to enhance GUARDIAN's understanding
    of AI Ethics, Quantum Security, and Cybersecurity best practices
    """
    
    def __init__(self):
        self.knowledge_sources = self._configure_knowledge_sources()
        self.knowledge_cache = {}
        self.last_sync = {}
    
    def _configure_knowledge_sources(self) -> List[KnowledgeSource]:
        """Configure external knowledge sources"""
        return [
            # NIST Publications API
            KnowledgeSource(
                name="nist_publications",
                base_url="https://csrc.nist.gov/api/publications",
                api_type="rest",
                update_frequency="weekly",
                knowledge_domains=["cybersecurity", "ai_ethics", "quantum_security"]
            ),
            
            # IEEE Standards API
            KnowledgeSource(
                name="ieee_standards",
                base_url="https://standards.ieee.org/api/v1",
                api_type="rest", 
                update_frequency="monthly",
                knowledge_domains=["ai_ethics", "cybersecurity"],
                requires_auth=True
            ),
            
            # arXiv AI Safety Papers
            KnowledgeSource(
                name="arxiv_ai_safety",
                base_url="http://export.arxiv.org/api/query",
                api_type="rest",
                update_frequency="daily",
                knowledge_domains=["ai_ethics", "quantum_security"]
            ),
            
            # ENISA Publications
            KnowledgeSource(
                name="enisa_publications",
                base_url="https://www.enisa.europa.eu/api",
                api_type="rest",
                update_frequency="weekly",
                knowledge_domains=["cybersecurity", "quantum_security"]
            ),
            
            # MITRE ATT&CK Framework
            KnowledgeSource(
                name="mitre_attack",
                base_url="https://raw.githubusercontent.com/mitre/cti/master",
                api_type="rest",
                update_frequency="monthly",
                knowledge_domains=["cybersecurity"]
            ),
            
            # OWASP Security Knowledge Base
            KnowledgeSource(
                name="owasp_knowledge",
                base_url="https://owasp.org/api",
                api_type="rest",
                update_frequency="weekly",
                knowledge_domains=["cybersecurity", "ai_ethics"]
            ),
            
            # Partnership on AI Research
            KnowledgeSource(
                name="partnership_ai",
                base_url="https://partnershiponai.org/api",
                api_type="rest",
                update_frequency="weekly",
                knowledge_domains=["ai_ethics"]
            ),
            
            # Quantum Computing Reports
            KnowledgeSource(
                name="quantum_computing_report",
                base_url="https://quantumcomputingreport.com/api",
                api_type="rest",
                update_frequency="weekly",
                knowledge_domains=["quantum_security"]
            )
        ]
    
    async def sync_knowledge_sources(self, domains: Optional[List[str]] = None) -> Dict[str, Any]:
        """Synchronize knowledge from external sources"""
        
        sync_results = {"successful": [], "failed": [], "total_documents": 0}
        
        relevant_sources = self.knowledge_sources
        if domains:
            relevant_sources = [s for s in self.knowledge_sources 
                              if any(domain in s.knowledge_domains for domain in domains)]
        
        for source in relevant_sources:
            try:
                result = await self._sync_single_source(source)
                if result:
                    sync_results["successful"].append({
                        "source": source.name,
                        "documents_retrieved": result.get("count", 0),
                        "last_updated": datetime.now().isoformat()
                    })
                    sync_results["total_documents"] += result.get("count", 0)
                    self.last_sync[source.name] = datetime.now()
                else:
                    sync_results["failed"].append(source.name)
            except Exception as e:
                sync_results["failed"].append(f"{source.name}: {str(e)}")
        
        return sync_results
    
    async def _sync_single_source(self, source: KnowledgeSource) -> Optional[Dict[str, Any]]:
        """Synchronize a single knowledge source"""
        
        if source.name == "nist_publications":
            return await self._sync_nist_publications()
        elif source.name == "arxiv_ai_safety":
            return await self._sync_arxiv_papers()
        elif source.name == "mitre_attack":
            return await self._sync_mitre_attack()
        elif source.name == "ieee_standards":
            return await self._sync_ieee_standards()
        
        # Generic REST API sync
        return await self._sync_generic_rest(source)
    
    async def _sync_nist_publications(self) -> Dict[str, Any]:
        """Sync NIST cybersecurity and AI publications"""
        
        # Query NIST for recent AI and cybersecurity publications
        queries = [
            "artificial intelligence",
            "machine learning",
            "quantum",
            "cybersecurity framework",
            "privacy engineering"
        ]
        
        all_documents = []
        
        for query in queries:
            try:
                url = f"https://csrc.nist.gov/api/publications/search"
                params = {
                    "query": query,
                    "limit": 50,
                    "startDate": (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            documents = data.get("publications", [])
                            
                            for doc in documents:
                                enhanced_doc = self._enhance_nist_document(doc, query)
                                all_documents.append(enhanced_doc)
                        
            except Exception as e:
                print(f"NIST sync error for query '{query}': {e}")
        
        # Store in knowledge cache
        self.knowledge_cache["nist_publications"] = {
            "documents": all_documents,
            "last_updated": datetime.now(),
            "count": len(all_documents)
        }
        
        return {"count": len(all_documents), "source": "nist"}
    
    async def _sync_arxiv_papers(self) -> Dict[str, Any]:
        """Sync recent AI safety and quantum papers from arXiv"""
        
        search_terms = [
            "AI safety",
            "AI ethics", 
            "quantum cryptography",
            "post-quantum cryptography",
            "machine learning security",
            "algorithmic fairness"
        ]
        
        all_papers = []
        
        for term in search_terms:
            try:
                url = "http://export.arxiv.org/api/query"
                params = {
                    "search_query": f"all:{term}",
                    "start": 0,
                    "max_results": 20,
                    "sortBy": "submittedDate",
                    "sortOrder": "descending"
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            xml_data = await response.text()
                            papers = self._parse_arxiv_xml(xml_data, term)
                            all_papers.extend(papers)
                            
            except Exception as e:
                print(f"arXiv sync error for term '{term}': {e}")
        
        self.knowledge_cache["arxiv_papers"] = {
            "papers": all_papers,
            "last_updated": datetime.now(),
            "count": len(all_papers)
        }
        
        return {"count": len(all_papers), "source": "arxiv"}
    
    async def _sync_mitre_attack(self) -> Dict[str, Any]:
        """Sync MITRE ATT&CK framework data"""
        
        try:
            # Get latest enterprise attack patterns
            url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        attack_data = await response.json()
                        
                        # Extract techniques and tactics
                        techniques = []
                        for obj in attack_data.get("objects", []):
                            if obj.get("type") == "attack-pattern":
                                technique = {
                                    "id": obj.get("id"),
                                    "name": obj.get("name"),
                                    "description": obj.get("description", ""),
                                    "tactics": [ref.get("external_id") for ref in obj.get("kill_chain_phases", [])],
                                    "domain": "cybersecurity",
                                    "source": "mitre_attack"
                                }
                                techniques.append(technique)
                        
                        self.knowledge_cache["mitre_attack"] = {
                            "techniques": techniques,
                            "last_updated": datetime.now(),
                            "count": len(techniques)
                        }
                        
                        return {"count": len(techniques), "source": "mitre"}
                        
        except Exception as e:
            print(f"MITRE ATT&CK sync error: {e}")
        
        return None
    
    async def _sync_ieee_standards(self) -> Dict[str, Any]:
        """Sync IEEE standards related to AI and cybersecurity"""
        
        # Note: This would require IEEE API access
        # For now, return placeholder structure
        
        standards = [
            {
                "standard_id": "IEEE 2857",
                "title": "Privacy Engineering for Artificial Intelligence",
                "domain": "ai_ethics",
                "status": "active",
                "description": "Framework for privacy engineering in AI systems"
            },
            {
                "standard_id": "IEEE 2857.1",
                "title": "Technical Processes for AI Privacy Engineering", 
                "domain": "ai_ethics",
                "status": "development",
                "description": "Technical processes for implementing privacy in AI"
            }
        ]
        
        self.knowledge_cache["ieee_standards"] = {
            "standards": standards,
            "last_updated": datetime.now(),
            "count": len(standards)
        }
        
        return {"count": len(standards), "source": "ieee"}
    
    async def _sync_generic_rest(self, source: KnowledgeSource) -> Optional[Dict[str, Any]]:
        """Generic REST API synchronization"""
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {}
                if source.requires_auth:
                    # Check for API keys in environment
                    api_key = os.environ.get(f"{source.name.upper()}_API_KEY")
                    if api_key:
                        headers["Authorization"] = f"Bearer {api_key}"
                
                async with session.get(source.base_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {"count": len(data) if isinstance(data, list) else 1, "source": source.name}
                        
        except Exception as e:
            print(f"Generic sync error for {source.name}: {e}")
        
        return None
    
    def _enhance_nist_document(self, doc: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Enhance NIST document with domain classification"""
        
        enhanced = doc.copy()
        enhanced["knowledge_domain"] = self._classify_domain(doc.get("title", "") + " " + doc.get("abstract", ""))
        enhanced["search_query"] = query
        enhanced["source"] = "nist"
        enhanced["relevance_score"] = self._calculate_relevance(doc, query)
        
        return enhanced
    
    def _parse_arxiv_xml(self, xml_data: str, search_term: str) -> List[Dict[str, Any]]:
        """Parse arXiv XML response into structured data"""
        
        # Simplified XML parsing - in production, use xml.etree.ElementTree
        papers = []
        
        # This is a placeholder - would need proper XML parsing
        paper = {
            "title": f"Sample paper for {search_term}",
            "authors": ["Author 1", "Author 2"],
            "abstract": f"Abstract related to {search_term}",
            "published": datetime.now().isoformat(),
            "knowledge_domain": self._classify_domain(search_term),
            "source": "arxiv"
        }
        papers.append(paper)
        
        return papers
    
    def _classify_domain(self, text: str) -> str:
        """Classify text into knowledge domain"""
        
        text_lower = text.lower()
        
        ai_ethics_keywords = ["ethics", "fairness", "bias", "transparency", "accountability", "privacy"]
        quantum_keywords = ["quantum", "post-quantum", "cryptography", "quantum computing"]
        cyber_keywords = ["cybersecurity", "security", "attack", "vulnerability", "threat"]
        
        if any(keyword in text_lower for keyword in ai_ethics_keywords):
            return "ai_ethics"
        elif any(keyword in text_lower for keyword in quantum_keywords):
            return "quantum_security"
        elif any(keyword in text_lower for keyword in cyber_keywords):
            return "cybersecurity"
        
        return "general"
    
    def _calculate_relevance(self, doc: Dict[str, Any], query: str) -> float:
        """Calculate relevance score for document"""
        
        title = doc.get("title", "").lower()
        abstract = doc.get("abstract", "").lower()
        query_lower = query.lower()
        
        title_matches = query_lower in title
        abstract_matches = query_lower in abstract
        
        score = 0.0
        if title_matches:
            score += 0.6
        if abstract_matches:
            score += 0.4
        
        return min(score, 1.0)
    
    async def get_domain_knowledge(self, domain: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve knowledge for specific domain"""
        
        domain_knowledge = []
        
        for source_name, cache_data in self.knowledge_cache.items():
            documents = cache_data.get("documents", cache_data.get("papers", cache_data.get("techniques", [])))
            
            for doc in documents:
                if doc.get("knowledge_domain") == domain or doc.get("domain") == domain:
                    domain_knowledge.append(doc)
        
        # Sort by relevance/recency and limit results
        domain_knowledge.sort(key=lambda x: x.get("relevance_score", 0.0), reverse=True)
        
        return domain_knowledge[:limit]
    
    async def search_knowledge(self, query: str, domains: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search across all cached knowledge"""
        
        results = []
        query_lower = query.lower()
        
        for source_name, cache_data in self.knowledge_cache.items():
            documents = cache_data.get("documents", cache_data.get("papers", cache_data.get("techniques", [])))
            
            for doc in documents:
                # Check domain filter
                if domains and doc.get("knowledge_domain") not in domains and doc.get("domain") not in domains:
                    continue
                
                # Search in title and description/abstract
                title = doc.get("title", "").lower()
                desc = doc.get("description", doc.get("abstract", "")).lower()
                
                if query_lower in title or query_lower in desc:
                    doc["search_relevance"] = self._calculate_search_relevance(doc, query)
                    results.append(doc)
        
        # Sort by search relevance
        results.sort(key=lambda x: x.get("search_relevance", 0.0), reverse=True)
        
        return results
    
    def _calculate_search_relevance(self, doc: Dict[str, Any], query: str) -> float:
        """Calculate search relevance score"""
        
        title = doc.get("title", "").lower()
        desc = doc.get("description", doc.get("abstract", "")).lower()
        query_lower = query.lower()
        
        score = 0.0
        
        # Title match gets higher weight
        if query_lower in title:
            score += 0.7
        
        # Description/abstract match
        if query_lower in desc:
            score += 0.3
        
        # Boost recent documents
        if "published" in doc or "last_updated" in doc:
            score += 0.1
        
        return min(score, 1.0)
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get synchronization status for all sources"""
        
        status = {
            "total_sources": len(self.knowledge_sources),
            "synced_sources": len(self.last_sync),
            "total_documents": sum(cache.get("count", 0) for cache in self.knowledge_cache.values()),
            "last_sync_times": {name: sync_time.isoformat() for name, sync_time in self.last_sync.items()},
            "cache_status": {name: {"count": cache.get("count", 0), "last_updated": cache.get("last_updated")} 
                           for name, cache in self.knowledge_cache.items()}
        }
        
        return status

# Global instance
knowledge_integrator = KnowledgeBaseIntegrator()