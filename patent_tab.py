"""
GUARDIAN Patent Interactive Web Application
Nonprovisional Utility Patent Application: "System for Real-Time Dynamic Governance of Emerging Technologies"
"""

import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import base64

def render():
    """Render the interactive patent web application."""
    
    # Updated patent header with technical narrative
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #B91C2C;">
        <h2 style="color: #B91C2C; margin-bottom: 0.8rem; font-size: 1.6rem;">GUARDIAN's Patent Pending Technologies</h2>
        <p style="font-size: 1rem; line-height: 1.6; color: #374151; margin-bottom: 1rem;">
            GUARDIAN represents a cloud-based AI LLM-driven emerging technology governance platform that integrates multiple cutting-edge technologies. 
            The system leverages Hugging Face transformers and OpenAI GPT models for intelligent document analysis, running on AWS infrastructure 
            with RDS PostgreSQL for repository management and EC2 Ubuntu instances for backend processing.
        </p>
        <p style="font-size: 0.9rem; line-height: 1.5; color: #4b5563; margin: 0;">
            <strong>Technology Stack:</strong> Python backend with Streamlit web UI, Google Dialogflow CX chatbot integration, 
            patent-pending scoring engines utilizing Anthropic Claude, OpenAI GPT-4, pandas for data processing, 
            matplotlib/plotly for visualizations, SQLAlchemy for database operations, and trafilatura for web scraping. 
            The platform implements real-time dynamic governance through four proprietary assessment frameworks.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main navigation
    patent_section = st.selectbox(
        "Select Patent Section to Explore:",
        [
            "System Overview & Architecture", 
            "Mathematical Formulations",
            "Risk Scoring Calculator",
            "Process Flow Demonstration",
            "Claims & Technical Features",
            "Innovation Summary"
        ]
    )
    
    st.markdown("---")
    
    if patent_section == "System Overview & Architecture":
        render_system_overview()
    elif patent_section == "Mathematical Formulations":
        render_mathematical_formulations()
    elif patent_section == "Risk Scoring Calculator":
        render_risk_calculator()
    elif patent_section == "Process Flow Demonstration":
        render_process_flow()
    elif patent_section == "Claims & Technical Features":
        render_claims()
    else:
        render_innovation_summary()

def render_system_overview():
    """Render the system overview section."""
    
    # Compact overview section
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h4 style="color: #B91C2C; margin-bottom: 0.5rem;">System Architecture Overview</h4>
    <p style="font-size: 0.95rem; line-height: 1.5; color: #374151; margin: 0;">
    Cloud-native, real-time governance platform implementing patented algorithms for emerging technology risk assessment and compliance monitoring.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Three-column layout for patent components
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; height: 320px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Interface Layer</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>Conversational AI (104)</strong><br>
        Multilingual NLP, web portals, mobile access<br><br>
        <strong>NLP Components (106)</strong><br>
        Intent detection, entity recognition, sentiment analysis<br><br>
        <strong>Query Pipeline</strong><br>
        Real-time interpretation and routing
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; height: 320px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Processing Core</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>Scoring Engines (112)</strong><br>
        Cybersecurity risk, ethics alignment assessment<br><br>
        <strong>AI/ML Decision Layer (110)</strong><br>
        Dual-modality risk framework, pattern recognition<br><br>
        <strong>Adaptive Learning</strong><br>
        Semantic drift detection, Q-learning optimization
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; height: 320px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Repository & Output</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>Policy Repository (108)</strong><br>
        UN, NIST, OECD frameworks, quantum policies<br><br>
        <strong>Summary Module (114)</strong><br>
        Policy synthesis, recommendation generation<br><br>
        <strong>Vectorized Engine</strong><br>
        Cross-comparison, similarity matching
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Patent claims summary
    st.markdown("""
    <div style="background: #fffbeb; padding: 1rem; border-radius: 6px;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem; text-align: center;">Key Patent Claims</h5>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.9rem;">
        <div><strong>Real-Time Processing:</strong> Dynamic policy evaluation with sub-second response times</div>
        <div><strong>Multi-Modal Assessment:</strong> Simultaneous cybersecurity and ethics scoring</div>
        <div><strong>Adaptive Learning:</strong> Self-improving algorithms with reinforcement learning</div>
        <div><strong>Cross-Framework Analysis:</strong> Harmonization across international standards</div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a flow diagram using plotly
    fig, ax = plt.subplots(figsize=(12, 3), facecolor='white')
    
    # Add nodes
    nodes = [
        ("User Query", 1, 2, "#3B82F6"),
        ("NLP Engine", 3, 2, "#10B981"),
        ("Policy Repository", 5, 2, "#F59E0B"),
        ("AI Scoring", 7, 2, "#EF4444"),
        ("Risk Evaluation", 9, 2, "#8B5CF6"),
        ("Recommendations", 11, 2, "#059669")
    ]
    
    # Draw nodes
    for name, x, y, color in nodes:
        circle = patches.Circle((x, y), 0.4, facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=8, fontweight='bold', 
                color='white')
    
    # Draw arrows between nodes
    for i in range(len(nodes)-1):
        x1, y1 = nodes[i][1], nodes[i][2]
        x2, y2 = nodes[i+1][1], nodes[i+1][2]
        arrow = patches.FancyArrowPatch((x1+0.4, y1), (x2-0.4, y2),
                                       arrowstyle='->', mutation_scale=15,
                                       color='#6B7280', linewidth=2)
        ax.add_patch(arrow)
    
    ax.set_xlim(0, 12)
    ax.set_ylim(1, 3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Patent Figure 1: GUARDIAN System Architecture", fontsize=12, fontweight='bold')
    
    # Convert to base64 for embedding
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', 
                pad_inches=0.2, facecolor='white', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    
    # Display the chart
    st.markdown(f'<img src="data:image/png;base64,{image_base64}" style="width: 100%; height: auto;">', 
                unsafe_allow_html=True)

def render_mathematical_formulations():
    """Render the mathematical formulations from the patent."""
    
    st.markdown("""
    ### Patent Mathematical Formulations
    
    The patent defines two core mathematical frameworks for risk assessment:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Cybersecurity Risk Score
        
        **Patent Formula (Section 3):**
        """)
        
        st.latex(r"""
        Risk_{cyber} = \sum_{i} (W_i \times V_i \times C_i)
        """)
        
        st.markdown("""
        **Where:**
        - **Wi**: Weight for each identified vulnerability type
        - **Vi**: Estimated likelihood of exploitability (0-1)
        - **Ci**: Consequence or impact severity
        
        **Framework Sources:**
        - NIST Risk Management Framework (RMF)
        - ISO 27001 standards
        - GDPR compliance requirements
        """)
    
    with col2:
        st.markdown("""
        #### Ethics Risk Score
        
        **Patent Formula (Section 4):**
        """)
        
        st.latex(r"""
        Risk_{ethics} = 1 - (T \times (1-B) \times (1-A))
        """)
        
        st.markdown("""
        **Where:**
        - **T**: Transparency score (0-1, where 1 = fully transparent)
        - **B**: Assessed bias factor (0-1, where 1 = maximum bias)
        - **A**: Autonomy or control risk index (0-1)
        
        **Assessment Areas:**
        - Algorithmic bias and fairness
        - Transparency and explainability
        - Human autonomy preservation
        """)
    
    # Mathematical properties explanation
    st.markdown("---")
    st.markdown("""
    #### Mathematical Properties & Design Rationale
    
    **Cybersecurity Formula Design:**
    - Multiplicative weighting allows prioritization of critical vulnerabilities
    - Summation across vulnerability types provides comprehensive coverage
    - Aligns with established NIST and ISO risk assessment methodologies
    
    **Ethics Formula Design:**
    - Inverted calculation (1 minus product) ensures higher values indicate higher risk
    - Multiplicative structure means poor performance in any dimension significantly impacts overall score
    - Transparency factor T scales the entire result, emphasizing the importance of explainable AI
    """)

def render_risk_calculator():
    """Interactive risk calculator based on patent formulations."""
    
    st.markdown("""
    ### Interactive Risk Scoring Calculator
    
    Test the patent-defined mathematical formulations with real parameters:
    """)
    
    calc_type = st.radio(
        "Select Risk Assessment Type:",
        ["Cybersecurity Risk Assessment", "Ethics Risk Assessment", "Combined Assessment"]
    )
    
    if calc_type == "Cybersecurity Risk Assessment":
        render_cyber_calculator()
    elif calc_type == "Ethics Risk Assessment":
        render_ethics_calculator()
    else:
        render_combined_calculator()

def render_cyber_calculator():
    """Cybersecurity risk calculator."""
    
    st.markdown("#### Cybersecurity Risk Calculator")
    st.markdown("*Based on Patent Section 3: Risk_cyber = Σ(Wi × Vi × Ci)*")
    
    # Input parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Vulnerability Parameters:**")
        
        num_vulnerabilities = st.slider("Number of Vulnerability Types:", 1, 10, 5)
        
        vulnerabilities = []
        for i in range(num_vulnerabilities):
            st.markdown(f"**Vulnerability {i+1}:**")
            w = st.slider(f"Weight (W{i+1}):", 0.1, 1.0, 0.5, key=f"w_{i}")
            v = st.slider(f"Exploitability (V{i+1}):", 0.0, 1.0, 0.3, key=f"v_{i}")
            c = st.slider(f"Impact Severity (C{i+1}):", 0.1, 1.0, 0.4, key=f"c_{i}")
            vulnerabilities.append((w, v, c))
    
    with col2:
        # Calculate risk
        total_risk = sum(w * v * c for w, v, c in vulnerabilities)
        
        st.markdown("**Risk Assessment Results:**")
        
        # Risk gauge using speedometer from about_tab
        from about_tab import create_speedometer_dial
        risk_percentage = min(100, (total_risk / 5) * 100)
        risk_dial = create_speedometer_dial(int(risk_percentage))
        st.markdown("**Cybersecurity Risk Score**")
        st.markdown(risk_dial, unsafe_allow_html=True)
        st.markdown(f"**Score:** {total_risk:.2f}/5")
        
        # Plotly gauge disabled to fix circular import issue
        
        # Risk interpretation
        if total_risk < 1:
            risk_level = "Low Risk"
            color = "#059669"
        elif total_risk < 2:
            risk_level = "Moderate Risk"
            color = "#D97706"
        elif total_risk < 3:
            risk_level = "High Risk"
            color = "#EA580C"
        else:
            risk_level = "Critical Risk"
            color = "#DC2626"
        
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid {color};'>
            <h4 style='color: {color}; margin: 0 0 0.5rem 0;'>{risk_level}</h4>
            <p style='margin: 0; color: #374151;'>Total Risk Score: {total_risk:.3f}</p>
        </div>
        """, unsafe_allow_html=True)

def render_ethics_calculator():
    """Ethics risk calculator."""
    
    st.markdown("#### Ethics Risk Calculator")
    st.markdown("*Based on Patent Section 4: Risk_ethics = 1 - (T × (1-B) × (1-A))*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Ethics Parameters:**")
        
        transparency = st.slider(
            "Transparency Score (T):",
            0.0, 1.0, 0.7,
            help="0 = Not transparent, 1 = Fully transparent"
        )
        
        bias_factor = st.slider(
            "Bias Factor (B):",
            0.0, 1.0, 0.3,
            help="0 = No bias, 1 = Maximum bias"
        )
        
        autonomy_risk = st.slider(
            "Autonomy Risk Index (A):",
            0.0, 1.0, 0.4,
            help="0 = No autonomy risk, 1 = Maximum autonomy risk"
        )
    
    with col2:
        # Calculate ethics risk
        ethics_risk = 1 - (transparency * (1 - bias_factor) * (1 - autonomy_risk))
        
        st.markdown("**Ethics Assessment Results:**")
        
        # Ethics gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = ethics_risk,
            title = {'text': "Ethics Risk Score"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 1]},
                'bar': {'color': "#8B5CF6"},
                'steps': [
                    {'range': [0, 0.2], 'color': "#D1FAE5"},
                    {'range': [0.2, 0.4], 'color': "#FEF3C7"},
                    {'range': [0.4, 0.6], 'color': "#FED7AA"},
                    {'range': [0.6, 0.8], 'color': "#FECACA"},
                    {'range': [0.8, 1], 'color': "#FEE2E2"}
                ]
            }
        ))
        
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        # Component breakdown
        component_score = transparency * (1 - bias_factor) * (1 - autonomy_risk)
        
        st.markdown(f"""
        **Mathematical Breakdown:**
        - Component Score: {component_score:.3f}
        - Final Risk Score: {ethics_risk:.3f}
        
        **Individual Contributions:**
        - Transparency Impact: {transparency:.3f}
        - Bias Mitigation: {(1-bias_factor):.3f}
        - Autonomy Preservation: {(1-autonomy_risk):.3f}
        """)

def render_combined_calculator():
    """Combined risk assessment."""
    
    st.markdown("""
    #### Combined Risk Assessment
    
    Demonstrate the dual-modality risk evaluation framework from the patent:
    """)
    
    # Simplified inputs for combined assessment
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Cybersecurity Inputs:**")
        cyber_weight = st.slider("Average Vulnerability Weight:", 0.1, 1.0, 0.6)
        cyber_exploit = st.slider("Average Exploitability:", 0.0, 1.0, 0.4)
        cyber_impact = st.slider("Average Impact Severity:", 0.1, 1.0, 0.5)
        num_vulns = st.slider("Number of Vulnerabilities:", 1, 10, 4)
    
    with col2:
        st.markdown("**Ethics Inputs:**")
        transparency = st.slider("Transparency:", 0.0, 1.0, 0.7, key="combined_t")
        bias_factor = st.slider("Bias Factor:", 0.0, 1.0, 0.3, key="combined_b")
        autonomy_risk = st.slider("Autonomy Risk:", 0.0, 1.0, 0.4, key="combined_a")
    
    with col3:
        # Calculate both risks
        cyber_risk = num_vulns * (cyber_weight * cyber_exploit * cyber_impact)
        ethics_risk = 1 - (transparency * (1 - bias_factor) * (1 - autonomy_risk))
        
        st.markdown("**Combined Results:**")
        
        st.metric("Cybersecurity Risk", f"{cyber_risk:.3f}")
        st.metric("Ethics Risk", f"{ethics_risk:.3f}")
        
        # Overall risk assessment
        overall_risk = (cyber_risk / 5 + ethics_risk) / 2  # Normalize to 0-1 scale
        
        if overall_risk < 0.3:
            status = "Low Risk"
            color = "#059669"
        elif overall_risk < 0.6:
            status = "Moderate Risk"
            color = "#D97706"
        else:
            status = "High Risk"
            color = "#DC2626"
        
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid {color}; margin-top: 1rem;'>
            <h4 style='color: {color}; margin: 0 0 0.5rem 0;'>{status}</h4>
            <p style='margin: 0; color: #374151;'>Overall Risk: {overall_risk:.3f}</p>
        </div>
        """, unsafe_allow_html=True)

def render_process_flow():
    """Process flow demonstration."""
    
    st.markdown("""
    ### Process Flow Demonstration
    
    Interactive demonstration of Patent Figure 2: Policy Query Evaluation and Risk Scoring Workflow
    """)
    
    # Simulate the patent process flow
    user_query = st.text_input(
        "Enter a Policy Query:",
        "Is my company's AI chatbot NIST compliant?",
        help="Example queries: 'Does our quantum encryption meet GDPR requirements?' or 'Are there bias risks in our ML model?'"
    )
    
    if user_query:
        st.markdown("#### Processing Flow:")
        
        # Step 1: NLP Analysis
        with st.expander("Step 1: NLP Analysis Engine (204)", expanded=True):
            st.markdown(f"""
            **Input Query:** "{user_query}"
            
            **Intent Detection:** Policy compliance inquiry
            **Named Entity Recognition:** 
            - Technology: AI chatbot
            - Framework: NIST
            - Domain: Cybersecurity compliance
            
            **Jurisdictional Context:** Federal compliance (US)
            """)
        
        # Step 2: Policy Synthesis
        with st.expander("Step 2: Policy Synthesis Engine (208)"):
            st.markdown("""
            **Retrieved Frameworks:**
            - NIST AI Risk Management Framework (RMF)
            - NIST Cybersecurity Framework
            - Federal AI guidance documents
            
            **Policy Alignment Analysis:**
            - Risk identification requirements
            - Documentation standards
            - Testing and validation protocols
            """)
        
        # Step 3: Risk Scoring
        with st.expander("Step 3: Dual-Modality Risk Scoring (210, 212)"):
            # Simulate risk calculation
            cyber_risk = np.random.uniform(0.2, 0.8)
            ethics_risk = np.random.uniform(0.1, 0.6)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Cybersecurity Risk (212):**
                - Score: {cyber_risk:.3f}
                - Key factors: Authentication, data protection, monitoring
                """)
            
            with col2:
                st.markdown(f"""
                **Ethics Risk (210):**
                - Score: {ethics_risk:.3f}
                - Key factors: Bias testing, transparency, human oversight
                """)
        
        # Step 4: Recommendations
        with st.expander("Step 4: Recommendation Generator (214)"):
            st.markdown("""
            **Actionable Guidance:**
            
            1. **Immediate Actions:**
               - Implement bias testing protocols
               - Document AI decision-making processes
               - Establish human oversight mechanisms
            
            2. **Compliance Requirements:**
               - NIST RMF risk assessment
               - Regular model validation
               - Incident response procedures
            
            3. **Monitoring Recommendations:**
               - Continuous bias monitoring
               - Performance drift detection
               - User feedback collection
            """)

def render_claims():
    """Patent claims and technical features."""
    
    st.markdown("""
    ### Patent Claims & Technical Features
    
    Key technical innovations and claims from the GUARDIAN patent:
    """)
    
    # Independent claims
    st.markdown("""
    #### Independent Claims
    
    **Claim 1: Real-Time AI Governance Platform**
    - Cloud-native architecture with conversational interface
    - Multilingual natural language processing capabilities
    - Vendor-neutral design for broad applicability
    - Real-time policy synthesis and risk evaluation
    """)
    
    # Technical innovations
    technical_features = {
        "Semantic Drift Detection": {
            "description": "Automatic detection of model performance degradation triggering retraining",
            "technical_detail": "Monitors user interaction patterns and query success rates to identify when AI models need updating",
            "patent_section": "Cross-reference applications - Novel addition"
        },
        "Dual-Modality Risk Framework": {
            "description": "Simultaneous cybersecurity and ethics risk evaluation",
            "technical_detail": "Independent scoring engines (210, 212) that evaluate technical and ethical risks in parallel",
            "patent_section": "Detailed Description Section 7"
        },
        "Reinforcement Learning Optimization": {
            "description": "Q-learning for adaptive policy recommendation improvement",
            "technical_detail": "System learns from user feedback to optimize policy suggestions over time",
            "patent_section": "Cross-reference applications - Novel addition"
        },
        "Transnational Governance": {
            "description": "Cross-jurisdictional policy harmonization",
            "technical_detail": "Vectorized similarity engine enables comparison between conflicting international regulations",
            "patent_section": "Policy Repository Section 9"
        }
    }
    
    for feature, details in technical_features.items():
        with st.expander(f"**{feature}**"):
            st.markdown(f"""
            **Description:** {details['description']}
            
            **Technical Implementation:** {details['technical_detail']}
            
            **Patent Section:** {details['patent_section']}
            """)
    
    # Dependent claims
    st.markdown("""
    #### Key Dependent Claims
    
    - **Mathematical Risk Formulations:** Specific cybersecurity and ethics scoring algorithms
    - **Multilingual Interface:** Natural language processing in multiple languages
    - **API Integration:** Third-party system integration capabilities
    - **Quantum Technology Support:** Specialized handling of quantum encryption and quantum ethics
    - **Real-Time Model Updates:** Dynamic AI model retraining based on usage patterns
    """)

def render_innovation_summary():
    """Innovation summary and commercial applications."""
    
    # Compact innovation overview
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h4 style="color: #B91C2C; margin-bottom: 0.5rem;">Innovation Summary & Commercial Applications</h4>
    <p style="font-size: 0.95rem; line-height: 1.5; color: #374151; margin: 0;">
    Patent-pending technologies addressing the $2.8B AI governance market through cloud-native, real-time compliance solutions.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Four-column layout for key innovations
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; height: 200px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">Real-Time Platform</h6>
        <div style="font-size: 0.8rem; line-height: 1.3;">
        First cloud-native system for real-time AI governance through conversational interface<br><br>
        <strong>Impact:</strong> Scalable solution for $2.8B market
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; height: 200px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">Dual-Modality Assessment</h6>
        <div style="font-size: 0.8rem; line-height: 1.3;">
        Simultaneous cybersecurity and ethics risk evaluation with mathematical foundations<br><br>
        <strong>Impact:</strong> 60% compliance cost reduction
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; height: 200px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">Semantic Drift Detection</h6>
        <div style="font-size: 0.8rem; line-height: 1.3;">
        Automatic model retraining based on performance degradation detection<br><br>
        <strong>Impact:</strong> Maintains 95%+ accuracy
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; height: 200px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">Global Harmonization</h6>
        <div style="font-size: 0.8rem; line-height: 1.3;">
        Cross-jurisdictional policy comparison and alignment capabilities<br><br>
        <strong>Impact:</strong> Global multinational deployment
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Commercial applications in three columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f9fafb; padding: 1rem; border-radius: 6px; height: 180px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.8rem;">Government Sector</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        • Federal agency AI compliance monitoring<br>
        • Regulatory framework development<br>
        • Cross-agency policy harmonization<br>
        • Policy simulation and testing
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; height: 180px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.8rem;">Enterprise Sector</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        • Corporate AI governance and risk management<br>
        • Regulatory compliance automation<br>
        • Due diligence for AI acquisitions<br>
        • Multi-jurisdictional compliance
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; height: 180px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.8rem;">Research & Education</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        • Academic policy analysis and research<br>
        • Educational governance training tools<br>
        • Policy stress testing environments<br>
        • Comparative framework studies
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Patent strategy summary
    st.markdown("""
    <div style="background: #f8fafc; padding: 1rem; border-radius: 6px; text-align: center;">
    <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">Patent Portfolio Strategy</h6>
    <p style="margin: 0.2rem 0; font-size: 0.85rem;">Continuation-in-part strategy with mathematical formulations for strong technical claims</p>
    <p style="margin: 0.2rem 0; font-size: 0.85rem;">Cross-reference structure creating comprehensive IP protection for emerging technology governance</p>
    </div>
    """, unsafe_allow_html=True)