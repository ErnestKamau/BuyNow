from extensions import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    __table_args__ = (
        db.CheckConstraint('quantity > 0', name='valid_quantity'),
        db.CheckConstraint('price >= 0', name='positive_price'),
    )
   
   
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)  # Snapshot of product price at order time
    notes = db.Column(db.String(200))
    
    product =  db.relationship("Product", back_populates="order_items")
    order = db.relationship("Order", back_populates="items")

    @property
    def subtotal(self):
        return self.quantity * self.unit_price
    
    
    def __repr__(self):
        return f'<OrderItem {self.product.name} x {self.quantity}>'