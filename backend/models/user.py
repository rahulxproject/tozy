import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
import bcrypt

class User:
    """User model for authentication and account management"""
    
    def __init__(self, db):
        self.db = db
    
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify a password against a hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def create_user(self, email, password, name=None):
        """Create a new user"""
        password_hash = self.hash_password(password)
        
        query = """
        INSERT INTO users (email, password_hash, name, subscription_tier, subscription_status, preferences)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, email, name, created_at
        """
        
        preferences = {
            'timezone': 'Asia/Kolkata',
            'default_strategies': [],
            'notification_enabled': True
        }
        
        result = self.db.execute(query, (
            email,
            password_hash,
            name,
            'free',
            'active',
            preferences
        ))
        
        return dict(result) if result else None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        result = self.db.execute(query, (email,))
        return dict(result) if result else None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = self.db.execute(query, (user_id,))
        return dict(result) if result else None
    
    def update_user(self, user_id, updates):
        """Update user information"""
        allowed_fields = ['name', 'preferences', 'subscription_tier', 'subscription_status']
        set_clauses = []
        values = []
        
        for field, value in updates.items():
            if field in allowed_fields:
                if isinstance(value, dict):
                    set_clauses.append(f"{field} = %s::jsonb")
                else:
                    set_clauses.append(f"{field} = %s")
                values.append(value)
        
        if not set_clauses:
            return False
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        
        self.db.execute(query, values)
        return True
