import streamlit as st
import plotly.graph_objects as go

def create_scoring_gauge(title, value, max_value=100, color_scheme="cybersecurity"):
    """Create a compact needle gauge for scoring visualization."""
    
    # Define vibrant color schemes
    color_schemes = {
        "cybersecurity": {
            "low": "#FF0000",      # Bright Red
            "medium": "#FF6600",   # Bright Orange  
            "good": "#00CC00",     # Bright Green
            "excellent": "#009900" # Dark Bright Green
        },
        "ethics": {
            "low": "#FF0000",      # Bright Red
            "medium": "#FF9900",   # Bright Amber
            "good": "#00AA00",     # Bright Emerald
            "excellent": "#007700" # Dark Bright Emerald
        }
    }
    
    colors = color_schemes.get(color_scheme, color_schemes["cybersecurity"])
    
    # Determine color based on value
    if value <= 25:
        needle_color = colors["low"]
        performance = "Needs Improvement"
    elif value <= 50:
        needle_color = colors["medium"] 
        performance = "Developing"
    elif value <= 75:
        needle_color = colors["good"]
        performance = "Good"
    else:
        needle_color = colors["excellent"]
        performance = "Excellent"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0.1, 0.9]},
        title = {'text': f"<b style='font-size:0.9em'>{title}</b>"},
        number = {'font': {'size': 20, 'color': needle_color}},
        gauge = {
            'axis': {
                'range': [None, max_value], 
                'tickwidth': 1, 
                'tickcolor': "#333333",
                'tickfont': {'size': 10}
            },
            'bar': {
                'color': needle_color, 
                'thickness': 0.15,  # Thinner needle
                'line': {'color': "#000000", 'width': 1}
            },
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#333333",
            'steps': [
                {'range': [0, 25], 'color': '#FF4444'},      # Bright red zone
                {'range': [25, 50], 'color': '#FF8844'},     # Bright orange zone
                {'range': [50, 75], 'color': '#44CC44'},     # Bright green zone
                {'range': [75, max_value], 'color': '#22AA22'}  # Dark bright green zone
            ],
            'threshold': {
                'line': {'color': "#333333", 'width': 2},
                'thickness': 0.8,
                'value': 75  # Excellence threshold
            }
        }
    ))
    
    fig.update_layout(
        height=150,  # More compact
        font={'color': "#333333", 'family': "Arial"},
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

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
            <strong>GUARDIAN</strong> (Governance Using AI for Risk Detection, Integration, Analysis, and Notification) is a 
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
    ### **Quantum Cybersecurity Maturity Scoring**
    
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
    
    # AI Cybersecurity Maturity Scoring section
    st.markdown("---")
    
    st.markdown("""
    ### **AI Cybersecurity Maturity Scoring (0-100 Scale)**
    
    This framework evaluates AI-specific cybersecurity implementations across four critical domains:
    """)
    
    ai_cyber_criteria = [
        ("**AI Data Security & Integrity (25 points)**", [
            "Training data encryption and access controls (0-5 points)",
            "Data poisoning detection and mitigation systems (0-6 points)",
            "Model versioning and integrity verification (0-5 points)", 
            "Secure data pipelines and preprocessing validation (0-5 points)",
            "Privacy-preserving techniques (differential privacy, federated learning) (0-4 points)"
        ]),
        ("**AI Model Protection (25 points)**", [
            "Model extraction and inversion attack prevention (0-8 points)",
            "Adversarial robustness testing and hardening (0-8 points)",
            "Secure model deployment and serving infrastructure (0-9 points)"
        ]),
        ("**AI Authentication & Access Control (25 points)**", [
            "Multi-factor authentication for AI systems (0-8 points)",
            "Role-based access control for model management (0-8 points)",
            "API security and rate limiting for AI services (0-9 points)"
        ]),
        ("**AI Incident Response & Monitoring (25 points)**", [
            "Real-time AI system monitoring and anomaly detection (0-8 points)",
            "AI-specific incident response procedures (0-8 points)",
            "Threat intelligence integration for AI vulnerabilities (0-9 points)"
        ])
    ]
    
    for category, criteria in ai_cyber_criteria:
        st.markdown(f"**{category}**")
        for criterion in criteria:
            st.markdown(f"- {criterion}")
        st.markdown("")
    
    st.markdown("**Score Progression:**")
    
    # Create interactive gauges for AI Cybersecurity scoring
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fig1 = create_scoring_gauge("Basic Level", 15, color_scheme="cybersecurity")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**0-25**: Basic awareness, minimal AI security measures")
    
    with col2:
        fig2 = create_scoring_gauge("Developing", 37, color_scheme="cybersecurity")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**26-50**: Developing capabilities, some AI-specific protections")
    
    with col3:
        fig3 = create_scoring_gauge("Comprehensive", 62, color_scheme="cybersecurity")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**51-75**: Comprehensive AI security framework with most controls")
    
    with col4:
        fig4 = create_scoring_gauge("Advanced", 85, color_scheme="cybersecurity")
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("**76-100**: Advanced AI cybersecurity with cutting-edge protections")
    
    # AI Ethics Scoring section
    st.markdown("---")
    
    st.markdown("""
    ### **AI Ethics Scoring (0-100 Scale)**
    
    This framework assesses ethical AI implementation across fairness, transparency, accountability, and privacy:
    """)
    
    ai_ethics_criteria = [
        ("**Fairness & Bias Mitigation (25 points)**", [
            "Pre-training bias assessment and data auditing (0-5 points)",
            "Algorithmic bias detection across protected classes (0-6 points)",
            "Post-deployment bias monitoring and correction (0-5 points)",
            "Diverse training data and representative datasets (0-5 points)",
            "Fairness-aware machine learning implementation (0-4 points)"
        ]),
        ("**Transparency & Explainability (25 points)**", [
            "Model interpretability and explanation capabilities (0-8 points)",
            "Decision audit trails and reasoning documentation (0-8 points)",
            "Clear AI disclosure to end users (0-9 points)"
        ]),
        ("**Accountability & Governance (25 points)**", [
            "AI ethics review boards and oversight committees (0-8 points)",
            "Responsibility frameworks for AI decisions (0-8 points)",
            "Compliance with ethical AI guidelines and standards (0-9 points)"
        ]),
        ("**Privacy & Human Rights (25 points)**", [
            "Data minimization and purpose limitation (0-8 points)",
            "Consent management and user control mechanisms (0-8 points)",
            "Human oversight and intervention capabilities (0-9 points)"
        ])
    ]
    
    for category, criteria in ai_ethics_criteria:
        st.markdown(f"**{category}**")
        for criterion in criteria:
            st.markdown(f"- {criterion}")
        st.markdown("")
    
    st.markdown("**Score Progression:**")
    
    # Create interactive gauges for AI Ethics scoring
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fig1 = create_scoring_gauge("Limited", 18, color_scheme="ethics")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**0-25**: Limited ethical considerations, reactive approach")
    
    with col2:
        fig2 = create_scoring_gauge("Basic", 40, color_scheme="ethics")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**26-50**: Basic ethical frameworks, some accountability measures")
    
    with col3:
        fig3 = create_scoring_gauge("Comprehensive", 65, color_scheme="ethics")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**51-75**: Comprehensive ethical AI practices with regular assessment")
    
    with col4:
        fig4 = create_scoring_gauge("Leading-edge", 88, color_scheme="ethics")
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("**76-100**: Leading-edge ethical AI with proactive governance")
    
    # Quantum Ethics Scoring section
    st.markdown("---")
    
    st.markdown("""
    ### **Quantum Ethics Scoring (0-100 Scale)**
    
    This emerging framework evaluates ethical considerations specific to quantum computing technologies:
    """)
    
    quantum_ethics_criteria = [
        ("**Quantum Advantage Ethics (25 points)**", [
            "Responsible use of quantum computational advantages (0-8 points)",
            "Prevention of quantum supremacy abuse and monopolization (0-8 points)",
            "Equitable access to quantum computational resources (0-9 points)"
        ]),
        ("**Quantum Privacy & Security (25 points)**", [
            "Quantum-safe privacy protection measures (0-8 points)",
            "Ethical quantum cryptography implementation (0-8 points)",
            "Protection against quantum-enabled surveillance (0-9 points)"
        ]),
        ("**Quantum Research Ethics (25 points)**", [
            "Responsible quantum research practices and disclosure (0-8 points)",
            "International cooperation and knowledge sharing (0-8 points)",
            "Quantum technology dual-use considerations (0-9 points)"
        ]),
        ("**Societal Impact & Accessibility (25 points)**", [
            "Quantum technology impact assessment and mitigation (0-8 points)",
            "Educational initiatives and workforce development (0-8 points)",
            "Bridging quantum digital divide and ensuring inclusion (0-9 points)"
        ])
    ]
    
    for category, criteria in quantum_ethics_criteria:
        st.markdown(f"**{category}**")
        for criterion in criteria:
            st.markdown(f"- {criterion}")
        st.markdown("")
    
    st.markdown("**Score Progression:**")
    
    # Create interactive gauges for Quantum Ethics scoring
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fig1 = create_scoring_gauge("Minimal", 20, color_scheme="ethics")
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("**0-25**: Minimal quantum ethics awareness, basic compliance only")
    
    with col2:
        fig2 = create_scoring_gauge("Developing", 42, color_scheme="ethics")
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("**26-50**: Developing quantum ethics frameworks and policies")
    
    with col3:
        fig3 = create_scoring_gauge("Comprehensive", 68, color_scheme="ethics")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("**51-75**: Comprehensive quantum ethics integration with monitoring")
    
    with col4:
        fig4 = create_scoring_gauge("Leadership", 90, color_scheme="ethics")
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("**76-100**: Advanced quantum ethics leadership with innovation")
    
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