from extensions import db
from flask import request, session
from flask_jwt_extended import create_access_token,  jwt_required, get_jwt_identity
from flask_restful import Resource
from datetime import datetime, timezone
from models import User
import json


class Register(Resource):
    
    def post(self):
        data = request.get_json()
        username = data.get('username')
        
        if not username:
            return {"error":"username cannot be empty!"}
            
        if User.query.filter( User.username==username ).first():
                return {"error":"Username already exists"}, 409
        
        required_fields = ['password', 'phone_number']
        for field in required_fields:
            if not data.get(field):
                return {"error":f"{field} is required!"}, 400
            
        
        user = User(
            username=username,
            phone_number=data['phone_number'],
            role="customer",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        user.password_hash = data['password']
        
        db.session.add(user)
        db.session.commit()
        
        return {"message":"User created successfully"}, 201
    
    
    
class Login(Resource):
    
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        
        if not username or not password:
            return {"error":"Username and Password Required"}
        
        user = User.query.filter_by( username=username ).first()
        
        if user and user.authenticate(password):
            identity = {
                "id" : user.id,
                "username":user.username,
                "role":user.role,
                "last_login":datetime.now(timezone.utc)
            }
            
            token = create_access_token(identity=json.dumps(identity))
            
            return {
                "message": f"successful login {user.username}",
                "token":token,
                "mobile_no":user.phone_number
            }, 200
        
        
        return {'error': 'Invalid credentials'}, 401
    
    
class ChangePassword(Resource):
    #change passsword from settings
    
    @jwt_required
    def post(self):
        current_user = json.loads(get_jwt_identity())
        data = request.get_json()
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return {"error":"Old password and New password are required"}, 400
        
        user = session.query(User).get(current_user['id'])
        
        if not user:
            return {"error":"User not found"}, 404
        
        if not user.authenticate(old_password):
            return {"error":"Invalid old password"}
        
        user.password_hash = new_password
        
        db.session.commit()
        
        return {"message": "Password changed successfully"}, 200
    
    
class ChangePhoneNumber(Resource):
    
    @jwt_required
    def post(self):
        current_user = json.loads(get_jwt_identity())
        data = request.get_json()
        
        new_no = data.get("new phone number")
        new_no = data.get("old phone number")
        
        if current_user:
            
        
        
        
        
            
        
        
        
    
            
            
            
        
        

        