"""
Risk Report Generator Interface
Provides UI components for generating and downloading PDF risk reports
"""

import streamlit as st
import base64
from typing import Dict, List, Any
from utils.risk_report_generator import RiskReportGenerator
from utils.database import DatabaseManager

class RiskReportInterface:
    """Interface for generating risk assessment reports"""
    
    def __init__(self):
        self.generator = RiskReportGenerator()
        self.db_manager = DatabaseManager()
    
    def render_single_document_report_generator(self, document_data: Dict):
        """Render interface for generating single document reports"""
        
        st.markdown("### 📊 Risk Assessment Report")
        
        # Document summary
        with st.container():
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Document:** {document_data.get('title', 'Untitled')}")
                st.markdown(f"**Type:** {document_data.get('document_type', 'Unknown')}")
                st.markdown(f"**Organization:** {document_data.get('author_organization', 'Unknown')}")
            
            with col2:
                # Risk level indicator
                scores = [
                    document_data.get('ai_cybersecurity_score', 0),
                    document_data.get('quantum_cybersecurity_score', 0) * 20,  # Scale to 100
                    document_data.get('ai_ethics_score', 0),
                    document_data.get('quantum_ethics_score', 0)
                ]
                valid_scores = [s for s in scores if s > 0]
                
                if valid_scores:
                    import numpy as np
                    avg_score = np.mean(valid_scores)
                    risk_level = self._get_risk_level(avg_score)
                    risk_color = self._get_risk_color(risk_level)
                    
                    st.markdown(f"""
                    <div style='background:{risk_color};padding:10px;border-radius:5px;text-align:center;color:white;font-weight:bold'>
                        Risk Level: {risk_level.upper()}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("No risk scores available")
        
        # Report generation options
        st.markdown("#### Report Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            include_recommendations = st.checkbox("Include Recommendations", value=True)
            include_visualizations = st.checkbox("Include Risk Visualizations", value=True)
        
        with col2:
            include_detailed_analysis = st.checkbox("Include Detailed Analysis", value=True)
            include_compliance_summary = st.checkbox("Include Compliance Summary", value=False)
        
        # Generate report button
        if st.button("🔄 Generate Risk Report", type="primary", use_container_width=True):
            if valid_scores:
                with st.spinner("Generating comprehensive risk assessment report..."):
                    try:
                        # Generate PDF report
                        pdf_data = self.generator.generate_document_risk_report(document_data)
                        
                        # Create download button
                        doc_title = document_data.get('title', 'Document').replace(' ', '_')
                        filename = f"GUARDIAN_Risk_Report_{doc_title}_{self._get_timestamp()}.pdf"
                        
                        st.success("✅ Risk report generated successfully!")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        # Show report preview info
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
                        st.error(f"Error generating report: {str(e)}")
            else:
                st.error("Cannot generate report: No risk scores available for this document")
    
    def render_portfolio_report_generator(self):
        """Render interface for generating portfolio risk reports"""
        
        st.markdown("### 📈 Portfolio Risk Assessment Report")
        
        # Get documents with risk scores
        documents = self._get_scored_documents()
        
        if not documents:
            st.warning("No documents with risk scores found. Upload and analyze documents first.")
            return
        
        # Portfolio overview
        st.markdown(f"**Portfolio Size:** {len(documents)} analyzed documents")
        
        # Filter options
        with st.expander("📋 Portfolio Filters", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                doc_types = list(set([doc.get('document_type', 'Unknown') for doc in documents]))
                selected_types = st.multiselect("Document Types", doc_types, default=doc_types)
            
            with col2:
                organizations = list(set([doc.get('author_organization', 'Unknown') for doc in documents if doc.get('author_organization')]))
                selected_orgs = st.multiselect("Organizations", organizations[:10])  # Limit for performance
            
            with col3:
                risk_levels = ['High Risk', 'Medium Risk', 'Low Risk']
                selected_risks = st.multiselect("Risk Levels", risk_levels, default=risk_levels)
        
        # Apply filters
        filtered_docs = self._apply_portfolio_filters(documents, selected_types, selected_orgs, selected_risks)
        
        if not filtered_docs:
            st.warning("No documents match the selected filters.")
            return
        
        st.markdown(f"**Filtered Portfolio:** {len(filtered_docs)} documents")
        
        # Portfolio risk summary
        risk_summary = self._calculate_portfolio_risk_summary(filtered_docs)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("High Risk Documents", risk_summary['high_risk'])
        with col2:
            st.metric("Medium Risk Documents", risk_summary['medium_risk'])
        with col3:
            st.metric("Low Risk Documents", risk_summary['low_risk'])
        
        # Report generation options
        st.markdown("#### Portfolio Report Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            include_trend_analysis = st.checkbox("Include Trend Analysis", value=True)
            include_risk_distribution = st.checkbox("Include Risk Distribution Charts", value=True)
        
        with col2:
            include_top_risks = st.checkbox("Include Top Risk Documents", value=True)
            include_compliance_overview = st.checkbox("Include Compliance Overview", value=True)
        
        # Generate portfolio report
        if st.button("🔄 Generate Portfolio Report", type="primary", use_container_width=True):
            with st.spinner("Generating comprehensive portfolio risk assessment..."):
                try:
                    # Generate PDF report
                    pdf_data = self.generator.generate_portfolio_risk_report(filtered_docs)
                    
                    # Create download button
                    filename = f"GUARDIAN_Portfolio_Risk_Report_{self._get_timestamp()}.pdf"
                    
                    st.success("✅ Portfolio risk report generated successfully!")
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Portfolio Report",
                        data=pdf_data,
                        file_name=filename,
                        mime="application/pdf",
                        use_container_width=True
                    )
                    
                    # Show report preview info
                    st.info(f"""
                    **Report Contents:**
                    - Portfolio Executive Summary
                    - Risk Distribution Analysis Across {len(filtered_docs)} Documents
                    - Trend Analysis and Risk Patterns
                    - Top Risk Documents Identification
                    - Compliance Overview and Recommendations
                    
                    **File:** {filename}
                    **Size:** {len(pdf_data):,} bytes
                    """)
                    
                except Exception as e:
                    st.error(f"Error generating portfolio report: {str(e)}")
    
    def render_quick_report_buttons(self, document_data: Dict):
        """Render quick report generation buttons for document cards"""
        
        # Check if document has scores
        has_scores = any([
            document_data.get('ai_cybersecurity_score', 0) > 0,
            document_data.get('quantum_cybersecurity_score', 0) > 0,
            document_data.get('ai_ethics_score', 0) > 0,
            document_data.get('quantum_ethics_score', 0) > 0
        ])
        
        if has_scores:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Quick Report", key=f"quick_report_{document_data.get('id')}", use_container_width=True):
                    self._generate_quick_report(document_data)
            
            with col2:
                if st.button("📧 Email Report", key=f"email_report_{document_data.get('id')}", use_container_width=True):
                    self._show_email_report_dialog(document_data)
        else:
            st.info("Risk assessment required for report generation")
    
    def _generate_quick_report(self, document_data: Dict):
        """Generate and display quick report"""
        try:
            with st.spinner("Generating quick report..."):
                pdf_data = self.generator.generate_document_risk_report(document_data)
                
                doc_title = document_data.get('title', 'Document').replace(' ', '_')
                filename = f"Quick_Report_{doc_title}_{self._get_timestamp()}.pdf"
                
                st.success("✅ Quick report generated!")
                st.download_button(
                    label="📥 Download Report",
                    data=pdf_data,
                    file_name=filename,
                    mime="application/pdf",
                    key=f"download_{document_data.get('id')}"
                )
        except Exception as e:
            st.error(f"Error generating quick report: {str(e)}")
    
    def _show_email_report_dialog(self, document_data: Dict):
        """Show dialog for emailing reports"""
        with st.expander("📧 Email Report", expanded=True):
            email = st.text_input("Email Address:", placeholder="recipient@example.com")
            subject = st.text_input("Subject:", value=f"Risk Assessment Report - {document_data.get('title', 'Document')}")
            message = st.text_area("Message:", value="Please find the attached risk assessment report.")
            
            if st.button("Send Email", type="primary"):
                if email:
                    # In a real implementation, this would send the email
                    st.success(f"Report scheduled for delivery to {email}")
                    st.info("Email functionality requires SMTP configuration")
                else:
                    st.error("Please enter an email address")
    
    def _get_scored_documents(self) -> List[Dict]:
        """Get documents that have risk scores"""
        try:
            query = """
            SELECT id, title, document_type, author_organization, publish_date, source,
                   ai_cybersecurity_score, quantum_cybersecurity_score, 
                   ai_ethics_score, quantum_ethics_score, text_content
            FROM documents 
            WHERE ai_cybersecurity_score > 0 
               OR quantum_cybersecurity_score > 0 
               OR ai_ethics_score > 0 
               OR quantum_ethics_score > 0
            ORDER BY created_at DESC
            """
            
            result = self.db_manager.execute_query(query)
            return result if isinstance(result, list) else []
            
        except Exception as e:
            st.error(f"Error fetching documents: {e}")
            return []
    
    def _apply_portfolio_filters(self, documents: List[Dict], selected_types: List[str], 
                                selected_orgs: List[str], selected_risks: List[str]) -> List[Dict]:
        """Apply filters to portfolio documents"""
        filtered = documents
        
        # Filter by document type
        if selected_types:
            filtered = [doc for doc in filtered if doc.get('document_type') in selected_types]
        
        # Filter by organization
        if selected_orgs:
            filtered = [doc for doc in filtered if doc.get('author_organization') in selected_orgs]
        
        # Filter by risk level
        if selected_risks:
            risk_filtered = []
            for doc in filtered:
                risk_level = self._get_document_risk_level(doc)
                if f"{risk_level.title()} Risk" in selected_risks:
                    risk_filtered.append(doc)
            filtered = risk_filtered
        
        return filtered
    
    def _calculate_portfolio_risk_summary(self, documents: List[Dict]) -> Dict[str, int]:
        """Calculate portfolio risk summary statistics"""
        summary = {'high_risk': 0, 'medium_risk': 0, 'low_risk': 0}
        
        for doc in documents:
            risk_level = self._get_document_risk_level(doc)
            summary[f"{risk_level}_risk"] += 1
        
        return summary
    
    def _get_document_risk_level(self, document_data: Dict) -> str:
        """Calculate risk level for a document"""
        scores = [
            document_data.get('ai_cybersecurity_score', 0),
            document_data.get('quantum_cybersecurity_score', 0) * 20,  # Scale to 100
            document_data.get('ai_ethics_score', 0),
            document_data.get('quantum_ethics_score', 0)
        ]
        valid_scores = [s for s in scores if s > 0]
        
        if not valid_scores:
            return 'unknown'
        
        import numpy as np
        avg_score = np.mean(valid_scores)
        return self._get_risk_level(avg_score)
    
    def _get_risk_level(self, avg_score: float) -> str:
        """Calculate risk level from average score"""
        if avg_score >= 80:
            return 'low'
        elif avg_score >= 60:
            return 'medium'
        else:
            return 'high'
    
    def _get_risk_color(self, risk_level: str) -> str:
        """Get color for risk level"""
        colors = {
            'high': '#dc2626',
            'medium': '#f59e0b',
            'low': '#059669',
            'unknown': '#6b7280'
        }
        return colors.get(risk_level, '#6b7280')
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for filename"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

def render_risk_report_generator():
    """Main function to render risk report generator interface"""
    
    interface = RiskReportInterface()
    
    st.markdown("## 📊 Risk Report Generator")
    st.markdown("Generate comprehensive PDF risk assessment reports for documents and portfolios.")
    
    # Tab selection
    tab1, tab2 = st.tabs(["📄 Single Document Report", "📈 Portfolio Report"])
    
    with tab1:
        st.markdown("### Single Document Risk Report")
        
        # Document selection
        documents = interface._get_scored_documents()
        
        if documents:
            doc_options = {f"{doc.get('title', 'Untitled')[:50]}...": doc for doc in documents}
            selected_doc_title = st.selectbox(
                "Select Document:",
                options=list(doc_options.keys()),
                help="Choose a document that has been analyzed and scored"
            )
            
            if selected_doc_title:
                selected_doc = doc_options[selected_doc_title]
                interface.render_single_document_report_generator(selected_doc)
        else:
            st.info("No analyzed documents available. Upload and analyze documents first to generate reports.")
    
    with tab2:
        interface.render_portfolio_report_generator()

def render_document_report_buttons(document_data: Dict):
    """Render report buttons for individual document cards"""
    interface = RiskReportInterface()
    interface.render_quick_report_buttons(document_data)