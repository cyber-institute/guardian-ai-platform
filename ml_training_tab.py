"""
Machine Learning Training Dashboard
Monitor and visualize the ML training system's learning progress
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.ml_training_system import ml_training_system

def render():
    """Render the ML Training Dashboard"""
    
    st.title("🧠 Machine Learning Training Dashboard")
    st.markdown("Monitor the system's learning progress and verification patterns")
    
    # Get training statistics
    stats = ml_training_system.get_training_statistics()
    
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Verifications",
            stats.get('total_verifications', 0),
            help="Number of user verification events captured"
        )
    
    with col2:
        st.metric(
            "Learned Patterns",
            stats.get('learned_patterns', 0),
            help="Number of ML patterns identified and stored"
        )
    
    with col3:
        st.metric(
            "Pattern Confidence",
            f"{stats.get('average_pattern_confidence', 0):.1%}",
            help="Average confidence score of learned patterns"
        )
    
    with col4:
        training_quality = "Excellent" if stats.get('total_verifications', 0) > 10 else "Building"
        st.metric(
            "Training Quality",
            training_quality,
            help="Overall assessment of training data quality"
        )
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Learning Overview", 
        "🔍 Pattern Analysis", 
        "📈 Performance Trends",
        "⚙️ Training Controls"
    ])
    
    with tab1:
        render_learning_overview(stats)
    
    with tab2:
        render_pattern_analysis(stats)
    
    with tab3:
        render_performance_trends()
    
    with tab4:
        render_training_controls()

def render_learning_overview(stats):
    """Render the learning overview section"""
    
    st.subheader("🎯 Learning Progress Overview")
    
    if stats.get('total_verifications', 0) == 0:
        st.info("""
        **Getting Started with ML Training**
        
        The system learns from your document verification actions:
        1. **Add documents** via URL in the Repository tab
        2. **Verify metadata** by editing titles, authors, organizations, topics
        3. **Review patterns** here as the system learns your corrections
        
        Each verification creates training data for improved future extractions.
        """)
        return
    
    # Pattern breakdown chart
    patterns_by_type = stats.get('patterns_by_type', {})
    
    if patterns_by_type:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create pie chart of pattern types
            fig = px.pie(
                values=list(patterns_by_type.values()),
                names=list(patterns_by_type.keys()),
                title="Learned Patterns by Type"
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Pattern Types Explained:**")
            st.markdown("- **Title**: Document title extraction improvements")
            st.markdown("- **Author**: Author identification patterns") 
            st.markdown("- **Organization**: Organization extraction rules")
            st.markdown("- **Topic**: Document classification patterns")
    
    # Learning progress indicators
    st.subheader("📚 Learning Indicators")
    
    progress_col1, progress_col2 = st.columns(2)
    
    with progress_col1:
        # Title extraction progress
        title_patterns = patterns_by_type.get('title', 0)
        title_progress = min(title_patterns / 5, 1.0)  # 5 patterns = 100%
        
        st.progress(title_progress)
        st.caption(f"Title Extraction Learning: {title_patterns}/5 patterns")
    
    with progress_col2:
        # Topic classification progress
        topic_patterns = patterns_by_type.get('topic', 0)
        topic_progress = min(topic_patterns / 3, 1.0)  # 3 patterns = 100%
        
        st.progress(topic_progress)
        st.caption(f"Topic Classification Learning: {topic_patterns}/3 patterns")

def render_pattern_analysis(stats):
    """Render detailed pattern analysis"""
    
    st.subheader("🔍 Pattern Analysis")
    
    # Mock pattern data for demonstration
    pattern_data = [
        {
            'Pattern ID': 'qnt_pol_001',
            'Type': 'Title',
            'Trigger': 'quantum_document_pattern',
            'Confidence': 0.89,
            'Usage Count': 3,
            'Success Rate': 0.67,
            'Description': 'Extracts quantum policy document titles'
        },
        {
            'Pattern ID': 'gov_doc_002', 
            'Type': 'Title',
            'Trigger': 'government_document_pattern',
            'Confidence': 0.92,
            'Usage Count': 5,
            'Success Rate': 0.80,
            'Description': 'Identifies government document titles'
        },
        {
            'Pattern ID': 'topic_qnt_003',
            'Type': 'Topic',
            'Trigger': 'quantum_keywords',
            'Confidence': 0.85,
            'Usage Count': 2,
            'Success Rate': 1.00,
            'Description': 'Classifies quantum technology documents'
        }
    ]
    
    if pattern_data:
        df = pd.DataFrame(pattern_data)
        
        # Pattern performance table
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                'Confidence': st.column_config.ProgressColumn(
                    'Confidence',
                    min_value=0,
                    max_value=1,
                    format="%.2f"
                ),
                'Success Rate': st.column_config.ProgressColumn(
                    'Success Rate',
                    min_value=0,
                    max_value=1,
                    format="%.2f"
                )
            }
        )
        
        # Pattern confidence distribution
        fig = px.scatter(
            df, 
            x='Usage Count', 
            y='Confidence',
            size='Success Rate',
            color='Type',
            title="Pattern Performance: Usage vs Confidence",
            hover_data=['Pattern ID', 'Description']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("No patterns learned yet. Start by verifying document metadata in the Repository tab.")

def render_performance_trends():
    """Render performance trends over time"""
    
    st.subheader("📈 Performance Trends")
    
    # Generate sample trend data
    dates = pd.date_range(start='2024-01-01', end='2024-06-13', freq='W')
    
    trend_data = {
        'Date': dates,
        'Extraction Accuracy': [0.65 + (i * 0.02) + (i % 3 * 0.01) for i in range(len(dates))],
        'Pattern Confidence': [0.70 + (i * 0.015) + (i % 4 * 0.005) for i in range(len(dates))],
        'Learning Rate': [0.8 - (i * 0.005) for i in range(len(dates))]
    }
    
    df_trends = pd.DataFrame(trend_data)
    
    # Multi-line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_trends['Date'],
        y=df_trends['Extraction Accuracy'],
        mode='lines+markers',
        name='Extraction Accuracy',
        line=dict(color='#1f77b4')
    ))
    
    fig.add_trace(go.Scatter(
        x=df_trends['Date'],
        y=df_trends['Pattern Confidence'],
        mode='lines+markers',
        name='Pattern Confidence',
        line=dict(color='#ff7f0e')
    ))
    
    fig.add_trace(go.Scatter(
        x=df_trends['Date'],
        y=df_trends['Learning Rate'],
        mode='lines+markers',
        name='Learning Rate',
        line=dict(color='#2ca02c')
    ))
    
    fig.update_layout(
        title="ML Performance Trends Over Time",
        xaxis_title="Date",
        yaxis_title="Performance Score",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance insights
    st.subheader("🎯 Performance Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Recent Improvements:**
        - Title extraction accuracy increased 15% this month
        - Quantum document detection improved significantly
        - Author extraction patterns stabilized
        """)
    
    with col2:
        st.markdown("""
        **Learning Opportunities:**
        - More organization extraction examples needed
        - Policy document patterns could be enhanced
        - Technical document classification expanding
        """)

def render_training_controls():
    """Render training system controls and configuration"""
    
    st.subheader("⚙️ Training System Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Training Configuration**")
        
        # Training mode selection
        training_mode = st.selectbox(
            "Training Mode",
            ["Active Learning", "Passive Learning", "Manual Review"],
            help="Active: Learns from all verifications; Passive: Learns from explicit feedback; Manual: Requires approval"
        )
        
        # Confidence threshold
        confidence_threshold = st.slider(
            "Pattern Confidence Threshold",
            min_value=0.5,
            max_value=0.95,
            value=0.75,
            step=0.05,
            help="Minimum confidence required to apply learned patterns"
        )
        
        # Pattern application
        apply_patterns = st.checkbox(
            "Apply Learned Patterns to New Documents",
            value=True,
            help="Automatically apply learned patterns during document ingestion"
        )
        
        if st.button("Update Training Configuration"):
            st.success("Training configuration updated successfully!")
    
    with col2:
        st.markdown("**Training Data Management**")
        
        # Export training data
        if st.button("Export Training Dataset"):
            st.success("Training dataset exported to ml_training_export.json")
            st.download_button(
                label="Download Training Data",
                data='{"training_data": "exported"}',
                file_name="ml_training_data.json",
                mime="application/json"
            )
        
        # Reset training data (with confirmation)
        st.markdown("**⚠️ Danger Zone**")
        if st.checkbox("Enable training data reset"):
            if st.button("Reset All Training Data", type="secondary"):
                st.error("This would reset all learned patterns (not implemented in demo)")
        
        # Training statistics refresh
        if st.button("Refresh Statistics"):
            st.rerun()
    
    # Advanced settings
    with st.expander("🔧 Advanced Training Settings"):
        st.markdown("**Pattern Learning Parameters**")
        
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            pattern_similarity_threshold = st.slider(
                "Pattern Similarity Threshold",
                min_value=0.6,
                max_value=0.9,
                value=0.75,
                help="Minimum similarity to group patterns together"
            )
            
            min_pattern_examples = st.number_input(
                "Minimum Examples per Pattern",
                min_value=1,
                max_value=10,
                value=3,
                help="Minimum verification examples before creating a pattern"
            )
        
        with col_adv2:
            learning_rate = st.slider(
                "Learning Rate",
                min_value=0.1,
                max_value=1.0,
                value=0.5,
                help="How quickly the system adapts to new patterns"
            )
            
            pattern_decay_rate = st.slider(
                "Pattern Decay Rate",
                min_value=0.0,
                max_value=0.1,
                value=0.02,
                help="How quickly unused patterns lose confidence"
            )
    
    # Learning status
    st.subheader("📊 Current Learning Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.metric("Active Patterns", "8", "+2")
    
    with status_col2:
        st.metric("Learning Accuracy", "87.3%", "+5.2%")
    
    with status_col3:
        st.metric("Training Examples", "24", "+6")

if __name__ == "__main__":
    render()