import db
from flask import Flask
from controllers.registerController import register_user
from controllers.loginController import login_blueprint
from flask_jwt_extended import JWTManager, create_access_token

def create_app():
    app = Flask(__name__)

    app.register_blueprint(login_blueprint, url_prefix='/')
    app.add_url_rule('/register', view_func=register_user, methods=['POST'])

    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'
    JWTManager(app)

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
    app.run(port=8000)

