from flask import request, jsonify
from werkzeug.security import generate_password_hash
from model.userModel import User
from db import user_collection


def register_user():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)

    if not username or not password or not email:
        return jsonify({"error": "Please provide username, password, and email"}), 400

    if user_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 409

    hashed_password = generate_password_hash(password)

    User.insert_user(username, email, hashed_password)

    return jsonify({"message": "User registered successfully"}), 201
