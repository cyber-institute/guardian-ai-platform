"""
Adaptive Color Palette Selector for GUARDIAN
Provides dynamic theme customization with predefined and custom color schemes
"""

import streamlit as st
import json
from typing import Dict, Any

class ColorPaletteManager:
    """Manages color palettes and theme switching for GUARDIAN"""
    
    def __init__(self):
        self.predefined_palettes = {
            "Guardian Red (Default)": {
                "primary": "#C4262E",
                "secondary": "#A01E24", 
                "accent": "#DC2626",
                "background": "#FFFFFF",
                "surface": "#F8FAFC",
                "text_primary": "#374151",
                "text_secondary": "#6B7280",
                "success": "#059669",
                "warning": "#D97706",
                "error": "#DC2626",
                "border": "#E5E7EB"
            },
            "Cybersecurity Blue": {
                "primary": "#1E40AF",
                "secondary": "#1E3A8A",
                "accent": "#3B82F6",
                "background": "#FFFFFF",
                "surface": "#F1F5F9",
                "text_primary": "#1E293B",
                "text_secondary": "#475569",
                "success": "#059669",
                "warning": "#D97706",
                "error": "#DC2626",
                "border": "#CBD5E1"
            },
            "Quantum Purple": {
                "primary": "#7C3AED",
                "secondary": "#5B21B6",
                "accent": "#8B5CF6",
                "background": "#FFFFFF",
                "surface": "#FAF5FF",
                "text_primary": "#4C1D95",
                "text_secondary": "#6D28D9",
                "success": "#059669",
                "warning": "#D97706",
                "error": "#DC2626",
                "border": "#DDD6FE"
            },
            "AI Green": {
                "primary": "#059669",
                "secondary": "#047857",
                "accent": "#10B981",
                "background": "#FFFFFF",
                "surface": "#F0FDF4",
                "text_primary": "#064E3B",
                "text_secondary": "#065F46",
                "success": "#059669",
                "warning": "#D97706",
                "error": "#DC2626",
                "border": "#D1FAE5"
            },
            "Dark Mode": {
                "primary": "#3B82F6",
                "secondary": "#1D4ED8",
                "accent": "#60A5FA",
                "background": "#111827",
                "surface": "#1F2937",
                "text_primary": "#F9FAFB",
                "text_secondary": "#D1D5DB",
                "success": "#10B981",
                "warning": "#F59E0B",
                "error": "#EF4444",
                "border": "#374151"
            },
            "Corporate Gray": {
                "primary": "#374151",
                "secondary": "#1F2937",
                "accent": "#6B7280",
                "background": "#FFFFFF",
                "surface": "#F9FAFB",
                "text_primary": "#111827",
                "text_secondary": "#4B5563",
                "success": "#059669",
                "warning": "#D97706",
                "error": "#DC2626",
                "border": "#E5E7EB"
            }
        }
    
    def get_current_palette(self) -> Dict[str, str]:
        """Get the currently selected color palette"""
        if 'selected_palette' not in st.session_state:
            st.session_state.selected_palette = "Guardian Red (Default)"
        
        palette_name = st.session_state.selected_palette
        if palette_name in self.predefined_palettes:
            return self.predefined_palettes[palette_name]
        elif 'custom_palette' in st.session_state:
            return st.session_state.custom_palette
        else:
            return self.predefined_palettes["Guardian Red (Default)"]
    
    def apply_palette_css(self, palette: Dict[str, str]) -> str:
        """Generate CSS for the selected color palette"""
        return f"""
        <style>
        :root {{
            --primary-color: {palette['primary']};
            --secondary-color: {palette['secondary']};
            --accent-color: {palette['accent']};
            --background-color: {palette['background']};
            --surface-color: {palette['surface']};
            --text-primary: {palette['text_primary']};
            --text-secondary: {palette['text_secondary']};
            --success-color: {palette['success']};
            --warning-color: {palette['warning']};
            --error-color: {palette['error']};
            --border-color: {palette['border']};
        }}
        
        /* Apply theme colors to GUARDIAN components */
        .guardian-title {{
            color: var(--primary-color) !important;
        }}
        
        .stApp {{
            background-color: var(--background-color) !important;
            color: var(--text-primary) !important;
        }}
        
        .main .block-container {{
            background-color: var(--background-color) !important;
        }}
        
        /* Sidebar styling */
        .css-1d391kg, .css-1cypcdb, .sidebar .sidebar-content {{
            background-color: var(--surface-color) !important;
            color: var(--text-primary) !important;
        }}
        
        /* Metric containers */
        [data-testid="metric-container"] {{
            background: linear-gradient(145deg, var(--background-color) 0%, var(--surface-color) 100%);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: var(--primary-color) !important;
            color: var(--background-color) !important;
            border: 1px solid var(--primary-color) !important;
        }}
        
        .stButton > button:hover {{
            background-color: var(--secondary-color) !important;
            border-color: var(--secondary-color) !important;
        }}
        
        /* Text inputs */
        .stTextInput > div > div > input {{
            background-color: var(--background-color) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }}
        
        /* Select boxes */
        .stSelectbox > div > div > div {{
            background-color: var(--background-color) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border-color) !important;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] button {{
            color: var(--text-secondary) !important;
        }}
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
            color: var(--primary-color) !important;
            border-bottom-color: var(--primary-color) !important;
        }}
        
        /* Score badges */
        .score-excellent {{
            border-left-color: var(--success-color);
            background: linear-gradient(145deg, var(--background-color) 0%, var(--surface-color) 100%);
        }}
        
        .score-good {{
            border-left-color: var(--warning-color);
            background: linear-gradient(145deg, var(--background-color) 0%, var(--surface-color) 100%);
        }}
        
        .score-moderate {{
            border-left-color: var(--error-color);
            background: linear-gradient(145deg, var(--background-color) 0%, var(--surface-color) 100%);
        }}
        
        /* Document cards */
        .document-card {{
            background: var(--background-color);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }}
        
        .document-card:hover {{
            border-color: var(--accent-color);
        }}
        
        /* Expanders */
        .stExpander > details > summary {{
            background: linear-gradient(145deg, var(--surface-color) 0%, var(--background-color) 100%);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }}
        
        /* Info boxes */
        .sidebar-info {{
            background: linear-gradient(145deg, var(--surface-color) 0%, var(--background-color) 100%);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
        }}
        </style>
        """
    
    def render_palette_selector(self):
        """Render the color palette selector interface"""
        st.markdown("### 🎨 Adaptive Color Palette")
        
        # Palette selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_palette = st.selectbox(
                "Choose Color Theme:",
                options=list(self.predefined_palettes.keys()) + ["Custom"],
                index=0 if 'selected_palette' not in st.session_state else 
                      list(self.predefined_palettes.keys()).index(st.session_state.selected_palette) 
                      if st.session_state.selected_palette in self.predefined_palettes else len(self.predefined_palettes),
                help="Select a predefined theme or create a custom one"
            )
        
        with col2:
            if st.button("Apply Theme", type="primary", use_container_width=True):
                st.session_state.selected_palette = selected_palette
                st.rerun()
        
        # Custom palette editor
        if selected_palette == "Custom":
            self.render_custom_palette_editor()
        else:
            # Show palette preview
            self.render_palette_preview(self.predefined_palettes[selected_palette])
        
        # Save/Load functionality
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Save Current Theme", use_container_width=True):
                self.save_current_palette()
        
        with col2:
            uploaded_file = st.file_uploader(
                "Load Theme File", 
                type=['json'], 
                help="Upload a previously saved theme file",
                label_visibility="collapsed"
            )
            if uploaded_file is not None:
                self.load_palette_from_file(uploaded_file)
        
        with col3:
            if st.button("Reset to Default", use_container_width=True):
                st.session_state.selected_palette = "Guardian Red (Default)"
                st.rerun()
    
    def render_custom_palette_editor(self):
        """Render the custom palette creation interface"""
        st.markdown("#### Custom Color Palette")
        
        # Initialize custom palette if not exists
        if 'custom_palette' not in st.session_state:
            st.session_state.custom_palette = self.predefined_palettes["Guardian Red (Default)"].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.custom_palette['primary'] = st.color_picker(
                "Primary Color", st.session_state.custom_palette['primary']
            )
            st.session_state.custom_palette['secondary'] = st.color_picker(
                "Secondary Color", st.session_state.custom_palette['secondary']
            )
            st.session_state.custom_palette['accent'] = st.color_picker(
                "Accent Color", st.session_state.custom_palette['accent']
            )
            st.session_state.custom_palette['success'] = st.color_picker(
                "Success Color", st.session_state.custom_palette['success']
            )
            st.session_state.custom_palette['warning'] = st.color_picker(
                "Warning Color", st.session_state.custom_palette['warning']
            )
            st.session_state.custom_palette['error'] = st.color_picker(
                "Error Color", st.session_state.custom_palette['error']
            )
        
        with col2:
            st.session_state.custom_palette['background'] = st.color_picker(
                "Background Color", st.session_state.custom_palette['background']
            )
            st.session_state.custom_palette['surface'] = st.color_picker(
                "Surface Color", st.session_state.custom_palette['surface']
            )
            st.session_state.custom_palette['text_primary'] = st.color_picker(
                "Primary Text", st.session_state.custom_palette['text_primary']
            )
            st.session_state.custom_palette['text_secondary'] = st.color_picker(
                "Secondary Text", st.session_state.custom_palette['text_secondary']
            )
            st.session_state.custom_palette['border'] = st.color_picker(
                "Border Color", st.session_state.custom_palette['border']
            )
        
        # Preview custom palette
        self.render_palette_preview(st.session_state.custom_palette)
    
    def render_palette_preview(self, palette: Dict[str, str]):
        """Render a preview of the color palette"""
        st.markdown("#### Color Preview")
        
        # Create color swatches
        cols = st.columns(6)
        color_names = ['primary', 'secondary', 'accent', 'success', 'warning', 'error']
        
        for i, color_name in enumerate(color_names):
            with cols[i]:
                st.markdown(f"""
                <div style="
                    background-color: {palette[color_name]};
                    height: 60px;
                    border-radius: 8px;
                    border: 1px solid #e5e7eb;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: {'white' if self.is_dark_color(palette[color_name]) else 'black'};
                    font-weight: bold;
                    font-size: 12px;
                    text-align: center;
                    margin-bottom: 5px;
                ">
                    {color_name.title()}
                </div>
                <div style="text-align: center; font-size: 10px; color: #6b7280;">
                    {palette[color_name]}
                </div>
                """, unsafe_allow_html=True)
    
    def is_dark_color(self, hex_color: str) -> bool:
        """Determine if a color is dark (for text contrast)"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        return luminance < 0.5
    
    def save_current_palette(self):
        """Save the current palette as a JSON file"""
        current_palette = self.get_current_palette()
        palette_name = st.session_state.get('selected_palette', 'Guardian Red (Default)')
        
        palette_data = {
            'name': palette_name,
            'colors': current_palette,
            'created_at': str(st.session_state.get('timestamp', 'unknown'))
        }
        
        st.download_button(
            label="Download Theme File",
            data=json.dumps(palette_data, indent=2),
            file_name=f"guardian_theme_{palette_name.lower().replace(' ', '_')}.json",
            mime="application/json"
        )
    
    def load_palette_from_file(self, uploaded_file):
        """Load a palette from an uploaded JSON file"""
        try:
            palette_data = json.load(uploaded_file)
            if 'colors' in palette_data and isinstance(palette_data['colors'], dict):
                st.session_state.custom_palette = palette_data['colors']
                st.session_state.selected_palette = "Custom"
                st.success(f"Successfully loaded theme: {palette_data.get('name', 'Custom')}")
                st.rerun()
            else:
                st.error("Invalid theme file format")
        except Exception as e:
            st.error(f"Error loading theme file: {str(e)}")

# Global instance for easy access
color_manager = ColorPaletteManager()

def render_color_palette_selector():
    """Main function to render the color palette selector"""
    color_manager.render_palette_selector()

def get_current_palette_css():
    """Get CSS for the current color palette"""
    current_palette = color_manager.get_current_palette()
    return color_manager.apply_palette_css(current_palette)

def apply_current_theme():
    """Apply the current color theme to the page"""
    css = get_current_palette_css()
    st.markdown(css, unsafe_allow_html=True)