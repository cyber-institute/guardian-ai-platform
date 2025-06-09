import streamlit as st
from quantum_tab_1749432492243 import render

def main():
    st.set_page_config(
        page_title="Quantum Maturity Scoring",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 Quantum Maturity Assessment Platform")
    st.markdown("AI-powered quantum readiness evaluation system")
    
    # Main content
    render()

if __name__ == "__main__":
    main()
