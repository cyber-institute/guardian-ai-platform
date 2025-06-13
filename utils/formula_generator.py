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
    """Generate comprehensive formula PNGs for Convergence AI mathematical pipeline"""
    
    formulas = {
        # Core Feature Extraction
        "feature_vector": r"F(text) = [f_1, f_2, \ldots, f_{100}] \in \mathbb{R}^{100}",
        
        "feature_components": r"\begin{align}" + \
                            r"f_1 &= \mu(\text{word frequencies}) \\" + \
                            r"f_2 &= \sigma(\text{word frequencies}) \\" + \
                            r"f_3 &= \max(\text{word frequencies}) \\" + \
                            r"f_4 &= \frac{|\text{unique words}|}{|\text{total words}|} \\" + \
                            r"f_5 &= \text{entropy}(\text{word distribution}) \\" + \
                            r"f_6 &= \text{readability\_score}" + \
                            r"\end{align}",
        
        "normalization": r"F_{\text{norm}} = \frac{F - \mu_F}{\sigma_F + \epsilon}, \quad \epsilon = 10^{-8}",
        
        # Advanced Bias Detection
        "bias_composite": r"B(text) = 0.4 \cdot B_{\text{pattern}} + 0.3 \cdot B_{\text{statistical}} + 0.3 \cdot B_{\text{contextual}}",
        
        "bias_pattern": r"B_{\text{pattern}} = \frac{1}{n} \sum_{i=1}^{n} \mathbb{I}[\text{pattern}_i \in \text{bias\_patterns}]",
        
        "bias_statistical": r"B_{\text{statistical}} = \min\left(2.0 \cdot \frac{\sum_{i=1}^{n} \mathbb{I}[Z_i > 2.0]}{n}, 1.0\right)",
        
        "bias_contextual": r"B_{\text{contextual}} = \max_{w \in \text{words}} \text{cosine\_sim}(e_w, \text{bias\_embeddings})",
        
        "z_score": r"Z_i = \frac{|\text{freq}_i - \mu_{\text{freq}}|}{\sigma_{\text{freq}} + \epsilon}",
        
        # Poisoning Detection
        "poisoning_score": r"P(text) = 0.6 \cdot P_{\text{adversarial}} + 0.4 \cdot P_{\text{anomaly}}",
        
        "adversarial_detection": r"P_{\text{adversarial}} = \max_{t \in \text{triggers}} \text{similarity}(\text{text}, t)",
        
        "anomaly_detection": r"P_{\text{anomaly}} = \frac{D_M(F)}{\text{threshold}} \cdot \mathbb{I}[D_M(F) > \text{threshold}]",
        
        # Similarity Analysis
        "cosine_similarity": r"\text{sim}_{\cos}(v_1, v_2) = \frac{v_1 \cdot v_2}{||v_1||_2 \cdot ||v_2||_2}",
        
        "mahalanobis": r"D_M(x) = \sqrt{(x - \mu)^T \Sigma^{-1} (x - \mu)}",
        
        "jensen_shannon": r"JS(P, Q) = \frac{1}{2} KL(P || M) + \frac{1}{2} KL(Q || M), \quad M = \frac{P + Q}{2}",
        
        # Multi-LLM Consensus
        "consensus_algorithm": r"\text{consensus} = \sum_{i=1}^{k} w_i \cdot \text{score}_i, \quad \sum_{i=1}^{k} w_i = 1",
        
        "weight_calculation": r"w_i = \frac{\text{confidence}_i \cdot (1 - B_i) \cdot (1 - P_i)}{\sum_{j=1}^{k} \text{confidence}_j \cdot (1 - B_j) \cdot (1 - P_j)}",
        
        "confidence_score": r"\text{confidence}_i = \frac{\text{model\_accuracy}_i + \text{response\_certainty}_i}{2}",
        
        # Quantum Orchestration
        "quantum_superposition": r"|\psi\rangle = \sum_{i=1}^{n} \alpha_i |s_i\rangle, \quad \sum_{i=1}^{n} |\alpha_i|^2 = 1",
        
        "quantum_entanglement": r"|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)",
        
        "quantum_measurement": r"P(|s_i\rangle) = |\alpha_i|^2 = \frac{\text{quality\_score}_i^2}{\sum_{j=1}^{n} \text{quality\_score}_j^2}",
        
        # Final Validation
        "validation_threshold": r"\text{validated} = (\text{consensus} \geq 0.7) \land (B \leq 0.3) \land (P \leq 0.25)",
        
        "quality_score": r"Q = \text{consensus} \cdot (1 - B) \cdot (1 - P) \cdot \text{coherence}",
        
        "training_update": r"\theta_{t+1} = \theta_t + \eta \cdot \nabla_{\theta} \mathcal{L}(Q, \text{target})"
    }
    
    # Generate PNGs for each formula with optimized sizing
    formula_images = {}
    for name, formula in formulas.items():
        if name == "feature_components":
            img_base64 = create_formula_png(formula, figsize=(14, 5), fontsize=12)
        elif name in ["consensus_algorithm", "weight_calculation", "quantum_superposition"]:
            img_base64 = create_formula_png(formula, figsize=(16, 3), fontsize=11)
        elif name in ["bias_composite", "poisoning_score", "validation_threshold"]:
            img_base64 = create_formula_png(formula, figsize=(15, 2.5), fontsize=12)
        elif name in ["quantum_entanglement", "quantum_measurement"]:
            img_base64 = create_formula_png(formula, figsize=(12, 2.5), fontsize=13)
        else:
            img_base64 = create_formula_png(formula, figsize=(11, 2), fontsize=13)
        
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