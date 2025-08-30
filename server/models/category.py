from extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')
    