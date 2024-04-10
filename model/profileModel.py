from werkzeug.security import generate_password_hash
from db import profile_collection
from model.userModel import User

class Profile:
    @staticmethod
    def create_profile(username, email):
        profile_document = {
            "username": username,
            "email": email,
            "phone_number": "",
            "avg_time": "",
        }
        result = profile_collection.insert_one(profile_document)
        if result.inserted_id:
            print(f"Profile created for user: {username}")
            return True
        else:
            print(f"Failed to create profile for user: {username}")
            return False