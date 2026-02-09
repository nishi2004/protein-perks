from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Order(Base):
    """
    Order model for storing customer orders.
    Contains customer information, payment details, and order status.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    
    # Customer Information
    customer_name = Column(String(200), nullable=False)
    customer_email = Column(String(200), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    shipping_address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(String(10), nullable=False)
    
    # Order Details
    total_amount = Column(Float, nullable=False)  # Total order amount in rupees
    order_status = Column(String(50), default="pending")  # pending, confirmed, shipped, delivered, cancelled
    

    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order #{self.id} - {self.customer_name} - ₹{self.total_amount}>"


class OrderItem(Base):
    """
    OrderItem model for storing individual products in an order.
    Links products to orders with quantity and price snapshot.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # Product Information (snapshot at time of order)
    product_name = Column(String(200), nullable=False)
    product_brand = Column(String(100), nullable=False)
    product_weight = Column(String(50), nullable=False)
    product_image = Column(String(500), nullable=False)
    
    # Order Item Details
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)  # Price at time of order
    subtotal = Column(Float, nullable=False)  # quantity * price_per_unit
    
    # Relationships
    order = relationship("Order", back_populates="items")
    
    def __repr__(self):
        return f"<OrderItem {self.product_name} x{self.quantity}>"
