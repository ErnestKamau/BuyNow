from flask import Flask, make_response
from flask_restful import Api, Resource
from flask_migrate import Migrate
from config import Config
from extensions import db, ma, jwt, bcrypt, cors

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
ma.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
cors.init_app(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
api = Api(app)
migrate = Migrate(app, db)

import models


class Home(Resource):
    
    def get(self):
        return ("Welcome to study-compass Api")
    

api.add_resource(Home, "/", endpoint='home' )