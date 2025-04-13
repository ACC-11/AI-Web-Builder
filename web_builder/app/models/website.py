import datetime
from bson import ObjectId
from web_builder.app.utils.database import get_db

class Website:
    """Website model for managing generated websites."""
    
    @classmethod
    def create_website(cls, user_id, name, industry, content):
        """Create a new website for a user."""
        db = get_db()
        
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                return None
        
        # Create website document
        website = {
            "user_id": user_id,
            "name": name,
            "industry": industry,
            "content": content,
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }
        
        # Insert website into database
        result = db.websites.insert_one(website)
        website['_id'] = result.inserted_id
        
        return website
    
    @classmethod
    def find_by_id(cls, website_id, user_id=None):
        """Find a website by ID, optionally filtering by user_id."""
        db = get_db()
        
        if isinstance(website_id, str):
            try:
                website_id = ObjectId(website_id)
            except:
                return None
        
        query = {"_id": website_id}
        
        # If user_id is provided, ensure the website belongs to this user
        if user_id:
            if isinstance(user_id, str):
                try:
                    user_id = ObjectId(user_id)
                except:
                    return None
            
            query["user_id"] = user_id
        
        return db.websites.find_one(query)
    
    @classmethod
    def find_all_by_user(cls, user_id):
        """Find all websites for a specific user."""
        db = get_db()
        
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                return []
        
        # Find all websites for the user, sort by creation date (newest first)
        websites = list(db.websites.find(
            {"user_id": user_id}
        ).sort("created_at", -1))
        
        return websites
    
    @classmethod
    def update_website(cls, website_id, user_id, updates):
        """Update a website."""
        db = get_db()
        
        if isinstance(website_id, str):
            try:
                website_id = ObjectId(website_id)
            except:
                return False
        
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                return False
        
        # Add updated_at timestamp to updates
        updates["updated_at"] = datetime.datetime.utcnow()
        
        # Update the website document
        result = db.websites.update_one(
            {"_id": website_id, "user_id": user_id},
            {"$set": updates}
        )
        
        return result.modified_count > 0
    
    @classmethod
    def delete_website(cls, website_id, user_id):
        """Delete a website."""
        db = get_db()
        
        if isinstance(website_id, str):
            try:
                website_id = ObjectId(website_id)
            except:
                return False
        
        if isinstance(user_id, str):
            try:
                user_id = ObjectId(user_id)
            except:
                return False
        
        # Delete the website document
        result = db.websites.delete_one(
            {"_id": website_id, "user_id": user_id}
        )
        
        return result.deleted_count > 0