from extensions import db
from datetime import datetime, timezone, timedelta
from models import Payment


class Sale(db.Model):
    """Primary transaction record - created when order is confirmed"""
    __tablename__ = 'sales'
    __table_args__ = (
        db.CheckConstraint('total_amount >= 0', name='positive_amount'),
    )
  
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, unique=True) #A one-to-one relationship in SQLAlchemy is basically a one-to-many with a unique constraint on the foreign key. Without unique=True, you’d have a one-to-many (multiple Sales could link to one Order).
    sale_number = db.Column(db.String(50), unique=True, nullable=True)  # e.g., SALE-2025-001
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(15), nullable=True)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    cost_amount = db.Column(db.Numeric(10, 2), nullable=False)
    profit_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum("fully-paid", "partial", "debt", "overdue", name="payment_status"), default="debt", nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)  # set if debt/partial
    transaction_id = db.Column(db.String(100), db.ForeignKey("mpesa_transactions.transaction_id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    items = db.relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="sale", cascade="all, delete-orphan")
    order = db.relationship("Order", back_populates="sale")
    transaction = db.relationship("MpesaTransaction", back_populates="sale")
    
    @property
    def total_paid(self):
        """Sum of all payments for this sale"""
        return sum(payment.amount for payment in self.payments)

    @property
    def balance(self):
        """Remaining balance"""
        return self.total_amount - self.total_paid
    
    @property
    def is_fully_paid(self):
        return self.balance <= 0

    def update_payment_status(self):
        """Auto-update status based on payments"""
        total_paid = self.total_paid
        
        if total_paid >= self.total_amount:
            self.payment_status = "paid"
        elif self.due_date and datetime.now(timezone.utc) > self.due_date:
            self.payment_status = "overdue"
        elif total_paid > 0:
            self.payment_status = "partial"
        else:
            self.payment_status = "debt"
        
        self.updated_at = datetime.now(timezone.utc)

        
    def add_payment(self, amount, method="cash", reference=None, notes=None, processed_by=None):
        """Add a payment to this sale"""
        payment = Payment(
            sale_id=self.id,
            amount=amount,
            method=method,
            reference=reference,
            notes=notes
        )
        db.session.add(payment)
        self.update_payment_status()
        return payment
        

    def set_as_debt(self, days=7):
        """Mark sale as debt with 7-day deadline."""
        if self.payment_status in ("debt", "partial") :
            self.due_date = datetime.now(timezone.utc) + timedelta(days=days)

    def is_near_due(self):
        if self.payment_status in ("debt", "partial") and self.due_date:
            return (self.due_date - datetime.now(timezone.utc)).days <= 2
        return False
    
    def __repr__(self):
        return f'<Sale {self.sale_number or self.id}>'