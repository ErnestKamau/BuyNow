from models import Order, Sale, SaleItem, MpesaTransaction
from extensions import db
from datetime import datetime, timezone, timedelta


# Helper functions
def create_sale_from_order(order_id, processed_by_user_id=None):
    """Convert order to sale (when customer decides to buy)"""
    order = Order.query.get(order_id)
    if not order:
        return None
    
    # Calculate totals
    total_amount = order.total_amount
    total_cost = sum(item.quantity * item.product.cost_price for item in order.items)
    
    # Create sale
    sale = Sale(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        total_amount=total_amount,
        cost_amount=total_cost,
        profit_amount=total_amount - total_cost,
        processed_by=processed_by_user_id,
        due_date=datetime.now(timezone.utc) + timedelta(days=7)  # 7-day default
    )
    db.session.add(sale)
    db.session.flush()  # Get sale.id
    
    # Create sale items
    for order_item in order.items:
        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=order_item.product_id,
            quantity=order_item.quantity,
            unit_price=order_item.unit_price,
            cost_price=order_item.product.cost_price
        )
        db.session.add(sale_item)
    
    # Update order status
    order.status = 'confirmed'
    
    db.session.commit()
    return sale


def process_mpesa_payment(sale_id, transaction_id, amount):
    """Process M-Pesa payment for a sale"""
    sale = Sale.query.get(sale_id)
    if not sale:
        return None
    
    # Create payment record
    payment = sale.add_payment(
        amount=amount,
        method="mpesa",
        reference=transaction_id
    )
    
    # Update M-Pesa transaction
    mpesa_tx = MpesaTransaction.query.get(transaction_id)
    if mpesa_tx:
        mpesa_tx.payment_id = payment.id
        mpesa_tx.status = "success"
        mpesa_tx.completed_at = datetime.now(timezone.utc)
    
    db.session.commit()
    return payment