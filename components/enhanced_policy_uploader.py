"""
Enhanced Policy Document Uploader with AI-Powered Gap Analysis
Implements GUARDIAN patent's policy reinforcement learning and recommendation capabilities
"""

import streamlit as st
from typing import Optional, Dict, List
from utils.policy_gap_analyzer import policy_gap_analyzer, GapAnalysisReport
from utils.document_recommendation_engine import recommendation_engine
from utils.db import save_document
from utils.pdf_ingestion_thumbnails import process_uploaded_pdf_with_thumbnail
import time

def render_enhanced_policy_uploader():
    """Render enhanced document uploader with intelligent gap analysis and recommendations."""
    
    st.markdown("### 📋 **Intelligent Policy Analysis & Upload**")
    st.markdown("Upload your draft policies, standards, regulations, or product specifications for comprehensive gap analysis and recommendations.")
    
    with st.form("enhanced_policy_upload"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # File upload
            uploaded_file = st.file_uploader(
                "Upload Document",
                type=['txt', 'md', 'pdf', 'docx'],
                help="Upload policy documents, standards, regulations, or product specifications"
            )
            
            # Document metadata
            title = st.text_input(
                "Document Title",
                help="Enter a descriptive title for your document"
            )
            
            document_type = st.selectbox(
                "Document Type",
                ["Policy", "Standard", "Regulation", "Product Specification", "Guidelines", "Framework"],
                help="Select the type of document for targeted analysis"
            )
        
        with col2:
            # Analysis options
            st.markdown("**Analysis Options:**")
            
            enable_gap_analysis = st.checkbox(
                "Enable Gap Analysis",
                value=True,
                help="Comprehensive gap analysis using GUARDIAN patent algorithms"
            )
            
            enable_recommendations = st.checkbox(
                "Generate Recommendations",
                value=True,
                help="AI-powered policy recommendations and improvements"
            )
            
            enable_compliance_check = st.checkbox(
                "Compliance Assessment",
                value=True,
                help="Check compliance against major frameworks"
            )
        
        # Manual content input (if no file uploaded)
        if not uploaded_file:
            manual_content = st.text_area(
                "Manual Content Input",
                height=200,
                placeholder="Paste your policy content here if not uploading a file...",
                help="Enter policy text directly for analysis"
            )
        else:
            manual_content = ""
        
        submitted = st.form_submit_button("🔍 Analyze & Upload", type="primary")
        
        if submitted:
            # Process the document
            process_enhanced_upload(
                uploaded_file, title, document_type, manual_content,
                enable_gap_analysis, enable_recommendations, enable_compliance_check
            )

def process_enhanced_upload(uploaded_file, title: str, document_type: str, 
                          manual_content: str, enable_gap_analysis: bool,
                          enable_recommendations: bool, enable_compliance_check: bool):
    """Process uploaded document with comprehensive analysis."""
    
    if not title:
        st.error("Please provide a document title")
        return
    
    # Extract content from file or use manual input
    document_content = ""
    has_thumbnail = False
    
    if uploaded_file:
        with st.spinner("Processing uploaded file..."):
            if uploaded_file.name.lower().endswith('.pdf'):
                # Process PDF with thumbnail extraction
                temp_doc_id = int(time.time() * 1000) % 1000000
                pdf_result = process_uploaded_pdf_with_thumbnail(uploaded_file, temp_doc_id)
                document_content = pdf_result.get('text_content', '')
                has_thumbnail = pdf_result.get('thumbnail_data') is not None
            else:
                # Process text files
                document_content = uploaded_file.read().decode('utf-8')
    elif manual_content:
        document_content = manual_content
    else:
        st.error("Please upload a file or provide manual content")
        return
    
    if not document_content.strip():
        st.error("No content found in the document")
        return
    
    # Perform comprehensive analysis
    with st.spinner("Performing intelligent analysis using GUARDIAN patent algorithms..."):
        
        # Generate gap analysis report
        if enable_gap_analysis:
            gap_report = policy_gap_analyzer.analyze_policy_document(
                document_content, title, document_type.lower()
            )
            
            # Display comprehensive analysis results
            display_gap_analysis_results(gap_report)
            
            # Generate and display recommendations
            if enable_recommendations:
                display_intelligent_recommendations(gap_report, document_content)
            
            # Show compliance assessment
            if enable_compliance_check:
                display_compliance_assessment(gap_report)
        
        # Save document to database with enhanced metadata
        save_enhanced_document(
            title, document_content, document_type, 
            gap_report if enable_gap_analysis else None,
            has_thumbnail
        )

def display_gap_analysis_results(report: GapAnalysisReport):
    """Display comprehensive gap analysis results."""
    
    st.markdown("---")
    st.markdown("## 📊 **Comprehensive Gap Analysis Report**")
    
    # Overall maturity score
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.metric(
            "Overall Maturity",
            f"{report.overall_maturity_score}/100",
            help="Composite maturity score across all frameworks"
        )
    
    with col2:
        severity_counts = {}
        for gap in report.identified_gaps:
            severity_counts[gap.severity] = severity_counts.get(gap.severity, 0) + 1
        
        critical_gaps = severity_counts.get("Critical", 0)
        st.metric(
            "Critical Gaps",
            critical_gaps,
            delta=f"-{critical_gaps}" if critical_gaps > 0 else "0",
            delta_color="inverse"
        )
    
    with col3:
        # Framework scores visualization
        frameworks = ["AI Cyber", "Quantum Cyber", "AI Ethics", "Quantum Ethics"]
        scores = [
            report.framework_scores['ai_cybersecurity_score'],
            report.framework_scores['quantum_cybersecurity_score'] * 20,  # Convert to 100 scale
            report.framework_scores['ai_ethics_score'],
            report.framework_scores['quantum_ethics_score']
        ]
        
        score_text = " | ".join([f"{fw}: {score:.0f}" for fw, score in zip(frameworks, scores)])
        st.markdown(f"**Framework Scores:** {score_text}")
    
    # Detailed framework analysis
    st.markdown("### 🎯 **Framework Assessment**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 AI Cybersecurity", "⚛️ Quantum Cybersecurity", "🎯 AI Ethics", "🔬 Quantum Ethics"])
    
    with tab1:
        display_framework_analysis("AI Cybersecurity", report, "ai_cybersecurity_score")
    
    with tab2:
        display_framework_analysis("Quantum Cybersecurity", report, "quantum_cybersecurity_score")
    
    with tab3:
        display_framework_analysis("AI Ethics", report, "ai_ethics_score")
    
    with tab4:
        display_framework_analysis("Quantum Ethics", report, "quantum_ethics_score")
    
    # Identified gaps
    if report.identified_gaps:
        st.markdown("### 🔍 **Identified Policy Gaps**")
        
        # Group gaps by severity
        gaps_by_severity = {}
        for gap in report.identified_gaps:
            if gap.severity not in gaps_by_severity:
                gaps_by_severity[gap.severity] = []
            gaps_by_severity[gap.severity].append(gap)
        
        for severity in ["Critical", "High", "Medium", "Low"]:
            if severity in gaps_by_severity:
                with st.expander(f"{severity} Priority Gaps ({len(gaps_by_severity[severity])})", 
                               expanded=(severity in ["Critical", "High"])):
                    for gap in gaps_by_severity[severity]:
                        display_gap_details(gap)

def display_framework_analysis(framework_name: str, report: GapAnalysisReport, score_key: str):
    """Display detailed framework analysis."""
    
    score = report.framework_scores[score_key]
    if score_key == "quantum_cybersecurity_score":
        display_score = f"{score}/5 (QCMEA Tier {int(score)})"
        percentage = score * 20
    else:
        display_score = f"{score}/100"
        percentage = score
    
    # Score display with progress bar
    st.markdown(f"**{framework_name} Score:** {display_score}")
    st.progress(percentage / 100)
    
    # Framework-specific gaps
    framework_gaps = [gap for gap in report.identified_gaps if gap.framework == framework_name]
    
    if framework_gaps:
        st.markdown(f"**Gaps in {framework_name}:**")
        for gap in framework_gaps[:3]:  # Show top 3 gaps
            st.markdown(f"• **{gap.category}:** {gap.gap_description}")
    else:
        st.success(f"No significant gaps identified in {framework_name}")
    
    # Show compliance status if available
    relevant_compliance = {}
    for framework, status in report.compliance_status.items():
        if framework_name.lower().split()[0] in framework.lower():
            relevant_compliance[framework] = status
    
    if relevant_compliance:
        st.markdown("**Compliance Status:**")
        for framework, status in relevant_compliance.items():
            color = "🟢" if status == "Compliant" else "🟡" if "Partial" in status else "🔴"
            st.markdown(f"{color} {framework}: {status}")

def display_gap_details(gap):
    """Display detailed information about a specific gap."""
    
    # Gap header with severity indicator
    severity_colors = {
        "Critical": "🔴",
        "High": "🟠", 
        "Medium": "🟡",
        "Low": "🟢"
    }
    
    severity_color = severity_colors.get(gap.severity, "⚪")
    
    st.markdown(f"""
    **{severity_color} {gap.category} - {gap.framework}**
    
    *{gap.gap_description}*
    
    **Recommendations:**
    """)
    
    for i, recommendation in enumerate(gap.recommendations, 1):
        st.markdown(f"{i}. {recommendation}")
    
    # Additional details
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**Confidence:** {gap.confidence_score:.1%}")
    with col2:
        if gap.reference_documents:
            st.markdown(f"**References:** {', '.join(gap.reference_documents)}")
    
    st.markdown("---")

def display_intelligent_recommendations(report: GapAnalysisReport, content: str):
    """Display AI-powered intelligent recommendations."""
    
    st.markdown("### 💡 **Intelligent Recommendations**")
    
    # Strategic recommendations
    if report.strategic_recommendations:
        st.markdown("#### 🎯 **Strategic Priorities**")
        for i, recommendation in enumerate(report.strategic_recommendations, 1):
            st.markdown(f"{i}. {recommendation}")
    
    # Learning insights using patent algorithms
    if report.learning_insights:
        st.markdown("#### 🧠 **AI Learning Insights**")
        for insight in report.learning_insights:
            st.info(insight)
    
    # Similar document recommendations
    st.markdown("#### 📚 **Related Documents**")
    with st.spinner("Finding similar documents..."):
        try:
            # Build content vectors for similarity analysis
            recommendation_engine.build_content_vectors()
            
            # Get contextual recommendations based on document type and scores
            similar_docs = recommendation_engine.get_context_recommendations(
                document_type=report.document_type,
                framework_focus="ai_cybersecurity" if report.framework_scores['ai_cybersecurity_score'] > 50 else None,
                top_k=3
            )
            
            if similar_docs:
                for doc in similar_docs:
                    st.markdown(f"""
                    **{doc.get('title', 'Unknown Title')}**  
                    📍 {doc.get('organization', 'Unknown')} | 📄 {doc.get('document_type', 'Document')}
                    """)
            else:
                st.info("No similar documents found in the repository")
                
        except Exception as e:
            st.warning("Unable to generate document recommendations at this time")

def display_compliance_assessment(report: GapAnalysisReport):
    """Display compliance assessment results."""
    
    st.markdown("### ✅ **Compliance Assessment**")
    
    if report.compliance_status:
        col1, col2 = st.columns(2)
        
        compliance_items = list(report.compliance_status.items())
        mid_point = len(compliance_items) // 2
        
        with col1:
            for framework, status in compliance_items[:mid_point]:
                display_compliance_status(framework, status)
        
        with col2:
            for framework, status in compliance_items[mid_point:]:
                display_compliance_status(framework, status)
    else:
        st.info("No compliance frameworks assessed")

def display_compliance_status(framework: str, status: str):
    """Display individual compliance status."""
    
    if status == "Compliant":
        st.success(f"✅ {framework}: {status}")
    elif "Partial" in status:
        st.warning(f"⚠️ {framework}: {status}")
    else:
        st.error(f"❌ {framework}: {status}")

def save_enhanced_document(title: str, content: str, document_type: str, 
                         gap_report: Optional[GapAnalysisReport], has_thumbnail: bool):
    """Save document with enhanced metadata from gap analysis."""
    
    # Prepare document data
    document_data = {
        'title': title,
        'content': content[:200] + "..." if len(content) > 200 else content,
        'text': content,
        'document_type': document_type,
        'source': 'enhanced_policy_upload',
        'has_thumbnail': has_thumbnail
    }
    
    # Add scoring data if gap analysis was performed
    if gap_report:
        document_data.update({
            'ai_cybersecurity_score': gap_report.framework_scores['ai_cybersecurity_score'],
            'quantum_cybersecurity_score': gap_report.framework_scores['quantum_cybersecurity_score'],
            'ai_ethics_score': gap_report.framework_scores['ai_ethics_score'],
            'quantum_ethics_score': gap_report.framework_scores['quantum_ethics_score'],
            'quantum_q': gap_report.framework_scores['quantum_cybersecurity_score'] * 20  # Legacy compatibility
        })
    
    # Save to database
    try:
        success = save_document(document_data)
        if success:
            st.success("✅ Document successfully analyzed and saved to repository!")
            
            # Show summary
            if gap_report:
                st.markdown("### 📈 **Analysis Summary**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Maturity", f"{gap_report.overall_maturity_score}/100")
                
                with col2:
                    critical_gaps = len([g for g in gap_report.identified_gaps if g.severity == "Critical"])
                    st.metric("Critical Gaps", critical_gaps)
                
                with col3:
                    compliant_frameworks = len([s for s in gap_report.compliance_status.values() if s == "Compliant"])
                    st.metric("Compliant Frameworks", f"{compliant_frameworks}/{len(gap_report.compliance_status)}")
            
            st.balloons()
        else:
            st.error("Failed to save document to database")
            
    except Exception as e:
        st.error(f"Error saving document: {e}")

def render_policy_analysis_dashboard():
    """Render policy analysis dashboard for uploaded documents."""
    
    st.markdown("### 📋 **Policy Analysis Dashboard**")
    st.markdown("Monitor and analyze uploaded policy documents with comprehensive gap analysis.")
    
    # Dashboard placeholder - can be expanded with analytics
    st.info("Policy analysis dashboard - coming soon with advanced analytics and trend analysis.")