from extensions import db
from datetime import datetime, timezone, timedelta


class Sale(db.Model):
    __tablename__ = 'sales'
    __table_args__ = (
        db.CheckConstraint('total_amount >= 0', name='positive_amount'),
    )
   
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, unique=True) #A one-to-one relationship in SQLAlchemy is basically a one-to-many with a unique constraint on the foreign key. Without unique=True, you’d have a one-to-many (multiple Sales could link to one Order).
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum("paid", "partial", "debt", "overdue"), default="debt", nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)  # set if debt/partial
    transaction_id = db.Column(db.String(100), db.ForeignKey("mpesa_transaction.id"))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    order = db.relationship("Order", back_populates="sale")
    transaction = db.relationship("MpesaTransaction", back_populates="sale")
    
    @property
    def paid_amount(self):
        """Sum of all payments linked to the order."""
        return sum(p.amount for p in self.order.payments)

    @property
    def balance(self):
        """Remaining balance."""
        return self.total_amount - self.paid_amount

    def update_status(self):
        """Automatically adjust status based on payments + due_date."""
        if self.paid_amount >= self.total_amount:
            self.payment_status = "paid"
        elif self.due_date and datetime.now(timezone.utc) > self.due_date:
            self.payment_status = "overdue"
        elif self.paid_amount > 0:
            self.payment_status = "partial"
        else:
            self.payment_status = "debt"

    def set_as_debt(self):
        """Mark sale as debt with 7-day deadline."""
        self.payment_status = "debt"
        self.due_date = datetime.now(timezone.utc) + timedelta(days=7)

    def is_near_due(self):
        if self.payment_status in ("debt", "partial") and self.due_date:
            return (self.due_date - datetime.now(timezone.utc)).days <= 2
        return False