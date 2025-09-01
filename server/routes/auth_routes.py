from extensions import db
from flask import request
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
            username=username
            phone_number=data['phone_number'],
            role="customer",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        user.password_hash = data['password']
        
        db.session.add(user)
        db.session.commit()
        
        return {"message":"User created successfully"}, 201
    
    
    

    
            
            
            
        
        
            
        