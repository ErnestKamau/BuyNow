from extensions import db
from datetime import datetime, timezone


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))  # Snapshot of product price at order time
    
    product =  db.relationship("Product", back_populates="order_items")