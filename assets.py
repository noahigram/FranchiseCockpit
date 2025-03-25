import streamlit as st
import html

# Icons for different business aspects
ICONS = {
    "cash_flow": "💰",
    "customer_satisfaction": "😊",
    "growth_potential": "📈",
    "risk_level": "⚠️"
}

# Colors for different metrics
COLORS = {
    "positive": "#28a745",  # Green
    "negative": "#dc3545",  # Red
    "neutral": "#6c757d",   # Gray
    "info": "#17a2b8",      # Blue
    "warning": "#ffc107"    # Yellow
}

# Background patterns for cards
def get_card_bg_style(pattern_type="default"):
    patterns = {
        "default": "linear-gradient(to right, #f8f9fa, #e9ecef)",
        "best_case": "linear-gradient(to right, #d4edda, #c3e6cb)",
        "worst_case": "linear-gradient(to right, #f8d7da, #f5c6cb)",
        "summary": "linear-gradient(to right, #cce5ff, #b8daff)"
    }
    return patterns.get(pattern_type, patterns["default"])

# Create styled metric display
def styled_metric(label, value, delta=None, prefix="", suffix="", show_icon=True):
    """
    Create a styled metric display with icon, label, and value
    
    Parameters:
    - label: The name of the metric
    - value: The current value
    - delta: Change value (optional)
    - prefix: Value prefix (e.g., "$")
    - suffix: Value suffix (e.g., "%")
    - show_icon: Whether to show an icon
    """
    icon = ICONS.get(label.lower().replace(" ", "_"), "📊")
    
    delta_html = ""
    if delta is not None:
        if delta > 0:
            delta_html = f'<span style="color: {COLORS["positive"]}">↑ {prefix}{abs(delta)}{suffix}</span>'
        elif delta < 0:
            delta_html = f'<span style="color: {COLORS["negative"]}">↓ {prefix}{abs(delta)}{suffix}</span>'
        else:
            delta_html = f'<span style="color: {COLORS["neutral"]}">↔ {prefix}{abs(delta)}{suffix}</span>'
    
    icon_html = f"{icon} " if show_icon else ""
    
    html_content = f"""
    <div style="background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 0.125rem 0.25rem rgba(0,0,0,0.075); margin-bottom: 1rem;">
        <div style="font-size: 0.875rem; color: #6c757d; margin-bottom: 0.5rem;">{icon_html}{html.escape(label)}</div>
        <div style="font-size: 1.5rem; font-weight: bold; color: #212529;">{prefix}{html.escape(str(value))}{suffix}</div>
        {delta_html}
    </div>
    """
    
    return html_content

# Create a styled card
def styled_card(title, content, card_type="default"):
    """
    Create a styled card with title and content
    
    Parameters:
    - title: Card title
    - content: Card content (HTML string)
    - card_type: Type of card styling (default, best_case, worst_case, summary)
    """
    bg_style = get_card_bg_style(card_type)
    
    border_color = {
        "default": "#dee2e6",
        "best_case": "#28a745",
        "worst_case": "#dc3545",
        "summary": "#17a2b8"
    }.get(card_type, "#dee2e6")
    
    html_content = f"""
    <div style="background: {bg_style}; border-left: 5px solid {border_color}; border-radius: 0.5rem; padding: 1.25rem; margin-bottom: 1.5rem; box-shadow: 0 0.25rem 0.5rem rgba(0,0,0,0.1);">
        <h4 style="margin-top: 0; margin-bottom: 1rem; color: #343a40;">{html.escape(title)}</h4>
        <div>
            {content}
        </div>
    </div>
    """
    
    return html_content

# Create a styled scenario option
def styled_scenario_option(title, description, consequences, option_type="best_case"):
    """
    Create a styled scenario option display
    
    Parameters:
    - title: Scenario title
    - description: Scenario description
    - consequences: Dictionary of consequences
    - option_type: Type of scenario (best_case or worst_case)
    """
    bg_color = "#d4edda" if option_type == "best_case" else "#f8d7da"
    border_color = "#28a745" if option_type == "best_case" else "#dc3545"
    icon = "✅" if option_type == "best_case" else "⚠️"
    
    consequences_html = ""
    for metric, value in consequences.items():
        formatted_metric = metric.replace("_", " ").title()
        if metric == "cash_flow":
            prefix = "$"
            suffix = ""
            color = COLORS["positive"] if value > 0 else COLORS["negative"]
        elif metric == "risk_level":
            prefix = ""
            suffix = "%"
            color = COLORS["negative"] if value > 0 else COLORS["positive"]
        else:
            prefix = ""
            suffix = "%"
            color = COLORS["positive"] if value > 0 else COLORS["negative"]
        
        if value > 0:
            change_icon = "↑"
        elif value < 0:
            change_icon = "↓"
        else:
            change_icon = "↔"
            color = COLORS["neutral"]
        
        consequences_html += f'<div style="margin: 0.25rem 0;"><span style="color: {color};">{change_icon} {html.escape(formatted_metric)}:</span> {prefix}{abs(value)}{suffix}</div>'
    
    html_content = f"""
    <div style="background-color: {bg_color}; border-left: 5px solid {border_color}; border-radius: 0.5rem; padding: 1.25rem; margin-bottom: 1.5rem;">
        <h4 style="margin-top: 0; margin-bottom: 0.5rem; color: #343a40;">{icon} {html.escape(title)}</h4>
        <p style="margin-bottom: 1rem;">{html.escape(description)}</p>
        <div style="background-color: rgba(255,255,255,0.5); padding: 0.75rem; border-radius: 0.25rem;">
            <div style="font-weight: bold; margin-bottom: 0.5rem;">Impact:</div>
            {consequences_html}
        </div>
    </div>
    """
    
    return html_content

# Create path visual
def generate_path_visual(history, width=600, height=200, text_color="#333333"):
    """
    Generate a simple visualization of the decision path
    Returns the HTML to embed in streamlit
    
    Parameters:
    - history: List of scenario history items
    - width: Width of the SVG element
    - height: Height of the SVG element
    - text_color: Color of the text labels
    """
    if not history:
        return ""
    
    step_width = width / (len(history) + 1)
    path_html = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Draw connecting lines
    path_html += f'<line x1="0" y1="{height/2}" x2="{width}" y2="{height/2}" stroke="#dee2e6" stroke-width="2" stroke-dasharray="5,5" />'
    
    # Draw decision points
    for i, decision in enumerate(history):
        x = (i + 1) * step_width
        y = height / 2
        
        # Determine color based on decision type
        color = "#28a745" if decision['choice'] == "Best Case" else "#dc3545"
        
        # Add circle for decision point
        path_html += f'<circle cx="{x}" cy="{y}" r="10" fill="{color}" />'
        
        # Add decision label with specified text color
        path_html += f'<text x="{x}" y="{y-20}" text-anchor="middle" font-size="12" fill="{text_color}">{html.escape(decision["topic"])}</text>'
        
    path_html += '</svg>'
    
    return path_html

# Generate a business logo
def generate_logo():
    """Generate a simple business logo for the simulator"""
    # Create a simple logo image
    from PIL import Image, ImageDraw, ImageFont
    import io
    import base64
    
    # Create a white canvas
    img = Image.new('RGBA', (200, 200), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a circular background
    draw.ellipse((10, 10, 190, 190), fill=(78, 137, 174, 255))
    
    # Add text
    try:
        # Try to load a font, fall back to default if not available
        font = ImageFont.truetype("Arial.ttf", 65)
    except IOError:
        font = ImageFont.load_default()
    
    draw.text((100, 100), "BW", fill=(255, 255, 255, 255), font=font, anchor="mm")
    
    # Convert to bytes
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f'<img src="data:image/png;base64,{img_str}" width="100">'

# Display an intro animation
def display_intro_animation():
    """Display a simple intro animation using HTML/CSS"""
    intro_html = """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .intro-title {
        animation: fadeIn 1.2s ease-out;
    }
    .intro-subtitle {
        animation: fadeIn 1.5s ease-out;
    }
    .intro-text {
        animation: fadeIn 1.8s ease-out;
    }
    .intro-button {
        animation: fadeIn 2.1s ease-out;
    }
    </style>
    
    <div style="text-align: center; padding: 2rem 0;">
        <div class="intro-title">
            <h1 style="font-size: 2.5rem; color: #43658b; margin-bottom: 1rem;">Best Case, Worst Case</h1>
        </div>
        <div class="intro-subtitle">
            <h2 style="font-size: 1.5rem; color: #6c757d; margin-bottom: 2rem;">Franchise Decision Simulator</h2>
        </div>
        <div class="intro-text">
            <p style="font-size: 1.1rem; max-width: 600px; margin: 0 auto 2rem auto;">
                Explore the impact of different business decisions on your franchise's success. 
                Navigate challenging scenarios and see how your choices affect key metrics.
            </p>
        </div>
    </div>
    """
    
    return intro_html 