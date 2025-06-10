"""
Realistic PDF Page Thumbnail Generator
Creates authentic-looking PDF page thumbnails from document content
"""

import base64
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import textwrap
import os
import re

def generate_realistic_pdf_thumbnail(doc_id, title, content, doc_type, organization):
    """Generate a realistic PDF page thumbnail from document content"""
    
    # Create realistic PDF page dimensions (8.5x11 aspect ratio, scaled to 120x150)
    width, height = 120, 150
    
    # Create white page background
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fallback to default
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
        header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 8)
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 6)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 5)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Add document header/letterhead area
    y_pos = 8
    if organization:
        org_lines = textwrap.wrap(organization.upper(), width=20)
        for line in org_lines[:2]:  # Max 2 lines for org
            draw.text((8, y_pos), line, fill='#2563eb', font=header_font)
            y_pos += 10
    
    # Add title
    if title:
        title_lines = textwrap.wrap(title, width=18)
        y_pos = max(y_pos + 5, 30)
        for line in title_lines[:3]:  # Max 3 lines for title
            draw.text((8, y_pos), line, fill='#000000', font=title_font)
            y_pos += 12
    
    # Add document type/classification
    if doc_type:
        y_pos += 5
        draw.text((8, y_pos), doc_type.upper(), fill='#6b7280', font=small_font)
        y_pos += 10
    
    # Add content body text simulation
    if content:
        # Clean and extract meaningful text
        text_content = re.sub(r'\s+', ' ', str(content)).strip()
        
        # Simulate document body with realistic text layout
        y_pos += 8
        line_height = 7
        max_lines = min(12, (height - y_pos - 20) // line_height)
        
        # Create realistic paragraph structure
        words = text_content.split()[:50]  # First 50 words
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if len(test_line) <= 20:  # Characters per line
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                if len(lines) >= max_lines:
                    break
        
        if current_line and len(lines) < max_lines:
            lines.append(current_line)
        
        # Draw text lines with realistic spacing
        for i, line in enumerate(lines):
            if y_pos + line_height > height - 15:
                break
            
            # Vary line lengths slightly for realism
            display_line = line
            if i % 4 == 3:  # Every 4th line slightly shorter (paragraph breaks)
                display_line = line[:int(len(line) * 0.8)]
            
            draw.text((8, y_pos), display_line, fill='#374151', font=body_font)
            y_pos += line_height
    
    # Add page number at bottom
    draw.text((width - 15, height - 12), "1", fill='#9ca3af', font=small_font)
    
    # Add subtle border to simulate page edge
    draw.rectangle([0, 0, width-1, height-1], outline='#e5e7eb', width=1)
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG', optimize=True)
    img_data = buffer.getvalue()
    
    # Cache the thumbnail
    os.makedirs("thumbnails", exist_ok=True)
    cache_path = f"thumbnails/pdf_page_{doc_id}.png"
    with open(cache_path, 'wb') as f:
        f.write(img_data)
    
    img_b64 = base64.b64encode(img_data).decode('utf-8')
    return f"data:image/png;base64,{img_b64}"

def get_pdf_page_thumbnail_html(doc_id, title, content, doc_type, organization):
    """Get HTML for realistic PDF page thumbnail"""
    
    # Check cache first
    cache_path = f"thumbnails/pdf_page_{doc_id}.png"
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as f:
            img_data = f.read()
            img_b64 = base64.b64encode(img_data).decode('utf-8')
            thumbnail_data = f"data:image/png;base64,{img_b64}"
    else:
        # Generate new PDF page thumbnail
        thumbnail_data = generate_realistic_pdf_thumbnail(doc_id, title, content, doc_type, organization)
    
    return f'<img src="{thumbnail_data}" style="width:120px;height:150px;margin-right:8px;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,0.2);" alt="Document page thumbnail">'