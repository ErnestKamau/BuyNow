from extensions import db
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = (
        db.CheckConstraint('sale_price >= 0 AND cost_price >= 0', name='positive_price'),
        db.CheckConstraint('in_stock >= 0', name='positive_stock'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    description = db.Column(db.Text)
    kilograms = db.Column(db.Numeric(5, 2), nullable=True)  # e.g., 0.50(1/2kg), 1.00(1kg), 12.35  kilograms
    sale_price = db.Column(db.Numeric(10, 2), nullable=True) #selling price
    cost_price = db.Column(db.Numeric(10, 2), nullable=True) #buying price
    in_stock = db.Column(db.Integer, default=0)   # Track current stock
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    category = db.relationship("Category", back_populates="products")
    order_items =  db.relationship("OrderItem", back_populates="product", cascade='all, delete-orphan')
    
    