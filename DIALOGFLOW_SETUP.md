# Google Dialogflow CX Setup Guide for GUARDIAN

## Prerequisites
1. Google Cloud Project with Dialogflow CX API enabled
2. Service Account with Dialogflow CX permissions
3. Active Dialogflow CX agent

## Step 1: Google Cloud Console Setup

### Create/Configure Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable the Dialogflow CX API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Dialogflow CX API"
   - Click "Enable"

### Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name: `guardian-chatbot-service`
4. Add roles:
   - Dialogflow CX Developer
   - Dialogflow CX Client

### Download Credentials
1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" > "Create New Key"
4. Select JSON format
5. Download the JSON file

## Step 2: Dialogflow CX Agent Setup

### Create Agent
1. Go to [Dialogflow CX Console](https://dialogflow.cloud.google.com/cx/)
2. Click "Create Agent"
3. Configure:
   - Display Name: `GUARDIAN Assistant`
   - Default Language: English
   - Time Zone: Your timezone
   - Location: Same as your Google Cloud project

### Configure Intents

#### Intent: ai.cybersecurity.help
**Training Phrases:**
- What is AI Cybersecurity Maturity?
- Explain AI cybersecurity scoring
- How does AI security assessment work?
- Tell me about AI cybersecurity framework

**Response:**
```
AI Cybersecurity Maturity (0-100 scale) evaluates your organization's security preparedness for AI systems. It assesses four key areas:

🔐 Encryption Standards: Data protection and secure communication protocols for AI systems
🔑 Authentication Mechanisms: Identity verification and access control for AI systems  
🛡️ Threat Monitoring: Real-time detection and response to AI-specific security threats
🚨 Incident Response: Structured response procedures for AI security breaches

Scores: 0-25 Basic | 26-50 Developing | 51-75 Intermediate | 76-100 Advanced
```

#### Intent: quantum.cybersecurity.help
**Training Phrases:**
- What is Quantum Cybersecurity Maturity?
- Explain QCMEA framework
- How does quantum security assessment work?
- Tell me about quantum cybersecurity levels

**Response:**
```
Quantum Cybersecurity Maturity uses the QCMEA 5-level framework from GUARDIAN patents:

1️⃣ Initial: Basic awareness of quantum threats with minimal preparation
2️⃣ Basic: Foundational quantum-safe measures and initial planning
3️⃣ Intermediate: Scalable quantum security solutions with active implementation  
4️⃣ Advanced: Comprehensive quantum-resistant infrastructure integration
5️⃣ Dynamic: Continuous adaptability to emerging quantum threats

This patent-based assessment helps organizations prepare for the quantum computing era.
```

#### Intent: ai.ethics.help
**Training Phrases:**
- What is AI Ethics scoring?
- Explain AI ethics assessment
- How do you measure AI ethics?
- Tell me about responsible AI practices

**Response:**
```
AI Ethics (0-100 scale) measures responsible AI practices across four key areas:

⚖️ Fairness and Bias Mitigation: Systems to identify and reduce algorithmic bias
🔍 Transparency and Explainability: Clear understanding of AI decision-making processes
📋 Accountability Mechanisms: Clear responsibility chains for AI system outcomes
🔒 Privacy Protection: Safeguarding personal data in AI processing

Higher scores indicate more comprehensive ethical AI implementation.
```

#### Intent: quantum.ethics.help
**Training Phrases:**
- What is Quantum Ethics?
- Explain quantum ethics scoring
- How do you assess quantum ethics?
- Tell me about quantum computing ethics

**Response:**
```
Quantum Ethics (0-100 scale) evaluates ethical considerations in quantum computing:

🌟 Quantum Advantage Ethics: Fair access and distribution of quantum computing benefits
🔐 Quantum Privacy Implications: Protection of sensitive data in quantum environments
🛡️ Quantum Security Standards: Ethical implementation of quantum-safe cryptography
🤝 Equitable Quantum Access: Ensuring quantum technologies benefit all stakeholders

This emerging field addresses the ethical implications of quantum technology advancement.
```

#### Intent: interface.help
**Training Phrases:**
- How do I use the interface?
- Explain the filters
- How do I navigate GUARDIAN?
- What are the display modes?

**Response:**
```
GUARDIAN Interface Guide:

📋 Display Modes:
• Card View: Detailed document display with full metadata and scores
• Compact Cards: Space-efficient overview with key information
• Table View: Sortable spreadsheet format for comparison
• Grid Layout: Visual arrangement for pattern identification
• Minimal List: Simple text-based listing for quick navigation

🔍 Filters:
• Document Type: Standards, Policies, Frameworks, Guidelines, Reports, Whitepapers
• Organization: Filter by authoring agency (NIST, CISA, ITI, etc.)
• Scores: Filter by maturity assessment levels

💡 Tip: Hover over score badges for detailed explanations!
```

#### Intent: document.types.help
**Training Phrases:**
- What are the document types?
- Explain document classifications
- What's the difference between standards and policies?

**Response:**
```
GUARDIAN Document Types:

📜 Standard: Formal technical specifications or best practices (e.g., NIST publications)
📋 Policy: Organizational guidelines and governance documents (e.g., ITI policies)
🏗️ Framework: Structured approaches for implementation (e.g., AI Risk Management Framework)
📖 Guideline: Recommended practices and procedures (e.g., CISA guidance)
📊 Report: Analysis and findings documents (e.g., research reports)
📄 Whitepaper: Detailed technical or policy analysis (e.g., industry studies)

Each type serves different purposes in technology governance and risk management.
```

## Step 3: Environment Variables

Add these to your environment or Replit Secrets:

```bash
GOOGLE_CLOUD_PROJECT_ID=your-project-id
DIALOGFLOW_LOCATION=global
DIALOGFLOW_AGENT_ID=your-agent-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
```

## Step 4: Testing the Integration

The GUARDIAN chatbot will automatically:
1. Try to connect to your Dialogflow CX agent
2. Fall back to local intelligent responses if unavailable
3. Provide contextual help through tooltips and chat interface

## Features

### Intelligent Tooltips
- Hover over score badges for detailed explanations
- Interactive help icons throughout the interface
- Context-aware scoring framework descriptions

### Chat Interface
- Floating chatbot widget in bottom-right corner
- Quick help buttons for common questions
- Natural language queries about GUARDIAN features

### Integration Points
- All Documents tab: Score explanations and filter help
- Patent Technology section: Framework explanations
- Repository Admin: Upload and configuration guidance

## Troubleshooting

### Common Issues
1. **Import Error**: Install dependencies with `pip install google-cloud-dialogflow-cx`
2. **Authentication**: Ensure service account JSON is accessible
3. **Permissions**: Verify Dialogflow CX roles are assigned
4. **Agent Not Found**: Check project ID and agent ID values

### Fallback Mode
If Dialogflow CX is unavailable, the system automatically uses local intelligent responses based on GUARDIAN's knowledge base.