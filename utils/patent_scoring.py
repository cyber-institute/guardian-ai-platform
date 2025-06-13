"""
Patent-based scoring systems for GUARDIAN
Implements scoring frameworks directly from patent specifications
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np

def draw_qcmea_scorecard(title, score):
    """
    Draw QCMEA (Quantum Cybersecurity Maturity Evaluation Algorithm) scorecard
    Based on patent: "Quantum Cybersecurity Framework for Policy Assessment and Maturity Evaluation"
    
    Five-tier maturity levels as defined in patent sections 5-9:
    1. Initial Maturity
    2. Basic Maturity  
    3. Intermediate Maturity
    4. Advanced Maturity
    5. Dynamic Maturity
    """
    # Convert score to 1-5 scale if needed
    if score > 5:
        maturity_level = min(5, max(1, round(score / 20)))
    else:
        maturity_level = min(5, max(1, round(score)))
    
    # Patent-defined maturity levels with exact descriptions
    level_definitions = {
        1: {
            "name": "Initial Maturity",
            "description": "Basic awareness of quantum computing risks but lack structured mitigation strategies",
            "actions": "Initiating awareness campaigns and assessing data vulnerability to quantum threats",
            "color": "#DC2626"  # Red
        },
        2: {
            "name": "Basic Maturity", 
            "description": "Adopting foundational quantum-resistant measures, hybrid cryptographic methods",
            "actions": "Implementing governance frameworks for quantum-safe implementations",
            "color": "#EA580C"  # Orange
        },
        3: {
            "name": "Intermediate Maturity",
            "description": "Deploying scalable quantum-safe solutions and conducting regular risk assessments",
            "actions": "Transitioning critical systems to lattice-based encryption protocols",
            "color": "#D97706"  # Amber
        },
        4: {
            "name": "Advanced Maturity",
            "description": "Comprehensive integration of quantum-safe technologies across all domains",
            "actions": "Aligning strategies with NIST Post-Quantum Cryptography Standards",
            "color": "#059669"  # Green
        },
        5: {
            "name": "Dynamic Maturity",
            "description": "Continuous adaptability to emerging quantum threats using machine learning",
            "actions": "Iterative policy refinement enabling preemptive risk mitigation",
            "color": "#7C3AED"  # Purple
        }
    }
    
    # Create numbered badges
    badges_html = ""
    for i in range(1, 6):
        level_def = level_definitions[i]
        if i <= maturity_level:
            badges_html += f"""
            <div style='display: inline-flex; margin: 0 0.3rem; width: 45px; height: 45px; 
                        background: {level_def["color"]}; color: white; border-radius: 50%;
                        font-weight: 700; font-size: 1rem; box-shadow: 0 3px 6px rgba(0,0,0,0.2);
                        align-items: center; justify-content: center;
                        border: 3px solid {level_def["color"]};'>
                {i}
            </div>"""
        else:
            badges_html += f"""
            <div style='display: inline-flex; margin: 0 0.3rem; width: 45px; height: 45px; 
                        background: #f3f4f6; color: #9ca3af; border-radius: 50%; 
                        font-weight: 600; font-size: 1rem; border: 3px dashed #d1d5db;
                        align-items: center; justify-content: center;'>
                {i}
            </div>"""
    
    # Display scorecard using Streamlit's native components to avoid HTML rendering issues
    with st.container():
        st.subheader(title)
        
        # Display maturity level with colored indicators
        cols = st.columns(5)
        for i in range(1, 6):
            with cols[i-1]:
                level_def = level_definitions[i]
                if i <= maturity_level:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background-color: {level_def["color"]}; 
                                color: white; border-radius: 50%; width: 40px; height: 40px; 
                                line-height: 20px; font-weight: bold; margin: 0 auto;'>
                        {i}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: center; padding: 10px; background-color: #f3f4f6; 
                                color: #9ca3af; border-radius: 50%; width: 40px; height: 40px; 
                                line-height: 20px; border: 2px dashed #d1d5db; margin: 0 auto;'>
                        {i}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Current level details using native Streamlit components
        current_level = level_definitions[maturity_level]
        
        st.markdown(f"### Level {maturity_level}: {current_level['name']}")
        st.info(f"**Description:** {current_level['description']}")
        st.success(f"**Recommended Actions:** {current_level['actions']}")

def draw_ai_ethics_scorecard(title, ecs_score, as_score, las_score, ifs_score):
    """
    Draw AI Ethics & Cybersecurity scorecard using patent-defined 0-100 scoring system
    Based on patent: "AI-Powered Policy Evaluation and Ethical Compliance System"
    
    Four scoring dimensions from patent section 21:
    - Ethical Compliance Score (ECS): 0-100 scale for ethical standards
    - Adaptability Score (AS): Future AI advancement compatibility
    - Legal Alignment Score (LAS): Global regulatory framework compliance  
    - Implementation Feasibility Score (IFS): Real-world adoption likelihood
    """
    
    # Patent-defined scoring criteria
    score_definitions = {
        "ECS": {
            "name": "Ethical Compliance Score",
            "description": "Policy adherence to ethical standards, bias mitigation, discrimination prevention",
            "color": "#8B5CF6"
        },
        "AS": {
            "name": "Adaptability Score", 
            "description": "Policy's ability to adapt to future AI advancements and innovation",
            "color": "#06B6D4"
        },
        "LAS": {
            "name": "Legal Alignment Score",
            "description": "Compliance with OECD AI Principles, EU AI Act, UNESCO AI Ethics",
            "color": "#10B981"
        },
        "IFS": {
            "name": "Implementation Feasibility Score",
            "description": "Likelihood of successful policy adoption in real-world scenarios",
            "color": "#F59E0B"
        }
    }
    
    scores = {"ECS": ecs_score, "AS": as_score, "LAS": las_score, "IFS": ifs_score}
    
    with st.container():
        st.markdown(f"**{title}**")
        
        # Create gauge charts for each score
        cols = st.columns(4)
        
        for i, (key, score) in enumerate(scores.items()):
            with cols[i]:
                score_def = score_definitions[key]
                
                # Create gauge chart
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    title = {'text': f"{score_def['name']}<br><span style='font-size:12px'>{key}</span>"},
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': score_def['color']},
                        'steps': [
                            {'range': [0, 25], 'color': "#FEE2E2"},
                            {'range': [25, 50], 'color': "#FEF3C7"},
                            {'range': [50, 75], 'color': "#D1FAE5"},
                            {'range': [75, 100], 'color': "#DBEAFE"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig.update_layout(
                    height=200,
                    margin=dict(l=20, r=20, t=40, b=20),
                    font=dict(size=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Score interpretation
                if score >= 75:
                    status = "Excellent"
                    status_color = "#059669"
                elif score >= 50:
                    status = "Good" 
                    status_color = "#D97706"
                elif score >= 25:
                    status = "Needs Improvement"
                    status_color = "#EA580C"
                else:
                    status = "Critical"
                    status_color = "#DC2626"
                    
                st.markdown(f"""
                <div style='text-align: center; margin-top: 0.5rem;'>
                    <span style='color: {status_color}; font-weight: bold; font-size: 0.9rem;'>
                        {status}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        
        # Overall assessment
        overall_score = (ecs_score + as_score + las_score + ifs_score) / 4
        
        st.markdown("---")
        st.markdown(f"""
        <div style='background: #f8fafc; padding: 1rem; border-radius: 8px; text-align: center;'>
            <h4 style='margin: 0 0 0.5rem 0; color: #374151;'>Overall AI Policy Assessment</h4>
            <div style='font-size: 2rem; font-weight: bold; color: #B91C2C; margin: 0.5rem 0;'>
                {overall_score:.1f}/100
            </div>
            <p style='margin: 0; font-size: 0.9rem; color: #6B7280;'>
                Based on patent-defined scoring criteria from sections 21-22
            </p>
        </div>
        """, unsafe_allow_html=True)

def calculate_cybersecurity_gap_score(policy_text):
    """
    Calculate cybersecurity and ethics gap score using patent formula
    From patent section 16: Gpolicy = 1 - ((Cmatch/Ctotal) + (Ematch/Etotal))/2
    """
    # Patent-defined cybersecurity provisions to check
    cybersecurity_provisions = [
        "encryption", "authentication", "access control", "data protection",
        "threat detection", "incident response", "vulnerability assessment",
        "security monitoring", "risk management", "compliance"
    ]
    
    # Patent-defined ethics provisions to check  
    ethics_provisions = [
        "bias mitigation", "fairness", "transparency", "accountability",
        "privacy protection", "human oversight", "discrimination prevention",
        "ethical review", "stakeholder engagement", "impact assessment"
    ]
    
    # Count matches in policy text
    text_lower = policy_text.lower()
    cybersecurity_matches = sum(1 for provision in cybersecurity_provisions if provision in text_lower)
    ethics_matches = sum(1 for provision in ethics_provisions if provision in text_lower)
    
    # Apply patent formula
    cybersecurity_ratio = cybersecurity_matches / len(cybersecurity_provisions)
    ethics_ratio = ethics_matches / len(ethics_provisions)
    gap_score = 1 - ((cybersecurity_ratio + ethics_ratio) / 2)
    
    return {
        "gap_score": gap_score,
        "cybersecurity_coverage": cybersecurity_ratio * 100,
        "ethics_coverage": ethics_ratio * 100,
        "cybersecurity_matches": cybersecurity_matches,
        "ethics_matches": ethics_matches,
        "total_cybersecurity": len(cybersecurity_provisions),
        "total_ethics": len(ethics_provisions)
    }