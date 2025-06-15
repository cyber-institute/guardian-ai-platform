#!/usr/bin/env python3
"""
Amazon RDS Setup Helper for GUARDIAN
Assists with RDS instance configuration and connection testing
"""

import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RDSHelper:
    def __init__(self):
        self.rds_config = {
            'host': None,
            'port': 5432,
            'database': None,
            'username': None,
            'password': None,
            'ssl_mode': 'require'
        }
    
    def configure_rds_connection(self, host, database, username, password, port=5432):
        """Configure RDS connection parameters."""
        self.rds_config.update({
            'host': host,
            'port': port,
            'database': database,
            'username': username,
            'password': password
        })
        
        # Generate connection URL
        connection_url = f"postgresql://{username}:{password}@{host}:{port}/{database}?sslmode=require"
        self.rds_config['connection_url'] = connection_url
        
        logger.info(f"RDS configuration set for: {host}:{port}/{database}")
        return connection_url
    
    def test_rds_connection(self):
        """Test connection to RDS instance."""
        if not all([self.rds_config['host'], self.rds_config['database'], 
                   self.rds_config['username'], self.rds_config['password']]):
            raise ValueError("RDS configuration incomplete. Call configure_rds_connection() first.")
        
        try:
            logger.info("Testing RDS connection...")
            
            conn = psycopg2.connect(
                host=self.rds_config['host'],
                port=self.rds_config['port'],
                database=self.rds_config['database'],
                user=self.rds_config['username'],
                password=self.rds_config['password'],
                sslmode=self.rds_config['ssl_mode'],
                connect_timeout=10
            )
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Test basic queries
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            
            cursor.execute("SELECT current_database(), current_user;")
            db_info = cursor.fetchone()
            
            cursor.execute("SELECT COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'public';")
            table_count = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            result = {
                'status': 'success',
                'postgresql_version': version['version'],
                'database': db_info['current_database'],
                'user': db_info['current_user'],
                'existing_tables': table_count['table_count'],
                'connection_url': self.rds_config['connection_url']
            }
            
            logger.info("RDS connection test successful!")
            logger.info(f"PostgreSQL version: {version['version']}")
            logger.info(f"Connected to database: {db_info['current_database']} as {db_info['current_user']}")
            logger.info(f"Existing tables in public schema: {table_count['table_count']}")
            
            return result
            
        except Exception as e:
            logger.error(f"RDS connection test failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'suggestions': [
                    "Check RDS security group settings",
                    "Verify database credentials",
                    "Ensure RDS instance is publicly accessible (if connecting from outside VPC)",
                    "Check SSL/TLS configuration",
                    "Verify network connectivity"
                ]
            }
    
    def create_rds_environment_file(self, filename='.env.rds'):
        """Create environment file for RDS configuration."""
        if not self.rds_config['connection_url']:
            raise ValueError("RDS configuration not set. Call configure_rds_connection() first.")
        
        env_content = f"""# Amazon RDS Configuration for GUARDIAN
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# RDS Connection URL
DATABASE_URL={self.rds_config['connection_url']}

# Individual connection parameters
RDS_HOST={self.rds_config['host']}
RDS_PORT={self.rds_config['port']}
RDS_DATABASE={self.rds_config['database']}
RDS_USERNAME={self.rds_config['username']}
RDS_PASSWORD={self.rds_config['password']}
RDS_SSL_MODE={self.rds_config['ssl_mode']}

# Application settings
ENVIRONMENT=production
SSL_REQUIRE=true
"""
        
        with open(filename, 'w') as f:
            f.write(env_content)
        
        logger.info(f"RDS environment file created: {filename}")
        return filename
    
    def verify_migration_readiness(self):
        """Verify that RDS instance is ready for migration."""
        logger.info("Verifying migration readiness...")
        
        try:
            conn = psycopg2.connect(
                host=self.rds_config['host'],
                port=self.rds_config['port'],
                database=self.rds_config['database'],
                user=self.rds_config['username'],
                password=self.rds_config['password'],
                sslmode=self.rds_config['ssl_mode']
            )
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            checks = {
                'connection': True,
                'ssl_enabled': False,
                'sufficient_privileges': False,
                'empty_database': False,
                'extensions_available': []
            }
            
            # Check SSL
            cursor.execute("SHOW ssl;")
            ssl_status = cursor.fetchone()
            checks['ssl_enabled'] = ssl_status['ssl'] == 'on'
            
            # Check privileges
            cursor.execute("""
                SELECT has_database_privilege(current_user, current_database(), 'CREATE') as can_create,
                       has_database_privilege(current_user, current_database(), 'CONNECT') as can_connect;
            """)
            privileges = cursor.fetchone()
            checks['sufficient_privileges'] = privileges['can_create'] and privileges['can_connect']
            
            # Check if database is empty (no user tables)
            cursor.execute("""
                SELECT COUNT(*) as user_tables 
                FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
            """)
            table_count = cursor.fetchone()
            checks['empty_database'] = table_count['user_tables'] == 0
            
            # Check available extensions
            cursor.execute("SELECT name FROM pg_available_extensions WHERE installed_version IS NOT NULL;")
            extensions = cursor.fetchall()
            checks['extensions_available'] = [ext['name'] for ext in extensions]
            
            cursor.close()
            conn.close()
            
            # Evaluate readiness
            readiness_score = 0
            if checks['connection']: readiness_score += 1
            if checks['ssl_enabled']: readiness_score += 1
            if checks['sufficient_privileges']: readiness_score += 1
            if checks['empty_database']: readiness_score += 1
            
            checks['readiness_score'] = f"{readiness_score}/4"
            checks['ready_for_migration'] = readiness_score >= 3
            
            logger.info(f"Migration readiness: {checks['readiness_score']}")
            
            if not checks['ready_for_migration']:
                logger.warning("RDS instance may not be ready for migration. Check the following:")
                if not checks['ssl_enabled']:
                    logger.warning("- SSL is not enabled")
                if not checks['sufficient_privileges']:
                    logger.warning("- User lacks CREATE privileges")
                if not checks['empty_database']:
                    logger.warning("- Database is not empty (existing tables found)")
            
            return checks
            
        except Exception as e:
            logger.error(f"Migration readiness check failed: {e}")
            return {
                'connection': False,
                'error': str(e),
                'ready_for_migration': False
            }

def interactive_rds_setup():
    """Interactive RDS setup wizard."""
    print("GUARDIAN Amazon RDS Setup Helper")
    print("=" * 40)
    
    helper = RDSHelper()
    
    # Collect RDS information
    print("\nEnter your Amazon RDS connection details:")
    host = input("RDS Endpoint (e.g., mydb.abc123.us-east-1.rds.amazonaws.com): ").strip()
    database = input("Database name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    port = input("Port (default 5432): ").strip()
    
    if not port:
        port = 5432
    else:
        port = int(port)
    
    # Configure connection
    connection_url = helper.configure_rds_connection(host, database, username, password, port)
    
    print(f"\nGenerated connection URL:")
    print(f"postgresql://{username}:***@{host}:{port}/{database}?sslmode=require")
    
    # Test connection
    print("\nTesting RDS connection...")
    result = helper.test_rds_connection()
    
    if result['status'] == 'success':
        print("✅ RDS connection successful!")
        print(f"PostgreSQL version: {result['postgresql_version']}")
        print(f"Connected as: {result['user']}")
        print(f"Existing tables: {result['existing_tables']}")
        
        # Check migration readiness
        print("\nChecking migration readiness...")
        readiness = helper.verify_migration_readiness()
        
        if readiness['ready_for_migration']:
            print("✅ RDS instance is ready for migration!")
        else:
            print("⚠️  RDS instance needs attention before migration")
            print(f"Readiness score: {readiness['readiness_score']}")
        
        # Create environment file
        env_file = helper.create_rds_environment_file()
        print(f"\n📄 Environment file created: {env_file}")
        print("Update your application to use this configuration for RDS connection.")
        
    else:
        print("❌ RDS connection failed!")
        print(f"Error: {result['error']}")
        print("\nSuggestions:")
        for suggestion in result['suggestions']:
            print(f"- {suggestion}")
    
    return helper, result

if __name__ == "__main__":
    interactive_rds_setup()