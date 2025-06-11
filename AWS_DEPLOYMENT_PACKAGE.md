# AWS Deployment Package - Complete File Replacement

## Your AWS Infrastructure Details (From Screenshots)
- **EC2 Instance**: `ec2-3-128-199-3.us-east-2.compute.amazonaws.com`
- **RDS Database**: `guardian-db.c5ufmq84p4a.us-east-2.rds.amazonaws.com:5432`
- **Security Groups**: Configured for ports 5000, 8081, 22, 5432
- **Region**: us-east-2

## Deployment Steps

### 1. Connect to Your EC2 Instance
```bash
ssh -i your-key.pem ubuntu@ec2-3-128-199-3.us-east-2.compute.amazonaws.com
```

### 2. Prepare Environment
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install python3-pip python3-venv nginx -y

# Create application directory
sudo mkdir -p /opt/guardian
sudo chown ubuntu:ubuntu /opt/guardian
cd /opt/guardian
```

### 3. Upload and Extract Files
```bash
# Create virtual environment
python3 -m venv guardian_env
source guardian_env/bin/activate

# Install dependencies (will be provided in requirements.txt)
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create `.env` file with your database connection:
```
DATABASE_URL=postgresql://guardian_admin:******@guardian-db.c5ufmq84p4a.us-east-2.rds.amazonaws.com:5432/guardian-db
PGHOST=guardian-db.c5ufmq84p4a.us-east-2.rds.amazonaws.com
PGPORT=5432
PGUSER=guardian_admin
PGPASSWORD=******
PGDATABASE=guardian-db
```

### 5. Configure Systemd Services
Two services will be created:
- `guardian-streamlit.service` - Main Streamlit app on port 5000
- `guardian-webhook.service` - Webhook handler on port 8081

### 6. Configure Nginx (Optional)
For production deployment with domain name and SSL.

## Files Included in This Package
- All optimized Python files with performance improvements
- Database initialization scripts
- Systemd service configurations
- Nginx configuration
- Requirements.txt with exact versions
- Deployment automation scripts