#!/usr/bin/env python3
"""
Simple Database Export for GUARDIAN RDS Migration
Creates a complete export package for migrating to Amazon RDS
"""

import os
import json
import csv
import logging
from datetime import datetime
from pathlib import Path
from utils.database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleDBExporter:
    def __init__(self):
        self.db = DatabaseManager()
        self.export_dir = Path('./database_export')
        self.export_dir.mkdir(exist_ok=True)
        
    def export_table_schema(self):
        """Export table schema information"""
        logger.info("Exporting table schema...")
        
        schema_query = """
        SELECT 
            table_name,
            column_name,
            data_type,
            is_nullable,
            column_default,
            ordinal_position
        FROM information_schema.columns 
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """
        
        schema_data = self.db.execute_query(schema_query)
        
        if schema_data:
            schema_file = self.export_dir / 'table_schema.json'
            with open(schema_file, 'w') as f:
                json.dump(schema_data, f, indent=2, default=str)
            logger.info(f"Schema exported to {schema_file}")
            return schema_data
        return []
    
    def export_table_data(self, table_name):
        """Export data from a specific table"""
        logger.info(f"Exporting data from table: {table_name}")
        
        # Get table data
        query = f"SELECT * FROM {table_name} ORDER BY id"
        data = self.db.execute_query(query)
        
        if data:
            csv_file = self.export_dir / f'{table_name}_data.csv'
            
            # Write to CSV
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                if data:
                    writer = csv.DictWriter(f, fieldnames=data[0].keys())
                    writer.writeheader()
                    
                    for row in data:
                        # Handle special data types
                        clean_row = {}
                        for key, value in row.items():
                            if value is None:
                                clean_row[key] = ''
                            elif isinstance(value, (dict, list)):
                                clean_row[key] = json.dumps(value)
                            else:
                                clean_row[key] = str(value)
                        writer.writerow(clean_row)
                    
                    logger.info(f"Exported {len(data)} rows to {csv_file}")
                else:
                    # Empty table - just write headers
                    writer = csv.writer(f)
                    # Get column names from schema
                    cols_query = f"""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = '{table_name}' AND table_schema = 'public'
                    ORDER BY ordinal_position
                    """
                    columns = self.db.execute_query(cols_query)
                    if columns:
                        headers = [col['column_name'] for col in columns]
                        writer.writerow(headers)
                    logger.info(f"Table {table_name} is empty - created header-only CSV")
        else:
            logger.info(f"No data found in table: {table_name}")
    
    def create_ddl_script(self, schema_data):
        """Create DDL script from schema data"""
        logger.info("Creating DDL script...")
        
        ddl_file = self.export_dir / 'create_tables.sql'
        
        # Group columns by table
        tables = {}
        for col in schema_data:
            table_name = col['table_name']
            if table_name not in tables:
                tables[table_name] = []
            tables[table_name].append(col)
        
        with open(ddl_file, 'w') as f:
            f.write("-- GUARDIAN Database DDL Script\n")
            f.write(f"-- Generated: {datetime.now()}\n")
            f.write("-- Source: Replit PostgreSQL\n")
            f.write("-- Target: Amazon RDS PostgreSQL\n\n")
            
            # Create tables
            for table_name, columns in tables.items():
                f.write(f"-- Table: {table_name}\n")
                f.write(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
                
                column_defs = []
                for col in columns:
                    col_def = f"    {col['column_name']} {col['data_type']}"
                    if col['is_nullable'] == 'NO':
                        col_def += " NOT NULL"
                    if col['column_default']:
                        col_def += f" DEFAULT {col['column_default']}"
                    column_defs.append(col_def)
                
                f.write(",\n".join(column_defs))
                f.write("\n);\n\n")
        
        logger.info(f"DDL script created: {ddl_file}")
        return ddl_file
    
    def create_import_script(self):
        """Create import script for RDS"""
        logger.info("Creating import script...")
        
        import_file = self.export_dir / 'import_data.sql'
        
        with open(import_file, 'w') as f:
            f.write("-- GUARDIAN Database Import Script\n")
            f.write(f"-- Generated: {datetime.now()}\n")
            f.write("-- Execute on Amazon RDS PostgreSQL\n\n")
            
            tables = ['assessments', 'documents', 'scoring_criteria']
            
            for table in tables:
                f.write(f"-- Import {table}\n")
                f.write(f"\\COPY {table} FROM '{table}_data.csv' WITH CSV HEADER;\n\n")
            
            # Reset sequences
            f.write("-- Reset sequences\n")
            for table in tables:
                f.write(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE(MAX(id), 1)) FROM {table};\n")
        
        logger.info(f"Import script created: {import_file}")
        return import_file
    
    def create_migration_guide(self):
        """Create migration instructions"""
        logger.info("Creating migration guide...")
        
        guide_file = self.export_dir / 'MIGRATION_GUIDE.md'
        
        with open(guide_file, 'w') as f:
            f.write("""# GUARDIAN Database Migration to Amazon RDS

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
Generated: {}
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        logger.info(f"Migration guide created: {guide_file}")
    
    def export_all(self):
        """Export complete database"""
        logger.info("Starting complete database export...")
        
        try:
            # Export schema
            schema_data = self.export_table_schema()
            
            # Create DDL script
            self.create_ddl_script(schema_data)
            
            # Export table data
            tables = ['assessments', 'documents', 'scoring_criteria']
            for table in tables:
                self.export_table_data(table)
            
            # Create import script
            self.create_import_script()
            
            # Create migration guide
            self.create_migration_guide()
            
            # Summary
            files = list(self.export_dir.glob('*'))
            logger.info(f"Export completed! {len(files)} files created in {self.export_dir}")
            
            return {
                'status': 'success',
                'export_dir': str(self.export_dir),
                'files_created': [f.name for f in files]
            }
            
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }

def main():
    print("GUARDIAN Database Export for RDS Migration")
    print("=" * 50)
    
    exporter = SimpleDBExporter()
    result = exporter.export_all()
    
    if result['status'] == 'success':
        print(f"✅ Export completed successfully!")
        print(f"📁 Files created in: {result['export_dir']}")
        print(f"📄 Total files: {len(result['files_created'])}")
        print("\nFiles created:")
        for file in result['files_created']:
            print(f"  - {file}")
        print("\nNext steps:")
        print("1. Review MIGRATION_GUIDE.md for detailed instructions")
        print("2. Set up your Amazon RDS PostgreSQL instance")
        print("3. Execute the migration scripts")
    else:
        print(f"❌ Export failed: {result['error']}")

if __name__ == "__main__":
    main()