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
            <strong>GUARDIAN</strong> (Global Unified AI Risk Discovery & Impact Analysis Navigator) is an 
            AI-powered governance platform that provides real-time assessment and analysis of emerging 
            technology policies, with specialized focus on AI cybersecurity and quantum maturity evaluations and their ethical implementations.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.7; color: #374151;">
            Developed by the Cyber Institute, this system bridges the gap between complex regulatory 
            frameworks and practical compliance needs for organizations navigating the emerging technologies landscape.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Core capabilities section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 **Core Capabilities**
        
        **Real-Time Policy Analysis**
        - Instant evaluation of documents against quantum readiness frameworks
        - Dynamic scoring using AI-powered assessment algorithms
        - Cross-jurisdictional policy harmonization
        
        **Intelligent Document Classification**
        - Automatic detection of document types (policies, standards, strategies)
        - Context-aware analysis tailored to document purpose
        - Semantic understanding of regulatory language
        
        **Quantum Maturity Assessment**
        - Five-tier scoring system (🔴🟠🟡🟢🟣)
        - Comprehensive risk evaluation across multiple dimensions
        - Actionable insights for quantum readiness improvement
        """)
    
    with col2:
        st.markdown("""
        ### 🌐 **Who Benefits?**
        
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
    ### 🔧 **Technical Architecture**
    
    GUARDIAN employs a sophisticated multi-layered approach to governance analysis:
    """)
    
    # Architecture components
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🧠 AI Decision Layer**
        - Transformer-based language models
        - Named Entity Recognition (NER)
        - Semantic vector comparison
        - Reinforcement learning optimization
        """)
    
    with col2:
        st.markdown("""
        **📊 Risk Evaluation Engine**
        - Cybersecurity risk scoring
        - Ethical alignment assessment
        - Dual-modality risk framework
        - Real-time threat simulation
        """)
    
    with col3:
        st.markdown("""
        **🔄 Adaptive Learning**
        - Continuous model refinement
        - Semantic drift detection
        - User feedback integration
        - Dynamic policy updates
        """)
    
    # Scoring methodology section
    st.markdown("---")
    
    st.markdown("""
    ### 📈 **Quantum Maturity Scoring**
    
    Our five-tier scoring system provides clear, actionable insights:
    """)
    
    # Score legend with enhanced styling
    score_descriptions = [
        ("🔴", "Level 1 - Initial", "Limited quantum awareness with significant gaps in understanding and preparation"),
        ("🟠", "Level 2 - Developing", "Basic quantum concepts recognized but implementation strategies lacking"),
        ("🟡", "Level 3 - Defined", "Moderate quantum readiness with structured approaches emerging"),
        ("🟢", "Level 4 - Managed", "Strong quantum capabilities with systematic risk management"),
        ("🟣", "Level 5 - Optimized", "Advanced quantum integration with comprehensive governance frameworks")
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
            <span style="font-size: 1.5rem; margin-right: 1rem;">{badge}</span>
            <div>
                <strong style="color: #374151;">{level}</strong><br>
                <span style="color: #6b7280; font-size: 0.9rem;">{description}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Research foundation section
    st.markdown("---")
    
    st.markdown("""
    ### 🏛️ **Research Foundation**
    
    GUARDIAN is built upon extensive research and development, drawing from:
    
    - **Global Policy Frameworks**: Integration with UN, NIST, OECD, and ISO standards
    - **Academic Research**: Collaboration with leading quantum technology researchers
    - **Industry Expertise**: Real-world insights from quantum computing practitioners
    - **Regulatory Analysis**: Comprehensive study of emerging quantum governance landscapes
    """)
    
    # Patent and IP section
    st.markdown("""
    ### 📋 **Intellectual Property**
    
    GUARDIAN technology is protected under patent applications including "System for Real-Time 
    Dynamic Governance of Emerging Technologies" - a comprehensive framework for AI-driven 
    policy analysis and risk assessment in the quantum technology domain.
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