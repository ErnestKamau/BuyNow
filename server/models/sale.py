from extensions import db
from datetime import datetime, timezone


class Sale(db.Model):
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, unique=True) #A one-to-one relationship in SQLAlchemy is basically a one-to-many with a unique constraint on the foreign key. Without unique=True, you’d have a one-to-many (multiple Sales could link to one Order).
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_id = db.Column(db.String(100), db.ForeignKey("mpesa_transaction.id"))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    order = db.relationship("Order", back_populates="sale")
    transaction = db.relationship("MpesaTransaction", back_populates="sale")