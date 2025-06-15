#!/bin/bash
# Complete GUARDIAN Deployment Script
# Automates the full migration from Replit to AWS RDS

set -e  # Exit on any error

echo "=============================================="
echo "GUARDIAN Complete AWS Deployment Script"
echo "=============================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        error "AWS CLI not found. Please install AWS CLI first."
    fi
    
    # Check psql
    if ! command -v psql &> /dev/null; then
        error "PostgreSQL client (psql) not found. Please install postgresql-client."
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured. Run 'aws configure' first."
    fi
    
    log "Prerequisites check passed!"
}

# Get user inputs
get_deployment_config() {
    log "Gathering deployment configuration..."
    
    echo -e "${BLUE}Enter deployment configuration:${NC}"
    
    read -p "RDS Instance Identifier (default: guardian-production-db): " RDS_IDENTIFIER
    RDS_IDENTIFIER=${RDS_IDENTIFIER:-guardian-production-db}
    
    read -p "Database Master Username (default: guardianuser): " DB_USERNAME
    DB_USERNAME=${DB_USERNAME:-guardianuser}
    
    read -s -p "Database Master Password: " DB_PASSWORD
    echo
    
    if [ -z "$DB_PASSWORD" ]; then
        error "Database password cannot be empty"
    fi
    
    read -p "AWS Region (default: us-east-1): " AWS_REGION
    AWS_REGION=${AWS_REGION:-us-east-1}
    
    read -p "Application Name (default: guardian-ai-assessment): " APP_NAME
    APP_NAME=${APP_NAME:-guardian-ai-assessment}
    
    log "Configuration collected successfully"
}

# Create RDS instance
create_rds_instance() {
    log "Creating RDS PostgreSQL instance..."
    
    # Check if instance already exists
    if aws rds describe-db-instances --db-instance-identifier "$RDS_IDENTIFIER" --region "$AWS_REGION" &> /dev/null; then
        warn "RDS instance $RDS_IDENTIFIER already exists. Skipping creation."
        return 0
    fi
    
    # Get default VPC and subnet group
    DEFAULT_VPC=$(aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --query 'Vpcs[0].VpcId' --output text --region "$AWS_REGION")
    
    if [ "$DEFAULT_VPC" == "None" ]; then
        error "No default VPC found. Please create a VPC first."
    fi
    
    # Create security group for RDS
    RDS_SG_ID=$(aws ec2 create-security-group \
        --group-name "${APP_NAME}-rds-sg" \
        --description "Security group for ${APP_NAME} RDS instance" \
        --vpc-id "$DEFAULT_VPC" \
        --region "$AWS_REGION" \
        --query 'GroupId' --output text 2>/dev/null || \
        aws ec2 describe-security-groups \
            --group-names "${APP_NAME}-rds-sg" \
            --query 'SecurityGroups[0].GroupId' \
            --output text --region "$AWS_REGION")
    
    # Allow PostgreSQL access from anywhere (will be restricted later)
    aws ec2 authorize-security-group-ingress \
        --group-id "$RDS_SG_ID" \
        --protocol tcp \
        --port 5432 \
        --cidr 0.0.0.0/0 \
        --region "$AWS_REGION" 2>/dev/null || true
    
    log "Creating RDS instance (this may take 5-10 minutes)..."
    
    aws rds create-db-instance \
        --db-instance-identifier "$RDS_IDENTIFIER" \
        --db-instance-class db.t3.medium \
        --engine postgres \
        --engine-version 15.4 \
        --master-username "$DB_USERNAME" \
        --master-user-password "$DB_PASSWORD" \
        --allocated-storage 20 \
        --storage-type gp3 \
        --vpc-security-group-ids "$RDS_SG_ID" \
        --backup-retention-period 7 \
        --storage-encrypted \
        --region "$AWS_REGION" \
        --publicly-accessible
    
    # Wait for instance to be available
    log "Waiting for RDS instance to become available..."
    aws rds wait db-instance-available --db-instance-identifier "$RDS_IDENTIFIER" --region "$AWS_REGION"
    
    log "RDS instance created successfully!"
}

# Get RDS endpoint
get_rds_endpoint() {
    log "Getting RDS endpoint..."
    
    RDS_ENDPOINT=$(aws rds describe-db-instances \
        --db-instance-identifier "$RDS_IDENTIFIER" \
        --region "$AWS_REGION" \
        --query 'DBInstances[0].Endpoint.Address' \
        --output text)
    
    if [ "$RDS_ENDPOINT" == "None" ]; then
        error "Could not retrieve RDS endpoint"
    fi
    
    log "RDS Endpoint: $RDS_ENDPOINT"
}

# Import database
import_database() {
    log "Importing database schema and data..."
    
    DATABASE_URL="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${RDS_ENDPOINT}:5432/postgres?sslmode=require"
    
    # Test connection
    if ! psql "$DATABASE_URL" -c "SELECT 1;" &> /dev/null; then
        error "Cannot connect to RDS instance. Check credentials and security groups."
    fi
    
    # Import schema
    log "Creating database tables..."
    psql "$DATABASE_URL" -f database_export/create_tables.sql
    
    # Import data
    log "Importing data..."
    psql "$DATABASE_URL" -f database_export/import_data.sql
    
    # Verify import
    log "Verifying data import..."
    DOCUMENT_COUNT=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM documents;" | xargs)
    CRITERIA_COUNT=$(psql "$DATABASE_URL" -t -c "SELECT COUNT(*) FROM scoring_criteria;" | xargs)
    
    log "Import verification: $DOCUMENT_COUNT documents, $CRITERIA_COUNT scoring criteria"
    
    if [ "$DOCUMENT_COUNT" -lt 10 ]; then
        warn "Document count seems low. Please verify import manually."
    fi
}

# Deploy to Elastic Beanstalk
deploy_to_eb() {
    log "Deploying application to Elastic Beanstalk..."
    
    # Install EB CLI if not present
    if ! command -v eb &> /dev/null; then
        log "Installing Elastic Beanstalk CLI..."
        pip install awsebcli
    fi
    
    # Create environment configuration
    DATABASE_URL="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${RDS_ENDPOINT}:5432/postgres?sslmode=require"
    
    # Configure EB deployment
    python3 aws_deployment_config.py --rds-endpoint "$RDS_ENDPOINT" --db-name postgres --username "$DB_USERNAME" --password "$DB_PASSWORD" --non-interactive
    
    # Initialize EB if not already done
    if [ ! -d ".elasticbeanstalk" ]; then
        log "Initializing Elastic Beanstalk application..."
        eb init "$APP_NAME" --region "$AWS_REGION" --platform python-3.11
    fi
    
    # Create production environment
    if ! eb status production &> /dev/null; then
        log "Creating production environment..."
        eb create production \
            --instance-type t3.medium \
            --envvars DATABASE_URL="$DATABASE_URL",ENVIRONMENT=production,AWS_REGION="$AWS_REGION"
    else
        log "Production environment exists. Deploying update..."
        eb setenv DATABASE_URL="$DATABASE_URL" ENVIRONMENT=production AWS_REGION="$AWS_REGION"
        eb deploy production
    fi
    
    # Get application URL
    APP_URL=$(eb status production | grep "CNAME" | awk '{print $2}')
    log "Application deployed at: http://$APP_URL"
}

# Verify deployment
verify_deployment() {
    log "Verifying deployment..."
    
    # Get application URL
    APP_URL=$(eb status production | grep "CNAME" | awk '{print $2}')
    
    if [ -z "$APP_URL" ]; then
        warn "Could not retrieve application URL. Please check EB status manually."
        return 1
    fi
    
    # Test health endpoint
    log "Testing application health..."
    if curl -f "http://$APP_URL/_stcore/health" &> /dev/null; then
        log "Health check passed!"
    else
        warn "Health check failed. Application may still be starting up."
    fi
    
    # Test database connectivity
    log "Testing database connectivity..."
    DATABASE_URL="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${RDS_ENDPOINT}:5432/postgres?sslmode=require"
    if psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM documents;" &> /dev/null; then
        log "Database connectivity verified!"
    else
        warn "Database connectivity test failed."
    fi
}

# Setup monitoring
setup_monitoring() {
    log "Setting up CloudWatch monitoring..."
    
    # Create CloudWatch alarm for high CPU
    aws cloudwatch put-metric-alarm \
        --alarm-name "${APP_NAME}-High-CPU" \
        --alarm-description "High CPU usage for ${APP_NAME}" \
        --metric-name CPUUtilization \
        --namespace AWS/EC2 \
        --statistic Average \
        --period 300 \
        --threshold 80 \
        --comparison-operator GreaterThanThreshold \
        --evaluation-periods 2 \
        --region "$AWS_REGION" || warn "Could not create CPU alarm"
    
    # Create RDS monitoring alarm
    aws cloudwatch put-metric-alarm \
        --alarm-name "${APP_NAME}-RDS-High-CPU" \
        --alarm-description "High CPU usage for RDS instance" \
        --metric-name CPUUtilization \
        --namespace AWS/RDS \
        --statistic Average \
        --period 300 \
        --threshold 70 \
        --comparison-operator GreaterThanThreshold \
        --evaluation-periods 2 \
        --dimensions Name=DBInstanceIdentifier,Value="$RDS_IDENTIFIER" \
        --region "$AWS_REGION" || warn "Could not create RDS CPU alarm"
    
    log "CloudWatch monitoring configured"
}

# Generate deployment summary
generate_summary() {
    log "Generating deployment summary..."
    
    APP_URL=$(eb status production | grep "CNAME" | awk '{print $2}' 2>/dev/null || echo "Check EB console")
    
    cat > DEPLOYMENT_SUMMARY.md << EOF
# GUARDIAN Deployment Summary

## Deployment Details
- **Date**: $(date)
- **RDS Instance**: $RDS_IDENTIFIER
- **RDS Endpoint**: $RDS_ENDPOINT
- **Application URL**: http://$APP_URL
- **AWS Region**: $AWS_REGION

## Database Information
- **Engine**: PostgreSQL 15.4
- **Instance Class**: db.t3.medium
- **Storage**: 20GB GP3
- **Backup Retention**: 7 days

## Connection Information
\`\`\`
DATABASE_URL=postgresql://${DB_USERNAME}:***@${RDS_ENDPOINT}:5432/postgres?sslmode=require
\`\`\`

## Verification Steps
1. Access application: http://$APP_URL
2. Check "All Documents" tab for 13 documents
3. Test scoring functionality
4. Verify all framework scoring works

## Management Commands
\`\`\`bash
# Check application status
eb status

# View logs
eb logs

# Deploy updates
eb deploy production

# Scale application
eb scale <number-of-instances>
\`\`\`

## Cost Estimate
- RDS db.t3.medium: ~\$35/month
- EB t3.medium: ~\$25/month
- Load Balancer: ~\$18/month
- **Total**: ~\$78/month

## Support
- AWS Console: https://console.aws.amazon.com
- Deployment Guide: DEPLOYMENT_INSTRUCTIONS.md
- Troubleshooting: Check CloudWatch logs
EOF

    log "Deployment summary saved to DEPLOYMENT_SUMMARY.md"
}

# Main execution
main() {
    log "Starting GUARDIAN complete deployment..."
    
    check_prerequisites
    get_deployment_config
    create_rds_instance
    get_rds_endpoint
    import_database
    deploy_to_eb
    verify_deployment
    setup_monitoring
    generate_summary
    
    echo
    echo -e "${GREEN}=============================================="
    echo -e "✅ GUARDIAN DEPLOYMENT COMPLETED SUCCESSFULLY!"
    echo -e "=============================================="
    echo -e "${NC}"
    echo -e "🌐 Application URL: ${BLUE}http://$(eb status production | grep "CNAME" | awk '{print $2}' 2>/dev/null)${NC}"
    echo -e "🗄️  Database: ${BLUE}$RDS_ENDPOINT${NC}"
    echo -e "📊 Monitoring: AWS CloudWatch"
    echo -e "📋 Summary: DEPLOYMENT_SUMMARY.md"
    echo
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Test application functionality"
    echo "2. Configure custom domain (optional)"
    echo "3. Set up SSL certificate"
    echo "4. Configure API keys if needed"
    echo "5. Review monthly costs in AWS Billing"
    echo
}

# Run deployment
main "$@"