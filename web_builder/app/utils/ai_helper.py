import os
import json
import requests
from flask import current_app

def generate_website_content(business_name, industry, description=None):
    """
    Generate website content using Hugging Face API.
    
    Args:
        business_name: Name of the business
        industry: Industry type (e.g., "restaurant", "tech", "healthcare")
        description: Optional additional description
        
    Returns:
        Dict containing the generated content for different website sections
    """
    # Get API key from environment variables
    api_key = os.environ.get("HUGGINGFACE_API_KEY") or current_app.config.get("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("Hugging Face API key not found. Please set the HUGGINGFACE_API_KEY environment variable.")
    
    # Get the model to use
    model = os.environ.get("HUGGINGFACE_MODEL") or current_app.config.get("HUGGINGFACE_MODEL", "gpt2") #this is not used anywhere
    
    # Prepare the prompt for content generation
    prompt = f"""Generate website content for a {industry} business named '{business_name}'."""
    
    if description:
        prompt += f" {description}."
    
    prompt += """
    The content should include the following sections:
    1. Hero section with headline and subheadline
    2. About section with paragraphs, mission statement, and vision statement
    3. Services section with a list of services (at least 3)
    4. Contact section with business details
    5. Footer with company description
    
    Format the response as a valid JSON object with the following structure:
    {
      "hero": {
        "headline": "Main headline for the website",
        "subheadline": "Supporting text for the headline"
      },
      "about": {
        "paragraphs": ["Paragraph 1", "Paragraph 2"],
        "mission_title": "Our Mission",
        "mission_statement": "Mission statement text",
        "vision_title": "Our Vision",
        "vision_statement": "Vision statement text"
      },
      "services": {
        "description": "Brief description of services",
        "items": [
          {
            "title": "Service 1",
            "description": "Description of service 1",
            "icon_name": "chart-line"
          },
          {
            "title": "Service 2",
            "description": "Description of service 2",
            "icon_name": "users"
          },
          {
            "title": "Service 3",
            "description": "Description of service 3",
            "icon_name": "cog"
          }
        ]
      },
      "testimonials": {
        "items": [
          {
            "name": "Client Name",
            "position": "Position, Company",
            "quote": "Testimonial quote"
          }
        ]
      },
      "contact": {
        "description": "Brief text inviting visitors to get in touch",
        "address": "123 Business Street, City, State, ZIP",
        "phone": "+1 (123) 456-7890",
        "email": "contact@example.com",
        "hours": "Monday-Friday: 9am-5pm"
      },
      "footer": {
        "company_description": "Brief company description for footer"
      }
    }
    """

    try:
        # Make API request to Hugging Face
        # api_url = f"https://api-inference.huggingface.co/models/{model}"
        api_url = f"https://router.huggingface.co/novita/v3/openai/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        # payload = {"inputs": prompt, "parameters": {"max_length": 2048, "temperature": 0.7}}
        payload = {
            "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "model": "deepseek/deepseek-v3-0324",
                    "stream": False
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        print('response of ai')
        
        response.raise_for_status()
        
        # Extract generated text from response
        result = response.json()
        generated_text = ""
        print("Full API response:", json.dumps(result, indent=2))  # Debug print
        
        if isinstance(result, dict) and "choices" in result and len(result["choices"]) > 0:
            generated_text = result["choices"][0]["message"]["content"]
            
            # Extract JSON from the generated text (might be wrapped in markdown)
            json_str = extract_json_from_text(generated_text)
            
            if json_str:
                content = json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in generated text")
        else:
            raise ValueError("Unexpected API response format")
            
        # Validate and ensure all required sections exist
        content = validate_content_structure(content, business_name, industry)
        return content
        
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error calling API: {str(e)}")
    except Exception as e:
        print(f"Error processing response: {str(e)}")
        # Fallback to default content if anything goes wrong
        return create_default_content(business_name, industry, description)

def extract_json_from_text(text):
    """
    Extract JSON content from text that might contain markdown formatting.
    """
    # Try to find JSON between ```json and ``` markers
    json_start = text.find('```json')
    if json_start >= 0:
        json_start = text.find('\n', json_start) + 1
        json_end = text.find('```', json_start)
        return text[json_start:json_end].strip()
    
    # Try to find JSON between ``` and ``` markers
    json_start = text.find('```')
    if json_start >= 0:
        json_start = text.find('\n', json_start) + 1
        json_end = text.find('```', json_start)
        return text[json_start:json_end].strip()
    
    # Try to find standalone JSON
    json_start = text.find('{')
    json_end = text.rfind('}') + 1
    if json_start >= 0 and json_end > json_start:
        return text[json_start:json_end]
    
    return None

def create_default_content(business_name, industry, description=None):
    """
    Create default website content when the AI generation fails.
    
    Args:
        business_name: Name of the business
        industry: Industry type
        description: Optional description
        
    Returns:
        Dict containing default content
    """
    return {
        "hero": {
            "headline": f"Welcome to {business_name}",
            "subheadline": f"Your trusted partner in the {industry} industry"
        },
        "about": {
            "paragraphs": [
                f"{business_name} is a leading provider in the {industry} industry.",
                "We are committed to delivering exceptional value to our clients and customers."
            ],
            "mission_title": "Our Mission",
            "mission_statement": f"To provide exceptional {industry} solutions that exceed our clients' expectations.",
            "vision_title": "Our Vision",
            "vision_statement": f"To be the leading {industry} provider recognized for innovation and excellence."
        },
        "services": {
            "description": f"Explore our range of {industry} services designed to meet your needs.",
            "items": [
                {
                    "title": "Service 1",
                    "description": "Description of our first service offering.",
                    "icon_name": "chart-line"
                },
                {
                    "title": "Service 2",
                    "description": "Description of our second service offering.",
                    "icon_name": "users"
                },
                {
                    "title": "Service 3",
                    "description": "Description of our third service offering.",
                    "icon_name": "cog"
                }
            ]
        },
        "testimonials": {
            "items": [
                {
                    "name": "John Doe",
                    "position": "CEO, Company Name",
                    "quote": f"Working with {business_name} has been a fantastic experience. Their {industry} expertise is unmatched."
                }
            ]
        },
        "contact": {
            "description": "We'd love to hear from you. Contact us to learn more about our services.",
            "address": "123 Business Street, City, State, ZIP",
            "phone": "+1 (123) 456-7890",
            "email": f"contact@{business_name.lower().replace(' ', '')}.com",
            "hours": "Monday-Friday: 9am-5pm"
        },
        "footer": {
            "company_description": f"{business_name} provides top-quality {industry} services to clients worldwide."
        }
    }

def validate_content_structure(content, business_name, industry):
    """
    Validate and fill in missing sections in the content structure.
    
    Args:
        content: The content structure to validate
        business_name: Name of the business
        industry: Industry type
        
    Returns:
        Validated content structure
    """
    default_content = create_default_content(business_name, industry)
    
    # Ensure all top-level sections exist
    for section, default_section in default_content.items():
        if section not in content:
            content[section] = default_section
            continue
            
        # For each section, ensure all required fields exist
        if isinstance(default_section, dict):
            for key, default_value in default_section.items():
                if key not in content[section]:
                    content[section][key] = default_value
    
    return content