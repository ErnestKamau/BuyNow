from extensions import db
from datetime import datetime, timezone, timedelta

class MpesaTransaction(db.Model):
    __tablename__ = 'mpesa_transactions'
    
    transaction_id = db.Column(db.String(100), primary_key=True)  # M-Pesa transaction ID
    checkout_request_id = db.Column(db.String(100), unique=True)
    merchant_request_id = db.Column(db.String(100))
    account_reference = db.Column(db.String(100))  # Your custom reference (like "CONTRIB_123") that appears on the user's M-Pesa SMS - helps users identify what they paid for
    payment_id = db.Column(db.Integer, db.ForeignKey("payments.id"), nullable=False)  # Link to payment
    
    # Transaction Details
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    transaction_desc = db.Column(db.String(200))
    status = db.Column(db.Enum("pending", "success", "failed", "cancelled", name="mpesa_status"), default="pending", nullable=False)
    
    # M-Pesa Response Fields (populated by callback)
    mpesa_receipt_number = db.Column(db.String(200)) # M-Pesa confirmation code
    transaction_date = db.Column(db.DateTime) # When M-Pesa processed it
    result_code = db.Column(db.Integer) # M-Pesa result code (0 = success)
    result_desc = db.Column(db.String(200)) # M-Pesa result description
    
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    
    payment = db.relationship("Payment", back_populates="mpesa_transaction")
    
    @property
    def sale(self):
        """Get the sale this transaction belongs to via payment"""
        return self.payment.sale if self.payment else None
    
    def __repr__(self):
        return f'<MpesaTransaction {self.transaction_id}>'