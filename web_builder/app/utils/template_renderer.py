import datetime
from flask import render_template

def render_website(website_data):
    """
    Render a website using the base template and website data.
    
    Args:
        website_data: The website data to use for rendering
        
    Returns:
        Rendered HTML string
    """
    # Add current year for copyright notice
    current_year = datetime.datetime.now().year
    
    # Ensure all required sections exist in the website content
    # This helps prevent template errors if some content is missing
    if not website_data.get('content'):
        website_data['content'] = {}
    
    required_sections = ['hero', 'about', 'services', 'contact', 'footer']
    for section in required_sections:
        if section not in website_data['content']:
            website_data['content'][section] = {}
    
    # Make sure service items exists
    if 'items' not in website_data['content']['services']:
        website_data['content']['services']['items'] = []
    
    # Provide default icon names if missing
    for service in website_data['content']['services']['items']:
        if 'icon_name' not in service:
            service['icon_name'] = 'star'  # Default icon
    
    return render_template('website_template.html', 
                          website=website_data,
                          current_year=current_year)