from extensions import db
from datetime import datetime, timezone


class Payment(db.Model):
    __tablename__ = "payments"
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.id"), nullable=False)  # Direct to Sale!
    method = db.Column(db.Enum("cash", "mpesa", "bank_transfer", "card", name="payment_methods"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    reference = db.Column(db.String(100))  # M-Pesa transaction_id
    notes = db.Column(db.Text)
    paid_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    sale = db.relationship("Sale", back_populates="payments")  # Direct to Sale!
    mpesa_transaction = db.relationship("MpesaTransaction", back_populates="payment", uselist=False)
    
    
    
    def __repr__(self):
        return f'<Payment {self.method} - {self.amount}>'
