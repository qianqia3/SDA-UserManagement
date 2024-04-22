from flask import request, jsonify, Blueprint
from werkzeug.security import check_password_hash
from model.userModel import User
from db import user_collection
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token
import pyotp
from mail import mail
from flask_mail import Message

salt = 'some_random_salt'

login_blueprint = Blueprint('login', __name__)
@login_blueprint.route('login', methods=['POST'])
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
            if user.get('2fa_enabled'):
                # access_token = create_access_token(identity=str(user['_id']))
                # return jsonify(access_token=access_token), 200
                # Generate the OTP
                secret = pyotp.random_base32()
                print(secret)
                otp = pyotp.TOTP(secret).now()
                user_collection.update_one(
                    {"username": username},
                    {"$set": {"2fa_secret":otp}}
                )

                # Send OTP via email
                send_email(user['email'], otp)

                # Create a partial token that will be used to complete the 2FA verification
                partial_token = create_refresh_token(identity=str(user['_id']))
                return jsonify({"msg": "2FA token required", "2fa_required": True, "partial_token": partial_token}), 200
            else:
                # If 2FA is not enabled, provide the full access token
                access_token = create_access_token(identity=str(user['_id']))
                return jsonify(access_token=access_token), 200
    else:
        print(user['password'])
        return jsonify({"error": "Invalid username or password"}), 401
    
def send_email(recipient, otp):
    subject = "Your OTP for 2FA Login"
    sender = "no-reply@example.com"  # Your sender email
    recipients = [recipient]
    body = f"Your OTP is: {otp}"
    
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = body
    mail.send(message)