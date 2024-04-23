from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import Blueprint, request, jsonify
from db import user_collection  # Make sure to import your database connection
from bson import ObjectId
import pyotp
from flask_jwt_extended import get_jwt

verify_2fa_blueprint = Blueprint('verify_2fa', __name__)

@verify_2fa_blueprint.route('verify-2fa', methods=['POST'])
@jwt_required()
def verify_otp():
    current_user_id = get_jwt_identity()
    user = user_collection.find_one({"_id": ObjectId(current_user_id)})

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Get the OTP provided by the user
    otp_received = request.json.get('otp')
    if not otp_received:
        return jsonify({"msg": "Missing OTP"}), 400

    # Get the user's 2FA secret from the database
    user_2fa_secret = user.get('2fa_secret')
    if not user_2fa_secret:
        return jsonify({"msg": "2FA is not set up correctly"}), 400

    # Verify the OTP
    print(otp_received)
    print(user)
    # print(user.verify_2fa(str(user['_id']), otp_received))
    if user.get('2fa_secret') == otp_received:
        current_token = get_jwt()
        if current_token.get('type') == 'access':
            user_collection.update_one(
            {"_id": ObjectId(current_user_id)},
            {"$set": {"2fa_enabled": True}}
        )
            return jsonify({"msg": "OTP is correct and 2FA setup is complete"}), 200
        elif current_token.get('type') == 'refresh':
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid OTP"}), 400


@verify_2fa_blueprint.route('verify-2fa-login', methods=['POST'])
@jwt_required(refresh=True)
def verify_otp_login():
    current_user_id = get_jwt_identity()
    user = user_collection.find_one({"_id": ObjectId(current_user_id)})

    if not user:
        return jsonify({"msg": "User not found"}), 404

    # Get the OTP provided by the user
    otp_received = request.json.get('otp')
    if not otp_received:
        return jsonify({"msg": "Missing OTP"}), 400

    # Get the user's 2FA secret from the database
    user_2fa_secret = user.get('2fa_secret')
    if not user_2fa_secret:
        return jsonify({"msg": "2FA is not set up correctly"}), 400

    # Verify the OTP
    print(otp_received)
    print(user)
    # print(user.verify_2fa(str(user['_id']), otp_received))
    if user.get('2fa_secret') == otp_received:
        current_token = get_jwt()
        if current_token.get('type') == 'access':
            user_collection.update_one(
            {"_id": ObjectId(current_user_id)},
            {"$set": {"2fa_enabled": True}}
        )
            return jsonify({"msg": "OTP is correct and 2FA setup is complete"}), 200
        elif current_token.get('type') == 'refresh':
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Invalid OTP"}), 400
