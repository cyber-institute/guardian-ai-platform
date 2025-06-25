# GUARDIAN System - Replit.md

## Overview

GUARDIAN (Governance Using AI for Risk Detection, Integration, Analysis, and Notification) is a sophisticated AI-powered platform designed for comprehensive real-time assessment and mitigation of complex risks across cybersecurity, ethics, and policy domains for emerging technologies. The system provides automated document analysis, policy gap assessment, and risk scoring through advanced multi-LLM ensemble processing.

## System Architecture

### Frontend Architecture
- **Primary Interface**: Streamlit-based web application with professional government/nonprofit styling
- **Layout**: Wide layout with collapsed sidebar for streamlined experience
- **Components**: Modular tab-based interface (All Documents, About, Convergence AI, Quantum tabs)
- **Styling**: Custom CSS with Inter font family and clean visual hierarchy

### Backend Architecture
- **Web Framework**: Streamlit as the primary application framework
- **API Layer**: Flask-based API server for external integrations (webhook handling, button clicks)
- **Database Layer**: PostgreSQL with SQLAlchemy ORM for data persistence
- **Caching**: Multi-tier caching system using Streamlit's cache decorators for performance optimization

### Multi-LLM Ensemble System
- **Service Integration**: Supports 6+ LLM services (OpenAI, Anthropic, Groq, HuggingFace, Together AI, local Ollama)
- **Processing Modes**: Parallel processing and daisy-chain refinement for enhanced accuracy
- **Consensus Engine**: Weighted consensus algorithms for synthesizing multiple AI outputs
- **Quantum Router**: Qiskit-based quantum routing for probabilistic model selection

## Key Components

### Document Processing Engine
- **Multi-Format Support**: PDF, TXT, CSV, DOCX, and web content processing
- **Content Extraction**: PyPDF2 and trafilatura for text extraction
- **Thumbnail Generation**: Automated PDF thumbnail extraction and caching
- **Metadata Enhancement**: AI-powered content classification and metadata extraction

### Scoring Framework
- **AI Cybersecurity Maturity**: 0-100 scale evaluation with NIST framework alignment
- **Quantum Cybersecurity Evaluation (QCMEA)**: 5-tier quantum readiness assessment
- **AI Ethics Scoring**: Comprehensive ethical evaluation with bias detection
- **Content Analysis**: Multi-layer analysis including pattern-based, statistical, and contextual scoring

### Risk Assessment System
- **Patent-Protected Algorithms**: Three proprietary scoring methodologies
- **Convergence AI**: Anti-bias and anti-poisoning system with quantum-enhanced routing
- **Gap Analysis**: Automated policy gap identification and recommendation generation
- **Real-Time Monitoring**: Continuous assessment with instant alerts

### Intelligence Systems
- **Self-Healing URLs**: Automated URL discovery and validation system
- **Duplicate Detection**: Intelligent deduplication preventing repository bloat
- **Background Processing**: Automated maintenance tasks running every 6 hours
- **Search Integration**: Multiple search API integrations for content discovery

## Data Flow

### Document Ingestion
1. **Upload Interface**: Multi-file upload with drag-and-drop support
2. **Content Processing**: Text extraction, thumbnail generation, metadata extraction
3. **Duplicate Check**: Content-based deduplication with similarity analysis
4. **Database Storage**: Normalized storage with full-text search capabilities
5. **Background Enhancement**: URL discovery, metadata enrichment, validation

### Scoring Pipeline
1. **Content Analysis**: Deep content analysis using multiple analytical approaches
2. **Multi-LLM Processing**: Concurrent processing across available LLM services
3. **Consensus Formation**: Weighted synthesis of multiple AI model outputs
4. **Score Calculation**: Domain-specific scoring using specialized algorithms
5. **Validation**: Automated integrity checks and score validation

### Analytics Generation
1. **Performance Tracking**: Multi-LLM benchmarking and comparison analytics
2. **Trend Analysis**: Historical scoring trends and improvement tracking
3. **Visualization**: Interactive dashboards with Plotly and Matplotlib
4. **Reporting**: Comprehensive analysis reports with actionable insights

## External Dependencies

### Required Services
- **PostgreSQL Database**: Primary data storage (local or cloud-hosted)
- **Python 3.11+**: Runtime environment with extensive package ecosystem

### Optional LLM Services
- **OpenAI API**: GPT-4 and GPT-3.5 models for premium analysis
- **Anthropic API**: Claude models for advanced reasoning
- **Groq API**: Ultra-fast inference for real-time processing
- **HuggingFace API**: Specialized models for domain-specific analysis
- **Together AI**: Open-source model access
- **Local Ollama**: Privacy-focused local model execution

### Supporting Services
- **Google Cloud**: Dialogflow CX integration for conversational AI
- **Search APIs**: Google Custom Search, Bing Search for content discovery
- **Qiskit**: Quantum computing framework for quantum-enhanced routing

## Deployment Strategy

### Development Environment
- **Platform**: Replit with integrated PostgreSQL
- **Configuration**: Environment variables for API keys and database connection
- **Port Configuration**: Multiple ports for different services (5000, 5001, 5002)
- **Workflow**: Parallel execution of main app and supporting services

### Production Migration
- **Target Platform**: Amazon Web Services (AWS)
- **Database**: Amazon RDS PostgreSQL for scalable data storage
- **Compute**: EC2 instances or Elastic Beanstalk for application hosting
- **Migration Tools**: Comprehensive export/import scripts and automated deployment
- **Security**: SSL/TLS encryption, secure environment variable management

### Containerization
- **Docker Support**: Complete Dockerfile and docker-compose configuration
- **Service Orchestration**: Multi-container setup for scalable deployment
- **Load Balancing**: Nginx configuration for production traffic handling

## Changelog

- June 25, 2025: Configured private deployment with authentication layer and security features
- June 25, 2025: Implemented stable floating chat system with speech bubble design and working ARIA interface
- June 25, 2025: Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.
UI Design preferences: Speech bubble shaped chat buttons, blue gradient styling with white text, compact button sizing with 11px font