import random
from werkzeug.security import generate_password_hash
from db import user_collection
import pyotp

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
            "friend_id": friend_id,
            "2fa_enabled": False,
            "2fa_secret": None
        })

    @staticmethod
    def set_2fa_secret(user_id):
        secret = pyotp.random_base32()
        user_collection.update_one({"_id": user_id}, {"$set": {"2fa_secret": secret}})
        return secret

    @staticmethod
    def verify_2fa(user_id, otp):
        user = user_collection.find_one({"_id": user_id})
        if user and pyotp.TOTP(user['2fa_secret']).verify(otp):
            return True
        return False