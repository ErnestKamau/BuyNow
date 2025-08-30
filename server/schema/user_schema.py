from extensions import db, ma
from models import User
from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance=True
        sqla_session = db.session
        exclude = ['_password_hash']
        
    id = ma.auto_field()
    username = ma.auto_field()