from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from web_builder.app.website import bp
from web_builder.app.models.website import Website
from web_builder.app.utils.ai_helper import generate_website_content
from web_builder.app.utils.template_renderer import render_website
from bson import json_util
import json

@bp.route('', methods=['POST'])
@jwt_required()
def create_website():
    """Create a new website with AI-generated content."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate request data
    if not data or not data.get('name') or not data.get('industry'):
        return jsonify({'error': 'Website name and industry are required'}), 400
    
    # Generate content using Hugging Face API
    try:
        content = generate_website_content(
            data['name'],
            data['industry'],
            data.get('description')
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Error generating content: {str(e)}'}), 500
    
    # Create website in database
    website = Website.create_website(
        current_user_id,
        data['name'],
        data['industry'],
        content
    )
    
    # Convert MongoDB ObjectId to string for JSON response
    website_json = json.loads(json_util.dumps(website))
    
    return jsonify({
        'message': 'Website created successfully',
        'website': website_json
    }), 201

@bp.route('', methods=['GET'])
@jwt_required()
def get_websites():
    """Get all websites for the current user."""
    current_user_id = get_jwt_identity()
    
    websites = Website.find_all_by_user(current_user_id)
    websites_json = json.loads(json_util.dumps(websites))
    
    return jsonify({
        'websites': websites_json
    }), 200

@bp.route('/<website_id>', methods=['GET'])
@jwt_required()
def get_website(website_id):
    """Get a specific website by ID."""
    current_user_id = get_jwt_identity()
    
    website = Website.find_by_id(website_id, current_user_id)
    if not website:
        return jsonify({'error': 'Website not found'}), 404
    
    website_json = json.loads(json_util.dumps(website))
    
    return jsonify({
        'website': website_json
    }), 200

@bp.route('/<website_id>', methods=['PUT'])
@jwt_required()
def update_website(website_id):
    """Update a website's content."""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate request data
    if not data or not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    # Check if website exists
    website = Website.find_by_id(website_id, current_user_id)
    if not website:
        return jsonify({'error': 'Website not found'}), 404
    
    # Update the website
    updates = {
        'content': data['content']
    }
    
    # Optionally update name and industry if provided
    if data.get('name'):
        updates['name'] = data['name']
    if data.get('industry'):
        updates['industry'] = data['industry']
    
    success = Website.update_website(website_id, current_user_id, updates)
    if not success:
        return jsonify({'error': 'Failed to update website'}), 500
    
    # Get the updated website
    updated_website = Website.find_by_id(website_id, current_user_id)
    updated_website_json = json.loads(json_util.dumps(updated_website))
    
    return jsonify({
        'message': 'Website updated successfully',
        'website': updated_website_json
    }), 200

@bp.route('/<website_id>', methods=['DELETE'])
@jwt_required()
def delete_website(website_id):
    """Delete a website."""
    current_user_id = get_jwt_identity()
    
    # Check if website exists
    website = Website.find_by_id(website_id, current_user_id)
    if not website:
        return jsonify({'error': 'Website not found'}), 404
    
    # Delete the website
    success = Website.delete_website(website_id, current_user_id)
    if not success:
        return jsonify({'error': 'Failed to delete website'}), 500
    
    return jsonify({
        'message': 'Website deleted successfully'
    }), 200

# Preview route - outside the API route prefix
@bp.route('/preview/<website_id>', methods=['GET'])
@jwt_required()
def preview_website(website_id):
    """Preview a website using the template."""
    current_user_id = get_jwt_identity()
    
    website = Website.find_by_id(website_id, current_user_id)
    if not website:
        return jsonify({'error': 'Website not found'}), 404
    
    # Render the website using the template
    html = render_website(website)
    
    return html