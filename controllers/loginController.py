from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash
from model.userModel import User
from db import user_collection
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token


salt = 'some_random_salt'

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None).encode('utf-8')

    if not username or not password:
        return jsonify({"error": "Please provide both username and password"}), 400

    user = user_collection.find_one({"username": username})

    if user:
        # session['user_id'] = str(user['_id'])
        stored_hashed_pwd = user['password']
        if bcrypt.checkpw(password, stored_hashed_pwd):
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify(access_token=access_token), 200
    else:
        print(user['password'])
        return jsonify({"error": "Invalid username or password"}), 401