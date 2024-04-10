from flask import request, jsonify, Blueprint
from werkzeug.security import generate_password_hash
from model.userModel import User
from db import user_collection
import bcrypt
from model.profileModel import Profile

register_blueprint = Blueprint('register', __name__)

@register_blueprint.route('/register', methods=['POST'])
def register_user():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd, salt)
    email = request.json.get("email", None)

    if not username or not password or not email:
        return jsonify({"error": "Please provide username, password, and email"}), 400

    if user_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 409


    User.insert_user(username, email, hashed_password)
    # Profile.create_profile(username)

    if Profile.create_profile(username, email):
        # Respond with success
        return {"msg": "User registered and profile created successfully."}, 200
    else:
        # Handle profile creation failure, if necessary
        return {"msg": "User registered, but profile creation failed."}, 500

    # return jsonify({"message": "User registered successfully"}), 201
