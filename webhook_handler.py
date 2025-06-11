"""
Dialogflow CX Webhook Handler for GUARDIAN
Handles incoming webhook requests from your GUARDIANAgent
"""

from flask import Flask, request, jsonify
import json
import logging
from utils.dialogflow_chatbot import GuardianChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
chatbot = GuardianChatbot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle Dialogflow CX webhook requests."""
    try:
        # Parse incoming request
        req = request.get_json()
        
        # Extract intent and parameters
        intent_name = req.get('intentInfo', {}).get('displayName', '')
        query_text = req.get('text', '')
        session_info = req.get('sessionInfo', {})
        
        logger.info(f"Received webhook request for intent: {intent_name}")
        logger.info(f"Query text: {query_text}")
        
        # Handle different intents
        response_text = ""
        
        if intent_name == "upload_policy" or "upload" in query_text.lower():
            response_text = handle_document_upload_intent(query_text, session_info)
        elif intent_name == "ai_cybersecurity_help":
            response_text = handle_ai_cybersecurity_intent()
        elif intent_name == "quantum_cybersecurity_help":
            response_text = handle_quantum_cybersecurity_intent()
        elif intent_name == "ai_ethics_help":
            response_text = handle_ai_ethics_intent()
        elif intent_name == "quantum_ethics_help":
            response_text = handle_quantum_ethics_intent()
        else:
            # Use chatbot for general queries
            chatbot_response = chatbot.detect_intent(query_text)
            response_text = chatbot_response.get('response_text', 'I can help you with GUARDIAN questions. Ask me about document uploads, scoring frameworks, or system features.')
        
        # Build Dialogflow CX response
        webhook_response = {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            }
        }
        
        logger.info(f"Sending response: {response_text[:100]}...")
        return jsonify(webhook_response)
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        error_response = {
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": ["I'm having trouble processing your request. Please try again or contact support."]
                        }
                    }
                ]
            }
        }
        return jsonify(error_response), 500

def handle_document_upload_intent(query_text, session_info):
    """Handle document upload related queries."""
    return """I can help you upload documents to GUARDIAN!

📤 Upload Process:
1. Navigate to the 'Repository Admin' tab
2. Find the 'Document Management' section  
3. Use drag-and-drop or click 'Browse files'
4. Select your document (PDF, TXT, DOCX supported)

🔍 What happens next:
• Automatic metadata extraction (title, organization, date)
• AI-powered content analysis
• Comprehensive scoring across 4 frameworks:
  - AI Cybersecurity Maturity (0-100)
  - Quantum Cybersecurity Maturity (1-5)
  - AI Ethics (0-100)
  - Quantum Ethics (0-100)

📋 Document Types Supported:
• Policy documents
• Compliance frameworks
• Security standards
• Regulatory guidelines
• Technical specifications

Ready to upload your document? Just navigate to Repository Admin > Document Management!"""

def handle_ai_cybersecurity_intent():
    """Handle AI Cybersecurity questions."""
    return """AI Cybersecurity Maturity (0-100 scale) evaluates your organization's security preparedness for AI systems.

🔐 Key Assessment Areas:
• Encryption Standards: Data protection and secure communication protocols
• Authentication Mechanisms: Identity verification and access control
• Threat Monitoring: Real-time detection and response capabilities
• Incident Response: Structured response procedures for AI security breaches

📊 Score Ranges:
• 0-25: Basic security measures
• 26-50: Developing security framework
• 51-75: Intermediate security maturity
• 76-100: Advanced security implementation

This framework helps organizations build robust security for AI systems."""

def handle_quantum_cybersecurity_intent():
    """Handle Quantum Cybersecurity questions."""
    return """Quantum Cybersecurity Maturity uses the QCMEA 5-level framework:

⚛️ QCMEA Levels:
1. Initial: Basic awareness of quantum threats
2. Basic: Foundational quantum-safe measures
3. Intermediate: Scalable quantum security solutions
4. Advanced: Comprehensive quantum-resistant infrastructure
5. Dynamic: Continuous adaptability to emerging threats

🛡️ Focus Areas:
• Post-quantum cryptography implementation
• Quantum key distribution systems
• Quantum-safe communication protocols
• Quantum threat assessment and monitoring

This patent-based framework prepares organizations for the quantum computing era."""

def handle_ai_ethics_intent():
    """Handle AI Ethics questions."""
    return """AI Ethics (0-100 scale) measures responsible AI practices:

⚖️ Key Criteria:
• Fairness and Bias Mitigation: Systems to identify and reduce algorithmic bias
• Transparency and Explainability: Clear understanding of AI decision-making
• Accountability Mechanisms: Clear responsibility chains for AI outcomes
• Privacy Protection: Safeguarding personal data in AI processing

📈 Implementation Levels:
• 0-25: Basic ethical awareness
• 26-50: Developing ethical practices
• 51-75: Structured ethical frameworks
• 76-100: Comprehensive ethical AI governance

Higher scores indicate more mature ethical AI implementation."""

def handle_quantum_ethics_intent():
    """Handle Quantum Ethics questions."""
    return """Quantum Ethics (0-100 scale) addresses ethical considerations in quantum computing:

🌟 Key Areas:
• Quantum Advantage Ethics: Fair access and distribution of quantum benefits
• Quantum Privacy Implications: Protection of sensitive data in quantum environments
• Quantum Security Standards: Ethical implementation of quantum-safe cryptography
• Equitable Quantum Access: Ensuring quantum technologies benefit all stakeholders

🔬 Emerging Considerations:
• Quantum supremacy implications
• Quantum computing resource allocation
• International quantum governance
• Quantum technology democratization

This framework addresses the ethical implications of quantum technology advancement."""

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "GUARDIAN Webhook Handler"})

if __name__ == '__main__':
    # Run webhook server
    import os
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port, debug=False)