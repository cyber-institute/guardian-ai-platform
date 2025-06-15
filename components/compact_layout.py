"""
Compact Layout Component - Eliminates ALL white spacing
"""
import streamlit as st

def apply_ultra_compact_css():
    """Apply comprehensive CSS to eliminate all spacing between elements"""
    st.markdown("""
    <style>
    /* Remove all margins and padding from Streamlit containers */
    .main .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: none !important;
    }
    
    /* Remove all spacing from buttons */
    .stButton {
        margin: 0px !important;
        padding: 0px !important;
        gap: 0px !important;
    }
    
    .stButton > div {
        margin: 0px !important;
        padding: 0px !important;
        gap: 0px !important;
    }
    
    .stButton > div > div {
        margin: 0px !important;
        padding: 0px !important;
        gap: 0px !important;
    }
    
    .stButton > button {
        margin: 0px !important;
        border-radius: 0px !important;
        height: 20px !important;
        padding: 1px 4px !important;
        font-size: 4px !important;
        font-family: monospace !important;
        line-height: 1.0 !important;
    }
    
    /* Force ultra-small font size on ALL buttons */
    button, .stButton button, [data-testid*="button"], 
    button[kind="secondary"], button[kind="primary"] {
        font-size: 4px !important;
        font-family: monospace !important;
        height: 20px !important;
        min-height: 20px !important;
        max-height: 20px !important;
        padding: 1px 4px !important;
        margin: 0px !important;
        border-radius: 0px !important;
        line-height: 1.0 !important;
    }
    
    /* Remove all spacing from columns */
    div[data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        gap: 0px !important;
    }
    
    div[data-testid="column"] > div {
        gap: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* Remove all spacing from vertical blocks */
    div[data-testid="stVerticalBlock"] {
        gap: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        margin: 0px !important;
        padding: 0px !important;
        gap: 0px !important;
    }
    
    div[data-testid="stVerticalBlock"] > div > div {
        margin: 0px !important;
        padding: 0px !important;
        gap: 0px !important;
    }
    
    /* Remove spacing from element containers */
    .element-container {
        margin: 0px !important;
        padding: 0px !important;
        gap: 0px !important;
    }
    
    .element-container > div {
        margin: 0px !important;
        padding: 0px !important;
        gap: 0px !important;
    }
    
    /* Remove spacing from stMarkdown */
    .stMarkdown {
        margin: 0px !important;
        padding: 0px !important;
    }
    
    .stMarkdown > div {
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* Remove spacing from any divs */
    div[class*="st"] {
        gap: 0px !important;
    }
    
    /* Target Streamlit's internal spacing */
    .css-1d391kg, .css-12w0qpk, .css-1y4p8pa {
        gap: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* Remove spacing between adjacent elements */
    * + * {
        margin-top: 0px !important;
    }
    
    /* Expander specific styling */
    .stExpander {
        margin: 0px !important;
        padding: 0px !important;
    }
    
    /* Force zero spacing on all Streamlit components */
    [data-testid] {
        margin: 0px !important;
        gap: 0px !important;
    }
    
    [data-testid] > div {
        margin: 0px !important;
        gap: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)