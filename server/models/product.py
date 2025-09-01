from extensions import db
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = (
        db.CheckConstraint('sale_price >= 0', name='positive_sale_price'),
        db.CheckConstraint('cost_price >= 0', name='positive_cost_price'),
        db.CheckConstraint('in_stock >= 0', name='positive_stock'),
        db.CheckConstraint('kilograms > 0', name='positive_weight'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    description = db.Column(db.Text)
    kilograms = db.Column(db.Numeric(8, 3), nullable=True)  # e.g., 0.500 (1/2kg), 1.000 (1kg), 12.350
    sale_price = db.Column(db.Numeric(10, 2), nullable=False) #selling price
    cost_price = db.Column(db.Numeric(10, 2), nullable=False) #buying price
    in_stock = db.Column(db.Integer, default=0) # Current stock level
    minimum_stock = db.Column(db.Integer, default=5)  # Low stock alert threshold
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    category = db.relationship("Category", back_populates="products")
    order_items =  db.relationship("OrderItem", back_populates="product", cascade='all, delete-orphan')
    sale_items = db.relationship("SaleItem", back_populates="product", cascade='all, delete-orphan')
    
    
    @property
    def profit_margin(self):
        """Calculate profit margin percentage."""
        if self.cost_price and self.cost_price > 0:
            return ((self.sale_price - self.cost_price) / self.cost_price) * 100
        return 0
    
    @property
    def is_low_stock(self):
        """Check if product is below minimum stock threshold."""
        return self.in_stock <= self.minimum_stock
    
    def __repr__(self):
        return f'<Product {self.name}>'
    