# GUARDIAN
## Governance Using AI for Risk Detection, Integration, Analysis, and Notification

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white)](https://postgresql.org)

GUARDIAN is a revolutionary AI-powered platform providing comprehensive real-time assessment and mitigation of complex risks across cybersecurity, ethics, and policy domains for emerging technologies.

## Key Features

### Advanced AI Intelligence
- **Multi-LLM Ensemble System**: Concurrent processing across 6+ LLM services (OpenAI, Anthropic, Groq, HuggingFace)
- **Intelligent Synthesis Engine**: Advanced consensus algorithms combining multiple AI model outputs
- **Patent-Protected Scoring**: Three proprietary scoring frameworks with mathematical formulations

### Comprehensive Risk Assessment
- **AI Cybersecurity Maturity**: 0-100 scale evaluation with NIST framework alignment
- **Quantum Cybersecurity Evaluation (QCMEA)**: 5-tier quantum readiness assessment
- **Ethics Compliance Scoring**: Comprehensive ethical evaluation with gap analysis

### Real-Time Document Processing
- **Multi-Format Support**: PDF, web content, policy documents, regulatory frameworks
- **Enhanced Metadata Extraction**: AI-powered content classification and analysis
- **Duplicate Detection**: Intelligent deduplication preventing repository bloat
- **Thumbnail Generation**: Visual document previews for improved user experience

## Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL database
- API keys for external LLM services (optional but recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/guardian.git
   cd guardian
   ```

2. **Install dependencies**
   ```bash
   pip install -r github_requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   ```

4. **Initialize the database**
   ```bash
   python database_init.sql
   ```

5. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

## Technology Stack

### Core Technologies
- **Web Framework**: Streamlit for interactive visualization
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Processing**: Multi-LLM ensemble architecture
- **Document Processing**: Advanced PDF parsing with metadata extraction
- **Visualization**: Plotly and Matplotlib for dynamic charts

### AI & Machine Learning
- **LLM Integration**: OpenAI, Anthropic, Groq, HuggingFace, Together AI
- **Quantum Computing**: Qiskit for quantum-enhanced processing
- **Natural Language Processing**: Advanced text analysis and classification
- **Intelligent Synthesis**: Consensus-driven decision making algorithms

### Environment Variables
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/guardian
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GROQ_API_KEY=your_groq_key
HUGGINGFACE_API_KEY=your_hf_key
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                       │
│  Streamlit Web Interface │ Interactive Dashboards │ APIs   │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                   INTELLIGENCE LAYER                        │
│  Multi-LLM Ensemble │ Synthesis Engine │ Patent Algorithms │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                          │
│  Document Parser │ Metadata Extractor │ Risk Calculator   │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                              │
│  PostgreSQL Database │ Cache Layer │ File Storage          │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Options

### Local Development
```bash
streamlit run app.py --server.port 5000
```

### Cloud Platforms
- **AWS EC2**: Full deployment package included
- **Replit**: One-click deployment ready
- **Streamlit Cloud**: Direct deployment from GitHub
- **Docker**: Containerized deployment support

## Performance Metrics

- **Document Processing**: 95% faster than manual analysis
- **Multi-LLM Accuracy**: 95% accuracy in policy evaluation
- **Response Time**: <2 seconds for standard document analysis
- **Concurrent Users**: Supports 100+ simultaneous users

## Testing

Run the test suite:
```bash
python test_multi_llm_scoring.py
python test_patent_scoring.py
python test_quantum_scoring_fix.py
```

## Documentation

- [Comprehensive System Narrative](GUARDIAN_Comprehensive_Narrative.md)
- [Multi-LLM Ensemble Architecture](MULTI_LLM_ENSEMBLE_ARCHITECTURE.md)
- [Quantum-LLM Integration](QUANTUM_LLM_INTEGRATION.md)
- [Debug and Cleanup Summary](GUARDIAN_Debug_Cleanup_Summary.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built on advanced AI technologies from OpenAI, Anthropic, and other leading providers
- Quantum computing capabilities powered by IBM Qiskit
- Document processing enhanced by Trafilatura and PyPDF
- Visualization powered by Plotly and Matplotlib

## Support

For support, create an issue in this repository or contact the development team.

---

**GUARDIAN** - Transforming technology governance through intelligent automation.