"""
Content-based thumbnail generator that creates unique thumbnails from document content
"""

import base64
import hashlib
import re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

def generate_content_based_thumbnail(doc_id, title, content, doc_type, organization):
    """Generate thumbnail based on actual document content"""
    
    # Create unique color scheme based on content hash
    content_hash = hashlib.md5((title + str(content)[:100]).encode()).hexdigest()
    color_seed = int(content_hash[:6], 16) % 12
    
    # Color schemes based on document analysis
    color_schemes = [
        {"bg": "#1e40af", "accent": "#3b82f6", "text_color": "#ffffff"},  # Blue - Policy
        {"bg": "#dc2626", "accent": "#ef4444", "text_color": "#ffffff"},  # Red - Security
        {"bg": "#059669", "accent": "#10b981", "text_color": "#ffffff"},  # Green - Framework
        {"bg": "#7c3aed", "accent": "#8b5cf6", "text_color": "#ffffff"},  # Purple - AI
        {"bg": "#ea580c", "accent": "#f97316", "text_color": "#ffffff"},  # Orange - Technical
        {"bg": "#be185d", "accent": "#ec4899", "text_color": "#ffffff"},  # Pink - Guidance
        {"bg": "#0891b2", "accent": "#06b6d4", "text_color": "#ffffff"},  # Cyan - Cyber
        {"bg": "#475569", "accent": "#64748b", "text_color": "#ffffff"},  # Gray - Joint
        {"bg": "#166534", "accent": "#22c55e", "text_color": "#ffffff"},  # Dark Green - NIST
        {"bg": "#7c2d12", "accent": "#dc2626", "text_color": "#ffffff"},  # Brown - Standards
        {"bg": "#581c87", "accent": "#a855f7", "text_color": "#ffffff"},  # Deep Purple - Research
        {"bg": "#0f172a", "accent": "#334155", "text_color": "#ffffff"},  # Dark - Classification
    ]
    
    colors = color_schemes[color_seed]
    
    # Create image
    width, height = 120, 150
    img = Image.new('RGB', (width, height), colors["bg"])
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 12)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 8)
        font_tiny = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 6)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # White content area
    draw.rectangle([8, 8, width-8, height-8], fill="#ffffff", outline=colors["accent"], width=2)
    
    # Organization header
    org_short = organization[:8] if organization else "DOC"
    org_bbox = draw.textbbox((0, 0), org_short, font=font_small)
    org_width = org_bbox[2] - org_bbox[0]
    draw.rectangle([12, 12, width-12, 28], fill=colors["bg"])
    draw.text(((width - org_width) // 2, 17), org_short, fill=colors["text_color"], font=font_small)
    
    # Document type indicator
    doc_type_short = doc_type[:12] if doc_type else "Document"
    type_bbox = draw.textbbox((0, 0), doc_type_short, font=font_tiny)
    type_width = type_bbox[2] - type_bbox[0]
    draw.text(((width - type_width) // 2, 35), doc_type_short, fill=colors["bg"], font=font_tiny)
    
    # Content preview lines (simulate text content)
    if content:
        # Extract meaningful words from content
        words = re.findall(r'\b\w{3,}\b', str(content)[:200])
        preview_lines = []
        current_line = ""
        
        for word in words[:15]:  # Limit to first 15 meaningful words
            if len(current_line + " " + word) < 15:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    preview_lines.append(current_line)
                current_line = word
                if len(preview_lines) >= 8:  # Max 8 lines
                    break
        
        if current_line:
            preview_lines.append(current_line)
        
        # Draw content preview lines
        y_pos = 50
        for i, line in enumerate(preview_lines):
            line_width = int(80 - (i * 3))  # Varying line lengths
            if line_width > 20:
                draw.rectangle([15, y_pos, 15 + line_width, y_pos + 2], 
                             fill=colors["accent"] if i == 0 else "#d1d5db")
            y_pos += 8
    
    # Unique identifier pattern based on doc_id
    pattern_y = height - 40
    for i in range(5):
        x_pos = 20 + (i * 16)
        size = 3 + ((doc_id + i) % 3)
        draw.ellipse([x_pos, pattern_y + i*2, x_pos + size, pattern_y + i*2 + size], 
                    fill=colors["accent"])
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG', optimize=True)
    img_data = buffer.getvalue()
    
    # Cache the thumbnail
    os.makedirs("thumbnails", exist_ok=True)
    cache_path = f"thumbnails/content_thumb_{doc_id}.png"
    with open(cache_path, 'wb') as f:
        f.write(img_data)
    
    img_b64 = base64.b64encode(img_data).decode('utf-8')
    return f"data:image/png;base64,{img_b64}"

def get_content_thumbnail_html(doc_id, title, content, doc_type, organization):
    """Get HTML for content-based thumbnail"""
    
    # Check cache first
    cache_path = f"thumbnails/content_thumb_{doc_id}.png"
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            img_data = f.read()
            img_b64 = base64.b64encode(img_data).decode('utf-8')
            thumbnail_data = f"data:image/png;base64,{img_b64}"
    else:
        # Generate new thumbnail
        thumbnail_data = generate_content_based_thumbnail(doc_id, title, content, doc_type, organization)
    
    return f'<img src="{thumbnail_data}" style="width:120px;height:150px;margin-right:8px;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,0.2);" alt="Document thumbnail">'