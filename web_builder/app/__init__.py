import os
from flask import Flask, jsonify, render_template, request
from flask_jwt_extended import JWTManager

from web_builder.config import Config
from web_builder.app.utils.database import init_app as init_db

# Initialize globally accessible variables
jwt = JWTManager()

def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize JWT
    jwt.init_app(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from web_builder.app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from web_builder.app.website import bp as website_bp
    app.register_blueprint(website_bp, url_prefix='/api/websites')
    
    # Root route - redirect to login page or dashboard
    @app.route('/')
    def index():
        return render_template('login.html')
    
    # Login route
    @app.route('/login')
    def login_page():
        return render_template('login.html')
    
    # Register route
    @app.route('/register')
    def register_page():
        return render_template('register.html')
    
    # Dashboard route
    @app.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api'):
            return jsonify(error="Resource not found"), 404
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        app.logger.error(f"Server error: {error}")
        if request.path.startswith('/api'):
            return jsonify(error="Internal server error"), 500
        return render_template('500.html'), 500
    
    return app