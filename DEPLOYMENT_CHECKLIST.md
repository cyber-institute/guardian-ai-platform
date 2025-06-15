# GUARDIAN Production Deployment Checklist

## Pre-Migration Requirements ✓

### Database Export Package Created
- [x] Database schema exported (`database_export/table_schema.json`)
- [x] DDL script created (`database_export/create_tables.sql`)
- [x] Data exported to CSV files (13 documents, 9 scoring criteria)
- [x] Import scripts generated (`database_export/import_data.sql`)
- [x] Migration guide provided (`database_export/MIGRATION_GUIDE.md`)

### AWS Infrastructure Required
- [ ] Amazon RDS PostgreSQL instance created
- [ ] Security groups configured (RDS + Application)
- [ ] VPC and subnets configured
- [ ] SSL certificates obtained (AWS Certificate Manager)
- [ ] IAM roles and policies created

## Migration Steps

### Phase 1: RDS Setup
1. **Create RDS Instance**
   - Instance type: db.t3.medium (recommended)
   - Engine: PostgreSQL 15+
   - Multi-AZ: Yes (for production)
   - Storage: 20GB GP3 (expandable)
   - Backup retention: 7 days

2. **Configure Security**
   ```bash
   # Test RDS connection
   python3 rds_setup_helper.py
   ```
   - [ ] Database endpoint accessible
   - [ ] SSL connection verified
   - [ ] User permissions validated

3. **Import Database**
   ```bash
   # Execute DDL
   psql -h RDS_ENDPOINT -U USERNAME -d DATABASE -f database_export/create_tables.sql
   
   # Import data
   psql -h RDS_ENDPOINT -U USERNAME -d DATABASE -f database_export/import_data.sql
   ```
   - [ ] Tables created successfully
   - [ ] Data imported (13 documents, 9 criteria)
   - [ ] Sequences reset correctly

### Phase 2: Application Deployment

#### Option A: AWS Elastic Beanstalk (Recommended)
```bash
# Configure deployment
python3 aws_deployment_config.py

# Deploy application
./deploy_eb.sh
```

#### Option B: Docker Container
```bash
# Build and test locally
docker-compose up

# Deploy to ECS/Fargate
./deploy_docker.sh
```

### Phase 3: Production Configuration

1. **Environment Variables**
   ```
   DATABASE_URL=postgresql://user:pass@rds-endpoint:5432/db?sslmode=require
   ENVIRONMENT=production
   AWS_REGION=us-east-1
   ```

2. **API Keys (AWS Systems Manager)**
   - [ ] OPENAI_API_KEY stored securely
   - [ ] ANTHROPIC_API_KEY stored securely
   - [ ] Google Cloud credentials configured (if using Dialogflow)

3. **Monitoring Setup**
   - [ ] CloudWatch alarms configured
   - [ ] Application logs forwarded
   - [ ] Database performance monitoring enabled
   - [ ] Health check endpoints responding

## Post-Deployment Verification

### Application Health
- [ ] Main application loads (`https://your-domain.com`)
- [ ] Database connectivity verified
- [ ] All document scoring frameworks operational:
  - [ ] AI Cybersecurity scoring
  - [ ] Quantum Cybersecurity scoring  
  - [ ] AI Ethics scoring
  - [ ] Quantum Ethics scoring
- [ ] Document upload and processing working
- [ ] Multi-LLM ensemble analysis functional

### Performance Validation
- [ ] Response times < 3 seconds for document analysis
- [ ] Database queries optimized
- [ ] Memory usage within limits
- [ ] CPU utilization normal

### Security Verification
- [ ] HTTPS enforced
- [ ] Database connections encrypted
- [ ] No sensitive data in logs
- [ ] Security groups properly configured
- [ ] No public database access

## Estimated Costs (Monthly)

| Service | Instance Type | Estimated Cost |
|---------|---------------|----------------|
| RDS PostgreSQL | db.t3.medium | $35 |
| Elastic Beanstalk | t3.medium | $25 |
| Application Load Balancer | - | $18 |
| Data Transfer | ~100GB | $9 |
| CloudWatch | Standard | $5 |
| **Total** | | **~$92/month** |

## Rollback Plan

### If Migration Fails
1. Keep Replit environment active during transition
2. Update DNS to point back to Replit
3. Restore from RDS backup if needed

### Emergency Contacts
- AWS Support: [Account-specific]
- Database Admin: [Your team]
- Application Owner: [Your team]

## Success Criteria

### Technical Metrics
- [ ] 99.9% uptime
- [ ] < 2 second average response time
- [ ] Zero data loss during migration
- [ ] All 13 documents accessible and scoring correctly

### Business Metrics
- [ ] All assessment frameworks operational
- [ ] Document analysis accuracy maintained
- [ ] User experience equivalent or improved
- [ ] Cost within budget ($100/month target)

## Next Steps After Deployment

1. **Optimization**
   - Monitor performance for 1 week
   - Optimize database queries based on CloudWatch insights
   - Right-size instances based on actual usage

2. **Enhanced Features**
   - Configure auto-scaling
   - Set up automated backups
   - Implement blue-green deployment pipeline

3. **Monitoring & Maintenance**
   - Schedule regular security updates
   - Monitor cost optimization opportunities
   - Review and update disaster recovery procedures

---

**Migration Completion Date:** _______________  
**Verified By:** _______________  
**Production Ready:** ✓ / ✗