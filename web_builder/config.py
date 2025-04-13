import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev')
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-jwt-secret-key-for-dev')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
    
    # MongoDB configuration
    MONGO_URI = os.environ.get('MONGO_URI', '')
    MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'web_builder')
    
    # Hugging Face API configuration
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')
    HUGGINGFACE_MODEL = os.environ.get('HUGGINGFACE_MODEL', 'gpt2')
    
    # Debug mode (set to False in production)
    DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
    
    # Application settings
    APP_NAME = "AI Website Builder"
    
    # Logging configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')