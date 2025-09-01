from extensions import db
from datetime import datetime, timezone, timedelta

class MpesaTransaction(db.Model):
    __tablename__ = 'mpesa_transactions'
    
    transaction_id = db.Column(db.String(100), primary_key=True)  # M-Pesa transaction ID
    checkout_request_id = db.Column(db.String(100), unique=True)
    merchant_request_id = db.Column(db.String(100))
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=True)  # Link to payment
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    account_reference = db.Column(db.String(100))  # Can store sale_id for reference
    transaction_desc = db.Column(db.String(200))
    status = db.Column(db.Enum("pending", "success", "failed", "cancelled", name="mpesa_status"), default="pending", nullable=False)
    result_code = db.Column(db.Integer)
    result_desc = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime)
    
    
    payment = db.relationship("Payment", back_populates="mpesa_transaction")
    
    @property
    def sale(self):
        """Get the sale this transaction belongs to via payment"""
        return self.payment.sale if self.payment else None
    
    def __repr__(self):
        return f'<MpesaTransaction {self.transaction_id}>'