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
    account_reference = db.Column(db.String(100))  # sale_id
    transaction_desc = db.Column(db.String(200))
    status = db.Column(db.Enum("pending", "success", "failed", "cancelled", name="mpesa_status"), default="pending", nullable=False)
    result_code = db.Column(db.Integer)
    result_desc = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime)
    
    
    sale = db.relationship("Sale", back_populates="transaction")
    payment = db.relationship("Payment", back_populates="mpesa_transaction")
    
    def __repr__(self):
        return f'<MpesaTransaction {self.transaction_id}>'