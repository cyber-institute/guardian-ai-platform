#!/bin/bash

echo "Installing final missing dependencies for GUARDIAN..."

cd /opt/guardian
source guardian_env/bin/activate

# Install all remaining packages that are causing import errors
pip install --upgrade pip

# Install missing packages in correct order
pip install anthropic==0.7.8
pip install aiohttp==3.9.1
pip install google-auth==2.25.2
pip install google-auth-oauthlib==1.2.0
pip install google-cloud-dialogflow-cx==1.15.0

# Install any additional missing packages
pip install charset-normalizer==3.3.2
pip install certifi==2023.11.17
pip install idna==3.6
pip install urllib3==2.1.0

# Verify all critical imports
echo "Testing all imports..."
python3 -c "
import sys
modules = ['anthropic', 'aiohttp', 'sqlalchemy', 'openai', 'streamlit', 'pandas', 'numpy', 'matplotlib', 'plotly', 'sklearn']
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError as e:
        print(f'✗ {module}: {e}')
"

# Restart services
sudo systemctl restart guardian-streamlit guardian-webhook

# Check service status
sudo systemctl status guardian-streamlit --no-pager -l

echo "Installation complete. GUARDIAN should now run without any import errors."