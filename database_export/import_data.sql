-- GUARDIAN Database Import Script
-- Generated: 2025-06-15 05:57:04.169017
-- Execute on Amazon RDS PostgreSQL

-- Import assessments
\COPY assessments FROM 'assessments_data.csv' WITH CSV HEADER;

-- Import documents
\COPY documents FROM 'documents_data.csv' WITH CSV HEADER;

-- Import scoring_criteria
\COPY scoring_criteria FROM 'scoring_criteria_data.csv' WITH CSV HEADER;

-- Reset sequences
SELECT setval(pg_get_serial_sequence('assessments', 'id'), COALESCE(MAX(id), 1)) FROM assessments;
SELECT setval(pg_get_serial_sequence('documents', 'id'), COALESCE(MAX(id), 1)) FROM documents;
SELECT setval(pg_get_serial_sequence('scoring_criteria', 'id'), COALESCE(MAX(id), 1)) FROM scoring_criteria;
