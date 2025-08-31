from extensions import db
from datetime import datetime, timezone, timedelta

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))  # Price at sale time