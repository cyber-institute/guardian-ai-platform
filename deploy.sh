#!/bin/bash

# GUARDIAN AWS Deployment Script
# Run this script on your EC2 instance

set -e

echo "Starting GUARDIAN deployment on AWS EC2..."

# Update system packages
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx postgresql-client

# Create application directory
APP_DIR="/home/ubuntu/guardian-app"
sudo mkdir -p $APP_DIR
sudo chown ubuntu:ubuntu $APP_DIR
cd $APP_DIR

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r deploy_requirements.txt

# Set up environment variables
echo "Setting up environment variables..."
echo "Please ensure these environment variables are set:"
echo "export DATABASE_URL='postgresql://username:password@your-rds-endpoint:5432/database_name'"
echo ""
echo "Add the above to ~/.bashrc or create a .env file"

# Set up systemd service
echo "Setting up systemd service..."
sudo cp guardian.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable guardian
sudo systemctl start guardian

# Set up nginx
echo "Setting up nginx reverse proxy..."
sudo cp nginx.conf /etc/nginx/sites-available/guardian
sudo ln -sf /etc/nginx/sites-available/guardian /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Set up firewall
echo "Configuring firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "Deployment completed!"
echo ""
echo "Next steps:"
echo "1. Set your DATABASE_URL environment variable"
echo "2. Run the database initialization: psql \$DATABASE_URL -f database_init.sql"
echo "3. Check service status: sudo systemctl status guardian"
echo "4. Check application logs: sudo journalctl -u guardian -f"
echo "5. Access your application at http://your-ec2-public-ip"