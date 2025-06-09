import streamlit as st
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def draw_scorecard(title, score):
    """
    Draw a visual scorecard for quantum maturity scores.
    """
    if PLOTLY_AVAILABLE:
        # Create a gauge chart using Plotly
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': title},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100], 'tickfont': {'size': 14, 'family': 'Inter'}},
                'bar': {'color': "#1e40af", 'thickness': 0.8},
                'steps': [
                    {'range': [0, 25], 'color': "#f3f4f6"},
                    {'range': [25, 50], 'color': "#fef3c7"},
                    {'range': [50, 75], 'color': "#fed7aa"},
                    {'range': [75, 100], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "#dc2626", 'width': 3},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            font=dict(family="Inter, sans-serif", size=14, color="#374151"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Enhanced fallback visualization using Streamlit components
        st.markdown(f"### {title}")
        
        # Create columns for better layout
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Enhanced progress bar with government theme color coding
            progress_color = "#059669" if score >= 75 else "#d97706" if score >= 50 else "#dc2626"
            
            st.markdown(f"""
            <div style="
                background: #f1f5f9; 
                border-radius: 10px; 
                padding: 1rem; 
                margin: 1rem 0;
                border-left: 4px solid {progress_color};
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 600; color: #374151;">Quantum Maturity Score</span>
                    <span style="font-size: 1.5rem; font-weight: 700; color: {progress_color};">{score:.1f}/100</span>
                </div>
                <div style="
                    background: #e5e7eb; 
                    border-radius: 6px; 
                    height: 12px; 
                    margin-top: 0.5rem;
                    overflow: hidden;
                ">
                    <div style="
                        background: {progress_color}; 
                        height: 100%; 
                        width: {score}%; 
                        transition: width 0.5s ease;
                        border-radius: 6px;
                    "></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Status indicator
            if score >= 75:
                st.success("Excellent")
            elif score >= 50:
                st.warning("Good")
            elif score >= 25:
                st.warning("Moderate")
            else:
                st.error("Needs Work")

def get_score_analysis(score, category):
    """
    Generate analysis text based on the quantum maturity score.
    """
    if score >= 80:
        return f"""
        **Excellent {category} maturity!** Your organization demonstrates advanced understanding 
        and implementation of quantum-safe practices. You are well-prepared for the quantum era.
        """
    elif score >= 60:
        return f"""
        **Good {category} foundation.** Your organization shows solid awareness and some 
        implementation of quantum-safe practices. Consider strengthening specific areas.
        """
    elif score >= 40:
        return f"""
        **Moderate {category} awareness.** Your organization has basic understanding but 
        needs significant improvement in quantum readiness implementation.
        """
    elif score >= 20:
        return f"""
        **Limited {category} preparation.** Your organization shows minimal quantum awareness. 
        Immediate action is recommended to begin quantum readiness initiatives.
        """
    else:
        return f"""
        **Minimal {category} readiness.** Your organization lacks quantum preparedness. 
        Critical action needed to address quantum security risks.
        """

def get_deep_diagnostics(score, category):
    """
    Provide deep diagnostic analysis for quantum maturity scores.
    """
    diagnostics = []
    
    if score < 30:
        diagnostics.extend([
            "🚨 **Critical Gap**: Lack of quantum-safe cryptography planning",
            "📋 **Action Required**: Establish quantum security task force",
            "⏰ **Timeline**: Begin immediate risk assessment"
        ])
    elif score < 60:
        diagnostics.extend([
            "⚠️ **Moderate Risk**: Partial quantum readiness",
            "🔄 **Improvement Needed**: Strengthen implementation planning",
            "📈 **Next Steps**: Develop comprehensive migration strategy"
        ])
    else:
        diagnostics.extend([
            "✅ **Strong Foundation**: Good quantum awareness",
            "🚀 **Optimization**: Fine-tune existing strategies",
            "🎯 **Focus Areas**: Maintain continuous improvement"
        ])
    
    # Add category-specific diagnostics
    if category == "quantum ethics":
        diagnostics.extend([
            "🤖 **AI Integration**: Consider ethical AI implications in quantum systems",
            "🔒 **Privacy**: Evaluate quantum computing impact on data privacy",
            "⚖️ **Governance**: Establish quantum ethics committee"
        ])
    
    return "\n".join([f"- {diagnostic}" for diagnostic in diagnostics])

def calculate_weighted_score(raw_scores, weights):
    """
    Calculate weighted quantum maturity score from raw AI analysis results.
    """
    if not raw_scores or not weights:
        return 0
    
    total_weight = 0
    weighted_sum = 0
    
    for label, score in raw_scores.items():
        weight = weights.get(label, 1.0)
        try:
            score_value = float(score)
            weighted_sum += score_value * weight
            total_weight += weight
        except (ValueError, TypeError):
            continue
    
    if total_weight == 0:
        return 0
    
    return round(weighted_sum / total_weight, 2)
