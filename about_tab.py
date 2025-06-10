"""
About Tab for GUARDIAN System - Clean, Compact Layout
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge
import numpy as np
import io
import base64

def create_speedometer_dial(value, max_value=100):
    """Create a full circular speedometer dial gauge using matplotlib."""
    fig, ax = plt.subplots(figsize=(1.2, 1.2), facecolor='white')
    
    # Calculate angle for the value (full circle: 0 to 360 degrees)
    angle = (value / max_value) * 360
    
    # Create color zones
    colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#16a34a']  # Red to Green
    zone_size = 360 / 5  # Each zone is 72 degrees
    
    # Draw colored zones
    for i, color in enumerate(colors):
        start_angle = i * zone_size
        wedge = Wedge((0, 0), 0.8, start_angle, start_angle + zone_size,
                     facecolor=color, alpha=0.3, edgecolor='white', linewidth=1)
        ax.add_patch(wedge)
    
    # Draw the needle
    needle_angle_rad = np.radians(angle - 90)  # Adjust for matplotlib's coordinate system
    needle_x = 0.6 * np.cos(needle_angle_rad)
    needle_y = 0.6 * np.sin(needle_angle_rad)
    
    # Needle line
    ax.plot([0, needle_x], [0, needle_y], color='#B91C2C', linewidth=3, zorder=10)
    
    # Center dot
    center_circle = plt.Circle((0, 0), 0.08, color='#B91C2C', zorder=15)
    ax.add_patch(center_circle)
    
    # Add value text in center
    ax.text(0, -0.3, f'{value}', ha='center', va='center', fontsize=10, 
            fontweight='bold', color='#B91C2C')
    
    # Set equal aspect ratio and remove axes
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Convert to base64 for embedding
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100, 
                facecolor='white', transparent=True)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    
    # Return with fixed dimensions (square for circular gauge)
    return f'<img src="data:image/png;base64,{image_base64}" style="width: 90px; height: 90px; display: block; margin: 0 auto; object-fit: contain;">'

def render():
    """Render the About tab for GUARDIAN system."""
    
    # Compact hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #B91C2C;">
        <h2 style="color: #B91C2C; margin-bottom: 0.8rem; font-size: 1.6rem;">GUARDIAN Emerging Tech Tool</h2>
        <p style="font-size: 1rem; line-height: 1.5; color: #374151; margin: 0;">
            <strong>Governance Using AI for Risk Detection, Integration, Analysis, and Notification</strong> - 
            A comprehensive platform for real-time policy evaluation, cybersecurity assessment, and ethical compliance analysis across AI and quantum technology domains.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a more compact and organized layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f9fafb; padding: 1rem; border-radius: 6px; height: 280px;">
        <h4 style="color: #B91C2C; margin-bottom: 0.8rem;">Patent-Based Frameworks</h4>
        <div style="font-size: 0.9rem; line-height: 1.4;">
        <strong>AI Cybersecurity (0-100)</strong><br>
        Authentication, encryption, monitoring, incident response<br><br>
        <strong>Quantum Cybersecurity (1-5 QCMEA)</strong><br>
        Five-tier quantum readiness: awareness → adaptation<br><br>
        <strong>AI Ethics (0-100)</strong><br>
        Fairness, transparency, accountability, privacy<br><br>
        <strong>Quantum Ethics (0-100)</strong><br>
        Advantage equity, privacy protection, access fairness
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; height: 280px;">
        <h4 style="color: #B91C2C; margin-bottom: 0.8rem;">Mathematical Formulations</h4>
        <div style="font-size: 0.85rem; line-height: 1.3;">
        <strong>Patent 1 - AI Ethics Risk</strong><br>
        Ethics_Score = Σ(wi × Di × Ri)<br><br>
        <strong>Patent 2 - QCMEA Quantum</strong><br>
        QCMEA_Level = max{L | Σ(Qi × Wi) ≥ Threshold_L}<br><br>
        <strong>Patent 3 - Cybersecurity Risk</strong><br>
        Risk_Cyber = Σ(Wi × Vi × Ci × Ii)<br><br>
        <strong>Bayesian Dynamic Updates</strong><br>
        P(M|D) = P(D|M) × P(M) / P(D)
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; height: 280px;">
        <h4 style="color: #B91C2C; margin-bottom: 0.8rem;">Target Users</h4>
        <div style="font-size: 0.9rem; line-height: 1.4;">
        <strong>Government Agencies</strong><br>
        Policy compliance, regulatory analysis<br><br>
        <strong>Enterprise Teams</strong><br>
        Risk assessment, compliance monitoring<br><br>
        <strong>Research Institutions</strong><br>
        Academic analysis, framework studies<br><br>
        <strong>Compliance Officers</strong><br>
        Audit preparation, gap identification
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scoring Frameworks Overview with compact visual presentation
    st.markdown("""
    <div style="background: #fefefe; padding: 1.2rem; border-radius: 8px; border: 1px solid #e5e7eb;">
    <h4 style="color: #B91C2C; margin-bottom: 1rem; text-align: center;">Four Assessment Frameworks</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact scoring framework display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #fef2f2; border-radius: 6px;">
        <h5 style="color: #B91C2C; margin: 0 0 0.5rem 0;">AI Cybersecurity</h5>
        <p style="font-size: 0.8rem; margin: 0; color: #666;">0-100 Scale</p>
        <p style="font-size: 0.7rem; margin: 0.3rem 0 0 0; color: #888;">Encryption, Authentication, Monitoring, Response</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f0f9ff; border-radius: 6px;">
        <h5 style="color: #B91C2C; margin: 0 0 0.5rem 0;">Quantum Cybersecurity</h5>
        <p style="font-size: 0.8rem; margin: 0; color: #666;">1-5 QCMEA Scale</p>
        <p style="font-size: 0.7rem; margin: 0.3rem 0 0 0; color: #888;">Initial, Basic, Intermediate, Advanced, Dynamic</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #f0fdf4; border-radius: 6px;">
        <h5 style="color: #B91C2C; margin: 0 0 0.5rem 0;">AI Ethics</h5>
        <p style="font-size: 0.8rem; margin: 0; color: #666;">0-100 Scale</p>
        <p style="font-size: 0.7rem; margin: 0.3rem 0 0 0; color: #888;">Fairness, Transparency, Accountability, Privacy</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div style="text-align: center; padding: 1rem; background: #fffbeb; border-radius: 6px;">
        <h5 style="color: #B91C2C; margin: 0 0 0.5rem 0;">Quantum Ethics</h5>
        <p style="font-size: 0.8rem; margin: 0; color: #666;">0-100 Scale</p>
        <p style="font-size: 0.7rem; margin: 0.3rem 0 0 0; color: #888;">Advantage, Privacy, Security, Access</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # System Architecture Section
    st.markdown("""
    <div style="background: #fefefe; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e5e5; margin-bottom: 1.5rem;">
    <h4 style="color: #B91C2C; margin-bottom: 1rem;">System Architecture & Implementation</h4>
    </div>
    """, unsafe_allow_html=True)
    
    arch_col1, arch_col2 = st.columns(2)
    
    with arch_col1:
        st.markdown("""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Patent Formula Implementation</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>✓ AI Ethics Risk Assessment</strong><br>
        Ethics_Score = Σ(wi × Di × Ri) - Weighted dimensional analysis<br><br>
        <strong>✓ Quantum Cybersecurity (QCMEA)</strong><br>
        QCMEA_Level = max{L | Σ(Qi × Wi) ≥ Threshold_L} - 5-tier maturity<br><br>
        <strong>✓ AI Cybersecurity Risk</strong><br>
        Risk_Cyber = Σ(Wi × Vi × Ci × Ii) - Multi-factor vulnerability analysis<br><br>
        <strong>✓ Bayesian Dynamic Updates</strong><br>
        P(M|D) = P(D|M) × P(M) / P(D) - Continuous learning adaptation
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with arch_col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Technology Stack</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>Backend Processing</strong><br>
        PostgreSQL database, Python scoring engines, content analysis<br><br>
        <strong>Interactive Frontend</strong><br>
        Streamlit web interface, real-time visualizations, dynamic filtering<br><br>
        <strong>Document Intelligence</strong><br>
        PDF parsing, metadata extraction, thumbnail generation<br><br>
        <strong>AI Integration</strong><br>
        Google Dialogflow CX chatbot, intelligent content scoring
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Comprehensive scoring statistics
    try:
        from utils.comprehensive_patent_scoring import get_document_scores_summary
        stats = get_document_scores_summary()
        
        if stats:
            st.markdown("""
            <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
            <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Live Scoring Statistics</h5>
            </div>
            """, unsafe_allow_html=True)
            
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric(
                    "Documents Analyzed", 
                    stats['total_documents'],
                    help="Total documents with patent-based scoring applied"
                )
            
            with stat_col2:
                st.metric(
                    "AI Cybersecurity Avg", 
                    f"{stats['average_scores']['ai_cybersecurity']}",
                    help="Average AI Cybersecurity score (0-100 scale)"
                )
            
            with stat_col3:
                st.metric(
                    "Quantum QCMEA Avg", 
                    f"{stats['average_scores']['quantum_cybersecurity']}",
                    help="Average Quantum Cybersecurity maturity (1-5 QCMEA scale)"
                )
            
            with stat_col4:
                st.metric(
                    "AI Ethics Avg", 
                    f"{stats['average_scores']['ai_ethics']}",
                    help="Average AI Ethics score (0-100 scale)"
                )
                
    except Exception as e:
        st.info("Patent scoring statistics will appear here once the system is fully initialized.")
    
    # Compact contact and development info
    st.markdown("""
    <div style="background: #f8fafc; padding: 1rem; border-radius: 6px; text-align: center; margin-top: 1rem;">
    <h5 style="color: #B91C2C; margin-bottom: 0.5rem;">Development Team</h5>
    <p style="margin: 0.2rem 0; font-size: 0.9rem;">Dr. Andrew Vance & Dr. Taylor Rodriguez-Vance</p>
    <p style="margin: 0.2rem 0; font-size: 0.8rem; color: #666;">Cyber Institute | New York, NY</p>
    <p style="margin: 0.2rem 0; font-size: 0.8rem; color: #666;">Patent-pending technologies for emerging tech governance</p>
    </div>
    """, unsafe_allow_html=True)