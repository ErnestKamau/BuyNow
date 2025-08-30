from extensions import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    __table_args__ = (
        db.CheckConstraint('quantity > 0', name='valid_quantity'),
        db.CheckConstraint('price >= 0', name='positive_price'),
    )
    
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Snapshot of product price at order time
    
    product =  db.relationship("Product", back_populates="order_items")