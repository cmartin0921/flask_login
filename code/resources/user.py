from flask import request
from flask_restful import Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token

from schemas import UserSchema
from models import UserModel

from cerberus import Validator
from marshmallow import ValidationError

_flask_bcrypt = Bcrypt()

# TODO: move validation into another folder

class UserRegistration(Resource):
  def __init__(self):
    self.user_schema = UserSchema()
    self.validator = Validator({
      'username': {
        'type': 'string',
        'empty': False,
        'minlength': 4 ,
        'maxlength': 30
      },
      'password': {
        'type': 'string',
        'empty': False,
        'minlength': 4,
      },
      'email': {
        'type': 'string',
        'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'empty': False,
        'minlength': 5
      }
    })
    super().__init__
  
  
  def post(self):
    args = request.get_json()
    self.validator.validate(args)
    if len(self.validator.errors) > 0:
      return {
        'error': self.validator.errors
      }, 400
    
    existing_user = UserModel.query.filter_by(username=args.get('username')).first()
    if existing_user:
      return {
        'error': 'Username already taken'
      }, 400
    
    try:
      # Overriding value in dictionary to encrypted password
      args['password'] = _flask_bcrypt.generate_password_hash(password=args.get('password'), rounds=15).decode('utf-8')
      
      new_user = self.user_schema.load(args)
      new_user.save()
    except ValidationError as e:
      return {
        'error': f'{e}'
      }, 400
    except Exception as e:
      return {
        'error': f'{e}'
      }, 500
       
    return {
      'message': 'New user created!',
      'data': self.user_schema.dump(new_user)
      }, 201

class UserLogin(Resource):
  def __init__(self):
    self.user_schema = UserSchema()
    self.validator = Validator({
        'username': {
          'type': 'string',
          'empty': False,
          'minlength': 4
        },
        'password': {
        'type': 'string',
        'empty': False,
        'minlength': 4,
        'maxlength': 30
        }
    })
    super().__init__
    
  def post(self):
    args = request.get_json()
    self.validator.validate(args)
    if len(self.validator.errors) > 0:
      return {
        'error': self.validator.errors
      }, 400
    
    try:
      user = UserModel.query.filter_by(username=args.get('username')).first()
      if not (user and _flask_bcrypt.check_password_hash(user.password, args.get('password'))):
        return {
          'message': 'Invalid credentials. Wrong username/password combination.'
        }, 401
        
      access_token = create_access_token(identity=user.id, fresh=True)
      refresh_token = create_refresh_token(user.id)
    except ValidationError as e:
      return {
        'error': f'{e}'
      }, 400
    except Exception as e:
      return {
        'error': f'{e}'
      }, 500
    
    return {
      'access_token': access_token,
      'refresh_token': refresh_token
    }