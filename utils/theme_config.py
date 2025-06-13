"""
Professional Theme Configuration for GUARDIAN
Unified color scheme and styling across all components
"""

# Primary Color Palette
COLORS = {
    # Primary Blues
    "primary_blue": "#1e3a8a",        # Deep blue
    "secondary_blue": "#3b82f6",      # Medium blue
    "accent_blue": "#60a5fa",         # Light blue
    
    # Professional Greys
    "dark_grey": "#374151",           # Dark grey
    "medium_grey": "#6b7280",         # Medium grey
    "light_grey": "#9ca3af",          # Light grey
    "background_grey": "#f9fafb",     # Light background
    
    # Accent Colors
    "success_green": "#059669",       # Professional green
    "warning_orange": "#d97706",      # Professional orange
    "error_red": "#dc2626",           # Professional red
    "info_teal": "#0891b2",           # Professional teal
    
    # Neutral Colors
    "white": "#ffffff",
    "black": "#000000",
    "border_color": "#e5e7eb",
    "text_primary": "#111827",
    "text_secondary": "#4b5563"
}

def get_compact_header_style(title, subtitle="", bg_color="primary_blue", text_color="white"):
    """Generate compact professional header styling"""
    return f"""
    <div style="
        background: linear-gradient(135deg, {COLORS[bg_color]} 0%, {COLORS['secondary_blue']} 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid {COLORS['border_color']};
        color: {COLORS[text_color]};
    ">
        <h2 style="
            color: {COLORS[text_color]};
            margin: 0 0 0.5rem 0;
            font-size: 1.5rem;
            font-weight: 600;
            text-align: center;
        ">
            {title}
        </h2>
        {f'<p style="color: {COLORS["light_grey"]}; text-align: center; font-size: 0.95rem; margin: 0; line-height: 1.4;">{subtitle}</p>' if subtitle else ''}
    </div>
    """

def get_section_header_style(title, bg_color="background_grey", text_color="text_primary"):
    """Generate section header styling"""
    return f"""
    <div style="
        background: {COLORS[bg_color]};
        padding: 1rem;
        border-radius: 6px;
        margin: 1rem 0;
        border-left: 4px solid {COLORS['primary_blue']};
    ">
        <h4 style="
            color: {COLORS[text_color]};
            margin: 0;
            font-size: 1.1rem;
            font-weight: 600;
        ">
            {title}
        </h4>
    </div>
    """

def get_info_box_style(content, box_type="info"):
    """Generate styled info boxes"""
    color_map = {
        "info": COLORS["info_teal"],
        "success": COLORS["success_green"],
        "warning": COLORS["warning_orange"],
        "error": COLORS["error_red"]
    }
    
    return f"""
    <div style="
        background: {COLORS['background_grey']};
        padding: 1rem;
        border-radius: 6px;
        border-left: 4px solid {color_map[box_type]};
        margin: 1rem 0;
    ">
        <p style="
            color: {COLORS['text_primary']};
            margin: 0;
            font-size: 0.95rem;
            line-height: 1.5;
        ">
            {content}
        </p>
    </div>
    """

def get_metric_card_style(title, value, description="", color="primary_blue"):
    """Generate metric card styling"""
    return f"""
    <div style="
        background: {COLORS['white']};
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid {COLORS['border_color']};
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="
            color: {COLORS[color]};
            margin: 0 0 0.5rem 0;
            font-size: 1.8rem;
            font-weight: 700;
        ">
            {value}
        </h3>
        <p style="
            color: {COLORS['text_primary']};
            margin: 0 0 0.25rem 0;
            font-size: 0.9rem;
            font-weight: 600;
        ">
            {title}
        </p>
        {f'<p style="color: {COLORS["text_secondary"]}; margin: 0; font-size: 0.8rem;">{description}</p>' if description else ''}
    </div>
    """

def get_status_indicator(status, text):
    """Generate status indicators"""
    status_colors = {
        "online": COLORS["success_green"],
        "warning": COLORS["warning_orange"],
        "error": COLORS["error_red"],
        "info": COLORS["info_teal"]
    }
    
    return f"""
    <div style="
        display: inline-flex;
        align-items: center;
        background: {COLORS['background_grey']};
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid {status_colors[status]};
        color: {status_colors[status]};
        font-size: 0.85rem;
        font-weight: 600;
    ">
        <span style="
            width: 8px;
            height: 8px;
            background: {status_colors[status]};
            border-radius: 50%;
            margin-right: 0.5rem;
        "></span>
        {text}
    </div>
    """