"""
Professional Gauge and Bar Visualization Generator
Creates visualizations matching the professional assessment dashboard style
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Wedge, Circle
import numpy as np
import io
import base64

def create_professional_assessment_dashboard(scores_data):
    """
    Create professional assessment dashboard with horizontal bars and circular gauges
    
    Args:
        scores_data: Dict containing framework scores and parameters
    """
    fig = plt.figure(figsize=(14, 10), facecolor='white')
    
    # Create layout - main grid
    gs = fig.add_gridspec(3, 2, height_ratios=[0.3, 1, 0.3], width_ratios=[1, 1.2], 
                         hspace=0.4, wspace=0.3)
    
    # Header section
    header_ax = fig.add_subplot(gs[0, :])
    header_ax.text(0.5, 0.5, 'AI Cybersecurity Maturity Assessment', 
                   fontsize=20, weight='bold', ha='center', va='center', transform=header_ax.transAxes)
    header_ax.text(0.5, 0.2, "Based on the AI Policy patent's cybersecurity framework with 0-100 scoring system.",
                   fontsize=12, ha='center', va='center', transform=header_ax.transAxes, style='italic')
    header_ax.axis('off')
    
    # Left side - Parameter bars
    left_ax = fig.add_subplot(gs[1, 0])
    _create_parameter_bars(left_ax, scores_data)
    
    # Right side - Circular gauges
    right_ax = fig.add_subplot(gs[1, 1])
    _create_circular_gauges(right_ax, scores_data)
    
    # Bottom - Overall assessment
    bottom_ax = fig.add_subplot(gs[2, :])
    _create_overall_assessment(bottom_ax, scores_data)
    
    plt.tight_layout()
    
    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    
    return img_b64

def _create_parameter_bars(ax, scores_data):
    """Create horizontal parameter bars on the left side"""
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 4.5)
    ax.set_title('AI Cybersecurity Parameters:', fontsize=14, weight='bold', loc='left', pad=20)
    
    # Parameter data - matching the screenshot structure
    parameters = [
        ('Incident Response:', scores_data.get('incident_response', 70)),
        ('Threat Monitoring:', scores_data.get('threat_monitoring', 65)),
        ('Authentication Systems:', scores_data.get('authentication_systems', 90)),
        ('Encryption Standards:', scores_data.get('encryption_standards', 75))
    ]
    
    y_positions = [3.5, 2.5, 1.5, 0.5]
    
    for i, (param_name, score) in enumerate(parameters):
        y = y_positions[i]
        
        # Background bar
        bg_bar = patches.Rectangle((0, y-0.15), 100, 0.3, 
                                 facecolor='#f0f0f0', edgecolor='none')
        ax.add_patch(bg_bar)
        
        # Score bar with color based on value
        color = _get_bar_color(score)
        score_bar = patches.Rectangle((0, y-0.15), score, 0.3, 
                                    facecolor=color, edgecolor='none')
        ax.add_patch(score_bar)
        
        # Score circle at the end
        circle = Circle((score, y), 0.2, facecolor=color, edgecolor='white', linewidth=2, zorder=10)
        ax.add_patch(circle)
        
        # Parameter label
        ax.text(-5, y, param_name, fontsize=11, va='center', ha='right')
        
        # Score text
        ax.text(score + 3, y, str(score), fontsize=11, weight='bold', va='center', color=color)
    
    # Axis formatting
    ax.set_xticks([0, 100])
    ax.set_xticklabels(['0', '100'])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

def _create_circular_gauges(ax, scores_data):
    """Create circular gauges on the right side"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title('AI Cybersecurity Assessment', fontsize=14, weight='bold', loc='center', pad=20)
    ax.axis('off')
    
    # Gauge positions in 2x2 grid
    gauge_positions = [
        (2.5, 7.5, 'Ethical Compliance Score', 'ECS', scores_data.get('ai_ethics_score', 75), '#8b5cf6'),
        (7.5, 7.5, 'Adaptability Score', 'AS', scores_data.get('adaptability_score', 80), '#06b6d4'),
        (2.5, 2.5, 'Legal Alignment Score', 'LAS', scores_data.get('legal_alignment_score', 65), '#10b981'),
        (7.5, 2.5, 'Implementation Feasibility', 'IFS', scores_data.get('implementation_feasibility', 70), '#f59e0b')
    ]
    
    for x, y, title, acronym, score, color in gauge_positions:
        _create_single_circular_gauge(ax, x, y, score, title, acronym, color)

def _create_single_circular_gauge(ax, x, y, score, title, acronym, color):
    """Create a single circular gauge"""
    radius = 1.2
    
    # Background arc (full semicircle)
    bg_arc = Wedge((x, y), radius, 0, 180, width=0.3, 
                   facecolor='#f0f0f0', edgecolor='none')
    ax.add_patch(bg_arc)
    
    # Score arc
    score_angle = (score / 100) * 180
    score_arc = Wedge((x, y), radius, 0, score_angle, width=0.3, 
                     facecolor=color, edgecolor='none')
    ax.add_patch(score_arc)
    
    # Center circle
    center_circle = Circle((x, y), 0.6, facecolor='white', edgecolor=color, linewidth=3)
    ax.add_patch(center_circle)
    
    # Score text in center
    ax.text(x, y+0.1, str(score), fontsize=20, weight='bold', ha='center', va='center')
    ax.text(x, y-0.2, '/ 100', fontsize=10, ha='center', va='center', color='gray')
    
    # Scale markers
    for angle in [0, 45, 90, 135, 180]:
        angle_rad = np.radians(angle)
        x1 = x + (radius + 0.1) * np.cos(angle_rad)
        y1 = y + (radius + 0.1) * np.sin(angle_rad)
        x2 = x + (radius + 0.2) * np.cos(angle_rad)
        y2 = y + (radius + 0.2) * np.sin(angle_rad)
        ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1)
    
    # Scale labels
    ax.text(x - radius - 0.3, y, '0', fontsize=8, ha='center', va='center', color='gray')
    ax.text(x + radius + 0.3, y, '100', fontsize=8, ha='center', va='center', color='gray')
    
    # Title and acronym
    ax.text(x, y-2.2, acronym, fontsize=12, weight='bold', ha='center', va='center', color=color)
    
    # Assessment level
    level = _get_assessment_level(score)
    level_color = _get_level_color(level)
    ax.text(x, y-2.6, level, fontsize=10, weight='bold', ha='center', va='center', color=level_color)

def _create_overall_assessment(ax, scores_data):
    """Create overall assessment section"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis('off')
    
    # Overall score calculation
    ai_cyber = scores_data.get('ai_cybersecurity_score', 0)
    ai_ethics = scores_data.get('ai_ethics_score', 0)
    quantum_cyber = scores_data.get('quantum_cybersecurity_score', 0) * 20  # Convert 1-5 to 0-100
    quantum_ethics = scores_data.get('quantum_ethics_score', 0)
    
    scores = [s for s in [ai_cyber, ai_ethics, quantum_cyber, quantum_ethics] if s > 0]
    overall_score = sum(scores) / len(scores) if scores else 0
    
    # Title
    ax.text(5, 2.5, 'Overall AI Policy Assessment', fontsize=16, weight='bold', ha='center', va='center')
    
    # Large score display
    score_color = _get_bar_color(overall_score)
    ax.text(5, 1.5, f'{overall_score:.1f}/100', fontsize=32, weight='bold', ha='center', va='center', color=score_color)
    
    # Subtitle
    ax.text(5, 0.8, 'Based on patent-defined scoring criteria from sections 21-22', 
           fontsize=11, ha='center', va='center', style='italic', color='gray')

def _get_bar_color(score):
    """Get color for bar based on score"""
    if score >= 80:
        return '#10b981'  # Green
    elif score >= 60:
        return '#f59e0b'  # Orange  
    elif score >= 40:
        return '#ef4444'  # Red
    else:
        return '#dc2626'  # Dark red

def _get_assessment_level(score):
    """Get assessment level text"""
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Fair'
    else:
        return 'Poor'

def _get_level_color(level):
    """Get color for assessment level"""
    level_colors = {
        'Excellent': '#10b981',
        'Good': '#f59e0b', 
        'Fair': '#ef4444',
        'Poor': '#dc2626'
    }
    return level_colors.get(level, '#6b7280')

def create_quantum_assessment_dashboard(scores_data):
    """Create quantum cybersecurity assessment dashboard"""
    fig = plt.figure(figsize=(14, 10), facecolor='white')
    
    # Similar structure but for quantum cybersecurity
    gs = fig.add_gridspec(3, 2, height_ratios=[0.3, 1, 0.3], width_ratios=[1, 1.2], 
                         hspace=0.4, wspace=0.3)
    
    # Header
    header_ax = fig.add_subplot(gs[0, :])
    header_ax.text(0.5, 0.5, 'Quantum Cybersecurity Maturity Assessment', 
                   fontsize=20, weight='bold', ha='center', va='center', transform=header_ax.transAxes)
    header_ax.text(0.5, 0.2, "Based on the Quantum Policy patent's 5-tier maturity framework.",
                   fontsize=12, ha='center', va='center', transform=header_ax.transAxes, style='italic')
    header_ax.axis('off')
    
    # Left side - Tier indicators  
    left_ax = fig.add_subplot(gs[1, 0])
    _create_quantum_tier_indicators(left_ax, scores_data)
    
    # Right side - Quantum metrics
    right_ax = fig.add_subplot(gs[1, 1])
    _create_quantum_metrics(right_ax, scores_data)
    
    # Bottom - Overall quantum assessment
    bottom_ax = fig.add_subplot(gs[2, :])
    _create_quantum_overall_assessment(bottom_ax, scores_data)
    
    plt.tight_layout()
    
    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight', facecolor='white')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    
    return img_b64

def _create_quantum_tier_indicators(ax, scores_data):
    """Create quantum tier indicators"""
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 6)
    ax.set_title('Quantum Cybersecurity Tiers:', fontsize=14, weight='bold', loc='left', pad=20)
    
    current_tier = scores_data.get('quantum_cybersecurity_score', 3)
    
    tier_names = [
        'Tier 1: Basic Awareness',
        'Tier 2: Risk Assessment', 
        'Tier 3: Active Monitoring',
        'Tier 4: Advanced Protection',
        'Tier 5: Quantum-Ready'
    ]
    
    colors = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#008000']
    
    for i, (tier_name, color) in enumerate(zip(tier_names, colors)):
        y = 5 - i
        
        # Tier circle
        is_active = (i + 1) <= current_tier
        circle_color = color if is_active else '#f0f0f0'
        edge_color = color if is_active else '#d1d5db'
        
        circle = Circle((0.5, y), 0.2, facecolor=circle_color, edgecolor=edge_color, linewidth=2)
        ax.add_patch(circle)
        
        # Tier number
        text_color = 'white' if is_active else '#9ca3af'
        ax.text(0.5, y, str(i+1), fontsize=12, weight='bold', ha='center', va='center', color=text_color)
        
        # Tier name
        name_color = 'black' if is_active else '#9ca3af'
        ax.text(1, y, tier_name, fontsize=11, va='center', color=name_color, weight='bold' if is_active else 'normal')
    
    ax.axis('off')

def _create_quantum_metrics(ax, scores_data):
    """Create quantum-specific metrics display"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_title('Quantum Security Metrics', fontsize=14, weight='bold', loc='center', pad=20)
    ax.axis('off')
    
    # Quantum-specific metrics
    quantum_score = scores_data.get('quantum_cybersecurity_score', 3)
    quantum_ethics = scores_data.get('quantum_ethics_score', 65)
    
    # Large tier display
    tier_color = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#008000'][min(quantum_score-1, 4)]
    
    # Main tier circle
    main_circle = Circle((5, 6), 1.5, facecolor=tier_color, edgecolor='white', linewidth=4)
    ax.add_patch(main_circle)
    
    ax.text(5, 6.2, f'Tier {quantum_score}', fontsize=16, weight='bold', ha='center', va='center', color='white')
    ax.text(5, 5.8, '/ 5', fontsize=12, ha='center', va='center', color='white')
    
    # Ethics score
    ethics_color = _get_bar_color(quantum_ethics)
    ethics_circle = Circle((2, 3), 1, facecolor=ethics_color, edgecolor='white', linewidth=3)
    ax.add_patch(ethics_circle)
    
    ax.text(2, 3.2, str(quantum_ethics), fontsize=14, weight='bold', ha='center', va='center', color='white')
    ax.text(2, 2.8, 'Ethics', fontsize=10, ha='center', va='center', color='white')
    ax.text(2, 1.5, 'Quantum Ethics Score', fontsize=10, weight='bold', ha='center', va='center')
    
    # Readiness indicator
    readiness_circle = Circle((8, 3), 1, facecolor='#6366f1', edgecolor='white', linewidth=3)
    ax.add_patch(readiness_circle)
    
    readiness_pct = (quantum_score / 5) * 100
    ax.text(8, 3.2, f'{readiness_pct:.0f}%', fontsize=14, weight='bold', ha='center', va='center', color='white')
    ax.text(8, 2.8, 'Ready', fontsize=10, ha='center', va='center', color='white')
    ax.text(8, 1.5, 'Quantum Readiness', fontsize=10, weight='bold', ha='center', va='center')

def _create_quantum_overall_assessment(ax, scores_data):
    """Create quantum overall assessment"""
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis('off')
    
    quantum_tier = scores_data.get('quantum_cybersecurity_score', 3)
    
    # Title
    ax.text(5, 2.5, 'Overall Quantum Cybersecurity Assessment', fontsize=16, weight='bold', ha='center', va='center')
    
    # Tier display
    tier_color = ['#ff0000', '#ff8000', '#ffff00', '#00ff00', '#008000'][min(quantum_tier-1, 4)]
    ax.text(5, 1.5, f'Tier {quantum_tier}/5', fontsize=32, weight='bold', ha='center', va='center', color=tier_color)
    
    # Status
    status = ['Critical', 'Developing', 'Adequate', 'Advanced', 'Quantum-Ready'][min(quantum_tier-1, 4)]
    ax.text(5, 0.8, f'Status: {status}', fontsize=14, weight='bold', ha='center', va='center', color=tier_color)