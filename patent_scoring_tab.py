"""
Patent-Based Scoring Systems Tab
Demonstrates the specific frameworks from the three GUARDIAN patents
"""

import streamlit as st
import numpy as np
from utils.patent_scoring import draw_qcmea_scorecard, draw_ai_ethics_scorecard, calculate_cybersecurity_gap_score

def render():
    """Render the Patent-Based Scoring Systems tab."""
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #082454 0%, #10244D 50%, #133169 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
    ">
        <h2 style="color: white; margin-bottom: 1rem; font-size: 2.2rem; text-align: center;">
            Patent-Based Scoring Frameworks
        </h2>
        <p style="font-size: 1.1rem; line-height: 1.7; color: #e5e7eb; text-align: center;">
            Demonstrating the specific assessment frameworks defined in GUARDIAN's three foundational patents
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Framework selection
    framework_choice = st.selectbox(
        "Select Patent Framework to Demonstrate:",
        [
            "Quantum Cybersecurity Maturity Evaluation (QCMEA)",
            "AI Ethics & Cybersecurity Assessment", 
            "Cybersecurity & Ethics Gap Analysis"
        ]
    )
    
    st.markdown("---")
    
    if framework_choice == "Quantum Cybersecurity Maturity Evaluation (QCMEA)":
        render_qcmea_demo()
    elif framework_choice == "AI Ethics & Cybersecurity Assessment":
        render_ai_ethics_demo()
    else:
        render_gap_analysis_demo()

def render_qcmea_demo():
    """Demonstrate the QCMEA 5-tier framework from Quantum Policy patent."""
    
    st.markdown("""
    ### Quantum Cybersecurity Maturity Evaluation Algorithm (QCMEA)
    
    **Patent Source:** "Quantum Cybersecurity Framework for Policy Assessment and Maturity Evaluation"  
    **Framework Definition:** Patent sections 4-10, five-tier structured maturity model
    """)
    
    # Interactive scoring
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Test the Framework")
        
        # Maturity level selector
        maturity_level = st.slider(
            "Set Quantum Cybersecurity Maturity Level:",
            min_value=1,
            max_value=5,
            value=3,
            help="Levels as defined in patent sections 5-9"
        )
        
        # Sample organization types
        org_type = st.selectbox(
            "Organization Type:",
            ["Government Agency", "Financial Institution", "Healthcare System", "Technology Company", "Research Institution"]
        )
    
    with col2:
        st.markdown("#### QCMEA Assessment Results")
        draw_qcmea_scorecard(f"{org_type} - Quantum Cybersecurity Maturity", maturity_level)
    
    # Patent details
    st.markdown("---")
    st.markdown("""
    #### Patent Framework Details
    
    **Core Components Supporting QCMEA (Patent Section 11):**
    - **Bayesian Inference:** Dynamic maturity evaluation updates
    - **Graph Neural Networks (GNNs):** Interdependency analysis for systemic risks
    - **Reinforcement Learning (RL):** Policy optimization through iterative simulations
    - **Simulation and Validation:** Quantum risk scenario testing (e.g., AES-256 vs CRYSTALS-Kyber)
    
    **Centralized Policy Repository (Patent Section 12):**
    - NIST Post-Quantum Cryptography Standards
    - GDPR quantum-safe provisions
    - EU Quantum Technologies Flagship Initiative
    """)

def render_ai_ethics_demo():
    """Demonstrate the AI Ethics 0-100 scoring from AI Policy patent."""
    
    st.markdown("""
    ### AI Ethics & Cybersecurity Assessment Framework
    
    **Patent Source:** "AI-Powered Policy Evaluation and Ethical Compliance System"  
    **Framework Definition:** Patent section 21, four primary scoring criteria (0-100 scale)
    """)
    
    # Interactive scoring controls
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Adjust Scores")
        
        ecs_score = st.slider(
            "Ethical Compliance Score (ECS):",
            min_value=0,
            max_value=100,
            value=75,
            help="Patent section 21: Measures bias mitigation, discrimination prevention, privacy protection"
        )
        
        as_score = st.slider(
            "Adaptability Score (AS):",
            min_value=0,
            max_value=100,
            value=60,
            help="Patent section 21: Evaluates ability to adapt to future AI advancements"
        )
        
        las_score = st.slider(
            "Legal Alignment Score (LAS):",
            min_value=0,
            max_value=100,
            value=85,
            help="Patent section 21: Compliance with OECD AI Principles, EU AI Act, UNESCO AI Ethics"
        )
        
        ifs_score = st.slider(
            "Implementation Feasibility Score (IFS):",
            min_value=0,
            max_value=100,
            value=70,
            help="Patent section 21: Likelihood of successful real-world policy adoption"
        )
        
        policy_type = st.selectbox(
            "Policy Type:",
            ["AI Hiring Policy", "Healthcare AI Governance", "Financial AI Compliance", "Autonomous Vehicle Regulation", "AI Research Ethics"]
        )
    
    with col2:
        st.markdown("#### Assessment Dashboard")
        draw_ai_ethics_scorecard(f"{policy_type} Assessment", ecs_score, as_score, las_score, ifs_score)
    
    # Patent scoring criteria details
    st.markdown("---")
    st.markdown("""
    #### Patent-Defined Scoring Criteria (Section 21)
    
    **Ethical Compliance Score (ECS) - Range: 0 (high risk) to 100 (fully ethical)**
    - Bias mitigation effectiveness
    - Discrimination prevention measures
    - Privacy protection mechanisms
    - Example: AI hiring policy excluding marginalized groups receives penalty
    
    **Adaptability Score (AS) - Future compatibility assessment**
    - Policy flexibility for AI advancement
    - Innovation accommodation
    - Example: Over-regulation hindering innovation results in lower AS score
    
    **Legal Alignment Score (LAS) - Global regulatory compliance**
    - OECD AI Principles alignment
    - EU AI Act compliance
    - UNESCO AI Ethics conformity
    - Example: GDPR contradiction reduces LAS score
    
    **Implementation Feasibility Score (IFS) - Real-world adoption prediction**
    - Practical constraint assessment
    - Industry resistance evaluation
    - Infrastructure requirement analysis
    - Example: Mandating open-source AI models may face resistance, lowering IFS
    """)

def render_gap_analysis_demo():
    """Demonstrate the Gap Analysis framework from AI Policy patent."""
    
    st.markdown("""
    ### Cybersecurity & Ethics Gap Analysis
    
    **Patent Source:** "AI-Powered Policy Evaluation and Ethical Compliance System"  
    **Framework Definition:** Patent section 16, machine learning-powered gap score calculation
    """)
    
    # Sample policy text input
    st.markdown("#### Test Policy Document")
    
    sample_policies = {
        "Strong AI Governance Policy": """This policy establishes comprehensive guidelines for AI deployment including robust encryption protocols, 
        multi-factor authentication systems, granular access control mechanisms, and continuous data protection measures. 
        The framework mandates regular threat detection audits, structured incident response procedures, systematic vulnerability assessments, 
        and real-time security monitoring. Risk management protocols ensure compliance with regulatory standards. 
        Ethical provisions include algorithmic bias mitigation strategies, fairness assessment protocols, full transparency in AI decision-making, 
        clear accountability structures, comprehensive privacy protection measures, mandatory human oversight for critical decisions, 
        active discrimination prevention programs, regular ethical review processes, structured stakeholder engagement, 
        and thorough impact assessment procedures.""",
        
        "Basic AI Policy": """This policy covers basic AI usage guidelines. Systems should use standard security measures 
        and follow general ethical principles. Regular reviews will be conducted to ensure compliance.""",
        
        "Comprehensive Security Policy": """Advanced encryption standards, biometric authentication, role-based access control, 
        data loss prevention, AI-powered threat detection, automated incident response, continuous vulnerability scanning, 
        SIEM monitoring, enterprise risk management, regulatory compliance frameworks."""
    }
    
    selected_policy = st.selectbox("Select Sample Policy:", list(sample_policies.keys()))
    
    policy_text = st.text_area(
        "Policy Text (edit to see real-time gap analysis):",
        value=sample_policies[selected_policy],
        height=150,
        help="Patent formula analyzes cybersecurity and ethics provision coverage"
    )
    
    if policy_text:
        # Calculate gap score using patent formula
        gap_analysis = calculate_cybersecurity_gap_score(policy_text)
        
        # Display results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Gap Score",
                f"{gap_analysis['gap_score']:.3f}",
                help="Patent Formula: 1 - ((Cmatch/Ctotal) + (Ematch/Etotal))/2"
            )
        
        with col2:
            st.metric(
                "Cybersecurity Coverage",
                f"{gap_analysis['cybersecurity_coverage']:.1f}%",
                f"{gap_analysis['cybersecurity_matches']}/{gap_analysis['total_cybersecurity']} provisions"
            )
        
        with col3:
            st.metric(
                "Ethics Coverage", 
                f"{gap_analysis['ethics_coverage']:.1f}%",
                f"{gap_analysis['ethics_matches']}/{gap_analysis['total_ethics']} provisions"
            )
        
        # Gap score interpretation
        if gap_analysis['gap_score'] < 0.3:
            interpretation = "Excellent coverage - minimal gaps detected"
            color = "#059669"
        elif gap_analysis['gap_score'] < 0.5:
            interpretation = "Good coverage - minor gaps to address"
            color = "#D97706" 
        elif gap_analysis['gap_score'] < 0.7:
            interpretation = "Moderate gaps - significant improvements needed"
            color = "#EA580C"
        else:
            interpretation = "Major gaps - comprehensive policy revision required"
            color = "#DC2626"
        
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; border-left: 4px solid {color}; margin: 1rem 0;'>
            <h4 style='color: {color}; margin: 0 0 0.5rem 0;'>Gap Analysis Result</h4>
            <p style='margin: 0; color: #374151;'>{interpretation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Patent formula explanation
    st.markdown("---")
    st.markdown("""
    #### Patent Gap Score Formula (Section 16)
    
    **Mathematical Definition:**
    ```
    Gpolicy = 1 - ((Cmatch/Ctotal) + (Ematch/Etotal))/2
    ```
    
    Where:
    - **Gpolicy**: Cybersecurity and ethics gap score
    - **Cmatch**: Number of cybersecurity provisions found in policy
    - **Ctotal**: Expected cybersecurity provisions (patent-defined list)
    - **Ematch**: Number of ethics provisions found in policy  
    - **Etotal**: Expected ethical provisions (patent-defined list)
    
    **Patent-Defined Provision Categories:**
    - **Cybersecurity**: Encryption, authentication, access control, threat detection, incident response, etc.
    - **Ethics**: Bias mitigation, fairness, transparency, accountability, privacy protection, etc.
    
    **Output**: Comprehensive compliance report with detected gaps and enhancement suggestions
    """)