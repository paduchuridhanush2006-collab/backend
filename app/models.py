from .extensions import mongo
from bson import ObjectId
import bcrypt
from datetime import datetime

class User:
    @staticmethod
    def create_user(username, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            "username": username,
            "email": email,
            "password": hashed_password
        }
        result = mongo.db.users.insert_one(user)
        return result.inserted_id

    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def verify_password(stored_password, provided_password):
        return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

class Favorite:
    @staticmethod
    def add_favorite(user_id, city_name):
        existing = mongo.db.favorites.find_one({"user_id": ObjectId(user_id), "city_name": city_name})
        if existing:
            return None
        
        favorite = {
            "user_id": ObjectId(user_id),
            "city_name": city_name,
            "added_at": datetime.utcnow()
        }
        
        result = mongo.db.favorites.insert_one(favorite)
        return result.inserted_id

    @staticmethod
    def get_user_favorites(user_id):
        return list(mongo.db.favorites.find({"user_id": ObjectId(user_id)}))

    @staticmethod
    def remove_favorite(favorite_id, user_id):
        result = mongo.db.favorites.delete_one({"_id": ObjectId(favorite_id), "user_id": ObjectId(user_id)})
        return result.deleted_count > 0
