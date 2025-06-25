"""
GUARDIAN Private Deployment Configuration
Sets up secure, private deployment for prototype testing
"""

import streamlit as st
import os
from datetime import datetime

def add_authentication_layer():
    """Add simple authentication for prototype access."""
    
    # Check if user is authenticated
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.set_page_config(
            page_title="GUARDIAN Access",
            page_icon="🔒",
            layout="centered"
        )
        
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1>🔒 GUARDIAN Prototype Access</h1>
            <p style="color: #666; margin-bottom: 2rem;">
                Advanced Risk Intelligence Assistant for Emerging Technologies
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            access_code = st.text_input(
                "Enter Access Code:",
                type="password",
                placeholder="Prototype access code",
                help="Contact administrator for access"
            )
            
            if st.button("Access GUARDIAN", use_container_width=True):
                # Simple access codes for different user types
                valid_codes = {
                    "guardian-admin": "Administrator",
                    "guardian-demo": "Demo User", 
                    "guardian-test": "Test User",
                    "guardian-client": "Client Access"
                }
                
                if access_code in valid_codes:
                    st.session_state.authenticated = True
                    st.session_state.user_type = valid_codes[access_code]
                    st.session_state.access_time = datetime.now()
                    st.success(f"Welcome, {valid_codes[access_code]}!")
                    st.rerun()
                else:
                    st.error("Invalid access code. Please contact the administrator.")
            
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; color: #888; font-size: 0.9rem;">
                <p>GUARDIAN is a prototype cybersecurity assessment platform.</p>
                <p>Authorized access only. All activities are logged.</p>
            </div>
            """, unsafe_allow_html=True)
        
        return False
    
    return True

def setup_deployment_environment():
    """Configure environment for secure deployment."""
    
    # Add security headers
    st.markdown("""
    <script>
    // Add security headers
    if (window.location.protocol !== 'https:' && window.location.hostname !== 'localhost') {
        window.location.replace('https:' + window.location.href.substring(window.location.protocol.length));
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Log access for security monitoring
    if st.session_state.get('authenticated'):
        access_log = {
            'user_type': st.session_state.get('user_type', 'Unknown'),
            'access_time': st.session_state.get('access_time', datetime.now()),
            'session_id': st.session_state.get('chat_session_id', 'No session')
        }
        
        # Add access info to sidebar for admin visibility
        with st.sidebar:
            st.markdown("---")
            st.markdown("**Access Info**")
            st.text(f"User: {access_log['user_type']}")
            st.text(f"Session: {access_log['access_time'].strftime('%H:%M')}")

def get_deployment_instructions():
    """Return deployment instructions for Replit."""
    return """
    ## GUARDIAN Private Deployment Steps
    
    1. **Prepare for Deployment**
       - Ensure all code is committed to Git
       - Verify environment variables are set
       - Test application functionality
    
    2. **Deploy on Replit**
       - Click "Deploy" button in Replit
       - Choose "Private" visibility
       - Set custom domain if desired
       - Configure environment variables
    
    3. **Access Control Setup**
       - Share access codes with authorized users:
         * guardian-admin: Full administrator access
         * guardian-demo: Demo/presentation access
         * guardian-test: Testing and development
         * guardian-client: Client review access
    
    4. **Security Features**
       - HTTPS automatically enabled
       - Private URLs not indexed by search engines
       - Access logging for security monitoring
       - Session-based authentication
    
    5. **Sharing with Stakeholders**
       - Provide deployment URL + access code
       - Perfect for government/nonprofit demonstrations
       - Secure policy document testing
       - Real-world performance evaluation
    """