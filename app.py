import streamlit as st
from quantum_tab_1749432492243 import render

def main():
    st.set_page_config(
        page_title="Quantum Maturity Scoring",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS styling
    st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    
    .quantum-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .quantum-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .quantum-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .score-excellent {
        border-left-color: #22c55e;
    }
    
    .score-good {
        border-left-color: #f59e0b;
    }
    
    .score-moderate {
        border-left-color: #ef4444;
    }
    
    .document-separator {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    .stExpander > details > summary {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
    }
    
    .sidebar-info {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="quantum-header">
        <h1>🔐 Quantum Maturity Assessment Platform</h1>
        <p>AI-powered quantum readiness evaluation system</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar information
    with st.sidebar:
        st.markdown("### 📊 Assessment Overview")
        st.markdown("""
        <div class="sidebar-info">
        <strong>Evaluation Criteria:</strong><br>
        • Post-Quantum Cryptography<br>
        • Risk Assessment<br>
        • Implementation Planning<br>
        • Standards Compliance<br>
        • Migration Strategy
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Scoring Scale")
        st.markdown("""
        <div class="sidebar-info">
        <strong>90-100:</strong> Quantum-Ready<br>
        <strong>75-89:</strong> Advanced<br>
        <strong>50-74:</strong> Developing<br>
        <strong>25-49:</strong> Basic<br>
        <strong>0-24:</strong> Initial
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔍 Analysis Features")
        st.markdown("""
        <div class="sidebar-info">
        • AI-powered text analysis<br>
        • Keyword density scoring<br>
        • Maturity trait detection<br>
        • Standards reference checking<br>
        • Implementation gap analysis
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    render()

if __name__ == "__main__":
    main()
