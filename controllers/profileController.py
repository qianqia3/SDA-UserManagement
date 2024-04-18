from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import user_collection  # Import your user collection or database interface as needed
from bson import ObjectId

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

    if 'email' in update_data and not '@' in update_data['email']:
        return jsonify({"msg": "Invalid email address"}), 400
    
    update_fields = {}
    if 'email' in update_data:
        update_fields['email'] = update_data['email']
    if 'phone_number' in update_data:
        update_fields['phone_number'] = update_data['phone_number']

    result = user_collection.update_one({"_id": ObjectId(current_user_id)}, {"$set": update_fields})

    if result.matched_count == 0:
        return jsonify({"msg": "User not found"}), 404
    elif result.modified_count == 0:
        return jsonify({"msg": "No changes made to the user profile"}), 304

    return jsonify({"msg": "User profile updated successfully"}), 200


@profile_blueprint.route('profile/<username>', methods=['GET'])
@jwt_required()
def get_user_info(username):
    user_profile = user_collection.find_one({"username": username})

    if user_profile:
        user_profile['_id'] = str(user_profile['_id'])
        user_profile.pop("password", None)
        return jsonify(user_profile), 200
    else:
        return jsonify({"error": "User not found"}), 404