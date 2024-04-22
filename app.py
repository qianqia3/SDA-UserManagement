import db
from flask import Flask
from controllers.registerController import register_blueprint
from controllers.loginController import login_blueprint
from controllers.profileController import profile_blueprint
from controllers.twofaController import two_factor_blueprint
from controllers.verify import verify_2fa_blueprint
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from flask_mail import Mail
from mail import mail

def create_app():
    app = Flask(__name__)

    CORS(app)
    app.register_blueprint(register_blueprint, url_prefix='/')
    app.register_blueprint(login_blueprint, url_prefix='/')
    # profile
    app.register_blueprint(profile_blueprint, url_prefix='/')
    # 2fa
    app.register_blueprint(two_factor_blueprint, url_prefix='/')
    app.register_blueprint(verify_2fa_blueprint, url_prefix='/')


    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'
    JWTManager(app)

    # 2FA mail setup
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'laurali00825@gmail.com'
    app.config['MAIL_PASSWORD'] = 'kaxl kzlm mulx odvx'

    mail.init_app(app)

    return app


# @app.route('/')
# def flask_mongodb_atlas():
#     return "flask mongodb atlas!"

# #test to insert data to the data base
# @app.route("/test")
# def test():
#     db.db.collection.insert_one({"name": "John"})
#     return "Connected to the data base!"

# app.add_url_rule('/register', view_func=register_user, methods=['POST'])
# app.add_url_rule('/login', view_func=login, methods=['POST'])

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)

