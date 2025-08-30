from extensions import db
from datetime import datetime, timezone

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    description = db.Column(db.Text)
    status = db.Column(db.Enum("pending", "paid", "cancelled"), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    user = db.relationship("User", back_populates="orders")
    items = db.relationship("OrderItem", back_populates="order", cascade='all, delete-orphan')
    
    