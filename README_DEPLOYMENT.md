# GUARDIAN AWS Migration Package

Complete deployment package for migrating GUARDIAN from Replit to Amazon Web Services with RDS PostgreSQL.

## Quick Start

### One-Command Deployment
```bash
# Complete automated deployment
./deploy_complete.sh
```

### Manual Step-by-Step
```bash
# 1. Export database
python3 simple_db_export.py

# 2. Test RDS connection
python3 rds_setup_helper.py

# 3. Configure AWS deployment
python3 aws_deployment_config.py

# 4. Deploy with Elastic Beanstalk
./deploy_eb.sh
```

## Package Contents

### Database Migration
- `database_export/` - Complete database export (13 documents, 9 criteria)
- `simple_db_export.py` - Database export script
- `export_to_rds.py` - Advanced export with pg_dump
- `rds_setup_helper.py` - RDS connection testing

### AWS Deployment
- `aws_deployment_config.py` - AWS configuration generator
- `deploy_complete.sh` - Full automation script
- `Dockerfile` - Container deployment option
- `docker-compose.yml` - Local testing
- `requirements.txt` - Python dependencies

### Documentation
- `DEPLOYMENT_INSTRUCTIONS.md` - Complete step-by-step guide
- `DEPLOYMENT_CHECKLIST.md` - Verification checklist
- `AWS_DEPLOYMENT_GUIDE.md` - AWS-specific instructions

## Prerequisites

1. **AWS Account** with billing configured
2. **AWS CLI** installed and configured
3. **PostgreSQL client** (`psql`) installed
4. **Python 3.11+** with required packages

### Quick Setup
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Configure AWS
aws configure

# Install PostgreSQL client
sudo apt-get install postgresql-client

# Install Python dependencies
pip install awsebcli psycopg2-binary boto3 flask
```

## Current Database Status

✅ **Export Completed Successfully**
- 13 documents exported with full content and metadata
- 9 scoring criteria definitions
- All framework scoring data preserved
- Schema and constraints exported

## Deployment Options

### Option 1: Elastic Beanstalk (Recommended)
- **Cost**: ~$78/month
- **Features**: Auto-scaling, load balancing, monitoring
- **Setup**: `./deploy_complete.sh`

### Option 2: Docker Container
- **Cost**: ~$45/month (ECS Fargate)
- **Features**: Containerized, portable
- **Setup**: `docker-compose up`

### Option 3: Manual AWS Setup
- **Cost**: Variable
- **Features**: Full control
- **Setup**: Follow `DEPLOYMENT_INSTRUCTIONS.md`

## Expected Costs (Monthly)

| Service | Instance | Cost |
|---------|----------|------|
| RDS PostgreSQL | db.t3.medium | $35 |
| Elastic Beanstalk | t3.medium | $25 |
| Load Balancer | ALB | $18 |
| Data Transfer | 100GB | $9 |
| CloudWatch | Standard | $5 |
| **Total** | | **$92** |

## Verification Steps

After deployment, verify:

1. **Application Access**
   ```bash
   curl -f https://your-app-url.com
   ```

2. **Database Connectivity**
   ```bash
   psql -h RDS_ENDPOINT -U guardianuser -d postgres -c "SELECT COUNT(*) FROM documents;"
   ```

3. **Functional Testing**
   - Navigate to "All Documents" tab
   - Verify 13 documents display correctly
   - Test scoring functionality across all frameworks
   - Check modal popups for detailed analysis

## Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check security groups
aws ec2 describe-security-groups

# Test connectivity
telnet RDS_ENDPOINT 5432
```

**Application Won't Start**
```bash
# Check logs
eb logs

# Verify environment variables
eb printenv
```

**High Costs**
```bash
# Monitor usage
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-01-31

# Right-size instances
eb scale 1  # Reduce to single instance
```

## Support Commands

```bash
# Application management
eb status                    # Check app status
eb deploy                    # Deploy updates
eb logs                      # View application logs
eb ssh                       # SSH to instance

# Database management
psql $DATABASE_URL          # Connect to database
aws rds describe-db-instances # Check RDS status

# Monitoring
aws cloudwatch get-metric-statistics # View metrics
aws ce get-cost-and-usage    # Check costs
```

## Security Notes

- All database connections use SSL encryption
- API keys stored in AWS Systems Manager Parameter Store
- Security groups configured with minimal required access
- RDS instance in private subnet with backup enabled

## Next Steps After Deployment

1. **Configure Custom Domain** (Optional)
   - Request SSL certificate via AWS Certificate Manager
   - Update Route 53 DNS records
   - Configure load balancer HTTPS

2. **Optimize Performance**
   - Monitor CloudWatch metrics
   - Adjust instance sizes based on usage
   - Configure auto-scaling policies

3. **Set Up Monitoring**
   - Create CloudWatch dashboards
   - Configure cost alerts
   - Set up notification alarms

## Files Generated During Deployment

- `DEPLOYMENT_SUMMARY.md` - Post-deployment summary
- `.env.production` - Production environment configuration
- `.elasticbeanstalk/` - EB configuration files
- `application.py` - AWS-compatible application entry point

## Emergency Procedures

### Rollback to Replit
```bash
# If AWS deployment fails, keep Replit active
# Update DNS to point back to Replit domain
# Restore from RDS backup if needed
```

### Scale Down for Cost Savings
```bash
eb scale 0                   # Stop all instances
aws rds stop-db-instance --db-instance-identifier guardian-production-db
```

### Quick Recovery
```bash
eb deploy --version-label previous-version  # Rollback app
aws rds start-db-instance --db-instance-identifier guardian-production-db
```

---

**Ready for Production Deployment**

Your GUARDIAN application is ready for AWS migration with complete database export, automated deployment scripts, and comprehensive documentation.

Execute `./deploy_complete.sh` to begin automated deployment to AWS.