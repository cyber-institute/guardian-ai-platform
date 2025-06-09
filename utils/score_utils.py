import streamlit as st
try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def draw_scorecard(title, score):
    """
    Draw a visual scorecard for quantum maturity scores (1-5 scale).
    """
    # Convert score to 1-5 scale if it's on 0-100 scale
    if score > 5:
        maturity_level = min(5, max(1, round(score / 20)))
    else:
        maturity_level = min(5, max(1, round(score)))
    
    # Level definitions
    level_names = {1: "Initial", 2: "Basic", 3: "Developing", 4: "Advanced", 5: "Expert"}
    level_colors = {1: "#dc2626", 2: "#f59e0b", 3: "#d97706", 4: "#059669", 5: "#10b981"}
    level_descriptions = {
        1: "Minimal quantum awareness",
        2: "Basic understanding of quantum risks", 
        3: "Developing quantum readiness strategies",
        4: "Advanced quantum security implementation",
        5: "Expert-level quantum maturity"
    }
    
    # Create level badges
    badges_html = ""
    for i in range(1, 6):
        if i <= maturity_level:
            badges_html += f"""
            <div style='display: inline-block; margin: 0 0.25rem; padding: 0.75rem 1.25rem; 
                        background: {level_colors[i]}; color: white; border-radius: 10px; 
                        font-weight: 600; font-size: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                {i}
            </div>"""
        else:
            badges_html += f"""
            <div style='display: inline-block; margin: 0 0.25rem; padding: 0.75rem 1.25rem; 
                        background: #e5e7eb; color: #9ca3af; border-radius: 10px; 
                        font-weight: 600; font-size: 1rem; border: 2px dashed #d1d5db;'>
                {i}
            </div>"""
    
    st.markdown(f"""
    <div style='padding: 1.5rem; background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                border-radius: 12px; margin: 1rem 0; border: 1px solid #e2e8f0;'>
        <h3 style='margin: 0 0 1rem 0; color: #374151; text-align: center; font-family: Inter, sans-serif;'>{title}</h3>
        <div style='text-align: center; margin: 1.5rem 0;'>{badges_html}</div>
        <div style='text-align: center; margin: 1rem 0;'>
            <div style='font-size: 1.4rem; font-weight: 700; color: {level_colors[maturity_level]}; margin-bottom: 0.5rem;'>
                Level {maturity_level}: {level_names[maturity_level]}
            </div>
            <div style='font-size: 1rem; color: #6b7280; font-style: italic;'>
                {level_descriptions[maturity_level]}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_score_analysis(score, category):
    """
    Generate analysis text based on the quantum maturity score (1-5 scale).
    """
    # Convert score to 1-5 scale if it's on 0-100 scale
    if score > 5:
        maturity_level = min(5, max(1, round(score / 20)))
    else:
        maturity_level = min(5, max(1, round(score)))
    
    if maturity_level == 5:
        return f"""
        **Expert-level {category} maturity!** Your organization demonstrates advanced understanding 
        and implementation of quantum-safe practices. You are well-prepared for the quantum era.
        """
    elif maturity_level == 4:
        return f"""
        **Advanced {category} foundation.** Your organization shows strong awareness and solid 
        implementation of quantum-safe practices. Consider fine-tuning specific areas.
        """
    elif maturity_level == 3:
        return f"""
        **Developing {category} awareness.** Your organization has good understanding but 
        needs continued improvement in quantum readiness implementation.
        """
    elif maturity_level == 2:
        return f"""
        **Basic {category} preparation.** Your organization shows fundamental quantum awareness. 
        Focus on expanding knowledge and building implementation strategies.
        """
    else:
        return f"""
        **Initial {category} readiness.** Your organization is beginning quantum preparedness. 
        Start with basic education and risk assessment activities.
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
