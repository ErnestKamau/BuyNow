from extensions import db
from datetime import datetime, timezone


class Payment(db.Model):
    __tablename__ = "payments"
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    method = db.Column(db.Enum("cash", "mpesa", "card"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_id = db.Column(db.String(100))  # e.g. M-Pesa transaction code
    paid_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    order = db.relationship("Order", back_populates="payments")
