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
    
    # Level definitions with color progression
    level_names = {1: "Initial", 2: "Basic", 3: "Developing", 4: "Advanced", 5: "Expert"}
    level_colors = {
        1: "#dc2626",  # Red
        2: "#f97316",  # Orange
        3: "#eab308",  # Yellow
        4: "#22c55e",  # Green
        5: "#8b5cf6"   # Purple
    }
    level_text_colors = {
        1: "#ffffff",  # White text
        2: "#ffffff",  # White text
        3: "#374151",  # Dark text on yellow
        4: "#ffffff",  # White text
        5: "#ffffff"   # White text
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
            <div style='display: inline-block; margin: 0 0.3rem; width: 40px; height: 40px; 
                        background: {level_colors[i]}; color: {level_text_colors[i]}; border-radius: 50%; 
                        font-weight: 700; font-size: 0.9rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        display: flex; align-items: center; justify-content: center;
                        border: 2px solid {level_colors[i]};'>
                {i}
            </div>"""
        else:
            badges_html += f"""
            <div style='display: inline-block; margin: 0 0.3rem; width: 40px; height: 40px; 
                        background: #f3f4f6; color: #9ca3af; border-radius: 50%; 
                        font-weight: 600; font-size: 0.9rem; border: 2px dashed #d1d5db;
                        display: flex; align-items: center; justify-content: center;'>
                {i}
            </div>"""
    
    # Create compact legend
    legend_html = ""
    for i in range(1, 6):
        legend_html += f"""
        <div style='display: flex; align-items: center; margin: 0.1rem 0;'>
            <div style='width: 12px; height: 12px; background: {level_colors[i]}; border-radius: 50%; 
                        margin-right: 0.4rem; flex-shrink: 0;'></div>
            <span style='font-size: 0.7rem; color: #374151;'>{i}: {level_names[i]}</span>
        </div>"""
    
    # Create compact display using native Streamlit components
    with st.container():
        st.markdown(f"**{title}**")
        
        # Create horizontal layout
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            # Circle badges in columns
            circle_cols = st.columns(5)
            for i, circle_col in enumerate(circle_cols, 1):
                with circle_col:
                    if i <= maturity_level:
                        # Use colored emoji circles or simple text badges
                        color_map = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "🟣"}
                        st.markdown(f"<div style='text-align: center; font-size: 1.5rem;'>{color_map[i]}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align: center; font-size: 0.7rem; font-weight: bold;'>{i}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align: center; font-size: 1.5rem;'>⚪</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align: center; font-size: 0.7rem; color: #999;'>{i}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**Level {maturity_level}: {level_names[maturity_level]}**")
            st.caption(level_descriptions[maturity_level])
        
        with col3:
            st.markdown("**Legend:**")
            st.markdown("🔴 1: Initial")
            st.markdown("🟠 2: Basic") 
            st.markdown("🟡 3: Developing")
            st.markdown("🟢 4: Advanced")
            st.markdown("🟣 5: Expert")

def get_score_analysis(score, category, doc_title="", doc_content="", doc_type=None):
    """
    Generate contextual analysis text based on quantum maturity score and document type.
    """
    from utils.document_classifier import detect_document_type, get_contextual_analysis_text
    
    # Detect document type if not provided
    if not doc_type:
        doc_type = detect_document_type(doc_title, doc_content)
    
    return get_contextual_analysis_text(score, category, doc_type, doc_title)

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
