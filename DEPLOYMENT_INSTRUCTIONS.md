# Complete AWS Deployment Instructions

## Quick Deployment Method

### Option 1: Direct File Transfer
1. Download the `guardian_aws_deployment.tar.gz` file from this Replit
2. Upload to your EC2 instance:
```bash
scp -i your-key.pem guardian_aws_deployment.tar.gz ubuntu@ec2-3-128-199-3.us-east-2.compute.amazonaws.com:/home/ubuntu/
```

3. SSH into your EC2 instance:
```bash
ssh -i your-key.pem ubuntu@ec2-3-128-199-3.us-east-2.compute.amazonaws.com
```

4. Extract and deploy:
```bash
# Remove any existing installation
sudo rm -rf /opt/guardian

# Create new deployment directory
sudo mkdir -p /opt/guardian
sudo chown ubuntu:ubuntu /opt/guardian

# Extract files
tar -xzf guardian_aws_deployment.tar.gz -C /opt/guardian
cd /opt/guardian

# Run deployment script
chmod +x aws_deploy.sh
./aws_deploy.sh
```

### Option 2: Git Clone Method
```bash
# SSH into your EC2 instance
ssh -i your-key.pem ubuntu@ec2-3-128-199-3.us-east-2.compute.amazonaws.com

# Clone from your repository (if you push this to GitHub)
sudo rm -rf /opt/guardian
sudo mkdir -p /opt/guardian
sudo chown ubuntu:ubuntu /opt/guardian
cd /opt/guardian

# Clone your repository here
# git clone YOUR_REPOSITORY_URL .

# Run deployment
chmod +x aws_deploy.sh
./aws_deploy.sh
```

## Critical Configuration Steps

### 1. Database Password
After deployment, edit the environment file:
```bash
cd /opt/guardian
nano .env
```
Replace `YOUR_PASSWORD` with your actual RDS password from AWS console.

### 2. Service Management
```bash
# Start services
sudo systemctl start guardian-streamlit guardian-webhook

# Check status
sudo systemctl status guardian-streamlit
sudo systemctl status guardian-webhook

# View logs
sudo journalctl -u guardian-streamlit -f
sudo journalctl -u guardian-webhook -f

# Restart if needed
sudo systemctl restart guardian-streamlit guardian-webhook
```

### 3. Access Your Application
- **Main Application**: http://ec2-3-128-199-3.us-east-2.compute.amazonaws.com:5000
- **Webhook Endpoint**: http://ec2-3-128-199-3.us-east-2.compute.amazonaws.com:8081

## Your AWS Configuration (Verified)
- **EC2 Instance**: ec2-3-128-199-3.us-east-2.compute.amazonaws.com
- **RDS Database**: guardian-db.c5ufmq84p4a.us-east-2.rds.amazonaws.com:5432
- **Security Groups**: Ports 5000, 8081, 22, 5432 properly configured
- **Database**: PostgreSQL ready with guardian-db database

## Performance Optimizations Included
- Intelligent caching system for document scoring
- Streamlined thumbnail generation
- HTML artifact prevention
- Optimized database queries
- Memory-efficient document processing

## Troubleshooting

### Database Connection Issues
```bash
# Test database connection
cd /opt/guardian
source guardian_env/bin/activate
python3 -c "from utils.database import get_db_connection; print(get_db_connection())"
```

### Service Not Starting
```bash
# Check logs for errors
sudo journalctl -u guardian-streamlit --no-pager
sudo journalctl -u guardian-webhook --no-pager

# Verify Python environment
cd /opt/guardian
source guardian_env/bin/activate
pip list
```

### Port Access Issues
```bash
# Check if ports are listening
sudo netstat -tlnp | grep -E ':(5000|8081)'

# Verify firewall
sudo ufw status
```

## Complete File Replacement
This deployment completely replaces any existing GUARDIAN installation with the optimized version from Replit, including all performance improvements and bug fixes.