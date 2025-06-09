-- Quantum Maturity Assessment Database Schema

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT,
    text_content TEXT,
    quantum_score DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    document_type VARCHAR(100),
    source VARCHAR(200),
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS assessments (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    assessment_type VARCHAR(100) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    confidence_scores JSONB,
    narrative TEXT[],
    traits JSONB,
    raw_analysis JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS scoring_criteria (
    id SERIAL PRIMARY KEY,
    criterion_name VARCHAR(200) NOT NULL,
    weight DECIMAL(3,2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default scoring criteria
INSERT INTO scoring_criteria (criterion_name, weight, category, description) VALUES
('quantum-aware-basic', 0.8, 'awareness', 'Basic quantum awareness indicators'),
('quantum-aware-advanced', 0.8, 'awareness', 'Advanced quantum awareness indicators'),
('quantum-ready-planning', 1.2, 'readiness', 'Quantum readiness planning indicators'),
('quantum-ready-testing', 1.2, 'readiness', 'Quantum readiness testing indicators'),
('quantum-controls-implemented', 1.5, 'controls', 'Implemented quantum controls'),
('quantum-controls-validated', 1.5, 'controls', 'Validated quantum controls'),
('post-quantum-cryptography', 1.8, 'implementation', 'Post-quantum cryptography implementation'),
('quantum-risk-assessment', 1.3, 'risk', 'Quantum risk assessment indicators'),
('quantum-migration-strategy', 1.4, 'strategy', 'Quantum migration strategy indicators')
ON CONFLICT DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_documents_quantum_score ON documents(quantum_score);
CREATE INDEX IF NOT EXISTS idx_documents_created_at ON documents(created_at);
CREATE INDEX IF NOT EXISTS idx_assessments_document_id ON assessments(document_id);
CREATE INDEX IF NOT EXISTS idx_assessments_score ON assessments(score);