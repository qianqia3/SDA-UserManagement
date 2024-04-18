import random
from werkzeug.security import generate_password_hash
from db import user_collection

def generate_unique_friend_id():
    while True:
        # a random 5-digit num for friend id
        friend_id = str(random.randint(10000, 99999))
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