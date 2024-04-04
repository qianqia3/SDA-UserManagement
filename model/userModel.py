from werkzeug.security import generate_password_hash
from db import user_collection

class User:
    @staticmethod
    def insert_user(username, email, password):
        user_collection.insert_one({
            "username": username,
            "email": email,
            "password": password
        })