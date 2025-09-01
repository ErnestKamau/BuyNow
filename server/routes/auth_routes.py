from extensions import db
from flask import request
from flask_jwt_extended import create_access_token,  jwt_required, get_jwt_identity
from flask_restful import Resource
from datetime import datetime, timezone
from models import User


