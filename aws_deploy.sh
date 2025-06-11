#!/bin/bash

# AWS Deployment Script for GUARDIAN System
# Complete file replacement deployment

echo "=== GUARDIAN AWS Deployment Script ==="
echo "This will deploy GUARDIAN to your AWS EC2 instance with RDS PostgreSQL"

# Configuration from your AWS setup
EC2_HOST="ec2-3-128-199-3.us-east-2.compute.amazonaws.com"
RDS_HOST="guardian-db.c5ufmq84p4a.us-east-2.rds.amazonaws.com"

# Step 1: Prepare deployment directory
echo "Creating deployment directory..."
sudo mkdir -p /opt/guardian
sudo chown ubuntu:ubuntu /opt/guardian
cd /opt/guardian

# Step 2: Create virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv guardian_env
source guardian_env/bin/activate

# Step 3: Install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-dev postgresql-client nginx poppler-utils

# Step 4: Install Python packages
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r aws_requirements.txt

# Step 5: Create environment file
echo "Creating environment configuration..."
cat > .env << EOF
DATABASE_URL=postgresql://guardian_admin:YOUR_PASSWORD@${RDS_HOST}:5432/guardian-db
PGHOST=${RDS_HOST}
PGPORT=5432
PGUSER=guardian_admin
PGPASSWORD=YOUR_PASSWORD
PGDATABASE=guardian-db
EOF

echo "⚠️  IMPORTANT: Edit .env file and replace YOUR_PASSWORD with your actual RDS password"

# Step 6: Create Streamlit config
echo "Creating Streamlit configuration..."
mkdir -p .streamlit
cat > .streamlit/config.toml << EOF
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "light"
EOF

# Step 7: Initialize database
echo "Setting up database tables..."
python3 -c "
import os
from utils.database import get_db_connection, create_tables

try:
    conn = get_db_connection()
    create_tables(conn)
    print('Database tables created successfully')
    conn.close()
except Exception as e:
    print(f'Database setup error: {e}')
    print('Please ensure your RDS credentials are correct in .env file')
"

# Step 8: Install systemd services
echo "Installing systemd services..."
sudo cp aws_streamlit_service.service /etc/systemd/system/guardian-streamlit.service
sudo cp aws_webhook_service.service /etc/systemd/system/guardian-webhook.service

# Step 9: Enable and start services
echo "Starting GUARDIAN services..."
sudo systemctl daemon-reload
sudo systemctl enable guardian-streamlit
sudo systemctl enable guardian-webhook
sudo systemctl start guardian-streamlit
sudo systemctl start guardian-webhook

# Step 10: Configure firewall
echo "Configuring firewall..."
sudo ufw allow 5000
sudo ufw allow 8081
sudo ufw allow 22
sudo ufw --force enable

# Step 11: Status check
echo "Checking service status..."
sudo systemctl status guardian-streamlit --no-pager
sudo systemctl status guardian-webhook --no-pager

echo ""
echo "=== Deployment Complete ==="
echo "✓ GUARDIAN Streamlit App: http://${EC2_HOST}:5000"
echo "✓ Webhook Handler: http://${EC2_HOST}:8081"
echo ""
echo "Next Steps:"
echo "1. Edit /opt/guardian/.env with your RDS password"
echo "2. Restart services: sudo systemctl restart guardian-streamlit guardian-webhook"
echo "3. Check logs: sudo journalctl -u guardian-streamlit -f"
echo ""
echo "Your GUARDIAN system is now deployed on AWS!"