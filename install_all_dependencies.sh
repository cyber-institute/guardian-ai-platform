#!/bin/bash

# Install All Missing Dependencies for GUARDIAN on EC2
echo "=== Installing All GUARDIAN Dependencies ==="

cd /opt/guardian
source guardian_env/bin/activate

# Update pip first
pip install --upgrade pip

# Install all required packages
echo "Installing core dependencies..."
pip install aiohttp==3.9.1
pip install anthropic==0.7.8
pip install Flask==3.0.0
pip install google-auth==2.25.2
pip install google-auth-oauthlib==1.2.0
pip install google-cloud-dialogflow-cx==1.15.0
pip install matplotlib==3.8.2
pip install numpy==1.26.2
pip install openai==1.6.1
pip install pandas==2.1.4
pip install pdf2image==1.17.0
pip install Pillow==10.2.0
pip install plotly==5.17.0
pip install psycopg2-binary==2.9.9
pip install PyPDF2==3.0.1
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install scikit-learn==1.3.2
pip install SQLAlchemy==2.0.23
pip install streamlit==1.29.0
pip install trafilatura==1.6.4
pip install gunicorn==21.2.0
pip install typing-extensions==4.8.0
pip install greenlet==3.0.3

# Verify key imports
echo "Verifying installations..."
python3 -c "import sqlalchemy; print(f'SQLAlchemy: {sqlalchemy.__version__}')"
python3 -c "import openai; print(f'OpenAI: {openai.__version__}')"
python3 -c "import streamlit; print(f'Streamlit: {streamlit.__version__}')"
python3 -c "import pandas; print(f'Pandas: {pandas.__version__}')"

# Test database connection
echo "Testing database connection..."
python3 -c "
try:
    from utils.database import get_db_connection
    conn = get_db_connection()
    print('Database connection: SUCCESS')
    conn.close()
except Exception as e:
    print(f'Database connection: ERROR - {e}')
"

# Restart services
echo "Restarting GUARDIAN services..."
sudo systemctl stop guardian-streamlit guardian-webhook
sleep 2
sudo systemctl start guardian-streamlit guardian-webhook

echo "Installation complete. Services restarted."
echo "Check: http://ec2-3-128-199-3.us-east-2.compute.amazonaws.com:5000"