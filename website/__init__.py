from flask import Flask
from flask_pymongo import PyMongo
import certifi

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdf'
    app.config["MONGO_URI"] = "mongodb+srv://kenzie:kenziekenzie@cluster0.cgmpycw.mongodb.net/test"
    mongo.init_app(app, tlsCAFile=certifi.where())

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app

