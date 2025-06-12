"""
Enhanced Policy Document Uploader with AI-Powered Gap Analysis
Implements GUARDIAN patent's policy reinforcement learning and recommendation capabilities
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge, Circle
import numpy as np
import base64
import io
from typing import Optional, Dict, List
from utils.policy_gap_analyzer import policy_gap_analyzer, GapAnalysisReport
from utils.professional_gauge_generator import create_professional_assessment_dashboard, create_quantum_assessment_dashboard
from utils.document_recommendation_engine import recommendation_engine
from utils.db import save_document
from utils.pdf_ingestion_thumbnails import process_uploaded_pdf_with_thumbnail
import time

# Import the exact gauge function from about_tab to ensure consistency
from about_tab import create_speedometer_dial

def create_tier_bubbles(value, max_value=5):
    """Create tier bubble visualization for 1-5 scale."""
    fig, ax = plt.subplots(figsize=(2, 0.8), facecolor='white')
    
    # Define tier colors - bold vibrant primary colors
    tier_colors = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#008000']
    
    # Draw bubbles
    for i in range(max_value):
        x = i * 0.4
        color = tier_colors[i] if i < value else '#e5e7eb'
        alpha = 1.0 if i < value else 0.3
        
        circle = Circle((x, 0), 0.15, color=color, alpha=alpha)
        ax.add_patch(circle)
        
        # Add tier number
        ax.text(x, 0, str(i+1), ha='center', va='center', 
               fontsize=8, fontweight='bold', color='white' if i < value else '#9ca3af')
    
    ax.set_xlim(-0.2, (max_value-1) * 0.4 + 0.2)
    ax.set_ylim(-0.3, 0.3)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Convert to base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100, 
                facecolor='white', transparent=True)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close(fig)
    
    return f'<img src="data:image/png;base64,{image_base64}" style="width: 160px; height: 64px; display: block; margin: 0 auto;">'

def render_enhanced_policy_uploader():
    """Render enhanced document uploader with intelligent gap analysis and recommendations."""
    
    # Enhanced header matching Cyber Institute style
    st.markdown(
        """<div style="background: linear-gradient(135deg, #082454 0%, #10244D 50%, #133169 100%); padding: 2.5rem; border-radius: 12px; margin-bottom: 2rem; color: white;">
            <h1 style="color: white; margin-bottom: 1.2rem; font-size: 2.2rem; font-weight: 700; text-align: center;">
                Intelligent Policy Analysis & Upload
            </h1>
            <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 10px; margin: 1.5rem 0; border: 1px solid rgba(255,255,255,0.2);">
                <h3 style="color: #3D9BE9; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600; text-align: center;">
                    AI-Powered Gap Analysis & Recommendation Engine
                </h3>
                <p style="color: #e5e7eb; text-align: center; font-size: 1.1rem; line-height: 1.6; margin: 0;">
                    Upload your draft policies, standards, regulations, or product specifications for comprehensive gap analysis and intelligent recommendations.
                </p>
            </div>
        </div>""", 
        unsafe_allow_html=True
    )
    
    # Standalone report generation button (outside form)
    if 'latest_gap_report' in st.session_state:
        st.markdown("---")
        st.markdown("### **Generate Comprehensive Report**")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info("Create a professional PDF report containing all the analysis results shown above, formatted for sharing and documentation.")
        
        with col2:
            if st.button("Generate PDF Report", type="primary", use_container_width=True):
                report_data = st.session_state.latest_gap_report
                generate_standalone_report(
                    report_data['title'], 
                    report_data['content'], 
                    report_data['document_type'], 
                    report_data['gap_report'], 
                    report_data['has_thumbnail']
                )
        st.markdown("---")

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
            
            generate_report = st.checkbox(
                "Generate Report",
                value=False,
                help="Create comprehensive PDF risk assessment report after analysis"
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
        
        submitted = st.form_submit_button("Upload & Analyze", type="primary")
        
        if submitted:
            # Process the document
            process_enhanced_upload(
                uploaded_file, title, document_type, manual_content,
                enable_gap_analysis, enable_recommendations, enable_compliance_check,
                generate_report
            )

def process_enhanced_upload(uploaded_file, title: str, document_type: str, 
                          manual_content: str, enable_gap_analysis: bool,
                          enable_recommendations: bool, enable_compliance_check: bool,
                          generate_report: bool = False):
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
            
            # Store gap report in session state for button outside form
            if gap_report:
                st.session_state.latest_gap_report = {
                    'title': title,
                    'content': document_content,
                    'document_type': document_type,
                    'gap_report': gap_report,
                    'has_thumbnail': has_thumbnail
                }
        
        # Save document to database with enhanced metadata
        save_enhanced_document(
            title, document_content, document_type, 
            gap_report if enable_gap_analysis else None,
            has_thumbnail, generate_report
        )

def display_gap_analysis_results(report: GapAnalysisReport):
    """Display comprehensive gap analysis results."""
    
    st.markdown("---")
    st.markdown("## **Comprehensive Gap Analysis Report**")
    
    # Professional Assessment Dashboard
    st.markdown("### **Assessment Dashboard**")
    
    # Get topic detection results if available
    if 'topic_detection' in report.framework_scores and isinstance(report.framework_scores['topic_detection'], dict):
        topic_detection = report.framework_scores['topic_detection']
    else:
        # Fallback: assume AI-related if any AI scores > 0
        ai_cyber_score = int(report.framework_scores['ai_cybersecurity_score'])
        ai_ethics_score = int(report.framework_scores['ai_ethics_score'])
        quantum_cyber_score = int(report.framework_scores['quantum_cybersecurity_score'])
        quantum_ethics_score = int(report.framework_scores['quantum_ethics_score'])
        
        topic_detection = {
            'is_ai_related': ai_cyber_score > 0 or ai_ethics_score > 0,
            'is_quantum_related': quantum_cyber_score > 0 or quantum_ethics_score > 0,
            'ai_keyword_count': 0,
            'quantum_keyword_count': 0
        }
    
    # Display topic detection information
    st.markdown("#### **Document Topic Analysis**")
    topic_col1, topic_col2 = st.columns(2)
    
    with topic_col1:
        ai_status = "✅ AI-Related" if topic_detection['is_ai_related'] else "❌ Not AI-Related"
        st.markdown(f"**{ai_status}**")
        if topic_detection.get('ai_keyword_count', 0) > 0:
            st.caption(f"AI keywords found: {topic_detection['ai_keyword_count']}")
    
    with topic_col2:
        quantum_status = "✅ Quantum-Related" if topic_detection['is_quantum_related'] else "❌ Not Quantum-Related"
        st.markdown(f"**{quantum_status}**")
        if topic_detection.get('quantum_keyword_count', 0) > 0:
            st.caption(f"Quantum keywords found: {topic_detection['quantum_keyword_count']}")
    
    # Create scores data for professional dashboard only if relevant
    scores_data = {
        'ai_cybersecurity_score': int(report.framework_scores['ai_cybersecurity_score']),
        'ai_ethics_score': int(report.framework_scores['ai_ethics_score']),
        'quantum_cybersecurity_score': int(report.framework_scores['quantum_cybersecurity_score']),
        'quantum_ethics_score': int(report.framework_scores['quantum_ethics_score']),
        'topic_detection': topic_detection
    }
    
    # Only add parameter scores for AI if document is AI-related
    if topic_detection['is_ai_related'] and scores_data['ai_cybersecurity_score'] > 0:
        scores_data.update({
            'encryption_standards': min(85, int(report.framework_scores['ai_cybersecurity_score']) + 10),
            'authentication_systems': min(95, int(report.framework_scores['ai_cybersecurity_score']) + 5),
            'threat_monitoring': max(45, int(report.framework_scores['ai_cybersecurity_score']) - 10),
            'incident_response': max(55, int(report.framework_scores['ai_cybersecurity_score']) - 5),
            'adaptability_score': min(85, int(report.framework_scores['ai_cybersecurity_score']) + 5),
            'legal_alignment_score': max(50, int(report.framework_scores['ai_ethics_score']) - 10),
            'implementation_feasibility': min(75, int(report.framework_scores['ai_ethics_score']) + 5)
        })
    
    # Display AI Cybersecurity Dashboard
    if scores_data['ai_cybersecurity_score'] > 0:
        dashboard_img = create_professional_assessment_dashboard(scores_data)
        st.markdown(f'<img src="data:image/png;base64,{dashboard_img}" style="width:100%; max-width:800px; margin:20px 0;">', unsafe_allow_html=True)
    
    # Display Quantum Cybersecurity Dashboard if quantum scores exist
    if scores_data['quantum_cybersecurity_score'] > 0:
        st.markdown("---")
        quantum_dashboard_img = create_quantum_assessment_dashboard(scores_data)
        st.markdown(f'<img src="data:image/png;base64,{quantum_dashboard_img}" style="width:100%; max-width:800px; margin:20px 0;">', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Critical gaps and framework scores
    col1, col2 = st.columns([1, 2])
    
    with col1:
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
    
    with col2:
        # Only show Framework Scores section for quantum or mixed documents
        topic_detection = report.framework_scores.get('topic_detection', {})
        is_quantum_related = topic_detection.get('is_quantum_related', False)
        is_ai_related = topic_detection.get('is_ai_related', True)
        
        if is_quantum_related:
            st.markdown("**Framework Scores:**")
            
            # Create 2x2 grid for gauges
            gauge_col1, gauge_col2 = st.columns(2)
            
            with gauge_col1:
                # AI Cybersecurity Gauge
                ai_cyber_score = int(report.framework_scores['ai_cybersecurity_score'])
                if topic_detection['is_ai_related'] and ai_cyber_score > 0:
                    st.markdown("<div style='text-align: center; margin-bottom: 15px;'>", unsafe_allow_html=True)
                    gauge_html = create_speedometer_dial(ai_cyber_score, 100)
                    st.markdown(gauge_html, unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; margin-top: 5px;'><strong>AI Cybersecurity</strong><br><span style='font-size: 14px; color: #666;'>{ai_cyber_score}/100</span></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'><strong>AI Cybersecurity</strong><br><span style='color: #6c757d;'>N/A - Not AI-Related</span></div>", unsafe_allow_html=True)
                
                # AI Ethics Gauge
                ai_ethics_score = int(report.framework_scores['ai_ethics_score'])
                if topic_detection['is_ai_related'] and ai_ethics_score > 0:
                    st.markdown("<div style='text-align: center; margin-bottom: 15px;'>", unsafe_allow_html=True)
                    gauge_html = create_speedometer_dial(ai_ethics_score, 100)
                    st.markdown(gauge_html, unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; margin-top: 5px;'><strong>AI Ethics</strong><br><span style='font-size: 14px; color: #666;'>{ai_ethics_score}/100</span></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'><strong>AI Ethics</strong><br><span style='color: #6c757d;'>N/A - Not AI-Related</span></div>", unsafe_allow_html=True)
            
            with gauge_col2:
                # Quantum Cybersecurity Tier Bubbles
                quantum_cyber_score = int(report.framework_scores['quantum_cybersecurity_score'])
                if topic_detection['is_quantum_related'] and quantum_cyber_score > 0:
                    st.markdown("<div style='text-align: center; margin-bottom: 15px;'>", unsafe_allow_html=True)
                    tier_html = create_tier_bubbles(quantum_cyber_score, 5)
                    st.markdown(tier_html, unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; margin-top: 5px;'><strong>Quantum Cybersecurity</strong><br><span style='font-size: 14px; color: #666;'>Tier {quantum_cyber_score}/5</span></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'><strong>Quantum Cybersecurity</strong><br><span style='color: #6c757d;'>N/A - Not Quantum-Related</span></div>", unsafe_allow_html=True)
                
                # Quantum Ethics Gauge
                quantum_ethics_score = int(report.framework_scores['quantum_ethics_score'])
                if topic_detection['is_quantum_related'] and quantum_ethics_score > 0:
                    st.markdown("<div style='text-align: center; margin-bottom: 15px;'>", unsafe_allow_html=True)
                    gauge_html = create_speedometer_dial(quantum_ethics_score, 100)
                    st.markdown(gauge_html, unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align: center; margin-top: 5px;'><strong>Quantum Ethics</strong><br><span style='font-size: 14px; color: #666;'>{quantum_ethics_score}/100</span></div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'><strong>Quantum Ethics</strong><br><span style='color: #6c757d;'>N/A - Not Quantum-Related</span></div>", unsafe_allow_html=True)
        else:
            # For AI-only documents, show a simple message
            st.markdown("**AI Policy Analysis Complete**")
            st.info("Framework scores are displayed in the main dashboard above. The detailed tabs below provide comprehensive analysis for each applicable framework.")
    
    # Detailed framework analysis
    st.markdown("### **Framework Assessment**")
    
    tab1, tab2, tab3, tab4 = st.tabs(["AI Cybersecurity", "Quantum Cybersecurity", "AI Ethics", "Quantum Ethics"])
    
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
        st.markdown("### **Identified Policy Gaps**")
        
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
    
    st.markdown("### **Intelligent Recommendations**")
    
    # Strategic recommendations
    if report.strategic_recommendations:
        st.markdown("#### **Strategic Priorities**")
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
    
    st.markdown("### **Compliance Assessment**")
    
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
        st.success(f"{framework}: {status}")
    elif "Partial" in status:
        st.warning(f"{framework}: {status}")
    else:
        st.error(f"{framework}: {status}")

def save_enhanced_document(title: str, content: str, document_type: str, 
                         gap_report: Optional[GapAnalysisReport], has_thumbnail: bool,
                         generate_report: bool = False):
    """Save document with enhanced metadata from gap analysis."""
    
    # Check for duplicates first
    try:
        from utils.duplicate_detector import check_document_duplicates
        
        duplicate_result = check_document_duplicates(
            title=title,
            content=content,
            url="",
            filename=""
        )
        
        if duplicate_result["is_duplicate"]:
            st.error("Duplicate document detected!")
            st.warning(f"Confidence: {duplicate_result['confidence']:.1%} - {duplicate_result.get('match_type', 'Unknown')}")
            
            if duplicate_result.get("matches"):
                st.info("Similar to existing documents:")
                for match in duplicate_result["matches"][:2]:
                    st.markdown(f"• **{match.get('title', 'Unknown')}** (ID: {match.get('id')}) - {match.get('reason', 'Similar content')}")
            
            st.warning("Document not saved to prevent duplicates. Please check if this document already exists in your repository.")
            return False
            
    except ImportError:
        st.warning("Duplicate detection temporarily unavailable")
    except Exception as e:
        st.warning(f"Duplicate check failed: {str(e)}")
    
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
            st.success("Document successfully analyzed and saved to repository!")
            
            # Show summary
            if gap_report:
                st.markdown("### **Analysis Summary**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Overall Maturity", f"{gap_report.overall_maturity_score}/100")
                
                with col2:
                    critical_gaps = len([g for g in gap_report.identified_gaps if g.severity == "Critical"])
                    st.metric("Critical Gaps", critical_gaps)
                
                with col3:
                    compliant_frameworks = len([s for s in gap_report.compliance_status.values() if s == "Compliant"])
                    st.metric("Compliant Frameworks", f"{compliant_frameworks}/{len(gap_report.compliance_status)}")
            
            # Generate PDF report if requested
            if generate_report and gap_report:
                st.markdown("### **Generating Risk Assessment Report**")
                try:
                    from utils.risk_report_generator import RiskReportGenerator
                    
                    generator = RiskReportGenerator()
                    
                    # Prepare document data for report generation
                    report_doc_data = document_data.copy()
                    report_doc_data['text_content'] = content
                    
                    with st.spinner("Creating comprehensive PDF report..."):
                        pdf_data = generator.generate_document_risk_report(report_doc_data)
                    
                    # Create filename
                    safe_title = title.replace(' ', '_').replace('/', '_')[:30]
                    from datetime import datetime
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"GUARDIAN_Risk_Report_{safe_title}_{timestamp}.pdf"
                    
                    st.success("Risk assessment report generated successfully!")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download PDF Risk Report",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    st.info(f"""
                    **Report Contents:**
                    - Executive Summary with Risk Level Assessment
                    - Risk Assessment Dashboard with Visualizations
                    - Detailed Analysis by Risk Category
                    - Prioritized Recommendations and Action Items
                    
                    **File:** {filename}
                    **Size:** {len(pdf_data):,} bytes
                    """)
                    
                except Exception as e:
                    st.error(f"Error generating PDF report: {str(e)}")
                    st.info("Report generation failed, but document was saved successfully.")
            
            st.balloons()
        else:
            st.error("Failed to save document to database")
            
    except Exception as e:
        st.error(f"Error saving document: {e}")

def generate_standalone_report(title: str, content: str, document_type: str, 
                              gap_report: GapAnalysisReport, has_thumbnail: bool):
    """Generate standalone PDF report containing the same analysis results displayed on screen."""
    
    try:
        from utils.enhanced_risk_report_generator import EnhancedRiskReportGenerator
        
        st.markdown("### **Generating Comprehensive Analysis Report**")
        
        with st.spinner("Creating professional PDF report with all analysis results..."):
            generator = EnhancedRiskReportGenerator()
            
            # Prepare comprehensive document data that matches on-screen analysis
            report_doc_data = {
                'title': title,
                'document_type': document_type,
                'text_content': content,
                'content': content[:200] + "..." if len(content) > 200 else content,
                'source': 'policy_analyzer',
                'has_thumbnail': has_thumbnail,
                
                # Include all scoring data from gap analysis
                'ai_cybersecurity_score': gap_report.framework_scores['ai_cybersecurity_score'],
                'quantum_cybersecurity_score': gap_report.framework_scores['quantum_cybersecurity_score'],
                'ai_ethics_score': gap_report.framework_scores['ai_ethics_score'],
                'quantum_ethics_score': gap_report.framework_scores['quantum_ethics_score'],
                
                # Include gap analysis results
                'gap_analysis_report': gap_report,
                'overall_maturity_score': gap_report.overall_maturity_score,
                'identified_gaps': gap_report.identified_gaps,
                'compliance_status': gap_report.compliance_status,
                'strategic_recommendations': gap_report.strategic_recommendations
            }
            
            # Generate enhanced PDF that matches screen content
            pdf_data = generator.generate_policy_analysis_report(report_doc_data)
        
        # Create filename
        safe_title = title.replace(' ', '_').replace('/', '_')[:30]
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"GUARDIAN_Policy_Analysis_{safe_title}_{timestamp}.pdf"
        
        st.success("Comprehensive analysis report generated successfully!")
        
        # Download button
        st.download_button(
            label="📥 Download Complete Analysis Report",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )
        
        st.info(f"""
        **Report Contents (Same as Screen Analysis):**
        - Executive Summary with Overall Maturity Score ({gap_report.overall_maturity_score}/100)
        - Detailed Framework Scoring (AI Cyber, Quantum Cyber, AI Ethics, Quantum Ethics)
        - Comprehensive Gap Analysis ({len(gap_report.identified_gaps)} gaps identified)
        - Compliance Assessment ({len(gap_report.compliance_status)} frameworks evaluated)
        - Intelligent Recommendations ({len(gap_report.strategic_recommendations)} action items)
        - Risk Visualizations and Professional Formatting
        
        **File:** {filename}
        **Size:** {len(pdf_data):,} bytes
        """)
        
    except Exception as e:
        st.error(f"Error generating comprehensive report: {str(e)}")
        st.info("Please try again or contact support if the issue persists.")

def render_policy_analysis_dashboard():
    """Render policy analysis dashboard for uploaded documents."""
    
    st.markdown("### **Policy Analysis Dashboard**")
    st.markdown("Monitor and analyze uploaded policy documents with comprehensive gap analysis.")
    
    # Dashboard placeholder - can be expanded with analytics
    st.info("Policy analysis dashboard - coming soon with advanced analytics and trend analysis.")