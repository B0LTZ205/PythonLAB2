from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
import os
import gridfs

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["studentdb"]
users_collection = db["users"]

def get_all_users():
    return list(users_collection.find())

def get_user_by_id(user_id):
    return users_collection.find_one({"_id": ObjectId(user_id)})

def get_user_by_email(email):
    return users_collection.find_one({"email": email})

def get_user_by_username(username):
    return users_collection.find_one({"username": username})

def hash_password(password, salt=None):
    """Hash a password using SHA-256 with a random salt"""
    if salt is None:
        salt = os.urandom(32)  # 32 bytes = 256 bits
    
    # Hash the password with the salt
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    
    # Return the salt and hash
    return salt + pwdhash

def verify_password(stored_password_hash, provided_password):
    """Verify a password against a stored hash"""
    # Extract the salt (first 32 bytes)
    salt = stored_password_hash[:32]
    
    # Hash the provided password with the extracted salt
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    
    # Compare the computed hash with the stored hash
    return salt + pwdhash == stored_password_hash

def add_user(data):
    # Hash the password before storing
    password = data.get("password", "")
    hashed_password = hash_password(password)
    
    # Replace plain text password with hashed password
    data["password"] = hashed_password
    
    # Set default role if not specified
    if "role" not in data:
        data["role"] = "user"
        
    return users_collection.insert_one(data)

def update_user(user_id, data):
    # If updating password, hash it
    if "password" in data and data["password"]:
        data["password"] = hash_password(data["password"])
    
    return users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})

def delete_user(user_id):
    return users_collection.delete_one({"_id": ObjectId(user_id)})