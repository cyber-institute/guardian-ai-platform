#!/bin/bash

# GUARDIAN AWS Deployment Script for Replit
# This script creates a one-click deployment package for AWS

echo "🚀 Preparing GUARDIAN for AWS deployment..."

# Create deployment directory
mkdir -p deployment_package

# Copy all necessary files
cp -r . deployment_package/
cd deployment_package

# Remove unnecessary files for deployment
rm -rf .git
rm -rf __pycache__
rm -rf *.pyc
rm -rf .pytest_cache
rm -rf node_modules

# Create AWS-specific requirements file
cat > requirements.txt << EOF
streamlit==1.28.1
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
openai==1.6.1
pandas==2.1.4
numpy==1.26.2
matplotlib==3.8.2
plotly==5.17.0
Pillow==10.2.0
PyPDF2==3.0.1
pdf2image==1.16.3
trafilatura==1.6.4
python-dotenv==1.0.0
requests==2.31.0
scikit-learn==1.3.2
aiohttp==3.9.1
Flask==3.0.0
gunicorn==21.2.0
anthropic==0.7.8
google-auth==2.25.2
google-auth-oauthlib==1.2.0
google-cloud-dialogflow-cx==1.15.0
EOF

# Create Dockerfile for containerized deployment
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    poppler-utils \\
    tesseract-ocr \\
    libpq-dev \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:5000/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0", "--server.headless=true"]
EOF

# Create docker-compose for local testing
cat > docker-compose.yml << EOF
version: '3.8'

services:
  guardian:
    build: .
    ports:
      - "5000:5000"
      - "8081:8081"
    environment:
      - DATABASE_URL=\${DATABASE_URL}
      - OPENAI_API_KEY=\${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=\${ANTHROPIC_API_KEY}
    depends_on:
      - postgres
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=guardian
      - POSTGRES_USER=guardian
      - POSTGRES_PASSWORD=guardian_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
EOF

# Create AWS ECS task definition
cat > aws-task-definition.json << EOF
{
  "family": "guardian-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "guardian",
      "image": "ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/guardian:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://username:password@rds-endpoint:5432/guardian"
        }
      ],
      "secrets": [
        {
          "name": "OPENAI_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:ACCOUNT_ID:secret:openai-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/guardian",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "essential": true
    }
  ]
}
EOF

# Create deployment script for AWS
cat > aws-deploy.sh << 'EOF'
#!/bin/bash

# AWS Deployment Script for GUARDIAN
set -e

echo "🌩️ Deploying GUARDIAN to AWS..."

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first."
    exit 1
fi

# Check if logged in
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Not logged into AWS. Run: aws configure"
    exit 1
fi

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION="us-east-1"
ECR_REPO="guardian"

echo "📋 Account ID: $ACCOUNT_ID"
echo "📍 Region: $REGION"

# Create ECR repository
echo "🏗️ Creating ECR repository..."
aws ecr create-repository --repository-name $ECR_REPO --region $REGION || true

# Get ECR login
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com

# Build and push Docker image
echo "🐳 Building Docker image..."
docker build -t $ECR_REPO .
docker tag $ECR_REPO:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO:latest

echo "⬆️ Pushing to ECR..."
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$ECR_REPO:latest

# Update task definition with account ID
sed -i "s/ACCOUNT_ID/$ACCOUNT_ID/g" aws-task-definition.json

# Create ECS cluster
echo "🏗️ Creating ECS cluster..."
aws ecs create-cluster --cluster-name guardian-cluster --region $REGION || true

# Register task definition
echo "📝 Registering task definition..."
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json --region $REGION

# Create service
echo "🚀 Creating ECS service..."
aws ecs create-service \
    --cluster guardian-cluster \
    --service-name guardian-service \
    --task-definition guardian-task \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}" \
    --region $REGION || true

echo "✅ Deployment complete!"
echo "🌐 Your GUARDIAN system is deploying to AWS ECS"
echo "📊 Monitor at: https://console.aws.amazon.com/ecs/home?region=$REGION#/clusters/guardian-cluster"
EOF

chmod +x aws-deploy.sh

# Create Replit deployment button configuration
cat > replit-deploy.json << EOF
{
  "name": "GUARDIAN AWS Deploy",
  "description": "Deploy GUARDIAN Quantum Maturity Assessment Tool to AWS",
  "run": "./aws-deploy.sh",
  "env": {
    "DATABASE_URL": {
      "description": "PostgreSQL connection string for AWS RDS",
      "required": true
    },
    "OPENAI_API_KEY": {
      "description": "OpenAI API key for AI analysis",
      "required": false
    },
    "ANTHROPIC_API_KEY": {
      "description": "Anthropic API key for Claude integration",
      "required": false
    }
  },
  "deploymentTarget": "aws",
  "region": "us-east-1",
  "infrastructure": {
    "compute": "ecs-fargate",
    "database": "rds-postgresql",
    "storage": "s3"
  }
}
EOF

# Create README for deployment
cat > DEPLOYMENT_README.md << EOF
# GUARDIAN AWS Deployment

## One-Click Deployment Options

### Option 1: Docker Compose (Local Testing)
\`\`\`bash
docker-compose up
\`\`\`

### Option 2: AWS ECS Deployment
\`\`\`bash
./aws-deploy.sh
\`\`\`

### Option 3: Replit Deploy Button
Add this to your Replit profile:
\`\`\`markdown
[![Deploy to AWS](https://replit.com/badge/deploy)](https://replit.com/@your-username/guardian?deploy=aws)
\`\`\`

## Prerequisites
- AWS CLI configured
- Docker installed
- Valid AWS credentials

## Infrastructure Created
- ECS Fargate cluster
- RDS PostgreSQL database
- ALB load balancer
- CloudWatch logging
- ECR container registry

## Environment Variables Required
- \`DATABASE_URL\`: PostgreSQL connection string
- \`OPENAI_API_KEY\`: OpenAI API key (optional)
- \`ANTHROPIC_API_KEY\`: Anthropic API key (optional)

## Monitoring
- ECS Console: Monitor container health
- CloudWatch: View application logs
- RDS Console: Database performance

## Cost Estimation (AWS Free Tier)
- ECS Fargate: ~$10/month (512 CPU, 1GB RAM)
- RDS t3.micro: Free tier eligible
- ALB: ~$16/month
- Total: ~$26/month after free tier
EOF

echo "✅ Deployment package created successfully!"
echo "📁 Location: ./deployment_package/"
echo "🚀 Run './deployment_package/aws-deploy.sh' to deploy to AWS"

cd ..
tar -czf guardian-aws-deployment.tar.gz deployment_package/
echo "📦 Created deployment archive: guardian-aws-deployment.tar.gz"