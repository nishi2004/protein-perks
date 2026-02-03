"""
Cart Service - Business logic for shopping cart operations.
Handles cart management using session-based storage.
"""
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product


def get_cart_from_session(session: dict) -> Dict[int, int]:
    """
    Get cart from session storage.
    Returns dict with product_id as key and quantity as value.
    """
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


def add_to_cart(session: dict, product_id: int, quantity: int = 1) -> bool:
    """
    Add a product to cart with specified quantity.
    If product already exists, increment quantity.
    
    Args:
        session: Request session object
        product_id: ID of product to add
        quantity: Quantity to add (default: 1)
    
    Returns:
        True if successful
    """
    cart = get_cart_from_session(session)
    
    # Convert to string for JSON serialization
    product_key = str(product_id)
    
    if product_key in cart:
        cart[product_key] += quantity
    else:
        cart[product_key] = quantity
    
    session["cart"] = cart
    return True


def update_quantity(session: dict, product_id: int, quantity: int) -> bool:
    """
    Update quantity of a product in cart.
    
    Args:
        session: Request session object
        product_id: ID of product to update
        quantity: New quantity (must be > 0)
    
    Returns:
        True if successful, False if product not in cart
    """
    cart = get_cart_from_session(session)
    product_key = str(product_id)
    
    if product_key not in cart:
        return False
    
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        del cart[product_key]
    else:
        cart[product_key] = quantity
    
    session["cart"] = cart
    return True


def remove_from_cart(session: dict, product_id: int) -> bool:
    """
    Remove a product from cart completely.
    
    Args:
        session: Request session object
        product_id: ID of product to remove
    
    Returns:
        True if successful, False if product not in cart
    """
    cart = get_cart_from_session(session)
    product_key = str(product_id)
    
    if product_key in cart:
        del cart[product_key]
        session["cart"] = cart
        return True
    
    return False


def get_cart_items(session: dict, db: Session) -> tuple[List[dict], float]:
    """
    Get all cart items with product details and calculate total.
    
    Args:
        session: Request session object
        db: Database session
    
    Returns:
        Tuple of (cart_items_list, total_amount)
        Each cart item is a dict with product details and quantity
    """
    cart = get_cart_from_session(session)
    
    if not cart:
        return [], 0.0
    
    cart_items = []
    total = 0.0
    
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if product:
            subtotal = product.price * quantity
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            total += subtotal
    
    return cart_items, total


def get_cart_count(session: dict) -> int:
    """
    Get total number of items in cart.
    
    Args:
        session: Request session object
    
    Returns:
        Total item count
    """
    cart = get_cart_from_session(session)
    return sum(cart.values())


def clear_cart(session: dict) -> None:
    """
    Clear all items from cart.
    
    Args:
        session: Request session object
    """
    session["cart"] = {}
