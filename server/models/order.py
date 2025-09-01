from extensions import db
from datetime import datetime, timezone

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    customer_name = db.Column(db.String(100), nullable=True)
    customer_phone = db.Column(db.String(15), nullable=True)
    description = db.Column(db.Text)
    status = db.Column(db.Enum("paid", "partial" ,"pending", "cancelled", name="order_status"), default="pending", nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    
    items = db.relationship("OrderItem", back_populates="order", cascade='all, delete-orphan')
    payments = db.relationship("Payment", back_populates="order", cascade="all, delete-orphan") #One order can have multiple partial payments.
    user = db.relationship("User", back_populates="orders")
    sale = db.relationship("Sale", back_populates="order", uselist=False, cascade="all, delete-orphan") # One-to-one   uselist=False makes Order.sale return a single object, not a list. 
    
    
    @property
    def total_amount(self):
        """Calculate total order amount."""
        return sum(item.subtotal for item in self.items)
    
    @property
    def total_paid(self):
        """Calculate total amount paid."""
        return sum(payment.amount for payment in self.payments)
    
    @property
    def balance(self):
        """Calculate remaining balance."""
        return self.total_amount - self.total_paid
    
    @property
    def is_fully_paid(self):
        """Check if order is fully paid."""
        return self.balance <= 0
    
    def __repr__(self):
        return f'<Order {self.id} - {self.customer_name}>'