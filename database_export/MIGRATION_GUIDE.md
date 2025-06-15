# GUARDIAN Database Migration to Amazon RDS

## Overview
This package contains your complete GUARDIAN database export for migration to Amazon RDS PostgreSQL.

## Files Included
- `table_schema.json` - Complete database schema
- `create_tables.sql` - DDL script to create tables
- `assessments_data.csv` - Assessments table data
- `documents_data.csv` - Documents table data  
- `scoring_criteria_data.csv` - Scoring criteria data
- `import_data.sql` - Import script for RDS

## Migration Steps

### 1. Prepare RDS Instance
- Create PostgreSQL RDS instance
- Configure security groups for access
- Note endpoint, username, password

### 2. Create Database Structure
```bash
psql -h your-rds-endpoint.amazonaws.com -U your-username -d your-database -f create_tables.sql
```

### 3. Import Data
Upload CSV files to RDS-accessible location, then:
```bash
psql -h your-rds-endpoint.amazonaws.com -U your-username -d your-database -f import_data.sql
```

### 4. Update Application
Set new DATABASE_URL:
```
DATABASE_URL=postgresql://username:password@your-rds-endpoint.amazonaws.com:5432/your-database?sslmode=require
```

### 5. Verify Migration
```sql
-- Check table counts
SELECT schemaname, tablename, n_tup_ins as rows
FROM pg_stat_user_tables;
```

## Important Notes
- Ensure SSL is enabled
- Configure proper security groups
- Set up automated backups
- Monitor performance metrics

---
Generated: 2025-06-15 05:57:04
