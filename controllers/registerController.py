from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from model.userModel import User
from db import user_collection
import bcrypt
from model.profileModel import Profile
from flask_jwt_extended import create_access_token

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('register', methods=['POST'])
def register_user():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd, salt)
    email = request.json.get("email", None)
    phone_number = request.json.get("phone_number", None)
    avg_payback_time = request.json.get("avg_payback_time", None)

    if not username or not password or not email:
        return jsonify({"error": "Please provide username, password, and email"}), 400

    if user_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 409


    User.insert_user(username, email, hashed_password)
    # Profile.create_profile(username)

    profile_created = Profile.create_profile(username, email, phone_number, avg_payback_time)
        # return {"msg": "User registered and profile created successfully."}, 200
    if not profile_created:
        # Handle profile creation failure, if necessary
        return {"msg": "User registered, but profile creation failed."}, 500
    
    access_token = create_access_token(identity=str(User.get_user_id(username)))
    return jsonify(access_token=access_token, username=username), 200

    # return jsonify({"message": "User registered successfully"}), 201
