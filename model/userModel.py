import random
from werkzeug.security import generate_password_hash
from db import user_collection

def generate_unique_friend_id():
    while True:
        friend_id = str(random.randint(10000, 99999))  # Generate a 5-digit number
        if not user_collection.find_one({"friend_id": friend_id}):
            return friend_id

class User:
    @staticmethod
    def insert_user(username, email, password):
        friend_id = generate_unique_friend_id()
        user_collection.insert_one({
            "username": username,
            "email": email,
            "password": password,
            "friend_id": friend_id
        })