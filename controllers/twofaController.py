from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from db import user_collection
from mail import mail
from flask_mail import Message
import pyotp
from bson import ObjectId
from model.userModel import User
from flask_jwt_extended import get_jwt

two_factor_blueprint = Blueprint('two', __name__)

@two_factor_blueprint.route('twofa', methods=['POST'])
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

@two_factor_blueprint.route('/verificationtwofa', methods=['POST'])
@jwt_required()
def verify_2fa():
    # Verify the existence of the partial 2FA claim
    current_claims = get_jwt()
    if not current_claims.get('is_2fa_temp_token'):
        return jsonify({"msg": "This endpoint requires a 2FA partial token"}), 401

    # Get the identity of the current user based on the partial 2FA JWT
    current_user_id = get_jwt_identity()

    # Retrieve the user's 2FA secret to verify the OTP provided
    user = user_collection.find_one({"_id": ObjectId(current_user_id)})
    if not user:
        return jsonify({"msg": "User not found"}), 404

    otp_received = request.json.get('otp')
    if not otp_received:
        return jsonify({"msg": "Missing 2FA token"}), 400

    # Verify the 2FA code
    if User.verify_2fa(str(user['_id']), otp_received):
        # If the 2FA code is correct, create a new access token for the user
        access_token = create_access_token(identity=str(user['_id']), additional_claims={"is_2fa_temp_token": False})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid 2FA token"}), 400