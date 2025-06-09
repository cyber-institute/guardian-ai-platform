# AWS Deployment Guide for GUARDIAN

## Files You Need to Copy

### Core Application Files
Copy all these files to your EC2 instance:

```
app.py                          # Main Streamlit application
all_docs_tab.py                 # Document display and analysis interface
components/document_uploader.py # File upload functionality
utils/database.py               # Database connection manager
utils/db.py                     # Database operations
utils/hf_ai_scoring.py          # AI scoring engine
utils/score_utils.py            # Scoring utilities
```

### Configuration Files
```
.streamlit/config.toml          # Streamlit server configuration
deploy_requirements.txt         # Python dependencies
database_init.sql              # Database schema setup
```

### Deployment Scripts
```
deploy.sh                      # Automated deployment script
guardian.service               # Systemd service configuration
nginx.conf                     # Nginx reverse proxy configuration
aws_setup.py                   # Setup utility script
```

## Quick Deployment Steps

### 1. EC2 Setup
```bash
# On your EC2 instance
mkdir /home/ubuntu/guardian-app
cd /home/ubuntu/guardian-app

# Copy all application files here
```

### 2. Environment Variables
Set your RDS connection:
```bash
export DATABASE_URL="postgresql://username:password@your-rds-endpoint.region.rds.amazonaws.com:5432/guardian_db"
```

### 3. Database Setup
Run on your RDS instance:
```bash
psql $DATABASE_URL -f database_init.sql
```

### 4. Deploy Application
```bash
chmod +x deploy.sh
./deploy.sh
```

### 5. Start Service
```bash
sudo systemctl start guardian
sudo systemctl enable guardian
```

Your app will be available at `http://your-ec2-public-ip`

## Security Considerations
- Use RDS security groups to restrict database access
- Configure EC2 security groups for ports 80, 443, 22
- Consider using SSL certificates for HTTPS
- Store DATABASE_URL in AWS Systems Manager Parameter Store for production

## Monitoring
- Check logs: `sudo journalctl -u guardian -f`
- Monitor service: `sudo systemctl status guardian`
- Nginx logs: `sudo tail -f /var/log/nginx/error.log`