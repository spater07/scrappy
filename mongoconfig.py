from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://bestdeals-master:Admin123Admin123@cluster0.kn2eb.mongodb.net/test?retryWrites=true&w=majority"
mongodb_client = PyMongo(app)
db = mongodb_client.db