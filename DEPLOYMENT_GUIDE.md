# GUARDIAN Private Deployment Guide

## Overview
This guide walks you through deploying GUARDIAN as a private, secure prototype for stakeholder testing and demonstrations.

## Pre-Deployment Checklist

### ✅ Code Preparation
- [x] All functionality tested and working
- [x] Authentication layer implemented
- [x] Requirements.txt updated
- [x] Environment variables configured
- [x] Database connections verified

### ✅ Security Features
- [x] Private access codes implemented
- [x] HTTPS enforcement
- [x] Access logging
- [x] Session management
- [x] Security headers

## Deployment Steps

### 1. Replit Deployment
1. **Click Deploy Button** in Replit interface
2. **Choose Deployment Settings**:
   - Visibility: **Private**
   - Name: `guardian-prototype`
   - Description: "GUARDIAN AI Risk Assessment Platform - Private Prototype"

### 2. Environment Configuration
Ensure these environment variables are set:
```
DATABASE_URL=your_postgres_connection_string
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
```

### 3. Access Control
**Available Access Codes**:
- `guardian-admin` - Full administrator access
- `guardian-demo` - Demo/presentation mode
- `guardian-test` - Testing and development
- `guardian-client` - Client review access

### 4. Post-Deployment Verification
1. Access the deployment URL
2. Test authentication with access codes
3. Verify all features work correctly
4. Test document upload and analysis
5. Confirm chat functionality

## Sharing with Stakeholders

### For Government/Nonprofit Demos
1. Provide deployment URL
2. Share appropriate access code
3. Include brief user guide
4. Schedule demonstration session

### For Client Testing
1. Use `guardian-client` access code
2. Provide sample documents for testing
3. Guide through key features
4. Collect feedback for improvements

## Security Considerations

### Access Monitoring
- All access attempts are logged
- Session information tracked
- User activity monitored

### Data Protection
- HTTPS encryption enforced
- Private deployment (not publicly indexed)
- Secure document upload handling
- Database connection encryption

### Best Practices
- Regularly rotate access codes
- Monitor access logs
- Backup database before major demos
- Test all functionality before stakeholder sessions

## Troubleshooting

### Common Issues
1. **Authentication Not Working**
   - Verify access codes are correct
   - Check session state persistence
   - Clear browser cache if needed

2. **Database Connection Issues**
   - Verify DATABASE_URL environment variable
   - Check PostgreSQL service status
   - Confirm connection string format

3. **API Keys Not Working**
   - Verify ANTHROPIC_API_KEY and OPENAI_API_KEY
   - Check API key permissions
   - Confirm keys are properly set in environment

### Support
For deployment issues or questions:
1. Check logs in Replit deployment dashboard
2. Verify environment variables
3. Test in development environment first
4. Contact system administrator if needed

## Success Metrics

### Deployment Success Indicators
- ✅ HTTPS URL accessible
- ✅ Authentication working
- ✅ All tabs loading correctly
- ✅ Document upload functional
- ✅ ARIA chat operational
- ✅ Database queries executing
- ✅ Scoring algorithms working

### Stakeholder Feedback Areas
- User interface intuitiveness
- Document analysis accuracy
- System performance
- Feature completeness
- Overall value proposition

## Next Steps
After successful private deployment and stakeholder feedback:
1. Incorporate feedback improvements
2. Prepare for wider beta testing
3. Consider production deployment options
4. Plan for scaling and optimization