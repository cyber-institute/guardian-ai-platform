#!/bin/bash

# Quick Fix for EC2 SQLAlchemy Error
echo "=== Fixing SQLAlchemy Import Error on EC2 ==="

# Navigate to guardian directory
cd /opt/guardian

# Activate virtual environment
source guardian_env/bin/activate

# Install missing dependencies with specific versions
echo "Installing SQLAlchemy and dependencies..."
pip install --upgrade pip
pip install SQLAlchemy==2.0.23
pip install sqlalchemy==2.0.23
pip install typing-extensions==4.8.0
pip install greenlet==3.0.3
pip install psycopg2-binary==2.9.9

# Verify installation
echo "Verifying SQLAlchemy installation..."
python3 -c "import sqlalchemy; print(f'SQLAlchemy version: {sqlalchemy.__version__}')"

# Test database connection
echo "Testing database connection..."
python3 -c "
try:
    from utils.database import get_db_connection
    conn = get_db_connection()
    print('Database connection successful')
    conn.close()
except Exception as e:
    print(f'Database connection error: {e}')
"

# Restart services
echo "Restarting GUARDIAN services..."
sudo systemctl stop guardian-streamlit guardian-webhook
sudo systemctl start guardian-streamlit guardian-webhook

# Check service status
echo "Checking service status..."
sudo systemctl status guardian-streamlit --no-pager
sudo systemctl status guardian-webhook --no-pager

echo "Fix completed. Check http://your-ec2-ip:5000"