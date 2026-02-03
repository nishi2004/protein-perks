from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Product(Base):
    """
    Product model for storing protein supplement products.
    Represents items available for purchase in the e-commerce store.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # protein, oats, muesli, peanut
    description = Column(Text, nullable=True)  # Product description
    price = Column(Integer, nullable=False)  # Price in rupees
    weight = Column(String(50), nullable=False)  # e.g., "1kg", "500g"
    stock = Column(Integer, default=100)  # Available quantity
    image = Column(String(500), nullable=False)  # Image URL or path
    
    def __repr__(self):
        return f"<Product {self.name} - ₹{self.price}>"
