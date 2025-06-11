#!/bin/bash

# Complete Installation Command for EC2
echo "Installing all remaining GUARDIAN dependencies..."

cd /opt/guardian
source guardian_env/bin/activate

# Install all Python packages in one command
pip install --upgrade pip setuptools wheel

# Install core ML and data science packages first
pip install numpy==1.26.2 scipy matplotlib==3.8.2

# Install scikit-learn with dependencies
pip install scikit-learn==1.3.2

# Install remaining packages
pip install plotly==5.17.0 trafilatura==1.6.4 anthropic==0.7.8 pandas==2.1.4 Pillow==10.2.0 PyPDF2==3.0.1 python-dotenv==1.0.0 requests==2.31.0 gunicorn==21.2.0 typing-extensions==4.8.0 greenlet==3.0.3 aiohttp==3.9.1 Flask==3.0.0

# Verify all key imports work
echo "Testing imports..."
python3 -c "
try:
    import sklearn
    import plotly
    import pdf2image
    import anthropic
    import trafilatura
    import pandas
    import numpy
    import matplotlib
    print('All packages imported successfully!')
except ImportError as e:
    print(f'Import error: {e}')
"

echo "Restarting services..."
sudo systemctl restart guardian-streamlit guardian-webhook

echo "Installation complete!"