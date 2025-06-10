"""
Google Dialogflow CX Chatbot Integration for GUARDIAN
Provides intelligent tooltips and explanations for filters, fields, and scoring systems
"""

import os
import json
import logging
from typing import Dict, Optional, List
import streamlit as st

# Try to import Dialogflow CX, fallback to local processing if unavailable
try:
    from google.cloud import dialogflow_cx
    DIALOGFLOW_AVAILABLE = True
except ImportError:
    DIALOGFLOW_AVAILABLE = False
    dialogflow_cx = None

logger = logging.getLogger(__name__)

class GuardianChatbot:
    """Dialogflow CX chatbot for GUARDIAN system explanations and help."""
    
    def __init__(self):
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
        self.location = os.environ.get('DIALOGFLOW_LOCATION', 'global')
        self.agent_id = os.environ.get('DIALOGFLOW_AGENT_ID')
        self.language_code = 'en'
        
        # Initialize Dialogflow CX client
        self.session_client = None
        self.initialize_client()
        
        # Knowledge base for GUARDIAN-specific content
        self.knowledge_base = self._load_guardian_knowledge()
    
    def initialize_client(self):
        """Initialize Dialogflow CX session client."""
        try:
            if DIALOGFLOW_AVAILABLE and all([self.project_id, self.agent_id]):
                self.session_client = dialogflow_cx.SessionsClient()
                logger.info("Dialogflow CX client initialized successfully")
            else:
                logger.info("Using local chatbot processing - Dialogflow CX credentials not configured")
        except Exception as e:
            logger.error(f"Failed to initialize Dialogflow CX client: {e}")
    
    def _load_guardian_knowledge(self) -> Dict:
        """Load GUARDIAN-specific knowledge base for intelligent responses."""
        return {
            "ai_cybersecurity_maturity": {
                "description": "AI Cybersecurity Maturity assessment (0-100 scale) evaluates an organization's security preparedness for AI systems",
                "criteria": [
                    "Encryption Standards: Data protection and secure communication protocols for AI systems",
                    "Authentication Mechanisms: Identity verification and access control for AI systems", 
                    "Threat Monitoring: Real-time detection and response to AI-specific security threats",
                    "Incident Response: Structured response procedures for AI security breaches"
                ],
                "scoring": "0-25: Basic, 26-50: Developing, 51-75: Intermediate, 76-100: Advanced"
            },
            "quantum_cybersecurity_maturity": {
                "description": "Quantum Cybersecurity Maturity assessment (1-5 scale) based on QCMEA framework from GUARDIAN patents",
                "levels": {
                    "1": "Initial: Basic awareness of quantum threats with minimal preparation",
                    "2": "Basic: Foundational quantum-safe measures and initial planning", 
                    "3": "Intermediate: Scalable quantum security solutions with active implementation",
                    "4": "Advanced: Comprehensive quantum-resistant infrastructure integration",
                    "5": "Dynamic: Continuous adaptability to emerging quantum threats"
                }
            },
            "ai_ethics": {
                "description": "AI Ethics assessment (0-100 scale) evaluates ethical compliance and responsible AI practices",
                "criteria": [
                    "Fairness and Bias Mitigation: Systems to identify and reduce algorithmic bias",
                    "Transparency and Explainability: Clear understanding of AI decision-making processes",
                    "Accountability Mechanisms: Clear responsibility chains for AI system outcomes",
                    "Privacy Protection: Safeguarding personal data in AI processing"
                ]
            },
            "quantum_ethics": {
                "description": "Quantum Ethics assessment (0-100 scale) addresses emerging ethical considerations in quantum computing",
                "areas": [
                    "Quantum Advantage Ethics: Fair access and distribution of quantum computing benefits",
                    "Quantum Privacy Implications: Protection of sensitive data in quantum environments",
                    "Quantum Security Standards: Ethical implementation of quantum-safe cryptography",
                    "Equitable Quantum Access: Ensuring quantum technologies benefit all stakeholders"
                ]
            },
            "document_types": {
                "Standard": "Formal technical specifications or best practices",
                "Policy": "Organizational guidelines and governance documents",
                "Framework": "Structured approaches for implementation",
                "Guideline": "Recommended practices and procedures",
                "Report": "Analysis and findings documents",
                "Whitepaper": "Detailed technical or policy analysis"
            },
            "filters_help": {
                "display_mode": "Choose how documents are presented: Card View (detailed), Compact Cards (overview), Table View (sortable), Grid Layout (visual), Minimal List (simple)",
                "document_type": "Filter documents by their classification: Standards, Policies, Frameworks, Guidelines, Reports, or Whitepapers",
                "organization": "Filter by the authoring organization: NIST, CISA, ITI, NSA, or other agencies",
                "scores": "Filter documents by their maturity assessment scores across the four GUARDIAN frameworks"
            }
        }
    
    def detect_intent(self, text: str, session_id: str = "default") -> Optional[Dict]:
        """Send query to Dialogflow CX and get response."""
        if not DIALOGFLOW_AVAILABLE or not self.session_client or not self.project_id or not self.agent_id:
            return self._get_local_response(text)
        
        try:
            # Create session path
            session_path = self.session_client.session_path(
                project=self.project_id,
                location=self.location,
                agent=self.agent_id,
                session=session_id
            )
            
            # Create text input
            text_input = dialogflow_cx.TextInput(text=text)
            query_input = dialogflow_cx.QueryInput(
                text=text_input,
                language_code=self.language_code
            )
            
            # Send request
            request = dialogflow_cx.DetectIntentRequest(
                session=session_path,
                query_input=query_input
            )
            
            response = self.session_client.detect_intent(request=request)
            
            return {
                "response_text": response.query_result.response_messages[0].text.text[0] if response.query_result.response_messages else "",
                "intent": response.query_result.intent.display_name if response.query_result.intent else "",
                "confidence": response.query_result.intent_detection_confidence
            }
            
        except Exception as e:
            logger.error(f"Dialogflow CX error: {e}")
            return self._get_local_response(text)
    
    def _get_local_response(self, text: str) -> Dict:
        """Provide local responses when Dialogflow CX is unavailable."""
        text_lower = text.lower()
        
        # AI Cybersecurity Maturity responses
        if any(term in text_lower for term in ["ai cybersecurity", "ai cyber", "ai security"]):
            return {
                "response_text": f"AI Cybersecurity Maturity (0-100): {self.knowledge_base['ai_cybersecurity_maturity']['description']}. Key areas: {', '.join(self.knowledge_base['ai_cybersecurity_maturity']['criteria'])}",
                "intent": "ai_cybersecurity_help",
                "confidence": 0.9
            }
        
        # Quantum Cybersecurity Maturity responses  
        elif any(term in text_lower for term in ["quantum cybersecurity", "quantum cyber", "qcmea"]):
            levels = self.knowledge_base['quantum_cybersecurity_maturity']['levels']
            level_desc = "\n".join([f"Level {k}: {v}" for k, v in levels.items()])
            return {
                "response_text": f"Quantum Cybersecurity Maturity (1-5 QCMEA scale): {self.knowledge_base['quantum_cybersecurity_maturity']['description']}.\n\n{level_desc}",
                "intent": "quantum_cybersecurity_help", 
                "confidence": 0.9
            }
        
        # AI Ethics responses
        elif any(term in text_lower for term in ["ai ethics", "ai ethical"]):
            return {
                "response_text": f"AI Ethics (0-100): {self.knowledge_base['ai_ethics']['description']}. Key criteria: {', '.join(self.knowledge_base['ai_ethics']['criteria'])}",
                "intent": "ai_ethics_help",
                "confidence": 0.9
            }
        
        # Quantum Ethics responses
        elif any(term in text_lower for term in ["quantum ethics", "quantum ethical"]):
            return {
                "response_text": f"Quantum Ethics (0-100): {self.knowledge_base['quantum_ethics']['description']}. Focus areas: {', '.join(self.knowledge_base['quantum_ethics']['areas'])}",
                "intent": "quantum_ethics_help",
                "confidence": 0.9
            }
        
        # Document type explanations
        elif any(term in text_lower for term in ["document type", "standard", "policy", "framework", "guideline"]):
            doc_types = self.knowledge_base['document_types']
            type_list = "\n".join([f"• {k}: {v}" for k, v in doc_types.items()])
            return {
                "response_text": f"Document Types in GUARDIAN:\n{type_list}",
                "intent": "document_types_help",
                "confidence": 0.9
            }
        
        # Filter help
        elif any(term in text_lower for term in ["filter", "display mode", "how to use"]):
            filters = self.knowledge_base['filters_help']
            filter_help = "\n".join([f"• {k.replace('_', ' ').title()}: {v}" for k, v in filters.items()])
            return {
                "response_text": f"GUARDIAN Interface Help:\n{filter_help}",
                "intent": "filters_help",
                "confidence": 0.9
            }
        
        # Scoring explanations
        elif any(term in text_lower for term in ["score", "scoring", "assessment", "maturity"]):
            return {
                "response_text": "GUARDIAN uses four assessment frameworks: AI Cybersecurity Maturity (0-100), Quantum Cybersecurity Maturity (1-5), AI Ethics (0-100), and Quantum Ethics (0-100). Each framework evaluates different aspects of technological readiness and responsible implementation.",
                "intent": "scoring_help",
                "confidence": 0.9
            }
        
        # General help
        else:
            return {
                "response_text": "I can help explain GUARDIAN's scoring systems, document types, filters, and assessment frameworks. Try asking about AI Cybersecurity, Quantum Cybersecurity, AI Ethics, Quantum Ethics, or how to use the interface.",
                "intent": "general_help",
                "confidence": 0.7
            }
    
    def get_tooltip_response(self, element_type: str, element_name: str) -> str:
        """Get specific tooltip response for UI elements."""
        responses = {
            "ai_cybersecurity_score": "AI Cybersecurity Maturity: Measures security preparedness for AI systems including encryption, authentication, threat monitoring, and incident response capabilities.",
            "quantum_cybersecurity_score": "Quantum Cybersecurity Maturity: QCMEA 5-level assessment of quantum threat preparedness from basic awareness to dynamic adaptability.",
            "ai_ethics_score": "AI Ethics: Evaluates responsible AI practices including fairness, transparency, accountability, and privacy protection measures.",
            "quantum_ethics_score": "Quantum Ethics: Assesses ethical considerations in quantum computing including equitable access, privacy implications, and responsible implementation.",
            "display_mode_cards": "Card View: Detailed document display with full metadata, scores, and content previews for comprehensive review.",
            "display_mode_compact": "Compact Cards: Space-efficient overview showing key information and scores in a condensed format.",
            "display_mode_table": "Table View: Sortable spreadsheet format ideal for comparing multiple documents and filtering by criteria.",
            "display_mode_grid": "Grid Layout: Visual arrangement optimized for scanning document collections and identifying patterns.",
            "display_mode_minimal": "Minimal List: Simple text-based listing focusing on titles and essential metadata for quick navigation.",
            "refresh_button": "Refresh Analysis: Updates all documents with the latest metadata extraction algorithms and scoring improvements.",
            "document_type_filter": "Document Type: Filter by classification - Standards (technical specs), Policies (governance), Frameworks (structured approaches), Guidelines (best practices), Reports (analysis), Whitepapers (detailed studies)."
        }
        
        return responses.get(f"{element_type}_{element_name}", 
                          f"Help information for {element_name.replace('_', ' ').title()}")

# Global chatbot instance
chatbot = GuardianChatbot()