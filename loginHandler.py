import abc
from flask import request, jsonify, Blueprint
from db import user_collection
from bson import ObjectId
import bcrypt
from flask_jwt_extended import get_jwt
import pyotp
from flask_mail import Message
from mail import mail
from flask_jwt_extended import create_access_token, create_refresh_token

class AbstractHanlder(abc.ABC):
    def __init__(self):
        self._successor = None

    def set_successor(self, successor):
        self._successor = successor
        return self._successor
    
    @abc.abstractmethod
    def handle_request(self, request):
         if self._successor is not None:
            return self._successor.handle_request(request)
        # No successor to handle the request
         else:
            print(f"No successor in {self.__class__.__name__}")
    

class UserExistHanlder(AbstractHanlder):
    def handle_request(self, request):
        username = request.json.get('username', None)
        user = user_collection.find_one({"username": username})
        if not user:
            return jsonify({"msg": "User not found"}), 404
        request.user = user
        return super().handle_request(request)
    
class PwdValidationHanlder(AbstractHanlder):
    def handle_request(self, request):
        password = request.json.get('password', None).encode('utf-8')
        user = request.user
        stored_hashed_pwd = user['password']
        if not bcrypt.checkpw(password, stored_hashed_pwd):
            return jsonify({"error": "Invalid username or password"}), 401
        return super().handle_request(request)
    
class TwoFactorAuthHanlder(AbstractHanlder):
    @staticmethod
    def send_email(recipient, otp):
        subject = "Your OTP for 2FA Login"
        sender = "no-reply@example.com"  # Your sender email
        recipients = [recipient]
        body = f"Your OTP is: {otp}"
        
        message = Message(subject, sender=sender, recipients=recipients)
        message.body = body
        mail.send(message)

    def handle_request(self, request):
        user = request.user
        if user.get('2fa_enabled'):
            secret = pyotp.random_base32()
            otp = pyotp.TOTP(secret).now()
            print(user)
            user_collection.update_one(
                {"username": user['username']},
                {"$set": {"2fa_secret":otp}}
            )
            self.send_email(user['email'], otp)
            partial_token = create_refresh_token(identity=str(user['_id']))
            return jsonify({"msg": "2FA token required", "2fa_required": True, "partial_token": partial_token}), 200
        else:
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify(access_token=access_token, username=user['username']), 200

chain_root = UserExistHanlder()
chain_root.set_successor(PwdValidationHanlder()).set_successor(TwoFactorAuthHanlder())