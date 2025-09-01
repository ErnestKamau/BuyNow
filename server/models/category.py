from extensions import db
from datetime import datetime, timezone

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')
    
    
    def __repr__(self):
        return f'<Category {self.name}>'