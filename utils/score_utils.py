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
    
    # Level definitions with improved color progression
    level_names = {1: "Initial", 2: "Basic", 3: "Developing", 4: "Advanced", 5: "Expert"}
    level_colors = {
        1: "#22c55e",  # Green
        2: "#cd7f32",  # Bronze
        3: "#c0c0c0",  # Silver
        4: "#ffd700",  # Gold
        5: "#e5e4e2"   # Platinum
    }
    level_text_colors = {
        1: "#ffffff",  # White text on green
        2: "#ffffff",  # White text on bronze
        3: "#374151",  # Dark text on silver
        4: "#374151",  # Dark text on gold
        5: "#374151"   # Dark text on platinum
    }
    level_descriptions = {
        1: "Minimal quantum awareness",
        2: "Basic understanding of quantum risks", 
        3: "Developing quantum readiness strategies",
        4: "Advanced quantum security implementation",
        5: "Expert-level quantum maturity"
    }
    
    # Create circular level badges
    badges_html = ""
    for i in range(1, 6):
        if i <= maturity_level:
            badges_html += f"""
            <div style='display: inline-block; margin: 0 0.4rem; width: 60px; height: 60px; 
                        background: {level_colors[i]}; color: {level_text_colors[i]}; border-radius: 50%; 
                        font-weight: 700; font-size: 1.2rem; box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                        display: flex; align-items: center; justify-content: center;
                        border: 3px solid {level_colors[i]};'>
                {i}
            </div>"""
        else:
            badges_html += f"""
            <div style='display: inline-block; margin: 0 0.4rem; width: 60px; height: 60px; 
                        background: #f3f4f6; color: #9ca3af; border-radius: 50%; 
                        font-weight: 600; font-size: 1.2rem; border: 3px dashed #d1d5db;
                        display: flex; align-items: center; justify-content: center;'>
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
