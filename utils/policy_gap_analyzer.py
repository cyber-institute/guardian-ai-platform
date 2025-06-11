"""
Policy Gap Analysis Engine - GUARDIAN Patent Implementation
Advanced policy reinforcement learning with intelligent gap detection and recommendation generation
Based on patent formulations for dynamic governance and adaptive learning systems
"""

import os
import re
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from utils.patent_scoring_engine import ComprehensivePatentScoringEngine
from utils.document_recommendation_engine import recommendation_engine

@dataclass
class PolicyGap:
    """Represents an identified policy gap with severity and recommendations."""
    framework: str
    category: str
    severity: str  # Critical, High, Medium, Low
    gap_description: str
    recommendations: List[str]
    confidence_score: float
    reference_documents: List[str]

@dataclass
class GapAnalysisReport:
    """Comprehensive gap analysis report for uploaded policy documents."""
    document_title: str
    document_type: str
    overall_maturity_score: float
    framework_scores: Dict[str, float]
    identified_gaps: List[PolicyGap]
    strategic_recommendations: List[str]
    compliance_status: Dict[str, str]
    learning_insights: List[str]

class PolicyGapAnalyzer:
    """
    Advanced policy gap analysis engine implementing GUARDIAN patent's 
    reinforcement learning and recommendation algorithms.
    """
    
    def __init__(self):
        self.scoring_engine = ComprehensivePatentScoringEngine()
        self.knowledge_base = self._initialize_knowledge_base()
        self.gap_patterns = self._load_gap_patterns()
        
    def _initialize_knowledge_base(self) -> Dict[str, Dict]:
        """Initialize knowledge base with framework requirements and best practices."""
        return {
            'ai_cybersecurity': {
                'critical_requirements': [
                    'AI model security validation',
                    'Adversarial attack protection',
                    'Data poisoning prevention',
                    'Model integrity monitoring',
                    'AI system authentication',
                    'Machine learning pipeline security',
                    'Automated threat detection',
                    'AI incident response procedures'
                ],
                'best_practices': [
                    'Regular AI security assessments',
                    'Continuous model monitoring',
                    'Security-by-design implementation',
                    'Multi-layer defense strategies',
                    'AI-specific penetration testing',
                    'Threat intelligence integration'
                ],
                'compliance_frameworks': [
                    'NIST AI Risk Management Framework',
                    'ISO/IEC 23053 AI Security',
                    'MITRE ATLAS Framework',
                    'ENISA AI Cybersecurity Guidelines'
                ]
            },
            'quantum_cybersecurity': {
                'critical_requirements': [
                    'Post-quantum cryptographic algorithms',
                    'Quantum key distribution protocols',
                    'Quantum-safe encryption standards',
                    'Quantum threat assessment procedures',
                    'Legacy system migration planning',
                    'Quantum readiness evaluation',
                    'NIST PQC algorithm implementation',
                    'Quantum-resistant authentication'
                ],
                'best_practices': [
                    'Cryptographic agility implementation',
                    'Hybrid classical-quantum approaches',
                    'Regular quantum threat monitoring',
                    'Supply chain quantum security',
                    'Quantum key management protocols',
                    'Future-proof encryption strategies'
                ],
                'compliance_frameworks': [
                    'NIST Post-Quantum Cryptography',
                    'FIPS 203/204/205 Standards',
                    'NSA CNSS Policy 15',
                    'ISO/IEC 29192 Quantum Cryptography'
                ]
            },
            'ai_ethics': {
                'critical_requirements': [
                    'Algorithmic bias detection and mitigation',
                    'AI decision transparency and explainability',
                    'Human oversight and accountability',
                    'Privacy protection in AI systems',
                    'Fair and non-discriminatory AI practices',
                    'AI impact assessment procedures',
                    'Stakeholder engagement protocols',
                    'Ethical AI governance frameworks'
                ],
                'best_practices': [
                    'Regular bias auditing',
                    'Diverse development teams',
                    'Ethical review boards',
                    'Public consultation processes',
                    'Continuous monitoring systems',
                    'Transparency reporting'
                ],
                'compliance_frameworks': [
                    'EU AI Act Requirements',
                    'IEEE Ethically Aligned Design',
                    'Partnership on AI Principles',
                    'OECD AI Ethics Guidelines'
                ]
            },
            'quantum_ethics': {
                'critical_requirements': [
                    'Quantum computing access equity',
                    'Quantum technology dual-use considerations',
                    'Privacy implications of quantum capabilities',
                    'Quantum advantage responsibility',
                    'International quantum cooperation ethics',
                    'Quantum workforce development equity',
                    'Environmental impact assessment',
                    'Quantum security disclosure protocols'
                ],
                'best_practices': [
                    'Inclusive quantum development',
                    'Responsible quantum research',
                    'Ethical quantum partnerships',
                    'Sustainable quantum practices',
                    'Transparent quantum capabilities',
                    'Community engagement'
                ],
                'compliance_frameworks': [
                    'Quantum Ethics Guidelines',
                    'National Quantum Initiatives',
                    'International Quantum Partnerships',
                    'Academic Quantum Ethics Standards'
                ]
            }
        }
    
    def _load_gap_patterns(self) -> Dict[str, List[str]]:
        """Load common gap patterns identified through reinforcement learning."""
        return {
            'policy_gaps': [
                'Missing implementation timelines',
                'Unclear responsibility assignments',
                'Insufficient compliance monitoring',
                'Lack of update mechanisms',
                'Inadequate stakeholder engagement',
                'Missing risk assessment procedures',
                'Undefined success metrics',
                'Limited enforcement mechanisms'
            ],
            'technical_gaps': [
                'Outdated technical standards',
                'Missing interoperability requirements',
                'Insufficient security specifications',
                'Lack of performance metrics',
                'Unclear technical architecture',
                'Missing validation procedures',
                'Inadequate testing protocols',
                'Limited scalability considerations'
            ],
            'governance_gaps': [
                'Unclear governance structure',
                'Missing oversight mechanisms',
                'Insufficient reporting requirements',
                'Lack of appeal processes',
                'Undefined decision-making authority',
                'Missing conflict resolution',
                'Inadequate transparency measures',
                'Limited public engagement'
            ]
        }
    
    def analyze_policy_document(self, content: str, title: str, 
                              document_type: str = "policy") -> GapAnalysisReport:
        """
        Comprehensive policy gap analysis using GUARDIAN patent algorithms.
        
        Args:
            content: Full document content
            title: Document title
            document_type: Type of document (policy, standard, regulation, product)
            
        Returns:
            Complete gap analysis report with recommendations
        """
        
        # Step 1: Apply patent-based scoring
        framework_scores = self.scoring_engine.assess_document_comprehensive(content, title)
        
        # Step 2: Identify specific gaps using reinforcement learning patterns
        identified_gaps = self._identify_gaps(content, framework_scores, document_type)
        
        # Step 3: Generate strategic recommendations
        strategic_recommendations = self._generate_strategic_recommendations(
            identified_gaps, framework_scores, document_type
        )
        
        # Step 4: Assess compliance status
        compliance_status = self._assess_compliance_status(content, framework_scores)
        
        # Step 5: Generate learning insights
        learning_insights = self._generate_learning_insights(
            content, identified_gaps, framework_scores
        )
        
        # Step 6: Calculate overall maturity
        overall_maturity = self._calculate_overall_maturity(framework_scores)
        
        return GapAnalysisReport(
            document_title=title,
            document_type=document_type,
            overall_maturity_score=overall_maturity,
            framework_scores=framework_scores,
            identified_gaps=identified_gaps,
            strategic_recommendations=strategic_recommendations,
            compliance_status=compliance_status,
            learning_insights=learning_insights
        )
    
    def _identify_gaps(self, content: str, scores: Dict[str, float], 
                      doc_type: str) -> List[PolicyGap]:
        """Identify specific gaps using patent-based analysis algorithms."""
        gaps = []
        content_lower = content.lower()
        
        # AI Cybersecurity Gap Analysis
        if scores['ai_cybersecurity_score'] < 60:  # Below threshold
            ai_cyber_gaps = self._analyze_ai_cybersecurity_gaps(content_lower, scores)
            gaps.extend(ai_cyber_gaps)
        
        # Quantum Cybersecurity Gap Analysis
        if scores['quantum_cybersecurity_score'] < 3:  # Below QCMEA tier 3
            quantum_cyber_gaps = self._analyze_quantum_cybersecurity_gaps(content_lower, scores)
            gaps.extend(quantum_cyber_gaps)
        
        # AI Ethics Gap Analysis
        if scores['ai_ethics_score'] < 50:  # Below ethical threshold
            ai_ethics_gaps = self._analyze_ai_ethics_gaps(content_lower, scores)
            gaps.extend(ai_ethics_gaps)
        
        # Quantum Ethics Gap Analysis
        if scores['quantum_ethics_score'] < 40:  # Below ethical threshold
            quantum_ethics_gaps = self._analyze_quantum_ethics_gaps(content_lower, scores)
            gaps.extend(quantum_ethics_gaps)
        
        # Document-type specific gaps
        type_specific_gaps = self._analyze_document_type_gaps(content_lower, doc_type)
        gaps.extend(type_specific_gaps)
        
        return gaps
    
    def _analyze_ai_cybersecurity_gaps(self, content: str, scores: Dict) -> List[PolicyGap]:
        """Analyze AI cybersecurity specific gaps."""
        gaps = []
        requirements = self.knowledge_base['ai_cybersecurity']['critical_requirements']
        
        for requirement in requirements:
            if not self._content_addresses_requirement(content, requirement):
                severity = self._determine_severity(requirement, scores['ai_cybersecurity_score'])
                
                gap = PolicyGap(
                    framework="AI Cybersecurity",
                    category="Security Requirements",
                    severity=severity,
                    gap_description=f"Missing or insufficient coverage of {requirement}",
                    recommendations=self._get_ai_cyber_recommendations(requirement),
                    confidence_score=0.85,
                    reference_documents=["NIST AI RMF", "MITRE ATLAS"]
                )
                gaps.append(gap)
        
        return gaps
    
    def _analyze_quantum_cybersecurity_gaps(self, content: str, scores: Dict) -> List[PolicyGap]:
        """Analyze quantum cybersecurity specific gaps."""
        gaps = []
        requirements = self.knowledge_base['quantum_cybersecurity']['critical_requirements']
        
        for requirement in requirements:
            if not self._content_addresses_requirement(content, requirement):
                severity = self._determine_severity(requirement, scores['quantum_cybersecurity_score'] * 20)
                
                gap = PolicyGap(
                    framework="Quantum Cybersecurity",
                    category="Cryptographic Security",
                    severity=severity,
                    gap_description=f"Lacks {requirement} specification",
                    recommendations=self._get_quantum_cyber_recommendations(requirement),
                    confidence_score=0.90,
                    reference_documents=["NIST PQC", "FIPS 203/204/205"]
                )
                gaps.append(gap)
        
        return gaps
    
    def _analyze_ai_ethics_gaps(self, content: str, scores: Dict) -> List[PolicyGap]:
        """Analyze AI ethics specific gaps."""
        gaps = []
        requirements = self.knowledge_base['ai_ethics']['critical_requirements']
        
        for requirement in requirements:
            if not self._content_addresses_requirement(content, requirement):
                severity = self._determine_severity(requirement, scores['ai_ethics_score'])
                
                gap = PolicyGap(
                    framework="AI Ethics",
                    category="Ethical Governance",
                    severity=severity,
                    gap_description=f"Insufficient {requirement} provisions",
                    recommendations=self._get_ai_ethics_recommendations(requirement),
                    confidence_score=0.80,
                    reference_documents=["EU AI Act", "IEEE Ethically Aligned Design"]
                )
                gaps.append(gap)
        
        return gaps
    
    def _analyze_quantum_ethics_gaps(self, content: str, scores: Dict) -> List[PolicyGap]:
        """Analyze quantum ethics specific gaps."""
        gaps = []
        requirements = self.knowledge_base['quantum_ethics']['critical_requirements']
        
        for requirement in requirements:
            if not self._content_addresses_requirement(content, requirement):
                severity = self._determine_severity(requirement, scores['quantum_ethics_score'])
                
                gap = PolicyGap(
                    framework="Quantum Ethics",
                    category="Emerging Technology Ethics",
                    severity=severity,
                    gap_description=f"Missing {requirement} considerations",
                    recommendations=self._get_quantum_ethics_recommendations(requirement),
                    confidence_score=0.75,
                    reference_documents=["Quantum Ethics Guidelines", "National Quantum Initiatives"]
                )
                gaps.append(gap)
        
        return gaps
    
    def _analyze_document_type_gaps(self, content: str, doc_type: str) -> List[PolicyGap]:
        """Analyze document-type specific gaps."""
        gaps = []
        
        if doc_type.lower() in ['policy', 'regulation']:
            # Policy-specific gap patterns
            if 'implementation timeline' not in content:
                gaps.append(PolicyGap(
                    framework="Policy Structure",
                    category="Implementation",
                    severity="High",
                    gap_description="Missing clear implementation timeline and milestones",
                    recommendations=["Define specific implementation phases", "Set measurable milestones", "Establish timeline accountability"],
                    confidence_score=0.90,
                    reference_documents=["Policy Development Best Practices"]
                ))
        
        elif doc_type.lower() == 'standard':
            # Standard-specific gap patterns
            if 'conformance' not in content and 'compliance' not in content:
                gaps.append(PolicyGap(
                    framework="Standard Structure",
                    category="Conformance",
                    severity="Critical",
                    gap_description="Missing conformance and compliance specifications",
                    recommendations=["Define conformance criteria", "Specify testing procedures", "Establish certification processes"],
                    confidence_score=0.95,
                    reference_documents=["ISO/IEC Directives"]
                ))
        
        elif doc_type.lower() == 'product':
            # Product-specific gap patterns
            if 'security' not in content:
                gaps.append(PolicyGap(
                    framework="Product Security",
                    category="Security Requirements",
                    severity="Critical",
                    gap_description="Insufficient security specifications for product",
                    recommendations=["Define security architecture", "Specify threat model", "Implement security controls"],
                    confidence_score=0.85,
                    reference_documents=["Secure Development Lifecycle"]
                ))
        
        return gaps
    
    def _content_addresses_requirement(self, content: str, requirement: str) -> bool:
        """Check if content adequately addresses a specific requirement."""
        # Convert requirement to searchable keywords
        keywords = self._extract_keywords_from_requirement(requirement)
        
        # Check for keyword presence with context
        found_keywords = 0
        for keyword in keywords:
            if keyword in content:
                found_keywords += 1
        
        # Requirement is addressed if majority of keywords found
        return found_keywords >= len(keywords) * 0.6
    
    def _extract_keywords_from_requirement(self, requirement: str) -> List[str]:
        """Extract searchable keywords from requirement text."""
        # Simple keyword extraction - can be enhanced with NLP
        words = requirement.lower().split()
        # Filter out common words
        stop_words = {'and', 'or', 'the', 'a', 'an', 'in', 'of', 'for', 'to', 'with'}
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        return keywords
    
    def _determine_severity(self, requirement: str, score: float) -> str:
        """Determine gap severity based on requirement importance and current score."""
        critical_terms = ['security', 'encryption', 'authentication', 'privacy', 'bias']
        
        if any(term in requirement.lower() for term in critical_terms):
            if score < 30:
                return "Critical"
            elif score < 50:
                return "High"
            else:
                return "Medium"
        else:
            if score < 40:
                return "High"
            elif score < 60:
                return "Medium"
            else:
                return "Low"
    
    def _get_ai_cyber_recommendations(self, requirement: str) -> List[str]:
        """Generate AI cybersecurity specific recommendations."""
        recommendations_map = {
            'AI model security validation': [
                "Implement model integrity checks",
                "Establish secure model versioning",
                "Deploy model authentication mechanisms"
            ],
            'Adversarial attack protection': [
                "Implement adversarial training techniques",
                "Deploy input validation and sanitization",
                "Establish anomaly detection systems"
            ],
            'Data poisoning prevention': [
                "Implement data validation pipelines",
                "Establish data provenance tracking",
                "Deploy statistical anomaly detection"
            ]
        }
        
        for key, recs in recommendations_map.items():
            if any(word in requirement.lower() for word in key.lower().split()):
                return recs
        
        return ["Implement comprehensive security measures", "Establish monitoring protocols", "Deploy defense-in-depth strategies"]
    
    def _get_quantum_cyber_recommendations(self, requirement: str) -> List[str]:
        """Generate quantum cybersecurity specific recommendations."""
        recommendations_map = {
            'Post-quantum cryptographic': [
                "Adopt NIST-approved PQC algorithms",
                "Implement cryptographic agility",
                "Plan migration from classical cryptography"
            ],
            'Quantum key distribution': [
                "Deploy QKD protocols for high-security communications",
                "Implement quantum-safe key management",
                "Establish quantum channel authentication"
            ],
            'Quantum threat assessment': [
                "Conduct regular quantum risk evaluations",
                "Monitor quantum computing developments",
                "Update threat models for quantum capabilities"
            ]
        }
        
        for key, recs in recommendations_map.items():
            if any(word in requirement.lower() for word in key.lower().split()):
                return recs
        
        return ["Implement quantum-safe security measures", "Establish quantum readiness protocols", "Deploy future-proof cryptography"]
    
    def _get_ai_ethics_recommendations(self, requirement: str) -> List[str]:
        """Generate AI ethics specific recommendations."""
        recommendations_map = {
            'bias detection': [
                "Implement algorithmic bias testing",
                "Establish diverse testing datasets",
                "Deploy continuous bias monitoring"
            ],
            'transparency': [
                "Implement explainable AI techniques",
                "Establish decision audit trails",
                "Deploy interpretability tools"
            ],
            'human oversight': [
                "Implement human-in-the-loop systems",
                "Establish override mechanisms",
                "Deploy accountability frameworks"
            ]
        }
        
        for key, recs in recommendations_map.items():
            if any(word in requirement.lower() for word in key.lower().split()):
                return recs
        
        return ["Implement ethical AI governance", "Establish accountability mechanisms", "Deploy fairness monitoring"]
    
    def _get_quantum_ethics_recommendations(self, requirement: str) -> List[str]:
        """Generate quantum ethics specific recommendations."""
        return [
            "Establish quantum ethics review board",
            "Implement inclusive quantum development practices",
            "Deploy responsible quantum research protocols"
        ]
    
    def _generate_strategic_recommendations(self, gaps: List[PolicyGap], 
                                         scores: Dict[str, float], 
                                         doc_type: str) -> List[str]:
        """Generate high-level strategic recommendations."""
        recommendations = []
        
        # Priority-based recommendations
        critical_gaps = [gap for gap in gaps if gap.severity == "Critical"]
        if critical_gaps:
            recommendations.append("Address critical security and ethical gaps as highest priority")
        
        # Framework-specific strategic guidance
        if scores['ai_cybersecurity_score'] < 50:
            recommendations.append("Develop comprehensive AI cybersecurity strategy with clear implementation roadmap")
        
        if scores['quantum_cybersecurity_score'] < 2:
            recommendations.append("Establish quantum readiness program with post-quantum cryptography migration plan")
        
        if scores['ai_ethics_score'] < 40:
            recommendations.append("Implement AI ethics governance framework with stakeholder engagement")
        
        if scores['quantum_ethics_score'] < 30:
            recommendations.append("Develop quantum ethics guidelines aligned with emerging best practices")
        
        # Document type specific strategies
        if doc_type.lower() == 'policy':
            recommendations.append("Establish clear governance structure with defined roles and responsibilities")
        elif doc_type.lower() == 'standard':
            recommendations.append("Develop conformance testing and certification procedures")
        elif doc_type.lower() == 'product':
            recommendations.append("Implement security-by-design principles throughout development lifecycle")
        
        return recommendations
    
    def _assess_compliance_status(self, content: str, scores: Dict[str, float]) -> Dict[str, str]:
        """Assess compliance status against major frameworks."""
        status = {}
        
        # AI frameworks
        if scores['ai_cybersecurity_score'] >= 70:
            status['NIST AI RMF'] = "Compliant"
        elif scores['ai_cybersecurity_score'] >= 50:
            status['NIST AI RMF'] = "Partially Compliant"
        else:
            status['NIST AI RMF'] = "Non-Compliant"
        
        # Quantum frameworks
        if scores['quantum_cybersecurity_score'] >= 4:
            status['NIST PQC'] = "Compliant"
        elif scores['quantum_cybersecurity_score'] >= 2:
            status['NIST PQC'] = "Partially Compliant"
        else:
            status['NIST PQC'] = "Non-Compliant"
        
        # Ethics frameworks
        if scores['ai_ethics_score'] >= 60:
            status['EU AI Act'] = "Compliant"
        elif scores['ai_ethics_score'] >= 40:
            status['EU AI Act'] = "Partially Compliant"
        else:
            status['EU AI Act'] = "Non-Compliant"
        
        return status
    
    def _generate_learning_insights(self, content: str, gaps: List[PolicyGap], 
                                  scores: Dict[str, float]) -> List[str]:
        """Generate learning insights using reinforcement learning patterns."""
        insights = []
        
        # Pattern recognition insights
        if len(gaps) > 5:
            insights.append("Document shows systematic gaps suggesting need for comprehensive policy framework review")
        
        # Score pattern insights - filter numeric values only
        numeric_scores = [v for v in scores.values() if isinstance(v, (int, float))]
        if len(numeric_scores) > 1:
            score_variance = np.var(numeric_scores)
            if score_variance > 100:
                insights.append("Significant variation in framework scores indicates uneven development across domains")
        
        # Gap pattern insights
        gap_categories = {}
        for gap in gaps:
            gap_categories[gap.category] = gap_categories.get(gap.category, 0) + 1
        
        if gap_categories:
            most_common_category = max(gap_categories.keys(), key=lambda x: gap_categories[x])
            insights.append(f"Most gaps identified in {most_common_category} - focus improvement efforts here")
        
        # Framework-specific insights
        if scores['ai_cybersecurity_score'] > scores['quantum_cybersecurity_score'] * 20:
            insights.append("Strong AI cybersecurity foundation - leverage for quantum security development")
        
        if scores['ai_ethics_score'] > scores['quantum_ethics_score']:
            insights.append("Established AI ethics practices can inform quantum ethics development")
        
        return insights
    
    def _calculate_overall_maturity(self, scores: Dict[str, float]) -> float:
        """Calculate overall policy maturity score."""
        # Weighted scoring based on patent formulations
        weights = {
            'ai_cybersecurity_score': 0.3,
            'quantum_cybersecurity_score': 0.25,  # Convert 5-scale to 100-scale
            'ai_ethics_score': 0.25,
            'quantum_ethics_score': 0.2
        }
        
        weighted_score = (
            scores['ai_cybersecurity_score'] * weights['ai_cybersecurity_score'] +
            scores['quantum_cybersecurity_score'] * 20 * weights['quantum_cybersecurity_score'] +
            scores['ai_ethics_score'] * weights['ai_ethics_score'] +
            scores['quantum_ethics_score'] * weights['quantum_ethics_score']
        )
        
        return round(weighted_score, 1)

# Global instance for use across the application
policy_gap_analyzer = PolicyGapAnalyzer()