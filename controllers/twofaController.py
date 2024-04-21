from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import user_collection
from mail import mail  # Import the configured mail instance
from flask_mail import Message
import pyotp
from bson import ObjectId

two_factor_blueprint = Blueprint('two', __name__)

@two_factor_blueprint.route('two', methods=['POST'])
@jwt_required()
def initiate_2fa():
    current_user_id = get_jwt_identity()
    user = user_collection.find_one({"_id": ObjectId(current_user_id)})
    if not user:
        return jsonify({"msg": "User not found"}), 404

    secret = pyotp.random_base32()
    user_collection.update_one({"_id": ObjectId(current_user_id)}, {"$set": {"2fa_secret": secret}})

    # Generate OTP and send it via email
    otp = pyotp.TOTP(secret).now()
    message = Message('Your 2FA Code', sender='laurali00825@gmail.com', recipients=[user['email']])
    message.body = f'Your One-Time Password for enabling 2FA is: {otp}'
    mail.send(message)

    return jsonify({"msg": "2FA setup initiated. Check your email for the OTP."}), 200

# Additional routes and logic as needed
