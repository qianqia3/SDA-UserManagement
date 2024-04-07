from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import user_collection  # Import your user collection or database interface as needed
from bson import ObjectId

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()

    print("Current User ID:", current_user_id)

    if not current_user_id:
        return jsonify({"msg": "Missing user identity"}), 400
    
    user_profile = user_collection.find_one({"_id": current_user_id})

    if not user_profile:
        return jsonify({"msg": "User not found"}), 404

    # Prepare the user profile data to return, excluding sensitive fields like password
    user_data = {
        "username": user_profile.get("username"),
        "email": user_profile.get("email"),
        "phone_number": user_profile.get("phone_number")
        # Add other fields as needed
    }

    return jsonify(user_data), 200

@profile_blueprint.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    pass