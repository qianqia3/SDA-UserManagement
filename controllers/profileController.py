from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import user_collection 
from bson import ObjectId
import pyotp
from mail import mail
from flask_mail import Message
import re

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route('profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()

    print("Current User ID:", current_user_id)

    if not current_user_id:
        return jsonify({"msg": "Missing user identity"}), 400
    
    user_profile = user_collection.find_one({"_id": ObjectId(current_user_id)})
    print(user_profile)

    if not user_profile:
        return jsonify({"msg": "User not found"}), 404

    # Prepare the user profile data to return, excluding sensitive fields like password
    user_data = {
        "username": user_profile.get("username"),
        "email": user_profile.get("email"),
        "phone_number": user_profile.get("phone_number"),
        "friend_id": user_profile.get("friend_id"),
        "2fa_enabled": user_profile.get("2fa_enabled"),
        "2fa_secret": user_profile.get("2fa_secret")
        # Add other fields as needed
    }

    return jsonify(user_data), 200

@profile_blueprint.route('profile', methods=['POST'])
@jwt_required()
def update_profile():
    current_user_id = get_jwt_identity()

    if not current_user_id:
        return jsonify({"msg": "Missing user identity"}), 400
    
    update_data = request.json
    user = user_collection.find_one({"_id": ObjectId(current_user_id)})

    if 'email' in update_data and not '@' in update_data['email']:
        return jsonify({"error": "Invalid email address."}), 400
    
    update_fields = {}
    if 'email' in update_data:
        update_fields['email'] = update_data['email']
    if 'phone_number' in update_data:
        phone_number = update_data['phone_number']
        # Check if phone_number is exactly 10 digits long
        if not re.match(r'^\d{10}$', phone_number):
            return jsonify({"error": "Invalid phone number."}), 400
        update_fields['phone_number'] = phone_number

    if '2fa_enabled' in update_data:
        if update_data['2fa_enabled']:
            # If enabling 2FA, generate the secret and send the email
            secret = pyotp.random_base32()
            otp = pyotp.TOTP(secret).now()
            user_collection.update_one(
                {"_id": ObjectId(current_user_id)},
                {"$set": {"2fa_secret":otp}}
            )

            print("2FA Secret:", user.get('2fa_secret'))
            send_email(
                subject='Your 2FA Code',
                sender='laurali00825@gmail.com',
                recipients=[user['email']],
                body=f'Your One-Time Password for enabling 2FA is: {otp}'
            )
            return jsonify({"msg": "2FA setup initiated. Check your email for the OTP."}), 200
        else:
            update_fields['2fa_enabled'] = False
            update_fields['2fa_secret'] = None
            user_collection.update_one({"_id": ObjectId(current_user_id)}, {"$set": {"2fa_enabled": False, "2fa_secret": None}})
            return jsonify({"msg": "2FA disabled"}), 200

    result = user_collection.update_one({"_id": ObjectId(current_user_id)}, {"$set": update_fields})

    if result.matched_count == 0:
        return jsonify({"msg": "User not found"}), 404
    elif result.modified_count == 0:
        return jsonify({"msg": "No changes made to the user profile"}), 304

    return jsonify({"msg": "User profile updated successfully"}), 200

def send_email(subject, sender, recipients, body):
    message = Message(subject, sender=sender, recipients=recipients)
    message.body = body
    mail.send(message)


@profile_blueprint.route('profile/avg-payback-time', methods=['POST'])
@jwt_required()
def update_user_avg_payback_time():
    data = request.get_json()
    print('data+',data)
    username = data.get('username')
    avg_payback_time = data.get('avg_payback_time')

    if not username or avg_payback_time is None:
        return jsonify({"error": "Missing username or average payback time"}), 400

    result = user_collection.update_one(
        {"username": username},
        {"$set": {"avg_payback_time": avg_payback_time}}
    )

    return jsonify({"message": "User updated successfully"}), 200
   


@profile_blueprint.route('profile/<username>', methods=['GET'])
# @jwt_required()
def get_user_info(username):
    user_profile = user_collection.find_one({"username": username})

    if user_profile:
        user_profile['_id'] = str(user_profile['_id'])
        user_profile.pop("password", None)
        public_user_data = {
            "username": user_profile.get("username"),
            "email": user_profile.get("email"),
            "phone_number": user_profile.get("phone_number"),
            "friend_id": user_profile.get("friend_id"),
            "avg_payback_time": user_profile.get("avg_payback_time"),
        }
        return jsonify(public_user_data), 200
        # return jsonify(user_profile), 200
    else:
        return jsonify({"error": "User not found"}), 404