#!/usr/bin/env python3
"""
GUARDIAN Database Export to Amazon RDS
Comprehensive migration script for exporting Replit PostgreSQL to AWS RDS
"""

import os
import json
import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatabaseExporter:
    def __init__(self):
        self.source_db_url = os.getenv('DATABASE_URL')
        self.export_dir = Path('./database_export')
        self.export_dir.mkdir(exist_ok=True)
        
        if not self.source_db_url:
            raise ValueError("DATABASE_URL environment variable not found")
    
    def get_database_schema(self):
        """Extract complete database schema including tables, indexes, and constraints."""
        logger.info("Extracting database schema...")
        
        try:
            conn = psycopg2.connect(self.source_db_url)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get all tables
            cursor.execute("""
                SELECT table_name, table_schema 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            schema_info = {
                'tables': [],
                'indexes': [],
                'constraints': [],
                'sequences': []
            }
            
            for table in tables:
                table_name = table['table_name']
                logger.info(f"Processing table: {table_name}")
                
                # Get table structure
                cursor.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = %s AND table_schema = 'public'
                    ORDER BY ordinal_position;
                """, (table_name,))
                columns = cursor.fetchall()
                
                # Get table constraints
                cursor.execute("""
                    SELECT constraint_name, constraint_type
                    FROM information_schema.table_constraints
                    WHERE table_name = %s AND table_schema = 'public';
                """, (table_name,))
                constraints = cursor.fetchall()
                
                # Get indexes
                cursor.execute("""
                    SELECT indexname, indexdef
                    FROM pg_indexes
                    WHERE tablename = %s AND schemaname = 'public';
                """, (table_name,))
                indexes = cursor.fetchall()
                
                schema_info['tables'].append({
                    'name': table_name,
                    'columns': [dict(col) for col in columns],
                    'constraints': [dict(cons) for cons in constraints],
                    'indexes': [dict(idx) for idx in indexes]
                })
            
            # Get sequences
            cursor.execute("""
                SELECT sequence_name
                FROM information_schema.sequences
                WHERE sequence_schema = 'public';
            """)
            sequences = cursor.fetchall()
            schema_info['sequences'] = [dict(seq) for seq in sequences]
            
            cursor.close()
            conn.close()
            
            # Save schema to file
            schema_file = self.export_dir / 'schema.json'
            with open(schema_file, 'w') as f:
                json.dump(schema_info, f, indent=2, default=str)
            
            logger.info(f"Schema exported to {schema_file}")
            return schema_info
            
        except Exception as e:
            logger.error(f"Error extracting schema: {e}")
            raise
    
    def generate_ddl_script(self, schema_info):
        """Generate DDL script for recreating database structure."""
        logger.info("Generating DDL script...")
        
        ddl_file = self.export_dir / 'create_tables.sql'
        
        with open(ddl_file, 'w') as f:
            f.write("-- GUARDIAN Database DDL Script\n")
            f.write(f"-- Generated: {datetime.now()}\n")
            f.write("-- Source: Replit PostgreSQL\n")
            f.write("-- Target: Amazon RDS PostgreSQL\n\n")
            
            # Create sequences first
            for seq in schema_info['sequences']:
                f.write(f"CREATE SEQUENCE IF NOT EXISTS {seq['sequence_name']};\n")
            f.write("\n")
            
            # Create tables
            for table in schema_info['tables']:
                f.write(f"-- Table: {table['name']}\n")
                f.write(f"CREATE TABLE IF NOT EXISTS {table['name']} (\n")
                
                column_defs = []
                for col in table['columns']:
                    col_def = f"    {col['column_name']} {col['data_type']}"
                    if col['is_nullable'] == 'NO':
                        col_def += " NOT NULL"
                    if col['column_default']:
                        col_def += f" DEFAULT {col['column_default']}"
                    column_defs.append(col_def)
                
                f.write(",\n".join(column_defs))
                f.write("\n);\n\n")
                
                # Add indexes
                for idx in table['indexes']:
                    if 'CREATE' in idx['indexdef']:
                        f.write(f"{idx['indexdef']};\n")
                f.write("\n")
        
        logger.info(f"DDL script generated: {ddl_file}")
        return ddl_file
    
    def export_table_data(self, table_name, batch_size=1000):
        """Export table data to CSV format with batching for large tables."""
        logger.info(f"Exporting data from table: {table_name}")
        
        try:
            conn = psycopg2.connect(self.source_db_url)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get total row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count_result = cursor.fetchone()
            total_rows = count_result[0] if count_result else 0
            
            if total_rows == 0:
                logger.info(f"Table {table_name} is empty, creating empty CSV file")
                # Still create the CSV with headers for consistency
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                columns = [desc[0] for desc in cursor.description]
                
                csv_file = self.export_dir / f'{table_name}_data.csv'
                with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)  # Header only
                
                cursor.close()
                conn.close()
                return
            
            logger.info(f"Exporting {total_rows} rows from {table_name}")
            
            # Get column names
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
            columns = [desc[0] for desc in cursor.description]
            
            # Export data in batches
            csv_file = self.export_dir / f'{table_name}_data.csv'
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)  # Header
                
                offset = 0
                while offset < total_rows:
                    cursor.execute(f"""
                        SELECT * FROM {table_name} 
                        ORDER BY (SELECT NULL) 
                        LIMIT {batch_size} OFFSET {offset}
                    """)
                    
                    rows = cursor.fetchall()
                    for row in rows:
                        # Handle None values and convert to string
                        processed_row = []
                        for value in row:
                            if value is None:
                                processed_row.append('')
                            elif isinstance(value, (dict, list)):
                                processed_row.append(json.dumps(value))
                            else:
                                processed_row.append(str(value))
                        writer.writerow(processed_row)
                    
                    offset += batch_size
                    logger.info(f"Exported {min(offset, total_rows)}/{total_rows} rows from {table_name}")
            
            cursor.close()
            conn.close()
            
            logger.info(f"Data exported to {csv_file}")
            
        except Exception as e:
            logger.error(f"Error exporting table {table_name}: {e}")
            raise
    
    def create_import_script(self, schema_info):
        """Create SQL script to import data into RDS."""
        logger.info("Creating import script...")
        
        import_file = self.export_dir / 'import_data.sql'
        
        with open(import_file, 'w') as f:
            f.write("-- GUARDIAN Database Data Import Script\n")
            f.write(f"-- Generated: {datetime.now()}\n")
            f.write("-- Execute this script on your Amazon RDS instance\n\n")
            
            f.write("-- Disable foreign key checks during import\n")
            f.write("SET session_replication_role = replica;\n\n")
            
            for table in schema_info['tables']:
                table_name = table['name']
                csv_file = f"{table_name}_data.csv"
                
                f.write(f"-- Import data for table: {table_name}\n")
                f.write(f"\\COPY {table_name} FROM '{csv_file}' WITH CSV HEADER;\n\n")
            
            f.write("-- Re-enable foreign key checks\n")
            f.write("SET session_replication_role = DEFAULT;\n\n")
            
            # Update sequences
            for table in schema_info['tables']:
                table_name = table['name']
                # Look for ID columns that might use sequences
                for col in table['columns']:
                    if (col['column_name'].endswith('_id') or col['column_name'] == 'id') and 'nextval' in str(col['column_default']):
                        f.write(f"-- Update sequence for {table_name}\n")
                        f.write(f"SELECT setval(pg_get_serial_sequence('{table_name}', '{col['column_name']}'), MAX({col['column_name']})) FROM {table_name};\n")
            
        logger.info(f"Import script created: {import_file}")
        return import_file
    
    def create_pg_dump_backup(self):
        """Create a complete pg_dump backup as alternative export method."""
        logger.info("Creating pg_dump backup...")
        
        dump_file = self.export_dir / 'guardian_database_backup.sql'
        
        try:
            # Extract connection parameters from DATABASE_URL
            import urllib.parse as urlparse
            parsed = urlparse.urlparse(self.source_db_url)
            
            env = os.environ.copy()
            env['PGPASSWORD'] = parsed.password
            
            cmd = [
                'pg_dump',
                '-h', parsed.hostname,
                '-p', str(parsed.port),
                '-U', parsed.username,
                '-d', parsed.path[1:],  # Remove leading slash
                '--verbose',
                '--clean',
                '--no-owner',
                '--no-privileges',
                '--format=plain',
                '-f', str(dump_file)
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"pg_dump backup created: {dump_file}")
                return dump_file
            else:
                logger.warning(f"pg_dump failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.warning(f"Could not create pg_dump backup: {e}")
            return None
    
    def export_full_database(self):
        """Perform complete database export."""
        logger.info("Starting full database export...")
        
        export_summary = {
            'export_date': datetime.now().isoformat(),
            'source_database': 'Replit PostgreSQL',
            'target_database': 'Amazon RDS PostgreSQL',
            'files_created': []
        }
        
        try:
            # Step 1: Extract schema
            schema_info = self.get_database_schema()
            export_summary['files_created'].append('schema.json')
            
            # Step 2: Generate DDL script
            ddl_file = self.generate_ddl_script(schema_info)
            export_summary['files_created'].append('create_tables.sql')
            
            # Step 3: Export table data
            for table in schema_info['tables']:
                self.export_table_data(table['name'])
                export_summary['files_created'].append(f"{table['name']}_data.csv")
            
            # Step 4: Create import script
            import_file = self.create_import_script(schema_info)
            export_summary['files_created'].append('import_data.sql')
            
            # Step 5: Try to create pg_dump backup
            dump_file = self.create_pg_dump_backup()
            if dump_file:
                export_summary['files_created'].append('guardian_database_backup.sql')
            
            # Step 6: Create migration instructions
            self.create_migration_instructions()
            export_summary['files_created'].append('MIGRATION_INSTRUCTIONS.md')
            
            # Save export summary
            summary_file = self.export_dir / 'export_summary.json'
            with open(summary_file, 'w') as f:
                json.dump(export_summary, f, indent=2)
            
            logger.info("Database export completed successfully!")
            logger.info(f"Export directory: {self.export_dir}")
            logger.info(f"Files created: {len(export_summary['files_created'])}")
            
            return export_summary
            
        except Exception as e:
            logger.error(f"Database export failed: {e}")
            raise
    
    def create_migration_instructions(self):
        """Create detailed migration instructions."""
        instructions_file = self.export_dir / 'MIGRATION_INSTRUCTIONS.md'
        
        with open(instructions_file, 'w') as f:
            f.write("""# GUARDIAN Database Migration to Amazon RDS

## Overview
This package contains a complete export of your GUARDIAN PostgreSQL database from Replit, ready for import into Amazon RDS.

## Files Included

1. **schema.json** - Complete database schema information
2. **create_tables.sql** - DDL script to create all tables and indexes
3. **[table]_data.csv** - Data export files for each table
4. **import_data.sql** - Script to import all data
5. **guardian_database_backup.sql** - Complete pg_dump backup (if available)
6. **export_summary.json** - Export process summary

## Migration Steps

### Prerequisites
- Amazon RDS PostgreSQL instance running
- PostgreSQL client tools installed (psql, pg_restore)
- Network access to your RDS instance

### Step 1: Prepare RDS Instance
```bash
# Connect to your RDS instance
psql -h your-rds-endpoint.amazonaws.com -U your-username -d your-database
```

### Step 2: Create Database Structure
```bash
# Execute DDL script
psql -h your-rds-endpoint.amazonaws.com -U your-username -d your-database -f create_tables.sql
```

### Step 3: Import Data

#### Option A: Using CSV Import (Recommended)
```bash
# Upload CSV files to your RDS-accessible location
# Then execute the import script
psql -h your-rds-endpoint.amazonaws.com -U your-username -d your-database -f import_data.sql
```

#### Option B: Using pg_dump Backup (if available)
```bash
psql -h your-rds-endpoint.amazonaws.com -U your-username -d your-database -f guardian_database_backup.sql
```

### Step 4: Verify Migration
```sql
-- Check table counts
SELECT schemaname, tablename, n_tup_ins as "rows"
FROM pg_stat_user_tables
ORDER BY n_tup_ins DESC;

-- Verify sequences
SELECT sequence_name, last_value FROM information_schema.sequences;
```

### Step 5: Update Application Configuration
Update your application's DATABASE_URL to point to the new RDS instance:
```
DATABASE_URL=postgresql://username:password@your-rds-endpoint.amazonaws.com:5432/your-database
```

## Important Notes

1. **SSL Configuration**: Ensure your application is configured for SSL connections to RDS
2. **Security Groups**: Configure RDS security groups to allow connections from your application
3. **Backup Strategy**: Set up automated backups for your RDS instance
4. **Performance**: Consider configuring connection pooling for production use

## Troubleshooting

### Common Issues:
- **Permission errors**: Ensure RDS user has necessary privileges
- **SSL errors**: Configure SSL settings in connection string
- **Timeout errors**: Check security group and network connectivity

### Support:
- Check AWS RDS documentation for specific configuration options
- Monitor RDS CloudWatch metrics for performance optimization

## Security Checklist
- [ ] Database credentials properly secured
- [ ] SSL/TLS encryption enabled
- [ ] Security groups properly configured
- [ ] Regular backups scheduled
- [ ] Monitoring and alerting configured

---
Generated: {}
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        logger.info(f"Migration instructions created: {instructions_file}")

def main():
    """Main execution function."""
    print("GUARDIAN Database Export to Amazon RDS")
    print("=" * 50)
    
    try:
        exporter = DatabaseExporter()
        export_summary = exporter.export_full_database()
        
        print(f"\n✅ Export completed successfully!")
        print(f"📁 Export directory: {exporter.export_dir}")
        print(f"📄 Files created: {len(export_summary['files_created'])}")
        print(f"\nNext steps:")
        print(f"1. Review the files in {exporter.export_dir}")
        print(f"2. Follow instructions in MIGRATION_INSTRUCTIONS.md")
        print(f"3. Set up your Amazon RDS instance")
        print(f"4. Execute the migration scripts")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()