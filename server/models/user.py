from extensions import db,bcrypt
from datetime import datetime, timezone
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.Integer(10), nullable=False)
    role = db.Column(db.Enum("admin", "customer", "shopkeeper"), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hash may not be viewed.')
    
    @password_hash.setter
    def password_hash(self, password):
        hashed_password=bcrypt.generate_password_hash(password)
        self._password_hash=hashed_password.decode('utf-8')
        
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)
  


