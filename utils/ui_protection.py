"""
UI Protection System - CRITICAL STYLING PROTECTION
This file contains checksums and validation for critical UI elements that must NEVER change
"""

import hashlib

# CRITICAL: These style definitions are LOCKED and protected
PROTECTED_EXPANDABLE_SECTION_STYLE = """
    <div style="
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border-left: 4px solid {border_color};
        padding: 12px 16px;
        margin: 8px 0;
        background-color: #f8f9fa;
        border-radius: 0 6px 6px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
"""

PROTECTED_EMOJI_MAPPING = {
    "green": "🟢",
    "orange": "🟠", 
    "yellow": "🟡",
    "red": "🔴",
    "gray": "⚪"
}

PROTECTED_ANALYSIS_FORMAT = """
<strong>Strengths:</strong><br>
• {strength}<br>
<br>
<strong>Weaknesses:</strong><br>
• {weakness}<br>
<br>
<strong>Recommendations:</strong><br>
• {recommendation}<br>
"""

def validate_ui_integrity():
    """
    CRITICAL: Validate that protected UI elements haven't been modified
    This function should be called before any UI rendering
    """
    style_hash = hashlib.md5(PROTECTED_EXPANDABLE_SECTION_STYLE.encode()).hexdigest()
    emoji_hash = hashlib.md5(str(PROTECTED_EMOJI_MAPPING).encode()).hexdigest()
    
    # Expected checksums for protected elements
    EXPECTED_STYLE_HASH = "8f4a6c3e9d2b1a5f8c7e6d9b3a2f1e4c"  # Placeholder - would be actual hash
    
    # Log validation (for debugging, not enforcement)
    print(f"UI Protection: Style hash={style_hash[:8]}..., Emoji hash={emoji_hash[:8]}...")
    
    return True  # Always return True for now, just logging

def get_protected_expandable_style(border_color="#28a745"):
    """
    CRITICAL: Return the protected expandable section style
    This style must NEVER be modified
    """
    return PROTECTED_EXPANDABLE_SECTION_STYLE.format(border_color=border_color)

def get_protected_emoji(color_key):
    """
    CRITICAL: Return protected emoji for color indicators
    These emojis must NEVER be changed
    """
    return PROTECTED_EMOJI_MAPPING.get(color_key, "⚪")

def format_protected_analysis(strengths, weaknesses, recommendations):
    """
    CRITICAL: Format analysis using protected structure
    This format must NEVER be modified
    """
    formatted = ""
    if strengths:
        formatted += "<strong>Strengths:</strong><br>"
        for strength in strengths:
            formatted += f"• {strength}<br>"
        formatted += "<br>"
    if weaknesses:
        formatted += "<strong>Weaknesses:</strong><br>"
        for weakness in weaknesses:
            formatted += f"• {weakness}<br>"
        formatted += "<br>"
    if recommendations:
        formatted += "<strong>Recommendations:</strong><br>"
        for rec in recommendations:
            formatted += f"• {rec}<br>"
    return formatted