from flask import Flask, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from ma import ma
from resources import UserRegistration, UserLogin

import os

app = Flask(__name__)
api = Api(app)
flask_bcrypt = Bcrypt(app)

# SQL Alchemy Settings
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTION'] = True

# Authentication
app.secret_key = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

@app.before_first_request
def create_tables():
  db.create_all()

api.add_resource(UserRegistration, '/register', endpoint = 'UserRegistration')
api.add_resource(UserLogin, '/login', endpoint = 'UserLogin')

if __name__ == '__main__':
  from db import db
  
  db.init_app(app)
  ma.init_app(app)
  app.run(debug=True, port=5000)