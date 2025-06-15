-- GUARDIAN Database DDL Script
-- Generated: 2025-06-15 05:55:35.178831
-- Source: Replit PostgreSQL
-- Target: Amazon RDS PostgreSQL

CREATE SEQUENCE IF NOT EXISTS documents_id_seq;
CREATE SEQUENCE IF NOT EXISTS assessments_id_seq;
CREATE SEQUENCE IF NOT EXISTS scoring_criteria_id_seq;

-- Table: assessments
CREATE TABLE IF NOT EXISTS assessments (
    id integer NOT NULL DEFAULT nextval('assessments_id_seq'::regclass),
    document_id integer,
    assessment_type character varying NOT NULL,
    score numeric NOT NULL,
    confidence_scores jsonb,
    narrative ARRAY,
    traits jsonb,
    raw_analysis jsonb,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX assessments_pkey ON public.assessments USING btree (id);

-- Table: documents
CREATE TABLE IF NOT EXISTS documents (
    id integer NOT NULL DEFAULT nextval('documents_id_seq'::regclass),
    title character varying NOT NULL,
    content text,
    text_content text,
    quantum_score numeric DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    document_type character varying,
    source text,
    metadata jsonb,
    author_organization character varying,
    publish_date date,
    content_preview text,
    ai_cybersecurity_score integer,
    quantum_cybersecurity_score integer,
    ai_ethics_score integer,
    quantum_ethics_score integer,
    detected_region character varying DEFAULT 'Unknown'::character varying,
    region_confidence double precision DEFAULT 0.0,
    region_reasoning text DEFAULT ''::text,
    topic character varying DEFAULT 'General'::character varying,
    url_valid boolean,
    url_status text,
    url_checked timestamp without time zone,
    source_redirect text
);

CREATE UNIQUE INDEX documents_pkey ON public.documents USING btree (id);

-- Table: scoring_criteria
CREATE TABLE IF NOT EXISTS scoring_criteria (
    id integer NOT NULL DEFAULT nextval('scoring_criteria_id_seq'::regclass),
    criterion_name character varying NOT NULL,
    weight numeric NOT NULL,
    category character varying NOT NULL,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX scoring_criteria_pkey ON public.scoring_criteria USING btree (id);

