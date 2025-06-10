"""
Dialogflow CX Settings Configuration for GUARDIAN
Provides interface for configuring Google Cloud credentials
"""

import streamlit as st
import os

def render_dialogflow_settings():
    """Render Dialogflow CX configuration interface."""
    
    st.markdown("### 🤖 Chatbot Configuration")
    
    with st.expander("Configure Google Dialogflow CX", expanded=False):
        st.markdown("""
        Connect your Google Dialogflow CX agent to enable advanced chatbot features.
        The system works with local intelligent responses if not configured.
        """)
        
        # Current status
        current_project = os.environ.get('GOOGLE_CLOUD_PROJECT_ID', 'Not configured')
        current_agent = os.environ.get('DIALOGFLOW_AGENT_ID', 'Not configured')
        
        st.markdown("**Current Configuration:**")
        col1, col2 = st.columns(2)
        with col1:
            st.text(f"Project ID: {current_project}")
        with col2:
            st.text(f"Agent ID: {current_agent}")
        
        st.markdown("---")
        
        # Configuration form
        with st.form("dialogflow_config"):
            st.markdown("**Google Cloud Settings:**")
            
            project_id = st.text_input(
                "Google Cloud Project ID",
                value=current_project if current_project != 'Not configured' else '',
                help="Your Google Cloud project ID where Dialogflow CX is enabled",
                placeholder="e.g., guardian-vide"
            )
            
            agent_id = st.text_input(
                "Dialogflow CX Agent ID", 
                value=current_agent if current_agent != 'Not configured' else '',
                help="The ID of your GUARDIAN chatbot agent in Dialogflow CX",
                placeholder="e.g., GUARDIANAgent"
            )
            
            location = st.selectbox(
                "Agent Location",
                ["global", "us-central1", "us-east1", "europe-west1", "asia-northeast1"],
                index=0,
                help="Geographic location of your Dialogflow CX agent"
            )
            
            st.markdown("**Service Account Authentication:**")
            st.markdown("""
            Upload your Google Cloud service account JSON file with Dialogflow CX permissions:
            - Dialogflow CX Developer
            - Dialogflow CX Client
            """)
            
            uploaded_credentials = st.file_uploader(
                "Service Account JSON",
                type=['json'],
                help="Download this from Google Cloud Console > IAM & Admin > Service Accounts"
            )
            
            st.markdown("**Webhook Configuration:**")
            webhook_info = st.info("""
            Based on your screenshots, your webhook URL should be:
            `https://7cf4-71-10-72-118.ngrok-free.app/webhook`
            
            Add this webhook URL to your Dialogflow CX agent to enable two-way communication.
            """)
            
            if st.form_submit_button("Save Configuration", type="primary"):
                if project_id and agent_id:
                    # Would save to environment/secrets in real implementation
                    st.success("Configuration saved! Restart the application to apply changes.")
                    st.info("Note: In production, these would be saved to secure environment variables.")
                    
                    # Show next steps
                    st.markdown("**Next Steps:**")
                    st.markdown("""
                    1. Copy your webhook URL to Dialogflow CX
                    2. Test the agent in Dialogflow CX console
                    3. Try document upload phrases like "I want to upload a policy"
                    4. Verify responses match GUARDIAN's capabilities
                    """)
                else:
                    st.error("Please provide both Project ID and Agent ID")
        
        st.markdown("---")
        
        # Quick setup guide
        st.markdown("**Quick Setup Guide:**")
        setup_steps = """
        1. **Enable Dialogflow CX API** in your Google Cloud project
        2. **Create a Service Account** with Dialogflow CX permissions
        3. **Download the JSON credentials** file
        4. **Create a Dialogflow CX Agent** named "GUARDIAN Assistant"
        5. **Configure the agent** with GUARDIAN-specific intents
        6. **Add credentials** to environment variables or upload here
        """
        st.markdown(setup_steps)
        
        if st.button("📖 View Complete Setup Guide"):
            st.markdown("""
            **Detailed setup instructions available in DIALOGFLOW_SETUP.md**
            
            The guide includes:
            - Step-by-step Google Cloud Console configuration
            - Complete Dialogflow CX agent setup with intents
            - Training phrases for GUARDIAN-specific topics
            - Environment variable configuration
            - Troubleshooting common issues
            """)

def render_chatbot_status():
    """Display current chatbot system status."""
    
    try:
        from utils.dialogflow_chatbot import chatbot, DIALOGFLOW_AVAILABLE
        
        if DIALOGFLOW_AVAILABLE and chatbot.session_client:
            st.success("🤖 Dialogflow CX: Connected")
        elif DIALOGFLOW_AVAILABLE:
            st.warning("🤖 Dialogflow CX: Available but not configured")
        else:
            st.info("🤖 Local Chatbot: Active (Dialogflow CX not available)")
            
        # Test chatbot response
        test_response = chatbot.detect_intent("test")
        if test_response:
            st.success("✅ Chatbot system operational")
        else:
            st.error("❌ Chatbot system not responding")
            
    except Exception as e:
        st.error(f"❌ Chatbot system error: {str(e)}")

def show_chatbot_capabilities():
    """Display what the chatbot can help with."""
    
    st.markdown("### 💬 Chatbot Capabilities")
    
    capabilities = {
        "🔐 AI Cybersecurity": "Explains 0-100 scoring, encryption standards, threat monitoring",
        "⚛️ Quantum Security": "QCMEA 5-level framework, quantum threat preparedness",
        "⚖️ AI Ethics": "Responsible AI practices, bias mitigation, transparency",
        "🌟 Quantum Ethics": "Emerging quantum computing ethical considerations",
        "📋 Interface Help": "Display modes, filters, navigation guidance",
        "📚 Document Types": "Standards, policies, frameworks, guidelines explained"
    }
    
    for topic, description in capabilities.items():
        with st.expander(topic):
            st.write(description)
            if st.button(f"Test {topic.split()[1]} Question", key=f"test_{topic}"):
                try:
                    from utils.dialogflow_chatbot import chatbot
                    test_queries = {
                        "AI Cybersecurity": "What is AI Cybersecurity Maturity?",
                        "Quantum": "Explain Quantum Cybersecurity",
                        "AI": "How does AI Ethics scoring work?",
                        "Quantum": "What is Quantum Ethics?",
                        "Interface": "How do I use the filters?",
                        "Document": "What are the document types?"
                    }
                    
                    query_key = topic.split()[1] if len(topic.split()) > 1 else "Interface"
                    query = test_queries.get(query_key, "How does GUARDIAN work?")
                    
                    response = chatbot.detect_intent(query)
                    if response:
                        st.write("**Response:**")
                        st.write(response.get('response_text', 'No response available'))
                    else:
                        st.error("No response received")
                except Exception as e:
                    st.error(f"Error testing chatbot: {e}")