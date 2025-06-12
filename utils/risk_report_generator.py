"""
One-Click Risk Report Generator
Creates comprehensive PDF risk assessment reports with visualizations and analytics
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
from datetime import datetime
import io
import base64
from typing import Dict, List, Any, Optional

class RiskReportGenerator:
    """Generate comprehensive PDF risk assessment reports"""
    
    def __init__(self):
        self.colors = {
            'high_risk': '#dc2626',      # Red
            'medium_risk': '#f59e0b',    # Orange  
            'low_risk': '#059669',       # Green
            'primary': '#1f2937',        # Dark Gray
            'secondary': '#6b7280',      # Medium Gray
            'accent': '#3b82f6',         # Blue
            'background': '#f9fafb'      # Light Gray
        }
        
    def generate_document_risk_report(self, document_data: Dict) -> bytes:
        """Generate a comprehensive risk report for a single document"""
        
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        
        with PdfPages(pdf_buffer) as pdf:
            # Page 1: Executive Summary
            self._create_executive_summary_page(pdf, document_data)
            
            # Page 2: Risk Assessment Dashboard
            self._create_risk_dashboard_page(pdf, document_data)
            
            # Page 3: Detailed Risk Analysis
            self._create_detailed_analysis_page(pdf, document_data)
            
            # Page 4: Recommendations & Action Items
            self._create_recommendations_page(pdf, document_data)
        
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    
    def generate_portfolio_risk_report(self, documents: List[Dict]) -> bytes:
        """Generate a comprehensive risk report for multiple documents"""
        
        pdf_buffer = io.BytesIO()
        
        with PdfPages(pdf_buffer) as pdf:
            # Page 1: Portfolio Executive Summary
            self._create_portfolio_summary_page(pdf, documents)
            
            # Page 2: Risk Distribution Analysis
            self._create_portfolio_risk_distribution_page(pdf, documents)
            
            # Page 3: Trend Analysis
            self._create_portfolio_trend_analysis_page(pdf, documents)
            
            # Page 4: Top Risk Documents
            self._create_portfolio_top_risks_page(pdf, documents)
        
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    
    def _create_executive_summary_page(self, pdf: PdfPages, document_data: Dict):
        """Create executive summary page for single document"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        self._add_header(ax, "GUARDIAN Risk Assessment Report")
        
        # Document title and metadata
        title = document_data.get('title', 'Untitled Document')[:80]
        ax.text(5, 12, title, fontsize=16, weight='bold', ha='center', wrap=True)
        
        # Key metrics section
        y_pos = 11
        scores = {
            'AI Cybersecurity': document_data.get('ai_cybersecurity_score', 0),
            'Quantum Cybersecurity': document_data.get('quantum_cybersecurity_score', 0),
            'AI Ethics': document_data.get('ai_ethics_score', 0),
            'Quantum Ethics': document_data.get('quantum_ethics_score', 0)
        }
        
        # Risk level calculation
        avg_score = np.mean([s for s in scores.values() if s > 0])
        risk_level = self._calculate_risk_level(avg_score)
        risk_color = self._get_risk_color(risk_level)
        
        # Risk level indicator
        rect = patches.Rectangle((4, y_pos-0.3), 2, 0.6, 
                               facecolor=risk_color, alpha=0.8, edgecolor='black')
        ax.add_patch(rect)
        ax.text(5, y_pos, f"Risk Level: {risk_level.upper()}", 
               fontsize=14, weight='bold', ha='center', va='center', color='white')
        
        # Scoring matrix
        y_pos = 9.5
        ax.text(5, y_pos, "Risk Assessment Scores", fontsize=14, weight='bold', ha='center')
        
        y_pos = 8.8
        for metric, score in scores.items():
            if score > 0:
                score_color = self._get_score_color(score, metric)
                ax.text(2, y_pos, f"{metric}:", fontsize=12, weight='bold')
                ax.text(7, y_pos, f"{score}/100" if 'Ethics' in metric or 'AI' in metric else f"{score}/5", 
                       fontsize=12, color=score_color, weight='bold')
                y_pos -= 0.4
        
        # Key findings
        y_pos -= 0.5
        ax.text(5, y_pos, "Key Findings", fontsize=14, weight='bold', ha='center')
        
        findings = self._generate_key_findings(document_data, scores)
        y_pos -= 0.4
        for finding in findings[:4]:  # Top 4 findings
            ax.text(1, y_pos, f"• {finding}", fontsize=10, wrap=True)
            y_pos -= 0.4
        
        # Footer
        self._add_footer(ax)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_risk_dashboard_page(self, pdf: PdfPages, document_data: Dict):
        """Create risk dashboard with visualizations"""
        fig = plt.figure(figsize=(8.5, 11))
        
        # Create grid layout
        gs = fig.add_gridspec(4, 2, height_ratios=[0.5, 1, 1, 1], width_ratios=[1, 1])
        
        # Header
        header_ax = fig.add_subplot(gs[0, :])
        header_ax.text(0.5, 0.5, "Risk Assessment Dashboard", 
                      fontsize=18, weight='bold', ha='center', va='center')
        header_ax.axis('off')
        
        # Risk radar chart
        radar_ax = fig.add_subplot(gs[1, 0], projection='polar')
        self._create_risk_radar_chart(radar_ax, document_data)
        
        # Risk distribution pie chart
        pie_ax = fig.add_subplot(gs[1, 1])
        self._create_risk_distribution_chart(pie_ax, document_data)
        
        # Trend indicators
        trend_ax = fig.add_subplot(gs[2, :])
        self._create_trend_indicators(trend_ax, document_data)
        
        # Risk matrix
        matrix_ax = fig.add_subplot(gs[3, :])
        self._create_risk_matrix(matrix_ax, document_data)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_detailed_analysis_page(self, pdf: PdfPages, document_data: Dict):
        """Create detailed risk analysis page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        ax.text(5, 13.5, "Detailed Risk Analysis", fontsize=18, weight='bold', ha='center')
        
        # Document metadata
        y_pos = 12.8
        metadata = {
            'Document Type': document_data.get('document_type', 'Unknown'),
            'Organization': document_data.get('author_organization', 'Unknown'),
            'Date': document_data.get('publish_date', 'Unknown'),
            'Source': document_data.get('source', 'Unknown')
        }
        
        for key, value in metadata.items():
            ax.text(1, y_pos, f"{key}:", fontsize=12, weight='bold')
            ax.text(3.5, y_pos, str(value)[:50], fontsize=12)
            y_pos -= 0.3
        
        # Risk category analysis
        y_pos -= 0.5
        ax.text(5, y_pos, "Risk Category Analysis", fontsize=14, weight='bold', ha='center')
        
        categories = [
            ('AI Cybersecurity', document_data.get('ai_cybersecurity_score', 0), 
             "Artificial Intelligence security vulnerabilities and protection measures"),
            ('Quantum Cybersecurity', document_data.get('quantum_cybersecurity_score', 0),
             "Quantum computing threats and quantum-safe cryptography readiness"),
            ('AI Ethics', document_data.get('ai_ethics_score', 0),
             "Ethical AI considerations including bias, fairness, and transparency"),
            ('Quantum Ethics', document_data.get('quantum_ethics_score', 0),
             "Quantum technology ethical implications and governance frameworks")
        ]
        
        y_pos -= 0.4
        for category, score, description in categories:
            if score > 0:
                # Category header
                ax.text(1, y_pos, category, fontsize=12, weight='bold', color=self.colors['primary'])
                ax.text(8, y_pos, f"Score: {score}", fontsize=12, weight='bold', 
                       color=self._get_score_color(score, category))
                y_pos -= 0.25
                
                # Description
                ax.text(1.2, y_pos, description, fontsize=10, style='italic', wrap=True)
                y_pos -= 0.3
                
                # Risk assessment
                risk_text = self._generate_risk_assessment_text(category, score)
                ax.text(1.2, y_pos, risk_text, fontsize=10, wrap=True)
                y_pos -= 0.5
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_recommendations_page(self, pdf: PdfPages, document_data: Dict):
        """Create recommendations and action items page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        ax.text(5, 13.5, "Recommendations & Action Items", fontsize=18, weight='bold', ha='center')
        
        # Priority recommendations
        y_pos = 12.8
        ax.text(5, y_pos, "Priority Recommendations", fontsize=14, weight='bold', ha='center')
        
        recommendations = self._generate_recommendations(document_data)
        
        y_pos -= 0.5
        for i, (priority, rec) in enumerate(recommendations[:8]):  # Top 8 recommendations
            color = self.colors['high_risk'] if priority == 'High' else \
                   self.colors['medium_risk'] if priority == 'Medium' else self.colors['low_risk']
            
            # Priority indicator
            rect = patches.Rectangle((0.5, y_pos-0.1), 0.3, 0.2, 
                                   facecolor=color, alpha=0.8)
            ax.add_patch(rect)
            ax.text(0.65, y_pos, priority[0], fontsize=10, weight='bold', 
                   ha='center', va='center', color='white')
            
            # Recommendation text
            ax.text(1, y_pos, f"{i+1}. {rec}", fontsize=10, wrap=True)
            y_pos -= 0.6
        
        # Implementation timeline
        y_pos -= 0.5
        ax.text(5, y_pos, "Implementation Timeline", fontsize=14, weight='bold', ha='center')
        
        timeline_items = [
            ("Immediate (0-30 days)", "Address critical AI cybersecurity vulnerabilities"),
            ("Short-term (1-3 months)", "Implement quantum-safe cryptography planning"),
            ("Medium-term (3-6 months)", "Develop comprehensive AI ethics framework"),
            ("Long-term (6+ months)", "Complete quantum cybersecurity transformation")
        ]
        
        y_pos -= 0.4
        for timeframe, action in timeline_items:
            ax.text(1, y_pos, timeframe, fontsize=11, weight='bold', color=self.colors['accent'])
            ax.text(1.2, y_pos-0.25, action, fontsize=10)
            y_pos -= 0.7
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_portfolio_summary_page(self, pdf: PdfPages, documents: List[Dict]):
        """Create portfolio executive summary"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        self._add_header(ax, "GUARDIAN Portfolio Risk Assessment")
        
        # Portfolio overview
        total_docs = len(documents)
        ax.text(5, 12, f"Portfolio Overview: {total_docs} Documents Analyzed", 
               fontsize=16, weight='bold', ha='center')
        
        # Calculate portfolio metrics
        risk_distribution = self._calculate_portfolio_risk_distribution(documents)
        
        # Risk summary visualization
        y_pos = 10.5
        ax.text(5, y_pos, "Portfolio Risk Distribution", fontsize=14, weight='bold', ha='center')
        
        # Create horizontal bar chart for risk levels
        y_pos = 9.5
        for risk_level, count in risk_distribution.items():
            if count > 0:
                color = self._get_risk_color(risk_level)
                percentage = (count / total_docs) * 100
                
                # Risk level bar
                bar_width = percentage / 100 * 6  # Scale to fit
                rect = patches.Rectangle((2, y_pos-0.15), bar_width, 0.3, 
                                       facecolor=color, alpha=0.8)
                ax.add_patch(rect)
                
                # Labels
                ax.text(1.8, y_pos, risk_level.title(), fontsize=12, weight='bold', ha='right')
                ax.text(8.2, y_pos, f"{count} docs ({percentage:.1f}%)", fontsize=12, ha='left')
                y_pos -= 0.5
        
        # Key statistics
        y_pos -= 0.5
        ax.text(5, y_pos, "Key Portfolio Statistics", fontsize=14, weight='bold', ha='center')
        
        stats = self._calculate_portfolio_statistics(documents)
        y_pos -= 0.4
        
        for stat_name, stat_value in stats.items():
            ax.text(2, y_pos, f"{stat_name}:", fontsize=12, weight='bold')
            ax.text(7, y_pos, str(stat_value), fontsize=12)
            y_pos -= 0.3
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_risk_radar_chart(self, ax, document_data: Dict):
        """Create radar chart for risk assessment"""
        categories = ['AI Cyber', 'Quantum Cyber', 'AI Ethics', 'Quantum Ethics']
        scores = [
            document_data.get('ai_cybersecurity_score', 0) / 100,
            document_data.get('quantum_cybersecurity_score', 0) / 5,
            document_data.get('ai_ethics_score', 0) / 100,
            document_data.get('quantum_ethics_score', 0) / 100
        ]
        
        # Only include scores that exist
        valid_categories = []
        valid_scores = []
        for cat, score in zip(categories, scores):
            if score > 0:
                valid_categories.append(cat)
                valid_scores.append(score)
        
        if not valid_scores:
            ax.text(0.5, 0.5, 'No Scores Available', ha='center', va='center', transform=ax.transAxes)
            return
        
        # Angles for radar chart
        angles = np.linspace(0, 2 * np.pi, len(valid_categories), endpoint=False).tolist()
        valid_scores += valid_scores[:1]  # Complete the circle
        angles += angles[:1]
        
        # Plot
        ax.plot(angles, valid_scores, 'o-', linewidth=2, color=self.colors['accent'])
        ax.fill(angles, valid_scores, alpha=0.25, color=self.colors['accent'])
        
        # Add category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(valid_categories)
        ax.set_ylim(0, 1)
        ax.set_title('Risk Assessment Radar', fontsize=12, weight='bold', pad=20)
    
    def _calculate_risk_level(self, avg_score: float) -> str:
        """Calculate overall risk level from average score"""
        if avg_score >= 80:
            return 'low'
        elif avg_score >= 60:
            return 'medium'
        else:
            return 'high'
    
    def _get_risk_color(self, risk_level: str) -> str:
        """Get color for risk level"""
        return {
            'high': self.colors['high_risk'],
            'medium': self.colors['medium_risk'],
            'low': self.colors['low_risk']
        }.get(risk_level, self.colors['secondary'])
    
    def _get_score_color(self, score: int, metric: str) -> str:
        """Get color based on score value"""
        if 'Quantum Cybersecurity' in metric:
            # 1-5 scale
            return self.colors['low_risk'] if score >= 4 else \
                   self.colors['medium_risk'] if score >= 3 else self.colors['high_risk']
        else:
            # 0-100 scale
            return self.colors['low_risk'] if score >= 80 else \
                   self.colors['medium_risk'] if score >= 60 else self.colors['high_risk']
    
    def _generate_key_findings(self, document_data: Dict, scores: Dict) -> List[str]:
        """Generate key findings for the document"""
        findings = []
        
        for metric, score in scores.items():
            if score > 0:
                if score >= 80 or (metric == 'Quantum Cybersecurity' and score >= 4):
                    findings.append(f"Strong {metric.lower()} posture with comprehensive controls")
                elif score >= 60 or (metric == 'Quantum Cybersecurity' and score >= 3):
                    findings.append(f"Moderate {metric.lower()} awareness with room for improvement")
                else:
                    findings.append(f"Critical {metric.lower()} gaps requiring immediate attention")
        
        return findings
    
    def _generate_risk_assessment_text(self, category: str, score: int) -> str:
        """Generate detailed risk assessment text"""
        if 'Cybersecurity' in category:
            if score >= 80 or (category == 'Quantum Cybersecurity' and score >= 4):
                return "Comprehensive security framework with advanced threat protection measures."
            elif score >= 60 or (category == 'Quantum Cybersecurity' and score >= 3):
                return "Basic security controls present but requires enhanced monitoring and response capabilities."
            else:
                return "Critical security vulnerabilities identified. Immediate remediation required."
        else:  # Ethics
            if score >= 80:
                return "Strong ethical framework with comprehensive bias mitigation and fairness controls."
            elif score >= 60:
                return "Foundational ethical considerations present but lacks comprehensive governance."
            else:
                return "Significant ethical gaps requiring development of comprehensive oversight framework."
    
    def _generate_recommendations(self, document_data: Dict) -> List[tuple]:
        """Generate prioritized recommendations"""
        recommendations = []
        
        scores = {
            'ai_cybersecurity_score': document_data.get('ai_cybersecurity_score', 0),
            'quantum_cybersecurity_score': document_data.get('quantum_cybersecurity_score', 0),
            'ai_ethics_score': document_data.get('ai_ethics_score', 0),
            'quantum_ethics_score': document_data.get('quantum_ethics_score', 0)
        }
        
        for metric, score in scores.items():
            if score > 0:
                if score < 60 or (metric == 'quantum_cybersecurity_score' and score < 3):
                    priority = 'High'
                elif score < 80 or (metric == 'quantum_cybersecurity_score' and score < 4):
                    priority = 'Medium'
                else:
                    priority = 'Low'
                
                rec_text = self._get_recommendation_text(metric, score)
                recommendations.append((priority, rec_text))
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        recommendations.sort(key=lambda x: priority_order[x[0]])
        
        return recommendations
    
    def _get_recommendation_text(self, metric: str, score: int) -> str:
        """Get specific recommendation text for metric"""
        recommendations = {
            'ai_cybersecurity_score': "Implement comprehensive AI security monitoring and threat detection systems",
            'quantum_cybersecurity_score': "Develop quantum-safe cryptography migration strategy and timeline",
            'ai_ethics_score': "Establish AI ethics review board and bias monitoring protocols",
            'quantum_ethics_score': "Create quantum technology governance framework and ethical guidelines"
        }
        return recommendations.get(metric, "Review and enhance security posture")
    
    def _calculate_portfolio_risk_distribution(self, documents: List[Dict]) -> Dict[str, int]:
        """Calculate risk distribution across portfolio"""
        distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for doc in documents:
            scores = [
                doc.get('ai_cybersecurity_score', 0),
                doc.get('quantum_cybersecurity_score', 0) * 20,  # Scale to 100
                doc.get('ai_ethics_score', 0),
                doc.get('quantum_ethics_score', 0)
            ]
            valid_scores = [s for s in scores if s > 0]
            
            if valid_scores:
                avg_score = np.mean(valid_scores)
                risk_level = self._calculate_risk_level(avg_score)
                distribution[risk_level] += 1
        
        return distribution
    
    def _calculate_portfolio_statistics(self, documents: List[Dict]) -> Dict[str, Any]:
        """Calculate portfolio-wide statistics"""
        stats = {}
        
        # Document types
        doc_types = [doc.get('document_type', 'Unknown') for doc in documents]
        stats['Most Common Type'] = max(set(doc_types), key=doc_types.count)
        
        # Average scores
        ai_cyber_scores = [doc.get('ai_cybersecurity_score', 0) for doc in documents if doc.get('ai_cybersecurity_score', 0) > 0]
        if ai_cyber_scores:
            stats['Avg AI Cybersecurity'] = f"{np.mean(ai_cyber_scores):.1f}/100"
        
        quantum_cyber_scores = [doc.get('quantum_cybersecurity_score', 0) for doc in documents if doc.get('quantum_cybersecurity_score', 0) > 0]
        if quantum_cyber_scores:
            stats['Avg Quantum Cybersecurity'] = f"{np.mean(quantum_cyber_scores):.1f}/5"
        
        # Risk coverage
        scored_docs = len([doc for doc in documents if any([
            doc.get('ai_cybersecurity_score', 0) > 0,
            doc.get('quantum_cybersecurity_score', 0) > 0,
            doc.get('ai_ethics_score', 0) > 0,
            doc.get('quantum_ethics_score', 0) > 0
        ])])
        
        stats['Risk Assessment Coverage'] = f"{scored_docs}/{len(documents)} ({(scored_docs/len(documents)*100):.1f}%)"
        
        return stats
    
    def _add_header(self, ax, title: str):
        """Add header to PDF page"""
        # Logo area (placeholder)
        rect = patches.Rectangle((0.5, 13), 1, 0.8, facecolor=self.colors['accent'], alpha=0.8)
        ax.add_patch(rect)
        ax.text(1, 13.4, 'G', fontsize=24, weight='bold', ha='center', va='center', color='white')
        
        # Title
        ax.text(5, 13.4, title, fontsize=18, weight='bold', ha='center', va='center')
        
        # Date
        ax.text(9, 13.4, datetime.now().strftime("%Y-%m-%d"), fontsize=10, ha='right', va='center')
    
    def _add_footer(self, ax):
        """Add footer to PDF page"""
        ax.text(5, 0.5, "Generated by GUARDIAN Risk Assessment Platform", 
               fontsize=10, ha='center', style='italic', color=self.colors['secondary'])
        ax.text(5, 0.2, f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
               fontsize=8, ha='center', color=self.colors['secondary'])
    
    def _create_risk_distribution_chart(self, ax, document_data: Dict):
        """Create pie chart for risk distribution"""
        scores = [
            document_data.get('ai_cybersecurity_score', 0),
            document_data.get('quantum_cybersecurity_score', 0) * 20,  # Scale to 100
            document_data.get('ai_ethics_score', 0),
            document_data.get('quantum_ethics_score', 0)
        ]
        
        labels = ['AI Cyber', 'Quantum Cyber', 'AI Ethics', 'Quantum Ethics']
        colors = [self.colors['accent'], self.colors['high_risk'], 
                 self.colors['medium_risk'], self.colors['low_risk']]
        
        # Filter out zero scores
        valid_data = [(score, label, color) for score, label, color in zip(scores, labels, colors) if score > 0]
        
        if valid_data:
            valid_scores, valid_labels, valid_colors = zip(*valid_data)
            ax.pie(valid_scores, labels=valid_labels, colors=valid_colors, autopct='%1.1f%%')
        else:
            ax.text(0.5, 0.5, 'No Scores Available', ha='center', va='center', transform=ax.transAxes)
        
        ax.set_title('Score Distribution', fontsize=12, weight='bold')
    
    def _create_trend_indicators(self, ax, document_data: Dict):
        """Create trend indicators visualization"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 2)
        ax.axis('off')
        
        ax.text(5, 1.8, 'Risk Trend Indicators', fontsize=14, weight='bold', ha='center')
        
        # Mock trend data (in real implementation, this would compare historical data)
        trends = [
            ('AI Cybersecurity', 'improving', self.colors['low_risk']),
            ('Quantum Readiness', 'stable', self.colors['medium_risk']),
            ('Ethics Compliance', 'declining', self.colors['high_risk'])
        ]
        
        x_positions = [2, 5, 8]
        for i, (category, trend, color) in enumerate(trends):
            # Trend arrow
            if trend == 'improving':
                ax.arrow(x_positions[i], 1, 0, 0.3, head_width=0.1, head_length=0.05, fc=color, ec=color)
            elif trend == 'declining':
                ax.arrow(x_positions[i], 1.3, 0, -0.3, head_width=0.1, head_length=0.05, fc=color, ec=color)
            else:  # stable
                ax.arrow(x_positions[i], 1.15, 0.3, 0, head_width=0.05, head_length=0.05, fc=color, ec=color)
            
            # Labels
            ax.text(x_positions[i], 0.7, category, fontsize=10, ha='center', weight='bold')
            ax.text(x_positions[i], 0.5, trend.title(), fontsize=9, ha='center', color=color)
    
    def _create_risk_matrix(self, ax, document_data: Dict):
        """Create risk impact/probability matrix"""
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 2)
        ax.axis('off')
        
        ax.text(5, 1.8, 'Risk Matrix Assessment', fontsize=14, weight='bold', ha='center')
        
        # Create 3x3 grid
        grid_colors = [
            [self.colors['low_risk'], self.colors['medium_risk'], self.colors['high_risk']],
            [self.colors['low_risk'], self.colors['medium_risk'], self.colors['high_risk']],
            [self.colors['medium_risk'], self.colors['high_risk'], self.colors['high_risk']]
        ]
        
        cell_size = 0.3
        start_x, start_y = 3.5, 0.2
        
        for i in range(3):
            for j in range(3):
                rect = patches.Rectangle((start_x + j*cell_size, start_y + (2-i)*cell_size), 
                                       cell_size, cell_size, 
                                       facecolor=grid_colors[i][j], alpha=0.6, edgecolor='black')
                ax.add_patch(rect)
        
        # Labels
        ax.text(start_x - 0.5, start_y + 1.5*cell_size, 'Impact', fontsize=10, rotation=90, va='center')
        ax.text(start_x + 1.5*cell_size, start_y - 0.2, 'Probability', fontsize=10, ha='center')
    
    def _create_portfolio_risk_distribution_page(self, pdf: PdfPages, documents: List[Dict]):
        """Create portfolio risk distribution analysis page"""
        fig = plt.figure(figsize=(8.5, 11))
        
        # Create grid layout
        gs = fig.add_gridspec(3, 2, height_ratios=[0.5, 1, 1], width_ratios=[1, 1])
        
        # Header
        header_ax = fig.add_subplot(gs[0, :])
        header_ax.text(0.5, 0.5, "Portfolio Risk Distribution Analysis", 
                      fontsize=18, weight='bold', ha='center', va='center')
        header_ax.axis('off')
        
        # Risk level distribution pie chart
        pie_ax = fig.add_subplot(gs[1, 0])
        risk_distribution = self._calculate_portfolio_risk_distribution(documents)
        
        if any(risk_distribution.values()):
            labels = []
            sizes = []
            colors = []
            for risk_level, count in risk_distribution.items():
                if count > 0:
                    labels.append(f"{risk_level.title()} Risk ({count})")
                    sizes.append(count)
                    colors.append(self._get_risk_color(risk_level))
            
            pie_ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            pie_ax.set_title('Risk Level Distribution', fontsize=12, weight='bold')
        else:
            pie_ax.text(0.5, 0.5, 'No Risk Data Available', ha='center', va='center', transform=pie_ax.transAxes)
        
        # Score distribution histogram
        hist_ax = fig.add_subplot(gs[1, 1])
        all_scores = []
        for doc in documents:
            scores = [
                doc.get('ai_cybersecurity_score', 0),
                doc.get('quantum_cybersecurity_score', 0) * 20,
                doc.get('ai_ethics_score', 0),
                doc.get('quantum_ethics_score', 0)
            ]
            valid_scores = [s for s in scores if s > 0]
            if valid_scores:
                all_scores.extend(valid_scores)
        
        if all_scores:
            hist_ax.hist(all_scores, bins=20, color=self.colors['accent'], alpha=0.7, edgecolor='black')
            hist_ax.set_xlabel('Risk Scores')
            hist_ax.set_ylabel('Frequency')
            hist_ax.set_title('Score Distribution', fontsize=12, weight='bold')
        else:
            hist_ax.text(0.5, 0.5, 'No Score Data Available', ha='center', va='center', transform=hist_ax.transAxes)
        
        # Portfolio statistics table
        stats_ax = fig.add_subplot(gs[2, :])
        stats_ax.axis('off')
        
        stats = self._calculate_portfolio_statistics(documents)
        y_pos = 0.9
        stats_ax.text(0.5, y_pos, 'Portfolio Statistics', fontsize=14, weight='bold', ha='center', transform=stats_ax.transAxes)
        
        y_pos = 0.7
        for key, value in stats.items():
            stats_ax.text(0.1, y_pos, f"{key}:", fontsize=12, weight='bold', transform=stats_ax.transAxes)
            stats_ax.text(0.6, y_pos, str(value), fontsize=12, transform=stats_ax.transAxes)
            y_pos -= 0.1
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_portfolio_trend_analysis_page(self, pdf: PdfPages, documents: List[Dict]):
        """Create portfolio trend analysis page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        ax.text(5, 13.5, "Portfolio Trend Analysis", fontsize=18, weight='bold', ha='center')
        
        # Document type analysis
        y_pos = 12.5
        ax.text(5, y_pos, "Document Type Distribution", fontsize=14, weight='bold', ha='center')
        
        doc_types = {}
        for doc in documents:
            doc_type = doc.get('document_type', 'Unknown')
            doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
        
        y_pos = 11.8
        for doc_type, count in sorted(doc_types.items(), key=lambda x: x[1], reverse=True)[:5]:
            percentage = (count / len(documents)) * 100
            ax.text(2, y_pos, f"{doc_type}:", fontsize=12, weight='bold')
            ax.text(7, y_pos, f"{count} documents ({percentage:.1f}%)", fontsize=12)
            y_pos -= 0.4
        
        # Risk trends by category
        y_pos -= 0.5
        ax.text(5, y_pos, "Risk Assessment Coverage", fontsize=14, weight='bold', ha='center')
        
        categories = ['AI Cybersecurity', 'Quantum Cybersecurity', 'AI Ethics', 'Quantum Ethics']
        coverage = {}
        
        for category in categories:
            score_key = category.lower().replace(' ', '_') + '_score'
            covered_docs = len([doc for doc in documents if doc.get(score_key, 0) > 0])
            coverage[category] = (covered_docs / len(documents)) * 100
        
        y_pos -= 0.4
        for category, percentage in coverage.items():
            ax.text(2, y_pos, f"{category}:", fontsize=12, weight='bold')
            ax.text(7, y_pos, f"{percentage:.1f}% coverage", fontsize=12)
            y_pos -= 0.4
        
        # Risk patterns
        y_pos -= 0.5
        ax.text(5, y_pos, "Key Risk Patterns", fontsize=14, weight='bold', ha='center')
        
        patterns = self._analyze_risk_patterns(documents)
        y_pos -= 0.4
        for pattern in patterns[:6]:
            ax.text(1, y_pos, f"• {pattern}", fontsize=11, wrap=True)
            y_pos -= 0.4
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_portfolio_top_risks_page(self, pdf: PdfPages, documents: List[Dict]):
        """Create top risk documents page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        ax.text(5, 13.5, "Top Risk Documents", fontsize=18, weight='bold', ha='center')
        
        # Calculate risk scores for each document
        doc_risks = []
        for doc in documents:
            scores = [
                doc.get('ai_cybersecurity_score', 0),
                doc.get('quantum_cybersecurity_score', 0) * 20,
                doc.get('ai_ethics_score', 0),
                doc.get('quantum_ethics_score', 0)
            ]
            valid_scores = [s for s in scores if s > 0]
            
            if valid_scores:
                import numpy as np
                avg_score = np.mean(valid_scores)
                risk_level = self._calculate_risk_level(avg_score)
                
                doc_risks.append({
                    'title': doc.get('title', 'Untitled')[:50],
                    'type': doc.get('document_type', 'Unknown'),
                    'avg_score': avg_score,
                    'risk_level': risk_level,
                    'scores': {
                        'ai_cyber': doc.get('ai_cybersecurity_score', 0),
                        'quantum_cyber': doc.get('quantum_cybersecurity_score', 0),
                        'ai_ethics': doc.get('ai_ethics_score', 0),
                        'quantum_ethics': doc.get('quantum_ethics_score', 0)
                    }
                })
        
        # Sort by risk level (high risk first)
        risk_order = {'high': 0, 'medium': 1, 'low': 2}
        doc_risks.sort(key=lambda x: (risk_order.get(x['risk_level'], 3), -x['avg_score']))
        
        # Display top 10 risk documents
        y_pos = 12.8
        ax.text(5, y_pos, f"Top {min(10, len(doc_risks))} Risk Documents", fontsize=14, weight='bold', ha='center')
        
        y_pos = 12.2
        for i, doc_risk in enumerate(doc_risks[:10]):
            # Risk level indicator
            color = self._get_risk_color(doc_risk['risk_level'])
            rect = patches.Rectangle((0.5, y_pos-0.1), 0.3, 0.2, facecolor=color, alpha=0.8)
            ax.add_patch(rect)
            ax.text(0.65, y_pos, doc_risk['risk_level'][0].upper(), fontsize=10, weight='bold', 
                   ha='center', va='center', color='white')
            
            # Document info
            ax.text(1, y_pos, f"{i+1}. {doc_risk['title']}", fontsize=11, weight='bold')
            ax.text(1.2, y_pos-0.25, f"Type: {doc_risk['type']} | Avg Score: {doc_risk['avg_score']:.1f}", 
                   fontsize=9, color=self.colors['secondary'])
            
            # Individual scores
            score_text = f"AI Cyber: {doc_risk['scores']['ai_cyber']}, "
            score_text += f"Q Cyber: {doc_risk['scores']['quantum_cyber']}, "
            score_text += f"AI Ethics: {doc_risk['scores']['ai_ethics']}, "
            score_text += f"Q Ethics: {doc_risk['scores']['quantum_ethics']}"
            ax.text(1.2, y_pos-0.45, score_text, fontsize=8, color=self.colors['secondary'])
            
            y_pos -= 0.8
        
        if not doc_risks:
            ax.text(5, 7, "No documents with risk scores available", fontsize=12, ha='center', style='italic')
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _analyze_risk_patterns(self, documents: List[Dict]) -> List[str]:
        """Analyze risk patterns across the portfolio"""
        patterns = []
        
        # Count documents by risk category
        ai_cyber_count = len([doc for doc in documents if doc.get('ai_cybersecurity_score', 0) > 0])
        quantum_cyber_count = len([doc for doc in documents if doc.get('quantum_cybersecurity_score', 0) > 0])
        ai_ethics_count = len([doc for doc in documents if doc.get('ai_ethics_score', 0) > 0])
        quantum_ethics_count = len([doc for doc in documents if doc.get('quantum_ethics_score', 0) > 0])
        
        total_docs = len(documents)
        
        if ai_cyber_count > total_docs * 0.7:
            patterns.append("High AI cybersecurity focus across portfolio")
        elif ai_cyber_count < total_docs * 0.3:
            patterns.append("Limited AI cybersecurity coverage - potential gap")
        
        if quantum_cyber_count > total_docs * 0.5:
            patterns.append("Strong quantum cybersecurity awareness")
        elif quantum_cyber_count < total_docs * 0.2:
            patterns.append("Quantum cybersecurity readiness requires attention")
        
        if ai_ethics_count > total_docs * 0.6:
            patterns.append("Comprehensive AI ethics considerations")
        elif ai_ethics_count < total_docs * 0.3:
            patterns.append("AI ethics framework needs development")
        
        if quantum_ethics_count > total_docs * 0.4:
            patterns.append("Emerging quantum ethics awareness")
        else:
            patterns.append("Quantum ethics governance in early stages")
        
        # Risk level distribution patterns
        risk_dist = self._calculate_portfolio_risk_distribution(documents)
        high_risk_pct = (risk_dist.get('high', 0) / total_docs) * 100
        
        if high_risk_pct > 30:
            patterns.append(f"High risk concentration: {high_risk_pct:.1f}% of documents")
        elif high_risk_pct < 10:
            patterns.append("Well-managed risk profile across portfolio")
        
        return patterns