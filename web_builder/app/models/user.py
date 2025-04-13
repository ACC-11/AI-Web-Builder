import bcrypt
import datetime
from bson import ObjectId
from web_builder.app.utils.database import get_db

class User:
    """User model for authentication and account management."""
    
    @staticmethod
    def to_json(user_doc):
        """Convert MongoDB document to JSON-serializable format"""
        if user_doc:
            user_doc['_id'] = str(user_doc['_id'])  # Convert ObjectId to string
        return user_doc

    @staticmethod
    def hash_password(password):
        """Hash a password for storing."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def check_password(stored_password, provided_password):
        """Check if the provided password matches the stored password."""
        return bcrypt.checkpw(
            provided_password.encode('utf-8'),
            stored_password.encode('utf-8')
        )
    
    @classmethod
    def create_user(cls, email, password):
        """Create a new user."""
        db = get_db()
        
        # Check if user already exists
        existing_user = cls.find_by_email(email)
        if existing_user:
            return None
        
        # Create user document
        user = {
            "email": email,
            "password": cls.hash_password(password),
            "created_at": datetime.datetime.utcnow(),
            "last_login": None
        }
        
        # Insert user into database
        result = db.users.insert_one(user)
        user['_id'] = result.inserted_id
        
        # Don't return the password
        user = cls.to_json(user)
        user.pop('password', None)
        
        return user
    
    @classmethod
    def find_by_email(cls, email):
        """Find a user by email."""
        db = get_db()
        user = db.users.find_one({"email": email})
        if user:
            user = cls.to_json(user)
            # user.pop('password', None)
        return user
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find a user by ID."""
        db = get_db()
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                return None
        
        user = db.users.find_one({"_id": user_id})
        if user:
            # Don't return the password
            user = cls.to_json(user)
            user.pop('password', None)
        
        return user
    
    @classmethod
    def update_last_login(cls, user_id):
        """Update the last login time for a user."""
        db = get_db()
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                return False
        
        result = db.users.update_one(
            {"_id": user_id},
            {"$set": {"last_login": datetime.datetime.utcnow()}}
        )
        
        return result.modified_count > 0