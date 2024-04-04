import db
from flask import Flask
from controllers.registerController import register_user
from controllers.loginController import login


app = Flask(__name__)


# @app.route('/')
# def flask_mongodb_atlas():
#     return "flask mongodb atlas!"

# #test to insert data to the data base
# @app.route("/test")
# def test():
#     db.db.collection.insert_one({"name": "John"})
#     return "Connected to the data base!"

app.add_url_rule('/register', view_func=register_user, methods=['POST'])
app.add_url_rule('/login', view_func=login, methods=['POST'])

if __name__ == '__main__':
    app.run(port=8000)

