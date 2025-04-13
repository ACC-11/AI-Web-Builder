import os
from flask import current_app, g
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def get_db():
    """
    Get database connection.
    
    Returns:
        MongoDB database connection
    """
    if 'db' not in g:
        # Get MongoDB URI from environment variables or config
        mongo_uri = os.environ.get("MONGO_URI") or current_app.config.get("MONGO_URI")
        
        if not mongo_uri:
            # Using a placeholder message when URI is not available
            current_app.logger.warning("MongoDB URI not found. Please set the MONGO_URI environment variable.")
            # For development purposes, we raise an error to notify about missing credentials
            # In production, you might want to handle this differently
            raise ConnectionFailure("MongoDB URI not found. Please set the MONGO_URI environment variable.")
        
        try:
            # Connect to MongoDB
            client = MongoClient(mongo_uri)
            
            # Verify connection is successful
            client.admin.command('ping')
            
            # Get database name from URI or use default
            db_name = os.environ.get("MONGO_DBNAME") or current_app.config.get("MONGO_DBNAME", "web_builder")
            
            # Store client and db in flask g object
            g.mongo_client = client
            g.db = client[db_name]
            
            current_app.logger.info(f"Connected to MongoDB database: {db_name}")
            
        except ConnectionFailure as e:
            current_app.logger.error(f"MongoDB connection failed: {str(e)}")
            raise ConnectionFailure(f"Failed to connect to MongoDB: {str(e)}")
    
    return g.db

def close_db(e=None):
    """
    Close database connection.
    """
    mongo_client = g.pop('mongo_client', None)
    
    if mongo_client is not None:
        mongo_client.close()
        current_app.logger.info("Closed MongoDB connection")

def init_db():
    """
    Initialize database with required collections and indexes.
    """
    db = get_db()
    
    # Create collections if they don't exist
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
        # Create unique index on email
        db.users.create_index('email', unique=True)
        current_app.logger.info("Created users collection with email index")
    
    if 'websites' not in db.list_collection_names():
        db.create_collection('websites')
        # Create index on user_id for faster queries
        db.websites.create_index('user_id')
        current_app.logger.info("Created websites collection with user_id index")

def init_app(app):
    """
    Initialize the database connection for the app.
    """
    # Register close_db to be called when app context ends
    app.teardown_appcontext(close_db)
    
    # Initialize the database when the app starts
    with app.app_context():
        try:
            init_db()
        except ConnectionFailure as e:
            app.logger.warning(f"Could not initialize database: {str(e)}")
            app.logger.warning("The application will attempt to connect when MongoDB URI is provided.")