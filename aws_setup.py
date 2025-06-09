#!/usr/bin/env python3
"""
AWS Deployment Setup Script for GUARDIAN Quantum Maturity Assessment Tool
"""

import os
import subprocess
import sys

def create_database_tables():
    """Create database tables for AWS RDS deployment"""
    
    sql_commands = """
    -- Create documents table
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content TEXT,
        text TEXT,
        document_type VARCHAR(100) DEFAULT 'document',
        source VARCHAR(100) DEFAULT 'manual',
        quantum_score INTEGER DEFAULT 0,
        quantum_q INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create assessments table
    CREATE TABLE IF NOT EXISTS assessments (
        id SERIAL PRIMARY KEY,
        document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
        assessment_data JSONB,
        score INTEGER,
        analysis_method VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create scoring_criteria table
    CREATE TABLE IF NOT EXISTS scoring_criteria (
        id SERIAL PRIMARY KEY,
        category VARCHAR(100) NOT NULL,
        criteria_name VARCHAR(255) NOT NULL,
        weight DECIMAL(5,2) DEFAULT 1.0,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Insert default scoring criteria
    INSERT INTO scoring_criteria (category, criteria_name, weight, description) 
    VALUES 
        ('quantum', 'Post-Quantum Cryptography', 1.5, 'Implementation of quantum-resistant algorithms'),
        ('quantum', 'Risk Assessment', 1.2, 'Comprehensive quantum threat analysis'),
        ('quantum', 'Migration Planning', 1.3, 'Strategy for cryptographic transition'),
        ('quantum', 'Standards Compliance', 1.4, 'Adherence to NIST and FIPS standards'),
        ('quantum', 'Implementation Readiness', 1.1, 'Organizational preparedness for quantum transition')
    ON CONFLICT DO NOTHING;

    -- Create indexes for performance
    CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at);
    CREATE INDEX IF NOT EXISTS idx_documents_quantum_score ON documents(quantum_score);
    CREATE INDEX IF NOT EXISTS idx_assessments_document_id ON assessments(document_id);
    CREATE INDEX IF NOT EXISTS idx_assessments_created_at ON assessments(created_at);
    """
    
    return sql_commands

def main():
    print("GUARDIAN AWS Deployment Setup")
    print("=" * 50)
    
    # Check environment variables
    required_vars = ['DATABASE_URL']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        print("\nPlease set the following environment variables:")
        print("DATABASE_URL=postgresql://username:password@rds-endpoint:5432/database_name")
        sys.exit(1)
    
    print("Environment variables configured correctly")
    
    # Install dependencies
    print("\nInstalling Python dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'deploy_requirements.txt'], check=True)
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    print("streamlit run app.py --server.port 8501")

if __name__ == "__main__":
    main()