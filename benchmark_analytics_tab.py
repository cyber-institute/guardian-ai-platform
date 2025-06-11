"""
Multi-LLM Benchmarking Analytics Tab
Comprehensive performance measurement and comparison dashboard
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from utils.benchmarking_system import multi_llm_benchmarker

def render():
    """Render the benchmarking analytics dashboard"""
    
    st.title("🔬 Multi-LLM Performance Analytics")
    st.markdown("""
    **Measure the impact of Multi-LLM ensemble analysis vs standard single-model processing**
    
    This dashboard tracks improvements in confidence, accuracy, and consensus strength when using multiple LLMs.
    """)
    
    # Generate comprehensive benchmark report
    report = multi_llm_benchmarker.generate_benchmark_report()
    
    if report.get("no_data"):
        st.info("📊 **Getting Started with Benchmarking**")
        st.markdown("""
        To see Multi-LLM performance improvements:
        
        1. **Upload a document** with Multi-LLM Analysis **disabled** (baseline)
        2. **Upload the same document** with Multi-LLM Analysis **enabled** 
        3. **Return here** to see detailed performance comparisons
        
        The system will automatically detect identical content and show improvement metrics.
        """)
        
        st.markdown("### Quick Test Recommendations")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📝 Try uploading:**
            - AI policy documents
            - Cybersecurity frameworks  
            - Quantum computing papers
            - Technical specifications
            """)
        
        with col2:
            st.markdown("""
            **🎯 Key metrics to watch:**
            - Confidence improvement
            - Consensus strength
            - Processing time impact
            - Score enhancement
            """)
        
        return
    
    # Display overall performance summary
    st.success(f"📈 **Analysis Complete**: {report['total_comparisons']} document comparisons available")
    
    improvements = report["average_improvements"]
    quality = report["quality_indicators"]
    
    # Main metrics dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        confidence_boost = improvements["confidence_boost"]
        st.metric(
            "Average Confidence Boost", 
            f"+{confidence_boost}%",
            delta=confidence_boost if confidence_boost > 0 else None
        )
    
    with col2:
        consensus = improvements["consensus_strength"]
        st.metric(
            "Consensus Strength", 
            f"{consensus}/1.0",
            delta="Strong" if consensus > 0.7 else "Moderate" if consensus > 0.4 else "Weak"
        )
    
    with col3:
        time_change = improvements["processing_time_change"]
        st.metric(
            "Processing Time Change", 
            f"{time_change:+.1f}s",
            delta=f"{'Faster' if time_change < 0 else 'Slower'}" if abs(time_change) > 0.5 else "Similar"
        )
    
    with col4:
        score_improvements = improvements["score_improvements"]
        avg_improvement = sum(score_improvements.values()) / len(score_improvements) if score_improvements else 0
        st.metric(
            "Score Enhancement", 
            f"+{avg_improvement:.1f}",
            delta="Improved" if avg_improvement > 0 else None
        )
    
    # Quality indicators
    st.markdown("### 🎯 Quality Assessment")
    
    quality_col1, quality_col2, quality_col3 = st.columns(3)
    
    with quality_col1:
        if quality["multi_llm_advantage"]:
            st.success("✅ **Multi-LLM Advantage Confirmed**")
            st.caption("Ensemble analysis consistently outperforms single models")
        else:
            st.warning("⚠️ **Mixed Results**")
            st.caption("Some variations in performance detected")
    
    with quality_col2:
        if quality["consensus_reliability"]:
            st.success("✅ **High Consensus Reliability**")
            st.caption("Strong agreement between multiple LLMs")
        else:
            st.info("ℹ️ **Moderate Consensus**")
            st.caption("LLMs show some disagreement on complex topics")
    
    with quality_col3:
        if quality["improved_accuracy"]:
            st.success("✅ **Enhanced Accuracy**")
            st.caption("Measurable improvements in scoring accuracy")
        else:
            st.info("ℹ️ **Comparable Accuracy**")
            st.caption("Similar accuracy to baseline analysis")
    
    # Detailed analytics tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance Charts", "📈 Trend Analysis", "🔍 Document Comparisons", "⚙️ Methodology"])
    
    with tab1:
        render_performance_charts(report)
    
    with tab2:
        render_trend_analysis(report)
    
    with tab3:
        render_document_comparisons(report)
    
    with tab4:
        render_methodology_explanation()

def render_performance_charts(report):
    """Render performance visualization charts"""
    
    improvements = report["average_improvements"]
    
    # Confidence improvement chart
    st.subheader("Confidence Level Improvements")
    
    fig_confidence = go.Figure()
    
    fig_confidence.add_trace(go.Bar(
        x=["Standard Analysis", "Multi-LLM Analysis"],
        y=[80.0, 80.0 + improvements["confidence_boost"]],
        marker_color=["lightgray", "green"],
        text=[f"80.0%", f"{80.0 + improvements['confidence_boost']:.1f}%"],
        textposition="auto"
    ))
    
    fig_confidence.update_layout(
        title="Confidence Level Comparison",
        yaxis_title="Confidence Score (%)",
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig_confidence, use_container_width=True)
    
    # Score improvements radar chart
    if improvements["score_improvements"]:
        st.subheader("Score Enhancement Breakdown")
        
        categories = list(improvements["score_improvements"].keys())
        values = list(improvements["score_improvements"].values())
        
        fig_radar = go.Figure()
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Score Improvements'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[min(values + [0]), max(values + [10])]
                )),
            showlegend=False,
            title="Score Enhancement by Category",
            height=500
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Processing time analysis
    st.subheader("Processing Time Impact")
    
    time_change = improvements["processing_time_change"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_time = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=time_change,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Time Change (seconds)"},
            delta={'reference': 0},
            gauge={
                'axis': {'range': [None, max(10, abs(time_change) + 5)]},
                'bar': {'color': "red" if time_change > 5 else "green" if time_change < -1 else "orange"},
                'steps': [
                    {'range': [-10, -1], 'color': "lightgreen"},
                    {'range': [-1, 1], 'color': "yellow"},
                    {'range': [1, 10], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 5
                }
            }
        ))
        
        fig_time.update_layout(height=300)
        st.plotly_chart(fig_time, use_container_width=True)
    
    with col2:
        st.markdown("**Processing Time Analysis:**")
        if time_change < -1:
            st.success("🚀 Multi-LLM processing is faster than expected")
        elif time_change < 5:
            st.info("⚡ Reasonable processing time increase for improved quality")
        else:
            st.warning("⏱️ Significant time increase - consider optimizing")
        
        st.markdown(f"""
        - **Time change**: {time_change:+.1f} seconds
        - **Quality tradeoff**: {'Excellent' if time_change < 5 else 'Good' if time_change < 10 else 'Review needed'}
        - **Recommendation**: {'Optimal balance' if abs(time_change) < 5 else 'Consider standard analysis for speed-critical tasks'}
        """)

def render_trend_analysis(report):
    """Render trend analysis over time"""
    
    st.subheader("Performance Trends")
    
    # Get detailed comparisons for trend analysis
    comparisons = report.get("detailed_comparisons", [])
    
    if not comparisons:
        st.info("Upload more documents with both standard and Multi-LLM analysis to see trends")
        return
    
    # Create trend data
    trend_data = []
    for i, comp in enumerate(comparisons):
        improvements = comp["improvements"]
        trend_data.append({
            "Analysis #": i + 1,
            "Document": comp["standard_analysis"]["document_title"][:30] + "...",
            "Confidence Improvement": improvements.get("confidence_improvement", 0),
            "Consensus Strength": improvements["quality_metrics"].get("consensus_strength", 0),
            "Overall Improvement": improvements.get("overall_improvement", 0)
        })
    
    df = pd.DataFrame(trend_data)
    
    # Confidence improvement trend
    fig_trend = px.line(
        df, 
        x="Analysis #", 
        y="Confidence Improvement",
        title="Confidence Improvement Trend",
        markers=True
    )
    
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Consensus strength trend
    fig_consensus = px.scatter(
        df,
        x="Analysis #",
        y="Consensus Strength",
        size="Overall Improvement",
        hover_data=["Document"],
        title="Consensus Strength by Analysis"
    )
    
    fig_consensus.update_layout(height=400)
    st.plotly_chart(fig_consensus, use_container_width=True)
    
    # Summary statistics
    st.subheader("Statistical Summary")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Best Confidence Boost", f"+{df['Confidence Improvement'].max():.1f}%")
        st.metric("Average Boost", f"+{df['Confidence Improvement'].mean():.1f}%")
    
    with stat_col2:
        st.metric("Highest Consensus", f"{df['Consensus Strength'].max():.2f}")
        st.metric("Average Consensus", f"{df['Consensus Strength'].mean():.2f}")
    
    with stat_col3:
        improvement_rate = (df['Confidence Improvement'] > 0).mean() * 100
        st.metric("Improvement Rate", f"{improvement_rate:.0f}%")
        consistency = df['Confidence Improvement'].std()
        st.metric("Consistency", f"±{consistency:.1f}")

def render_document_comparisons(report):
    """Render detailed document-by-document comparisons"""
    
    st.subheader("Document-by-Document Analysis")
    
    comparisons = report.get("detailed_comparisons", [])
    
    if not comparisons:
        st.info("No detailed comparisons available yet")
        return
    
    for i, comp in enumerate(comparisons):
        with st.expander(f"📄 {comp['standard_analysis']['document_title']}", expanded=(i == 0)):
            
            standard = comp["standard_analysis"]
            multi_llm = comp["multi_llm_analysis"]
            improvements = comp["improvements"]
            
            # Comparison metrics
            comp_col1, comp_col2, comp_col3 = st.columns(3)
            
            with comp_col1:
                st.markdown("**Standard Analysis**")
                st.text(f"Confidence: {standard['confidence_score']:.1f}%")
                st.text(f"Processing Time: {standard['processing_time']:.2f}s")
                st.text(f"Services: {standard.get('services_used', 1)}")
            
            with comp_col2:
                st.markdown("**Multi-LLM Analysis**")
                st.text(f"Confidence: {multi_llm['confidence_score']:.1f}%")
                st.text(f"Processing Time: {multi_llm['processing_time']:.2f}s")
                st.text(f"Services: {multi_llm.get('services_used', 0)}")
            
            with comp_col3:
                st.markdown("**Improvements**")
                conf_imp = improvements.get("confidence_improvement", 0)
                st.text(f"Confidence: {conf_imp:+.1f}%")
                time_imp = improvements.get("processing_time_change", 0)
                st.text(f"Time Change: {time_imp:+.1f}s")
                consensus = improvements["quality_metrics"].get("consensus_strength", 0)
                st.text(f"Consensus: {consensus:.2f}")
            
            # Score improvements breakdown
            if improvements["score_improvements"]:
                st.markdown("**Score Enhancements:**")
                for score_type, improvement in improvements["score_improvements"].items():
                    color = "green" if improvement > 0 else "red" if improvement < 0 else "gray"
                    st.markdown(f"- **{score_type}**: <span style='color:{color}'>{improvement:+.1f}</span>", unsafe_allow_html=True)

def render_methodology_explanation():
    """Explain the benchmarking methodology"""
    
    st.subheader("📚 Benchmarking Methodology")
    
    st.markdown("""
    ### How Multi-LLM Performance is Measured
    
    **1. Content Identification**
    - Each document gets a unique content hash
    - System detects when the same document is analyzed multiple times
    - Enables direct before/after comparisons
    
    **2. Key Metrics Tracked**
    """)
    
    metric_col1, metric_col2 = st.columns(2)
    
    with metric_col1:
        st.markdown("""
        **Quality Metrics:**
        - **Confidence Score**: LLM certainty in analysis (0-100%)
        - **Consensus Strength**: Agreement between multiple LLMs (0-1.0)
        - **Score Enhancement**: Improvement in patent-based scoring frameworks
        """)
    
    with metric_col2:
        st.markdown("""
        **Performance Metrics:**
        - **Processing Time**: Total analysis duration
        - **Services Used**: Number of LLMs in ensemble
        - **Accuracy Improvements**: Enhanced detection capabilities
        """)
    
    st.markdown("""
    **3. Analysis Types Compared**
    
    - **Standard Analysis**: Single LLM with traditional scoring
    - **Multi-LLM Analysis**: Ensemble of multiple LLMs with consensus algorithms
    
    **4. Statistical Significance**
    
    - Improvements tracked across multiple document types
    - Trend analysis shows consistency over time
    - Quality indicators validate ensemble advantages
    
    **5. Real-World Impact**
    
    Multi-LLM improvements translate to:
    - More accurate risk assessments
    - Better policy gap detection  
    - Enhanced cybersecurity evaluations
    - Improved quantum readiness scoring
    """)
    
    st.info("""
    **💡 Pro Tip**: For best benchmarking results, upload the same document first with Multi-LLM disabled, 
    then again with Multi-LLM enabled. This creates perfect comparison conditions.
    """)