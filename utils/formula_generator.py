"""
Mathematical Formula PNG Generator for GUARDIAN
Creates high-quality PNG images of mathematical formulas for better visual presentation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import font_manager
import numpy as np
import io
import base64

def create_formula_png(formula_latex, filename=None, figsize=(10, 2), fontsize=16, dpi=150):
    """
    Create a PNG image of a mathematical formula
    
    Args:
        formula_latex: LaTeX string of the formula
        filename: Optional filename to save PNG
        figsize: Figure size (width, height)
        fontsize: Font size for the formula
        dpi: Resolution for the PNG
        
    Returns:
        base64 encoded PNG data for display in Streamlit
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.axis('off')
    
    # Set transparent background
    fig.patch.set_alpha(0)
    
    # Render the formula
    ax.text(0.5, 0.5, f'${formula_latex}$', 
            fontsize=fontsize, 
            ha='center', 
            va='center',
            transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="#e2e8f0"))
    
    # Save to bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', 
                transparent=True, pad_inches=0.2, dpi=dpi)
    buf.seek(0)
    
    # Convert to base64 for Streamlit display
    img_base64 = base64.b64encode(buf.read()).decode()
    
    plt.close(fig)
    
    if filename:
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(img_base64))
    
    return img_base64

def generate_convergence_ai_formulas():
    """Generate all formula PNGs for Convergence AI mathematical pipeline"""
    
    formulas = {
        "feature_vector": r"F(text) = [f_1, f_2, \ldots, f_{100}]",
        
        "feature_components": r"\begin{align}" + \
                            r"f_1 &= \mu(\text{word frequencies}) \\" + \
                            r"f_2 &= \sigma(\text{word frequencies}) \\" + \
                            r"f_3 &= \max(\text{word frequencies}) \\" + \
                            r"f_4 &= \frac{|\text{unique words}|}{|\text{total words}|}" + \
                            r"\end{align}",
        
        "normalization": r"F_{\text{normalized}} = \frac{F}{||F||_2 + \epsilon}",
        
        "bias_composite": r"B(text) = 0.4 \times B_{\text{pattern}} + 0.3 \times B_{\text{statistical}} + 0.3 \times B_{\text{contextual}}",
        
        "bias_statistical": r"B_{\text{statistical}} = \min\left(2.0 \times \frac{\sum(Z > 2.0)}{n_{\text{words}}}, 1.0\right)",
        
        "z_score": r"Z = \frac{|\text{freq}_i - \mu|}{\sigma}",
        
        "cosine_similarity": r"\text{cosine\_sim}(v_1, v_2) = \frac{v_1 \cdot v_2}{||v_1|| \times ||v_2||}",
        
        "mahalanobis": r"D_M(x) = \sqrt{(x - \mu)^T \Sigma^{-1} (x - \mu)}",
        
        "jensen_shannon": r"JS(P, Q) = \frac{1}{2} KL(P || M) + \frac{1}{2} KL(Q || M)",
        
        "consensus": r"\text{consensus} = 0.5 \times \mu(\text{cosine similarities}) + 0.3 \times \left(1 - \min\left(\frac{\mu(\text{mahalanobis})}{3}, 1\right)\right) + 0.2 \times (1 - \mu(\text{divergence scores}))",
        
        "weight_calculation": r"\text{weight}_i = \text{confidence}_i \times (1 - \text{bias}_i) \times (1 - \text{poisoning}_i)",
        
        "validation_threshold": r"\text{validated} = (\text{consensus} \geq 0.7) \land (\text{bias mitigation} \geq 0.7) \land (\text{poisoning resistance} \geq 0.75)",
        
        "quality_score": r"\text{quality} = \text{consensus} \times \text{bias mitigation} \times \text{poisoning resistance}"
    }
    
    # Generate PNGs for each formula
    formula_images = {}
    for name, formula in formulas.items():
        if name == "feature_components":
            img_base64 = create_formula_png(formula, figsize=(12, 4), fontsize=14)
        elif name == "consensus":
            img_base64 = create_formula_png(formula, figsize=(14, 3), fontsize=12)
        else:
            img_base64 = create_formula_png(formula, figsize=(10, 2), fontsize=14)
        
        formula_images[name] = img_base64
    
    return formula_images

def display_formula_png(formula_base64, caption=""):
    """Display a formula PNG in Streamlit with optional caption"""
    import streamlit as st
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0;">
        <img src="data:image/png;base64,{formula_base64}" style="max-width: 100%; height: auto;">
        {f'<p style="font-size: 0.9rem; color: #6b7280; margin-top: 0.5rem;">{caption}</p>' if caption else ''}
    </div>
    """, unsafe_allow_html=True)