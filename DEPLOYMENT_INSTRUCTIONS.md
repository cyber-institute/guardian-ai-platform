# GUARDIAN AWS Deployment - Complete Step-by-Step Instructions

## Overview
This guide provides complete instructions for migrating your GUARDIAN application from Replit to Amazon Web Services (AWS) with RDS PostgreSQL database.

## Prerequisites Checklist

### Required Accounts & Tools
- [ ] AWS Account with billing configured
- [ ] AWS CLI installed and configured
- [ ] PostgreSQL client (`psql`) installed locally
- [ ] Docker Desktop installed (optional, for containerized deployment)
- [ ] Git repository for code management

### Local Setup Commands
```bash
# Install AWS CLI (if not installed)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

# Install PostgreSQL client
sudo apt-get update && sudo apt-get install -y postgresql-client

# Verify installations
aws --version
psql --version
```

## Phase 1: Database Migration to RDS

### Step 1.1: Create RDS Instance
```bash
# Create RDS PostgreSQL instance via AWS CLI
aws rds create-db-instance \
    --db-instance-identifier guardian-production-db \
    --db-instance-class db.t3.medium \
    --engine postgres \
    --engine-version 15.4 \
    --master-username guardianuser \
    --master-user-password 'YourSecurePassword123!' \
    --allocated-storage 20 \
    --storage-type gp3 \
    --vpc-security-group-ids sg-xxxxxxxxx \
    --db-subnet-group-name default \
    --backup-retention-period 7 \
    --multi-az \
    --storage-encrypted \
    --deletion-protection

# Wait for instance to be available (5-10 minutes)
aws rds describe-db-instances --db-instance-identifier guardian-production-db --query 'DBInstances[0].DBInstanceStatus'
```

### Step 1.2: Configure Security Groups
```bash
# Create security group for RDS
aws ec2 create-security-group \
    --group-name guardian-rds-sg \
    --description "Security group for GUARDIAN RDS instance"

# Get security group ID
RDS_SG_ID=$(aws ec2 describe-security-groups --group-names guardian-rds-sg --query 'SecurityGroups[0].GroupId' --output text)

# Allow PostgreSQL access from application security group
aws ec2 authorize-security-group-ingress \
    --group-id $RDS_SG_ID \
    --protocol tcp \
    --port 5432 \
    --source-group guardian-app-sg
```

### Step 1.3: Get RDS Endpoint
```bash
# Get RDS endpoint for connection
RDS_ENDPOINT=$(aws rds describe-db-instances \
    --db-instance-identifier guardian-production-db \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text)

echo "RDS Endpoint: $RDS_ENDPOINT"
```

### Step 1.4: Test Database Connection
```bash
# Test connection to RDS instance
python3 rds_setup_helper.py
# Enter the RDS endpoint, database name, username, and password when prompted
```

### Step 1.5: Import Database Schema and Data
```bash
# Navigate to database export directory
cd database_export

# Create database structure
psql -h $RDS_ENDPOINT -U guardianuser -d postgres -f create_tables.sql

# Import data
psql -h $RDS_ENDPOINT -U guardianuser -d postgres -f import_data.sql

# Verify import
psql -h $RDS_ENDPOINT -U guardianuser -d postgres -c "
SELECT 
    schemaname, 
    tablename, 
    n_tup_ins as row_count 
FROM pg_stat_user_tables 
ORDER BY tablename;"
```

Expected output:
```
 schemaname |   tablename    | row_count 
------------+----------------+-----------
 public     | assessments    |         0
 public     | documents      |        13
 public     | scoring_criteria|         9
```

## Phase 2: Application Deployment

### Option A: AWS Elastic Beanstalk (Recommended)

#### Step 2A.1: Install EB CLI
```bash
pip install awsebcli
eb --version
```

#### Step 2A.2: Configure Deployment
```bash
# Configure AWS deployment with RDS connection
python3 aws_deployment_config.py
# Enter your RDS endpoint, database name, username, and password
```

#### Step 2A.3: Initialize Elastic Beanstalk
```bash
# Initialize EB application
eb init guardian-ai-assessment --region us-east-1 --platform python-3.11

# Create production environment
eb create production \
    --instance-type t3.medium \
    --envvars DATABASE_URL=postgresql://guardianuser:YourSecurePassword123!@$RDS_ENDPOINT:5432/postgres?sslmode=require
```

#### Step 2A.4: Deploy Application
```bash
# Deploy to Elastic Beanstalk
eb deploy production

# Check deployment status
eb status

# View application URL
eb open
```

### Option B: Docker Container Deployment

#### Step 2B.1: Build Docker Image
```bash
# Build Docker image
docker build -t guardian-ai:latest .

# Test locally
docker run -p 8501:8501 \
    -e DATABASE_URL=postgresql://guardianuser:YourSecurePassword123!@$RDS_ENDPOINT:5432/postgres?sslmode=require \
    guardian-ai:latest
```

#### Step 2B.2: Deploy to AWS ECS
```bash
# Create ECR repository
aws ecr create-repository --repository-name guardian-ai

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Tag and push image
docker tag guardian-ai:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/guardian-ai:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/guardian-ai:latest

# Create ECS cluster and service (via AWS Console or CLI)
```

## Phase 3: Production Configuration

### Step 3.1: Environment Variables
```bash
# Set environment variables in Elastic Beanstalk
eb setenv \
    DATABASE_URL=postgresql://guardianuser:YourSecurePassword123!@$RDS_ENDPOINT:5432/postgres?sslmode=require \
    ENVIRONMENT=production \
    AWS_REGION=us-east-1
```

### Step 3.2: Configure SSL Certificate
```bash
# Request SSL certificate
aws acm request-certificate \
    --domain-name guardian.yourdomain.com \
    --validation-method DNS \
    --region us-east-1

# Configure load balancer to use SSL (via AWS Console)
```

### Step 3.3: Set Up API Keys (Optional)
```bash
# Store API keys in Systems Manager Parameter Store
aws ssm put-parameter \
    --name "/guardian/openai-api-key" \
    --value "your-openai-api-key" \
    --type "SecureString"

aws ssm put-parameter \
    --name "/guardian/anthropic-api-key" \
    --value "your-anthropic-api-key" \
    --type "SecureString"
```

## Phase 4: Monitoring and Verification

### Step 4.1: CloudWatch Setup
```bash
# Create CloudWatch alarms
aws cloudwatch put-metric-alarm \
    --alarm-name "GUARDIAN-High-CPU" \
    --alarm-description "High CPU usage" \
    --metric-name CPUUtilization \
    --namespace AWS/EC2 \
    --statistic Average \
    --period 300 \
    --threshold 80 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 2
```

### Step 4.2: Health Check Verification
```bash
# Test application endpoints
curl -f https://your-guardian-url.com/health
curl -f https://your-guardian-url.com

# Check database connectivity
psql -h $RDS_ENDPOINT -U guardianuser -d postgres -c "SELECT COUNT(*) FROM documents;"
```

### Step 4.3: Functional Testing
Access your deployed application and verify:

1. **Document Repository**: Navigate to "All Documents" tab
   - Verify all 13 documents are displayed
   - Test document scoring functionality
   - Check all scoring frameworks (AI Cybersecurity, Quantum Cybersecurity, AI Ethics, Quantum Ethics)

2. **Scoring System**: 
   - Click on individual document scores
   - Verify modal popups show detailed analysis
   - Test different view modes (Compact, Grid, Minimal)

3. **Upload System**: Test document upload and processing

## Phase 5: Performance Optimization

### Step 5.1: Database Optimization
```sql
-- Connect to RDS and optimize
psql -h $RDS_ENDPOINT -U guardianuser -d postgres

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_documents_topic ON documents(topic);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at);
CREATE INDEX IF NOT EXISTS idx_assessments_document_id ON assessments(document_id);

-- Analyze tables
ANALYZE documents;
ANALYZE assessments;
ANALYZE scoring_criteria;
```

### Step 5.2: Application Scaling
```bash
# Configure auto-scaling for Elastic Beanstalk
eb config

# Add the following to the configuration:
# option_settings:
#   aws:autoscaling:asg:
#     MinSize: 1
#     MaxSize: 4
#   aws:autoscaling:trigger:
#     MeasureName: CPUUtilization
#     Unit: Percent
#     UpperThreshold: 70
#     LowerThreshold: 20
```

## Troubleshooting Guide

### Common Issues and Solutions

#### Database Connection Issues
```bash
# Test RDS connectivity
telnet $RDS_ENDPOINT 5432

# Check security groups
aws ec2 describe-security-groups --group-ids $RDS_SG_ID

# Verify RDS status
aws rds describe-db-instances --db-instance-identifier guardian-production-db
```

#### Application Deployment Issues
```bash
# Check EB logs
eb logs

# SSH to instance
eb ssh

# Check application status
sudo systemctl status web
```

#### Performance Issues
```bash
# Monitor RDS performance
aws rds describe-db-instances --db-instance-identifier guardian-production-db --query 'DBInstances[0].DBInstanceStatus'

# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS \
    --metric-name CPUUtilization \
    --dimensions Name=DBInstanceIdentifier,Value=guardian-production-db \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-01T23:59:59Z \
    --period 3600 \
    --statistics Average
```

## Cost Monitoring

### Expected Monthly Costs
- **RDS db.t3.medium**: ~$35/month
- **Elastic Beanstalk t3.medium**: ~$25/month  
- **Application Load Balancer**: ~$18/month
- **Data Transfer**: ~$9/month
- **CloudWatch**: ~$5/month
- **Total**: ~$92/month

### Cost Optimization Commands
```bash
# Monitor costs
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics UnblendedCost

# Set up cost alerts
aws budgets create-budget \
    --account-id 123456789012 \
    --budget file://budget.json
```

## Backup and Recovery

### Automated Backups
```bash
# Verify RDS backup configuration
aws rds describe-db-instances \
    --db-instance-identifier guardian-production-db \
    --query 'DBInstances[0].BackupRetentionPeriod'

# Create manual snapshot
aws rds create-db-snapshot \
    --db-snapshot-identifier guardian-production-snapshot-$(date +%Y%m%d) \
    --db-instance-identifier guardian-production-db
```

### Application Backup
```bash
# Create application version backup
eb appversion

# Save configuration
eb config save production --cfg production-config
```

## Post-Deployment Checklist

- [ ] RDS instance running and accessible
- [ ] Database schema and data imported successfully
- [ ] Application deployed and accessible via HTTPS
- [ ] All 13 documents displaying correctly
- [ ] Scoring systems functional across all frameworks
- [ ] SSL certificate configured and working
- [ ] CloudWatch monitoring enabled
- [ ] Backup strategy implemented
- [ ] Cost monitoring configured
- [ ] Performance baselines established

## Support and Maintenance

### Regular Maintenance Tasks
```bash
# Weekly health check
curl -f https://your-guardian-url.com/health

# Monthly cost review
aws ce get-cost-and-usage --time-period Start=$(date -d '1 month ago' +%Y-%m-01),End=$(date +%Y-%m-01) --granularity MONTHLY --metrics UnblendedCost

# Quarterly security updates
eb deploy production
```

### Emergency Procedures
```bash
# Quick rollback to previous version
eb deploy --version-label previous-version

# Scale down for cost savings
eb scale 0

# Database failover (if Multi-AZ enabled)
aws rds reboot-db-instance --db-instance-identifier guardian-production-db --force-failover
```

---

**Deployment completed successfully!** Your GUARDIAN application is now running on AWS with production-grade infrastructure.

For ongoing support:
- Monitor CloudWatch dashboards
- Review monthly cost reports  
- Maintain regular backups
- Keep dependencies updated

**Emergency Contact**: Keep this deployment guide accessible for troubleshooting and maintenance procedures.