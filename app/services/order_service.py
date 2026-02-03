"""
Order Service - Business logic for order management.
Handles order creation and retrieval.
"""
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from typing import List, Dict


def create_order(
    db: Session,
    customer_data: dict,
    cart_items: List[dict],
    payment_info: dict
) -> Order:
    """
    Create a new order in the database.
    
    Args:
        db: Database session
        customer_data: Dict with customer details (name, email, phone, address, etc.)
        cart_items: List of cart items with product and quantity
        payment_info: Dict with Razorpay payment details
    
    Returns:
        Created Order object
    """
    # Calculate total amount
    total_amount = sum(item["subtotal"] for item in cart_items)
    
    # Create order
    order = Order(
        customer_name=customer_data["name"],
        customer_email=customer_data["email"],
        customer_phone=customer_data["phone"],
        shipping_address=customer_data["address"],
        city=customer_data["city"],
        state=customer_data["state"],
        pincode=customer_data["pincode"],
        total_amount=total_amount,
        razorpay_order_id=payment_info.get("order_id"),
        razorpay_payment_id=payment_info.get("payment_id"),
        razorpay_signature=payment_info.get("signature"),
        payment_status="success" if payment_info.get("payment_id") else "pending",
        order_status="confirmed" if payment_info.get("payment_id") else "pending"
    )
    
    db.add(order)
    db.flush()  # Get order ID
    
    # Create order items
    for item in cart_items:
        product = item["product"]
        quantity = item["quantity"]
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            product_brand=product.brand,
            product_weight=product.weight,
            product_image=product.image,
            quantity=quantity,
            price_per_unit=product.price,
            subtotal=item["subtotal"]
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(order)
    
    return order


def get_order_by_id(db: Session, order_id: int) -> Order:
    """
    Retrieve an order by ID with all items.
    
    Args:
        db: Database session
        order_id: Order ID
    
    Returns:
        Order object or None if not found
    """
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_email(db: Session, email: str) -> List[Order]:
    """
    Retrieve all orders for a customer email.
    
    Args:
        db: Database session
        email: Customer email
    
    Returns:
        List of Order objects
    """
    return db.query(Order).filter(Order.customer_email == email).order_by(Order.created_at.desc()).all()
