# Complete Dialogflow CX Integration Guide for GUARDIAN

## Your Current Setup Status ✅

Based on your screenshots and testing, you have successfully:

- ✅ Created GUARDIANAgent in Dialogflow CX
- ✅ Configured upload_policy intent with training phrases
- ✅ Set up webhook URL: `https://7cf4-71-10-72-118.ngrok-free.app/webhook`
- ✅ GUARDIAN webhook server running on port 8080
- ✅ Successfully tested document upload intent responses

## Integration Architecture

```
User Query → Dialogflow CX → Webhook → GUARDIAN System → Response
```

### Your Training Phrases (Working)
- "Submit my compliance draft" ✅
- "Can I upload my policy?" ✅
- "Upload a policy" ✅
- "I want to upload a document" ✅
- "Add a new regulation" ✅
- "Upload document for review" ✅
- "Submit a new regulation" ✅

## Webhook Configuration

### Current Webhook Endpoint
```
URL: https://7cf4-71-10-72-118.ngrok-free.app/webhook
Method: POST
Content-Type: application/json
```

### Local Development Webhook
```
URL: http://localhost:8080/webhook
Status: Running ✅
Health Check: http://localhost:8080/health
```

## Intent Responses Configured

### 1. Document Upload Intent
**Trigger:** upload_policy, document upload phrases
**Response:**
- Step-by-step upload instructions
- Supported file formats (PDF, TXT, DOCX)
- Automatic analysis explanation
- Four scoring frameworks overview

### 2. AI Cybersecurity Help
**Trigger:** ai_cybersecurity_help
**Response:**
- 0-100 scoring scale explanation
- Key assessment areas (Encryption, Authentication, Monitoring, Incident Response)
- Score range interpretations

### 3. Quantum Cybersecurity Help
**Trigger:** quantum_cybersecurity_help
**Response:**
- QCMEA 5-level framework
- Level descriptions (Initial → Dynamic)
- Focus areas (Post-quantum crypto, QKD, protocols)

### 4. AI Ethics Help
**Trigger:** ai_ethics_help
**Response:**
- 0-100 scoring criteria
- Key areas (Fairness, Transparency, Accountability, Privacy)
- Implementation level guidelines

### 5. Quantum Ethics Help
**Trigger:** quantum_ethics_help
**Response:**
- Emerging ethical considerations
- Key focus areas (Advantage ethics, Privacy, Security, Access)
- Quantum governance framework

## Testing Your Integration

### 1. Test in Dialogflow CX Console
1. Open your GUARDIANAgent in Dialogflow CX
2. Use the simulator on the right side
3. Try these phrases:
   - "I want to upload a policy"
   - "Submit my compliance draft"
   - "What is AI Cybersecurity?"
   - "Explain Quantum Ethics"

### 2. Verify Webhook Responses
```bash
# Test document upload intent
curl -X POST https://7cf4-71-10-72-118.ngrok-free.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"intentInfo": {"displayName": "upload_policy"}, "text": "upload policy"}'

# Health check
curl http://localhost:8080/health
```

## Next Steps for Enhancement

### 1. Add More Intents
Create these additional intents in Dialogflow CX:

#### Scoring Framework Help
**Training Phrases:**
- "How does scoring work?"
- "Explain the four frameworks"
- "What are the assessment criteria?"

#### Document Type Guidance  
**Training Phrases:**
- "What document types are supported?"
- "Difference between standards and policies?"
- "What is a framework document?"

#### Navigation Help
**Training Phrases:**
- "How do I navigate GUARDIAN?"
- "Where are the filters?"
- "How to change display mode?"

### 2. Enhanced Webhook Features
Add these capabilities to the webhook handler:

#### Session Management
```python
# Track user sessions and context
session_data = session_info.get('parameters', {})
user_context = session_data.get('user_context', {})
```

#### Dynamic Responses
```python
# Personalized responses based on user role
if user_role == "compliance_officer":
    response = get_compliance_focused_help()
elif user_role == "security_analyst":
    response = get_security_focused_help()
```

#### Document Status Integration
```python
# Real-time document processing status
from utils.database import DatabaseManager
db = DatabaseManager()
recent_uploads = db.get_recent_uploads(user_id)
```

### 3. Advanced Features

#### Rich Responses
Add card responses, quick replies, and media to Dialogflow CX:

```json
{
  "card": {
    "title": "Document Upload Guide",
    "subtitle": "Step-by-step instructions",
    "imageUri": "https://guardian.app/upload-guide.png",
    "buttons": [
      {
        "text": "Upload Now",
        "postback": "navigate_to_upload"
      }
    ]
  }
}
```

#### Quick Replies
```json
{
  "quickReplies": {
    "title": "What would you like to do?",
    "quickReplies": [
      "Upload Document",
      "View Scores",
      "Check Status",
      "Get Help"
    ]
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Webhook Not Responding
- Check ngrok tunnel status
- Verify webhook URL in Dialogflow CX
- Check Flask server logs: port 8080

#### 2. Intent Not Triggering
- Review training phrases in Dialogflow CX
- Check intent matching in test console
- Verify webhook fulfillment is enabled

#### 3. Response Formatting Issues
- Validate JSON response structure
- Check character limits (max 4096 for text)
- Ensure proper escaping of special characters

### Debug Commands
```bash
# Check webhook server status
curl http://localhost:8080/health

# View server logs
# Check workflow logs in GUARDIAN interface

# Test intent locally
python3 -c "
from utils.dialogflow_chatbot import GuardianChatbot
chatbot = GuardianChatbot()
print(chatbot.detect_intent('upload policy'))
"
```

## Production Deployment

### 1. Secure Webhook
- Use HTTPS with valid SSL certificates
- Implement request signature verification
- Add rate limiting and authentication

### 2. Environment Variables
```bash
GOOGLE_CLOUD_PROJECT_ID=guardian-vide
DIALOGFLOW_AGENT_ID=GUARDIANAgent
DIALOGFLOW_LOCATION=global
WEBHOOK_PORT=8080
WEBHOOK_SECRET=your-webhook-secret
```

### 3. Monitoring
- Log all webhook requests and responses
- Monitor response times and error rates
- Set up alerting for webhook failures

## Success Metrics

Your integration is successful when:
- ✅ All training phrases trigger correct intents
- ✅ Webhook responses are delivered within 5 seconds
- ✅ Users can successfully navigate to document upload
- ✅ Contextual help improves user experience
- ✅ Error rates are below 1%

## Support Resources

### GUARDIAN Components
- `webhook_handler.py`: Flask webhook server
- `utils/dialogflow_chatbot.py`: Local chatbot logic
- `components/dialogflow_settings.py`: Configuration interface
- `components/chatbot_widget.py`: UI integration

### Google Cloud Resources
- [Dialogflow CX Documentation](https://cloud.google.com/dialogflow/cx/docs)
- [Webhook Integration Guide](https://cloud.google.com/dialogflow/cx/docs/concept/webhook)
- [Best Practices](https://cloud.google.com/dialogflow/cx/docs/concept/best-practices)

Your GUARDIANAgent is now fully integrated with the GUARDIAN system!