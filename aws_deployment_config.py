#!/usr/bin/env python3
"""
AWS Deployment Configuration for GUARDIAN
Comprehensive setup for deploying GUARDIAN to AWS with RDS integration
"""

import os
import json
import boto3
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AWSDeploymentConfig:
    def __init__(self):
        self.region = 'us-east-1'  # Default region
        self.app_name = 'guardian-ai-assessment'
        self.deployment_config = {}
        
    def create_rds_config(self, rds_endpoint, db_name, username, password, port=5432):
        """Configure RDS connection for AWS deployment"""
        logger.info("Configuring RDS connection...")
        
        self.deployment_config['rds'] = {
            'endpoint': rds_endpoint,
            'database': db_name,
            'username': username,
            'password': password,
            'port': port,
            'ssl_mode': 'require',
            'connection_url': f"postgresql://{username}:{password}@{rds_endpoint}:{port}/{db_name}?sslmode=require"
        }
        
        return self.deployment_config['rds']
    
    def create_elasticbeanstalk_config(self):
        """Create Elastic Beanstalk configuration"""
        logger.info("Creating Elastic Beanstalk configuration...")
        
        # Create .ebextensions directory
        eb_dir = Path('.ebextensions')
        eb_dir.mkdir(exist_ok=True)
        
        # Environment configuration
        env_config = {
            "option_settings": {
                "aws:elasticbeanstalk:application:environment": {
                    "PYTHONPATH": "/var/app/current",
                    "DATABASE_URL": self.deployment_config['rds']['connection_url']
                },
                "aws:elasticbeanstalk:container:python": {
                    "WSGIPath": "application.py"
                },
                "aws:autoscaling:launchconfiguration": {
                    "InstanceType": "t3.medium",
                    "IamInstanceProfile": "aws-elasticbeanstalk-ec2-role"
                },
                "aws:elasticbeanstalk:healthreporting:system": {
                    "SystemType": "enhanced"
                }
            }
        }
        
        # Write configuration
        with open(eb_dir / '01_environment.config', 'w') as f:
            json.dump(env_config, f, indent=2)
        
        # Python dependencies configuration
        python_config = {
            "commands": {
                "01_install_dependencies": {
                    "command": "pip install -r requirements.txt"
                }
            }
        }
        
        with open(eb_dir / '02_python.config', 'w') as f:
            json.dump(python_config, f, indent=2)
        
        logger.info("Elastic Beanstalk configuration created")
    
    def create_requirements_txt(self):
        """Create requirements.txt for AWS deployment"""
        logger.info("Creating requirements.txt...")
        
        requirements = [
            "streamlit>=1.28.0",
            "pandas>=1.5.0",
            "numpy>=1.24.0",
            "plotly>=5.15.0",
            "matplotlib>=3.7.0",
            "psycopg2-binary>=2.9.0",
            "sqlalchemy>=2.0.0",
            "anthropic>=0.3.0",
            "openai>=1.0.0",
            "beautifulsoup4>=4.12.0",
            "requests>=2.31.0",
            "python-dotenv>=1.0.0",
            "Pillow>=10.0.0",
            "aiohttp>=3.8.0",
            "scikit-learn>=1.3.0",
            "qiskit>=0.44.0",
            "qiskit-aer>=0.12.0",
            "trafilatura>=1.6.0",
            "pypdf>=3.15.0",
            "python-docx>=0.8.0",
            "pdf2image>=3.1.0",
            "google-auth>=2.22.0",
            "google-auth-oauthlib>=1.0.0",
            "google-cloud-dialogflow-cx>=1.14.0",
            "schedule>=1.2.0"
        ]
        
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(requirements))
        
        logger.info("requirements.txt created")
    
    def create_application_py(self):
        """Create application.py for Elastic Beanstalk"""
        logger.info("Creating application.py for Elastic Beanstalk...")
        
        application_code = '''#!/usr/bin/env python3
"""
AWS Elastic Beanstalk Application Entry Point for GUARDIAN
"""

import os
import sys
import subprocess
from flask import Flask

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create Flask app for health checks
application = Flask(__name__)

@application.route('/')
def health_check():
    return "GUARDIAN AI Assessment Tool - Healthy"

@application.route('/health')
def health():
    return {"status": "healthy", "service": "guardian-ai"}

# Start Streamlit in background
def start_streamlit():
    """Start Streamlit app in background"""
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ]
    subprocess.Popen(cmd)

if __name__ == "__main__":
    start_streamlit()
    application.run(host='0.0.0.0', port=8080)
'''
        
        with open('application.py', 'w') as f:
            f.write(application_code)
        
        logger.info("application.py created")
    
    def create_dockerfile(self):
        """Create Dockerfile for containerized deployment"""
        logger.info("Creating Dockerfile...")
        
        dockerfile_content = '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    libpq-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
'''
        
        with open('Dockerfile', 'w') as f:
            f.write(dockerfile_content)
        
        logger.info("Dockerfile created")
    
    def create_docker_compose(self):
        """Create docker-compose.yml for local testing"""
        logger.info("Creating docker-compose.yml...")
        
        compose_content = f'''version: '3.8'

services:
  guardian:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DATABASE_URL={self.deployment_config['rds']['connection_url']}
      - ENVIRONMENT=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
'''
        
        with open('docker-compose.yml', 'w') as f:
            f.write(compose_content)
        
        logger.info("docker-compose.yml created")
    
    def create_environment_template(self):
        """Create .env template for production"""
        logger.info("Creating environment template...")
        
        env_template = f'''# GUARDIAN Production Environment Configuration
# AWS Deployment Settings

# Database Configuration
DATABASE_URL={self.deployment_config['rds']['connection_url']}
RDS_ENDPOINT={self.deployment_config['rds']['endpoint']}
RDS_DATABASE={self.deployment_config['rds']['database']}
RDS_USERNAME={self.deployment_config['rds']['username']}
RDS_PASSWORD={self.deployment_config['rds']['password']}

# Application Settings
ENVIRONMENT=production
AWS_REGION={self.region}
APP_NAME={self.app_name}

# SSL/Security
SSL_REQUIRE=true
SECURE_COOKIES=true

# API Keys (Configure these in AWS Systems Manager Parameter Store)
# OPENAI_API_KEY=your_openai_key_here
# ANTHROPIC_API_KEY=your_anthropic_key_here

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance
MAX_WORKERS=4
TIMEOUT=300
'''
        
        with open('.env.production', 'w') as f:
            f.write(env_template)
        
        logger.info("Production environment template created")
    
    def create_deployment_scripts(self):
        """Create deployment scripts"""
        logger.info("Creating deployment scripts...")
        
        # Elastic Beanstalk deployment script
        eb_deploy_script = '''#!/bin/bash
# Deploy GUARDIAN to AWS Elastic Beanstalk

echo "Deploying GUARDIAN to AWS Elastic Beanstalk..."

# Initialize EB if not already done
if [ ! -d ".elasticbeanstalk" ]; then
    echo "Initializing Elastic Beanstalk..."
    eb init guardian-ai-assessment --region us-east-1 --platform python-3.11
fi

# Create environment if it doesn't exist
if ! eb status production > /dev/null 2>&1; then
    echo "Creating production environment..."
    eb create production --instance-type t3.medium --database
else
    echo "Production environment exists, deploying..."
fi

# Deploy application
eb deploy production

echo "Deployment complete!"
echo "Check status with: eb status"
echo "View logs with: eb logs"
'''
        
        with open('deploy_eb.sh', 'w') as f:
            f.write(eb_deploy_script)
        os.chmod('deploy_eb.sh', 0o755)
        
        # Docker deployment script
        docker_deploy_script = '''#!/bin/bash
# Deploy GUARDIAN using Docker

echo "Building and deploying GUARDIAN with Docker..."

# Build image
docker build -t guardian-ai:latest .

# Run container
docker-compose up -d

echo "GUARDIAN is running at http://localhost:8501"
echo "Check status with: docker-compose ps"
echo "View logs with: docker-compose logs -f"
'''
        
        with open('deploy_docker.sh', 'w') as f:
            f.write(docker_deploy_script)
        os.chmod('deploy_docker.sh', 0o755)
        
        logger.info("Deployment scripts created")
    
    def create_aws_deployment_guide(self):
        """Create comprehensive AWS deployment guide"""
        logger.info("Creating AWS deployment guide...")
        
        guide_content = f'''# GUARDIAN AWS Deployment Guide

## Overview
This guide covers deploying GUARDIAN to AWS using multiple deployment options with RDS PostgreSQL.

## Prerequisites
- AWS CLI configured with appropriate permissions
- Amazon RDS PostgreSQL instance set up
- Database migrated using the migration package

## Deployment Options

### Option 1: AWS Elastic Beanstalk (Recommended)

#### Setup
1. Install EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. Deploy:
   ```bash
   ./deploy_eb.sh
   ```

#### Features
- Auto-scaling
- Load balancing
- Health monitoring
- Easy rollbacks

### Option 2: Docker Container

#### Local Testing
```bash
docker-compose up
```

#### AWS ECS Deployment
1. Push to ECR:
   ```bash
   aws ecr create-repository --repository-name guardian-ai
   docker tag guardian-ai:latest <account>.dkr.ecr.us-east-1.amazonaws.com/guardian-ai:latest
   docker push <account>.dkr.ecr.us-east-1.amazonaws.com/guardian-ai:latest
   ```

2. Create ECS service with the image

### Option 3: AWS Lambda (Serverless)
For smaller workloads, use AWS Lambda with the Streamlit app.

## Environment Variables

Set these in your AWS environment:

```
DATABASE_URL={self.deployment_config['rds']['connection_url']}
ENVIRONMENT=production
AWS_REGION={self.region}
```

## Security Configuration

### RDS Security Group
- Allow inbound PostgreSQL (5432) from application security group
- No public access

### Application Security Group
- Allow inbound HTTP (80) and HTTPS (443) from 0.0.0.0/0
- Allow outbound to RDS security group on port 5432

### IAM Roles
Create IAM role with policies for:
- RDS access
- Systems Manager (for secrets)
- CloudWatch (for monitoring)

## Monitoring and Logging

### CloudWatch Integration
- Application logs automatically sent to CloudWatch
- Set up alarms for:
  - High CPU usage
  - Database connection errors
  - Application errors

### Health Checks
- Application health endpoint: `/health`
- Database connectivity checks
- Automatic restart on failures

## Backup and Recovery

### RDS Automated Backups
- Enable automated backups (7-30 days retention)
- Configure backup window during low usage

### Application Backup
- Code stored in version control
- Configuration in AWS Systems Manager

## Performance Optimization

### RDS Performance
- Use appropriate instance size (db.t3.medium recommended)
- Enable Performance Insights
- Configure connection pooling

### Application Performance
- Use t3.medium or larger for Elastic Beanstalk
- Enable auto-scaling based on CPU/memory
- Configure CloudFront for static assets

## Cost Optimization

### Estimated Monthly Costs (us-east-1)
- RDS db.t3.micro: ~$15
- EB t3.small: ~$15
- Data transfer: ~$5
- **Total: ~$35/month**

### Cost Reduction Tips
- Use Reserved Instances for predictable workloads
- Schedule non-production environments to stop during off-hours
- Monitor usage with AWS Cost Explorer

## Troubleshooting

### Common Issues
1. **Database Connection Errors**
   - Check security groups
   - Verify DATABASE_URL format
   - Test RDS connectivity

2. **Application Won't Start**
   - Check CloudWatch logs
   - Verify all dependencies installed
   - Check environment variables

3. **High Memory Usage**
   - Increase instance size
   - Optimize database queries
   - Enable connection pooling

### Support Commands
```bash
# Check EB status
eb status

# View application logs
eb logs

# SSH to instance
eb ssh

# Check Docker status
docker-compose ps
docker-compose logs
```

## Security Best Practices

1. **Secrets Management**
   - Store API keys in AWS Systems Manager Parameter Store
   - Never commit secrets to code

2. **Network Security**
   - RDS in private subnet
   - Application in public subnet with security groups
   - Enable VPC Flow Logs

3. **SSL/TLS**
   - Enable HTTPS with AWS Certificate Manager
   - Force SSL for database connections

4. **Access Control**
   - Use IAM roles, not access keys
   - Principle of least privilege
   - Regular access reviews

---
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
'''
        
        with open('AWS_DEPLOYMENT_GUIDE.md', 'w') as f:
            f.write(guide_content)
        
        logger.info("AWS deployment guide created")
    
    def setup_complete_deployment(self, rds_endpoint, db_name, username, password):
        """Set up complete AWS deployment configuration"""
        logger.info("Setting up complete AWS deployment configuration...")
        
        try:
            # Configure RDS
            self.create_rds_config(rds_endpoint, db_name, username, password)
            
            # Create all deployment files
            self.create_requirements_txt()
            self.create_application_py()
            self.create_dockerfile()
            self.create_docker_compose()
            self.create_elasticbeanstalk_config()
            self.create_environment_template()
            self.create_deployment_scripts()
            self.create_aws_deployment_guide()
            
            logger.info("AWS deployment configuration completed successfully!")
            
            return {
                'status': 'success',
                'rds_config': self.deployment_config['rds'],
                'files_created': [
                    'requirements.txt',
                    'application.py', 
                    'Dockerfile',
                    'docker-compose.yml',
                    '.env.production',
                    'deploy_eb.sh',
                    'deploy_docker.sh',
                    'AWS_DEPLOYMENT_GUIDE.md',
                    '.ebextensions/01_environment.config',
                    '.ebextensions/02_python.config'
                ]
            }
            
        except Exception as e:
            logger.error(f"Deployment configuration failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }

def interactive_aws_setup():
    """Interactive AWS deployment setup"""
    print("GUARDIAN AWS Deployment Configuration")
    print("=" * 45)
    
    config = AWSDeploymentConfig()
    
    print("\nEnter your Amazon RDS connection details:")
    rds_endpoint = input("RDS Endpoint: ").strip()
    db_name = input("Database Name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    result = config.setup_complete_deployment(rds_endpoint, db_name, username, password)
    
    if result['status'] == 'success':
        print(f"\n✅ AWS deployment configuration completed!")
        print(f"📁 Files created: {len(result['files_created'])}")
        print("\nNext steps:")
        print("1. Review AWS_DEPLOYMENT_GUIDE.md")
        print("2. Configure AWS CLI credentials")
        print("3. Choose deployment method (EB, Docker, or ECS)")
        print("4. Run appropriate deployment script")
    else:
        print(f"❌ Configuration failed: {result['error']}")
    
    return result

if __name__ == "__main__":
    interactive_aws_setup()