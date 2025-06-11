#!/bin/bash

# Fix matplotlib import error
cd /opt/guardian
source guardian_env/bin/activate

# Install matplotlib and its dependencies
pip install matplotlib==3.8.2
pip install kiwisolver pyparsing cycler fonttools pillow

# Restart streamlit
sudo systemctl restart guardian-streamlit

echo "Matplotlib fixed. Check your application again."