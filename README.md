# GUARDIAN - AI Risk Analysis Navigator

An advanced AI governance platform leveraging multi-LLM ensemble intelligence for comprehensive technological risk assessment and dynamic document analysis.

## Quick AWS Deployment

### Method 1: One-Click Deployment Script
```bash
chmod +x deploy.sh
./deploy.sh
```

This creates a complete deployment package with:
- Docker containerization
- AWS ECS Fargate configuration  
- RDS PostgreSQL setup
- ECR container registry
- CloudWatch logging

### Method 2: Deploy Button for Replit Profile

Add this badge to your Replit profile to enable one-click AWS deployment:

```markdown
[![Deploy GUARDIAN to AWS](https://img.shields.io/badge/Deploy-AWS-orange?style=for-the-badge&logo=amazon-aws)](https://replit.com/@your-username/guardian-aws-deploy)
```

### Method 3: Direct AWS ECS Deployment

1. Run the deployment script:
```bash
./deploy.sh
cd deployment_package
./aws-deploy.sh
```

2. The script will:
   - Create ECR repository
   - Build and push Docker image
   - Set up ECS Fargate cluster
   - Deploy with load balancer
   - Configure RDS PostgreSQL

## Infrastructure Requirements

### AWS Services Used
- **ECS Fargate**: Serverless container hosting
- **RDS PostgreSQL**: Managed database (Free Tier eligible)
- **ECR**: Container registry
- **Application Load Balancer**: Traffic distribution
- **CloudWatch**: Logging and monitoring
- **Secrets Manager**: API key storage

### Environment Variables
```bash
DATABASE_URL=postgresql://username:password@rds-endpoint:5432/guardian
OPENAI_API_KEY=your-openai-api-key  # Optional
ANTHROPIC_API_KEY=your-anthropic-key  # Optional
GROQ_API_KEY=your-groq-key  # Optional
```

## Cost Estimation (Monthly)
- **Free Tier Eligible**: RDS t3.micro, ECS Fargate 512 CPU/1GB RAM
- **After Free Tier**: ~$26/month total
  - ECS Fargate: ~$10/month
  - Application Load Balancer: ~$16/month
  - RDS: ~$13/month (if upgraded from Free Tier)

## Local Development

### Docker Compose
```bash
cd deployment_package
docker-compose up
```

Accesses GUARDIAN at `http://localhost:5000`

### Native Python
```bash
pip install -r requirements.txt
streamlit run app.py --server.port 5000
```

## Features

- **Multi-LLM Ensemble**: Integrates OpenAI, Anthropic, Groq, and other AI services
- **Patent-Based Scoring**: QCMEA framework and AI Ethics assessment
- **Document Analysis**: PDF ingestion with intelligent metadata extraction
- **Risk Assessment**: Comprehensive AI/Quantum cybersecurity evaluation
- **Interactive Visualizations**: Charts, graphs, and analytics dashboards

## API Integrations

### Primary LLMs
- OpenAI GPT-4 for primary analysis
- Anthropic Claude for ethical reasoning
- Groq for fast inference

### Knowledge Sources  
- Hugging Face models for specialized analysis
- Together AI for open source models
- Local Ollama integration (optional)

## Database Schema

PostgreSQL tables automatically created:
- `documents`: Document metadata and content
- `scoring_results`: AI/Quantum assessment scores
- `user_sessions`: Analytics and usage tracking

## Monitoring

### CloudWatch Dashboards
- Container health metrics
- Database performance
- API response times
- Error rate tracking

### Application Logs
- Document processing status
- LLM API usage
- Security events
- Performance metrics

## Security

- API keys stored in AWS Secrets Manager
- VPC isolation with private subnets
- SSL/TLS encryption in transit
- Database encryption at rest
- IAM roles for least privilege access

## Support

For deployment issues or questions, check the AWS CloudWatch logs or contact support through your Replit workspace.