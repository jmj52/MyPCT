from flask import Flask
from flask_pymongo import PyMongo
import certifi as cert

from website.extensions import mongo

def create_app():

    app = Flask(__name__)
    #app.config['SECRET_KEY'] = 'asdf'
    
    tlsCAFile = cert.where()
    app.config['MONGO_URI'] = f'mongodb+srv://joshua:joshuajoshua@cluster0.cgmpycw.mongodb.net/test?retryWrites=true&w=majority&ssl=true&tlsCAFile={tlsCAFile}'
    #app.config["MONGO_URI"] = "mongodb+srv://kenzie:kenziekenzie@cluster0.cgmpycw.mongodb.net/test"
    #mongo.init_app(app, tlsCAFile=certifi.where())
    mongo.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    return app

