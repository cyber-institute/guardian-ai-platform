import streamlit as st

def render():
    """Render the About tab for GUARDIAN system."""
    
    # Hero section with system overview
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid #B91C2C;
    ">
        <h2 style="color: #B91C2C; margin-bottom: 1rem; font-size: 1.8rem;">
            What is GUARDIAN?
        </h2>
        <p style="font-size: 1.1rem; line-height: 1.7; color: #374151; margin-bottom: 1rem;">
            <strong>GUARDIAN</strong> (Global Unified AI Risk Discovery & Impact Analysis Navigator) is a 
            comprehensive AI-powered governance platform that integrates multiple patented technologies for 
            real-time policy evaluation, cybersecurity assessment, and ethical compliance analysis across 
            AI and quantum technology domains.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.7; color: #374151;">
            Developed by the Cyber Institute, this unified system combines three breakthrough patent technologies: 
            Real-Time Dynamic Governance, AI-Powered Policy Evaluation, and Quantum Cybersecurity Framework 
            to provide organizations with comprehensive governance solutions for emerging technologies.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Core capabilities section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### **Core Capabilities**
        
        **AI-Powered Policy Repository**
        - Hybrid data collection via APIs, document parsing, and web scraping
        - Unbiased policy summarization using transformer-based models
        - Cross-jurisdictional policy comparison and harmonization
        
        **Cybersecurity & Ethics Gap Analysis**
        - Machine learning-powered compliance gap scoring
        - Alignment with global frameworks (NIST, OECD, EU AI Act)
        - Real-time vulnerability assessment and mitigation recommendations
        
        **Quantum Cybersecurity Framework**
        - Five-tier maturity evaluation algorithm (QCMEA)
        - Bayesian inference for dynamic threat assessment
        - Post-quantum cryptography readiness evaluation
        
        **Policy Optimization & Stress Testing**
        - Reinforcement learning for policy customization
        - Sandbox environment for regulatory impact simulation
        - Probabilistic adoption scoring and effectiveness prediction
        """)
    
    with col2:
        st.markdown("""
        ### **Who Benefits?**
        
        **Government Agencies**
        - Policy compliance verification
        - Regulatory gap analysis
        - Strategic planning for quantum initiatives
        
        **Enterprise Organizations**
        - Risk assessment for quantum adoption
        - Compliance monitoring and reporting
        - Technology readiness evaluation
        
        **Research Institutions**
        - Academic policy analysis
        - Comparative framework studies
        - Emerging technology governance research
        """)
    
    # Technical architecture section
    st.markdown("---")
    
    st.markdown("""
    ### **Technical Architecture**
    
    GUARDIAN employs a sophisticated multi-layered approach to governance analysis:
    """)
    
    # Architecture components
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **AI Decision Layer**
        - BERT and GPT-4 transformer models
        - Named Entity Recognition (NER) for policy extraction
        - Fuzzy logic-based probabilistic scoring
        - Sentiment analysis for bias detection
        """)
    
    with col2:
        st.markdown("""
        **Risk Evaluation Engine**
        - Graph Neural Networks (GNNs) for interdependency analysis
        - Dual-modality cybersecurity and ethics scoring
        - Quantum threat simulation and validation
        - Real-time vulnerability assessment
        """)
    
    with col3:
        st.markdown("""
        **Adaptive Learning**
        - Bayesian inference for dynamic updates
        - Reinforcement learning policy optimization
        - Semantic drift detection and retraining
        - Continuous compliance monitoring
        """)
    
    # Scoring methodology section
    st.markdown("---")
    
    st.markdown("""
    ### **Quantum Maturity Scoring**
    
    Our five-tier scoring system provides clear, actionable insights:
    """)
    
    # Score legend with enhanced styling
    score_descriptions = [
        ('<div style="width: 30px; height: 30px; background: #DC2626; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">1</div>', "Level 1 - Initial", "Limited quantum awareness with significant gaps in understanding and preparation"),
        ('<div style="width: 30px; height: 30px; background: #EA580C; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">2</div>', "Level 2 - Developing", "Basic quantum concepts recognized but implementation strategies lacking"),
        ('<div style="width: 30px; height: 30px; background: #D97706; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">3</div>', "Level 3 - Defined", "Moderate quantum readiness with structured approaches emerging"),
        ('<div style="width: 30px; height: 30px; background: #059669; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">4</div>', "Level 4 - Managed", "Strong quantum capabilities with systematic risk management"),
        ('<div style="width: 30px; height: 30px; background: #7C3AED; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">5</div>', "Level 5 - Optimized", "Advanced quantum integration with comprehensive governance frameworks")
    ]
    
    for badge, level, description in score_descriptions:
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            padding: 0.8rem;
            margin: 0.5rem 0;
            background: #f8fafc;
            border-radius: 8px;
            border-left: 3px solid #e5e7eb;
        ">
            <div style="margin-right: 1rem;">{badge}</div>
            <div>
                <strong style="color: #374151;">{level}</strong><br>
                <span style="color: #6b7280; font-size: 0.9rem;">{description}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Research foundation section
    st.markdown("---")
    
    st.markdown("""
    ### **Research Foundation**
    
    GUARDIAN integrates cutting-edge research across multiple domains:
    
    - **AI Policy Evaluation**: Advanced NLP models for bias-free policy summarization and gap analysis
    - **Quantum Cybersecurity**: Post-quantum cryptography standards and maturity assessment frameworks
    - **Regulatory Compliance**: Integration with NIST, OECD, EU AI Act, and UNESCO AI Ethics guidelines
    - **Machine Learning Innovation**: Bayesian inference, reinforcement learning, and graph neural networks
    """)
    
    # Patent and IP section
    st.markdown("""
    ---
    
    ### **Patented Technology Foundation**
    
    GUARDIAN integrates three breakthrough patent technologies:
    
    **1. Real-Time Dynamic Governance Framework**
    - Adaptive AI-driven policy assessment with continuous learning
    - Multi-modal risk evaluation across cybersecurity and ethical domains
    - Real-time threat detection and mitigation recommendations
    
    **2. AI-Powered Policy Evaluation and Ethical Compliance System**
    - Hybrid policy collection via APIs, parsing, and compliant web scraping
    - Unbiased summarization using transformer models with bias detection
    - Cybersecurity and ethics gap analysis with quantifiable scoring
    - Reinforcement learning-based policy optimization and sandbox stress testing
    
    **3. Quantum Cybersecurity Framework for Policy Assessment**
    - Five-tier Quantum Cybersecurity Maturity Evaluation Algorithm (QCMEA)
    - Bayesian inference for dynamic threat assessment and policy updates
    - Graph Neural Networks for interdependency analysis and cascading risk detection
    - Post-quantum cryptography readiness evaluation and implementation guidance
    """)
    
    # Contact and development info
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 👥 **Development Team**
        
        **Principal Investigators:**
        - Andrew Vance, PhD
        - Taylor Rodriguez Vance, PhD
        
        **Institution:**
        - Cyber Institute
        - 5 Union Square West, Suite 1124
        - New York, NY 10003
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 **Future Developments**
        
        - Enhanced multilingual support
        - Expanded quantum technology coverage
        - Real-time regulatory update integration
        - Advanced visualization capabilities
        - API access for enterprise integration
        """)
    
    # Footer with version info
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280; font-size: 0.9rem; margin-top: 2rem;">
        <p>GUARDIAN Quantum Maturity Assessment Tool | Powered by Cyber Institute</p>
        <p>© 2024 Cyber Institute. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)