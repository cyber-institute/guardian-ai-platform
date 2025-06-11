#!/bin/bash

# Final dependency installation for GUARDIAN on EC2
cd /opt/guardian
source guardian_env/bin/activate

# Install remaining missing packages
pip install aiohttp==3.9.1
pip install google-auth==2.25.2
pip install google-auth-oauthlib==1.2.0
pip install google-cloud-dialogflow-cx==1.15.0

# Restart streamlit service
sudo systemctl restart guardian-streamlit

echo "All dependencies installed. GUARDIAN should now run without import errors."