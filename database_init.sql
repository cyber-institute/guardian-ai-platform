-- Database initialization script for AWS RDS deployment
-- Run this on your PostgreSQL RDS instance

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

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;