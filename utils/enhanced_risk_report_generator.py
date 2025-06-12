"""
Enhanced Risk Report Generator for Policy Analysis
Creates comprehensive PDF reports that match the on-screen analysis results exactly
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
from datetime import datetime
import io
from typing import Dict, List, Any, Optional
from utils.risk_report_generator import RiskReportGenerator

class EnhancedRiskReportGenerator(RiskReportGenerator):
    """Enhanced report generator that includes comprehensive gap analysis details"""
    
    def generate_policy_analysis_report(self, document_data: Dict) -> bytes:
        """Generate comprehensive policy analysis report matching on-screen results"""
        
        pdf_buffer = io.BytesIO()
        
        with PdfPages(pdf_buffer) as pdf:
            # Page 1: Executive Summary with Gap Analysis Overview
            self._create_policy_executive_summary_page(pdf, document_data)
            
            # Page 2: Framework Scoring Dashboard
            self._create_framework_scoring_page(pdf, document_data)
            
            # Page 3: Detailed Gap Analysis
            self._create_gap_analysis_page(pdf, document_data)
            
            # Page 4: Compliance Assessment
            self._create_compliance_assessment_page(pdf, document_data)
            
            # Page 5: Recommendations and Action Items
            self._create_recommendations_page(pdf, document_data)
        
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    
    def _create_policy_executive_summary_page(self, pdf: PdfPages, document_data: Dict):
        """Create executive summary page with policy analysis overview"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        self._add_header(ax, "GUARDIAN Policy Analysis Report")
        
        # Document title and metadata
        title = document_data.get('title', 'Untitled Document')[:80]
        doc_type = document_data.get('document_type', 'Policy')
        
        ax.text(5, 12, title, fontsize=16, weight='bold', ha='center', wrap=True)
        ax.text(5, 11.5, f"Document Type: {doc_type}", fontsize=12, ha='center', style='italic')
        
        # Overall maturity score (matching screen display)
        overall_score = document_data.get('overall_maturity_score', 0)
        
        # Large maturity score display
        rect = patches.Rectangle((3, 10.2), 4, 1.2, 
                               facecolor=self._get_maturity_color(overall_score), 
                               alpha=0.8, edgecolor='black')
        ax.add_patch(rect)
        ax.text(5, 10.8, f"Overall Maturity Score", fontsize=14, weight='bold', ha='center', va='center')
        ax.text(5, 10.4, f"{overall_score}/100", fontsize=20, weight='bold', ha='center', va='center', color='white')
        
        # Framework scores summary (matching screen layout)
        y_pos = 9.5
        ax.text(5, y_pos, "Framework Assessment Results", fontsize=14, weight='bold', ha='center')
        
        y_pos = 8.8
        frameworks = [
            ('AI Cybersecurity', document_data.get('ai_cybersecurity_score', 0), '/100'),
            ('Quantum Cybersecurity', document_data.get('quantum_cybersecurity_score', 0), '/5'),
            ('AI Ethics', document_data.get('ai_ethics_score', 0), '/100'),
            ('Quantum Ethics', document_data.get('quantum_ethics_score', 0), '/100')
        ]
        
        for framework, score, scale in frameworks:
            if score > 0:
                score_color = self._get_score_color(score, framework)
                ax.text(2, y_pos, f"{framework}:", fontsize=12, weight='bold')
                ax.text(7, y_pos, f"{score}{scale}", fontsize=12, color=score_color, weight='bold')
                y_pos -= 0.4
        
        # Gap analysis summary (matching screen metrics)
        gap_report = document_data.get('gap_analysis_report')
        if gap_report:
            y_pos -= 0.5
            ax.text(5, y_pos, "Gap Analysis Summary", fontsize=14, weight='bold', ha='center')
            
            total_gaps = len(gap_report.identified_gaps)
            critical_gaps = len([g for g in gap_report.identified_gaps if g.severity == "Critical"])
            compliant_frameworks = len([s for s in gap_report.compliance_status.values() if s == "Compliant"])
            total_frameworks = len(gap_report.compliance_status)
            
            y_pos -= 0.4
            summary_stats = [
                f"• Total Gaps Identified: {total_gaps}",
                f"• Critical Gaps: {critical_gaps}",
                f"• Compliant Frameworks: {compliant_frameworks}/{total_frameworks}",
                f"• Recommendations Generated: {len(gap_report.recommendations)}"
            ]
            
            for stat in summary_stats:
                ax.text(2, y_pos, stat, fontsize=11)
                y_pos -= 0.3
        
        # Footer
        self._add_footer(ax)
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_framework_scoring_page(self, pdf: PdfPages, document_data: Dict):
        """Create detailed framework scoring page matching screen display"""
        fig = plt.figure(figsize=(8.5, 11))
        
        # Create grid layout
        gs = fig.add_gridspec(4, 2, height_ratios=[0.5, 1, 1, 1], width_ratios=[1, 1])
        
        # Header
        header_ax = fig.add_subplot(gs[0, :])
        header_ax.text(0.5, 0.5, "Framework Scoring Assessment", 
                      fontsize=18, weight='bold', ha='center', va='center')
        header_ax.axis('off')
        
        # Framework scoring charts (2x2 grid)
        frameworks = [
            ('AI Cybersecurity', document_data.get('ai_cybersecurity_score', 0), 100),
            ('Quantum Cybersecurity', document_data.get('quantum_cybersecurity_score', 0), 5),
            ('AI Ethics', document_data.get('ai_ethics_score', 0), 100),
            ('Quantum Ethics', document_data.get('quantum_ethics_score', 0), 100)
        ]
        
        positions = [(1, 0), (1, 1), (2, 0), (2, 1)]
        
        for i, (framework, score, max_score) in enumerate(frameworks):
            if score > 0:
                ax = fig.add_subplot(gs[positions[i]])
                self._create_framework_gauge(ax, framework, score, max_score)
        
        # Overall assessment text
        assessment_ax = fig.add_subplot(gs[3, :])
        assessment_ax.axis('off')
        
        overall_score = document_data.get('overall_maturity_score', 0)
        assessment_text = self._generate_overall_assessment_text(overall_score, document_data)
        
        assessment_ax.text(0.5, 0.8, "Overall Assessment", fontsize=14, weight='bold', 
                          ha='center', transform=assessment_ax.transAxes)
        assessment_ax.text(0.05, 0.5, assessment_text, fontsize=10, 
                          transform=assessment_ax.transAxes, wrap=True, va='top')
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_gap_analysis_page(self, pdf: PdfPages, document_data: Dict):
        """Create detailed gap analysis page matching screen results"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        ax.text(5, 13.5, "Comprehensive Gap Analysis", fontsize=18, weight='bold', ha='center')
        
        gap_report = document_data.get('gap_analysis_report')
        if not gap_report or not gap_report.identified_gaps:
            ax.text(5, 7, "No significant gaps identified in the analysis", 
                   fontsize=12, ha='center', style='italic')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            return
        
        # Group gaps by severity (matching screen organization)
        gaps_by_severity = {}
        for gap in gap_report.identified_gaps:
            severity = gap.severity
            if severity not in gaps_by_severity:
                gaps_by_severity[severity] = []
            gaps_by_severity[severity].append(gap)
        
        y_pos = 12.8
        
        # Display gaps by severity (Critical, High, Medium, Low)
        severity_order = ['Critical', 'High', 'Medium', 'Low']
        severity_colors = {
            'Critical': self.colors['high_risk'],
            'High': '#ff6b35',
            'Medium': self.colors['medium_risk'],
            'Low': self.colors['low_risk']
        }
        
        for severity in severity_order:
            if severity in gaps_by_severity:
                gaps = gaps_by_severity[severity]
                
                # Severity header
                color = severity_colors[severity]
                ax.text(1, y_pos, f"{severity} Severity Gaps ({len(gaps)})", 
                       fontsize=13, weight='bold', color=color)
                y_pos -= 0.3
                
                # Display individual gaps (matching screen format)
                for gap in gaps[:3]:  # Show top 3 gaps per severity to fit page
                    ax.text(1.5, y_pos, f"• {gap.framework} - {gap.category}", 
                           fontsize=11, weight='bold')
                    y_pos -= 0.2
                    
                    # Wrap description text
                    description = gap.gap_description[:100] + "..." if len(gap.gap_description) > 100 else gap.gap_description
                    ax.text(1.7, y_pos, description, fontsize=10, wrap=True)
                    y_pos -= 0.4
                
                if len(gaps) > 3:
                    ax.text(1.5, y_pos, f"... and {len(gaps) - 3} more {severity.lower()} gaps", 
                           fontsize=10, style='italic')
                    y_pos -= 0.3
                
                y_pos -= 0.2
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_compliance_assessment_page(self, pdf: PdfPages, document_data: Dict):
        """Create compliance assessment page matching screen display"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        ax.text(5, 13.5, "Compliance Assessment", fontsize=18, weight='bold', ha='center')
        
        gap_report = document_data.get('gap_analysis_report')
        if not gap_report or not gap_report.compliance_status:
            ax.text(5, 7, "No compliance frameworks assessed", 
                   fontsize=12, ha='center', style='italic')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            return
        
        # Compliance status overview (matching screen layout)
        y_pos = 12.5
        
        compliant_count = len([s for s in gap_report.compliance_status.values() if s == "Compliant"])
        partial_count = len([s for s in gap_report.compliance_status.values() if "Partial" in s])
        non_compliant_count = len(gap_report.compliance_status) - compliant_count - partial_count
        
        # Summary metrics
        ax.text(5, y_pos, "Compliance Overview", fontsize=14, weight='bold', ha='center')
        y_pos -= 0.5
        
        summary_stats = [
            f"✅ Compliant: {compliant_count} frameworks",
            f"⚠️ Partially Compliant: {partial_count} frameworks", 
            f"❌ Non-Compliant: {non_compliant_count} frameworks"
        ]
        
        for stat in summary_stats:
            ax.text(2, y_pos, stat, fontsize=12)
            y_pos -= 0.4
        
        # Detailed compliance status (matching screen format)
        y_pos -= 0.5
        ax.text(5, y_pos, "Framework-by-Framework Assessment", fontsize=14, weight='bold', ha='center')
        y_pos -= 0.4
        
        for framework, status in gap_report.compliance_status.items():
            # Status indicator
            if status == "Compliant":
                indicator = "✅"
                color = self.colors['low_risk']
            elif "Partial" in status:
                indicator = "⚠️"
                color = self.colors['medium_risk']
            else:
                indicator = "❌"
                color = self.colors['high_risk']
            
            ax.text(1.5, y_pos, f"{indicator} {framework}", fontsize=11, weight='bold')
            ax.text(7, y_pos, status, fontsize=11, color=color)
            y_pos -= 0.3
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _create_framework_gauge(self, ax, framework: str, score: int, max_score: int):
        """Create framework-specific gauge chart"""
        # Convert to percentage for display
        if max_score == 5:  # Quantum Cybersecurity
            percentage = (score / max_score) * 100
            display_score = f"{score}/5"
        else:
            percentage = score
            display_score = f"{score}/100"
        
        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = 0.8
        
        # Background arc
        ax.plot(r * np.cos(theta), r * np.sin(theta), 'lightgray', linewidth=8)
        
        # Score arc
        score_theta = np.linspace(0, np.pi * (percentage / 100), 50)
        color = self._get_score_color(score, framework)
        ax.plot(r * np.cos(score_theta), r * np.sin(score_theta), color=color, linewidth=8)
        
        # Center text
        ax.text(0, 0.2, framework, ha='center', va='center', fontsize=10, weight='bold')
        ax.text(0, -0.1, display_score, ha='center', va='center', fontsize=14, weight='bold')
        
        ax.set_xlim(-1, 1)
        ax.set_ylim(-0.3, 1)
        ax.set_aspect('equal')
        ax.axis('off')
    
    def _get_maturity_color(self, score: float) -> str:
        """Get color for maturity score"""
        if score >= 80:
            return self.colors['low_risk']
        elif score >= 60:
            return self.colors['medium_risk']
        else:
            return self.colors['high_risk']
    
    def _generate_overall_assessment_text(self, overall_score: float, document_data: Dict) -> str:
        """Generate overall assessment text matching screen analysis"""
        
        if overall_score >= 80:
            assessment = f"This document demonstrates strong maturity across assessed frameworks with an overall score of {overall_score}/100. "
        elif overall_score >= 60:
            assessment = f"This document shows moderate maturity with an overall score of {overall_score}/100. "
        else:
            assessment = f"This document requires significant improvement with an overall score of {overall_score}/100. "
        
        gap_report = document_data.get('gap_analysis_report')
        if gap_report:
            critical_gaps = len([g for g in gap_report.identified_gaps if g.severity == "Critical"])
            if critical_gaps > 0:
                assessment += f"There are {critical_gaps} critical gaps that require immediate attention. "
            
            compliant_frameworks = len([s for s in gap_report.compliance_status.values() if s == "Compliant"])
            total_frameworks = len(gap_report.compliance_status)
            assessment += f"Compliance achieved in {compliant_frameworks} of {total_frameworks} assessed frameworks."
        
        return assessment
    
    def _create_recommendations_page(self, pdf: PdfPages, document_data: Dict):
        """Create recommendations and action items page"""
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 14)
        ax.axis('off')
        
        # Header
        ax.text(5, 13.5, "Intelligent Recommendations", fontsize=18, weight='bold', ha='center')
        
        gap_report = document_data.get('gap_analysis_report')
        if not gap_report or not hasattr(gap_report, 'strategic_recommendations') or not gap_report.strategic_recommendations:
            ax.text(5, 7, "No specific recommendations generated", 
                   fontsize=12, ha='center', style='italic')
            pdf.savefig(fig, bbox_inches='tight')
            plt.close(fig)
            return
        
        y_pos = 12.8
        
        # Priority recommendations
        ax.text(5, y_pos, "Priority Action Items", fontsize=14, weight='bold', ha='center')
        y_pos -= 0.5
        
        # Group recommendations by priority
        priority_order = ['High', 'Medium', 'Low']
        recommendations_by_priority = {}
        
        for rec in gap_report.recommendations:
            priority = getattr(rec, 'priority', 'Medium')
            if priority not in recommendations_by_priority:
                recommendations_by_priority[priority] = []
            recommendations_by_priority[priority].append(rec)
        
        for priority in priority_order:
            if priority in recommendations_by_priority:
                recs = recommendations_by_priority[priority]
                
                # Priority header
                ax.text(1, y_pos, f"{priority} Priority ({len(recs)} items)", 
                       fontsize=12, weight='bold', color=self._get_priority_color(priority))
                y_pos -= 0.3
                
                # Show recommendations
                for i, rec in enumerate(recs[:4]):  # Limit to 4 per priority
                    rec_text = getattr(rec, 'recommendation', str(rec))[:80] + "..."
                    ax.text(1.5, y_pos, f"{i+1}. {rec_text}", fontsize=10)
                    y_pos -= 0.25
                
                if len(recs) > 4:
                    ax.text(1.5, y_pos, f"... and {len(recs) - 4} more {priority.lower()} priority items", 
                           fontsize=9, style='italic')
                    y_pos -= 0.3
                
                y_pos -= 0.2
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)
    
    def _get_priority_color(self, priority: str) -> str:
        """Get color for priority level"""
        if priority == 'High':
            return self.colors['high_risk']
        elif priority == 'Medium':
            return self.colors['medium_risk']
        else:
            return self.colors['low_risk']
    
    def _get_score_color(self, score: int, framework: str) -> str:
        """Get color for framework score"""
        if 'Quantum Cybersecurity' in framework:
            # 5-point scale
            if score >= 4:
                return self.colors['low_risk']
            elif score >= 3:
                return self.colors['medium_risk']
            else:
                return self.colors['high_risk']
        else:
            # 100-point scale
            if score >= 80:
                return self.colors['low_risk']
            elif score >= 60:
                return self.colors['medium_risk']
            else:
                return self.colors['high_risk']