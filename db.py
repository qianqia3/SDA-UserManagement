from flask import Flask
from flask_pymongo import pymongo


CONNECTION_STRING = "mongodb+srv://qianqia3:1orange@sda.oh22dpu.mongodb.net/?retryWrites=true&w=majority&appName=SDA"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database("Users")
user_collection = pymongo.collection.Collection(db, "Users")
profile_collection = pymongo.collection.Collection(db, "Profiles")
