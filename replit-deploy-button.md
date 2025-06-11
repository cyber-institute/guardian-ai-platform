# Replit Deploy Button Configuration

## For Your Replit Profile

Add this to your Replit bio or project description to enable one-click AWS deployment:

```markdown
[![Deploy GUARDIAN to AWS](https://img.shields.io/badge/Deploy%20to%20AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://replit.com/@your-username/guardian-quantum-assessment?v=1)
```

## Alternative Button Styles

### Simple Deploy Button
```markdown
[![Deploy](https://deploy-button.vercel.app/deploy.svg)](https://replit.com/@your-username/guardian-quantum-assessment)
```

### Custom GUARDIAN Button
```markdown
[![Deploy GUARDIAN](https://img.shields.io/badge/🛡️%20Deploy%20GUARDIAN-blue?style=for-the-badge)](https://replit.com/@your-username/guardian-quantum-assessment)
```

## Setup Instructions

1. **Fork this Replit** to your account
2. **Add the badge** to your profile or project README
3. **Configure secrets** in your Replit environment:
   - `DATABASE_URL` (required for AWS RDS)
   - `OPENAI_API_KEY` (optional)
   - `ANTHROPIC_API_KEY` (optional)

## When Someone Clicks the Button

The deployment process will:
1. Clone the GUARDIAN repository
2. Run the automated deployment script
3. Create AWS infrastructure (ECS, RDS, ALB)
4. Deploy the containerized application
5. Provide the live URL

## Required AWS Permissions

The user clicking deploy needs:
- AWS CLI configured
- ECS full access
- RDS create permissions
- ECR repository access
- CloudWatch logs access

## Cost Information

Display this near your deploy button:
```markdown
**AWS Free Tier Eligible** - Estimated cost: $0-26/month
- RDS t3.micro: Free for 12 months
- ECS Fargate: 20GB-hours/month free
- ALB: ~$16/month (only paid component)
```