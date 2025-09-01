from extensions import db
from datetime import datetime, timezone, timedelta

class SaleItem(db.Model):
    __tablename__ = 'sale_items'
    __table_args__ = (
        db.CheckConstraint('quantity > 0', name='valid_quantity'),
        db.CheckConstraint('unit_price >= 0 AND cost_price >= 0', name='positive_prices'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric(10, 2))  # Price at sale time
    
    sale = db.relationship("Sale", back_populates="items")
    product = db.relationship("Product", back_populates="sale_items")
    
    @property
    def subtotal(self):
        """Calculate line total (revenue)."""
        return self.quantity * self.unit_price
    
    def __repr__(self):
        return f'<SaleItem {self.product.name} x {self.quantity}>'