"""
Script to add products to Protein Perks database
Run this script to populate products in your store
"""

from app.core.database import SessionLocal
from app.models.product import Product

# Create a database session
db = SessionLocal()

# Sample products to add
products = [
    # Protein Powders
    Product(
        name="Gold Standard Whey",
        brand="Optimum Nutrition",
        category="protein",
        description="100% Whey Gold Standard Protein - Premium blend for muscle building",
        price=2500,  # Price in rupees
        weight="1kg",
        stock=50,
        image="/static/images/Protein/ON-Gold-Standard.jpg"
    ),
    Product(
        name="MuscleBlaze Whey Isolate",
        brand="Muscle Blaze",
        category="protein",
        description="Fast absorbing whey isolate for quick muscle recovery",
        price=1999,
        weight="1kg",
        stock=75,
        image="/static/images/Protein/Muscle Blaze/muscleblaze-whey.jpg"
    ),
    Product(
        name="Avvatar Whey Protein",
        brand="Avvatar",
        category="protein",
        description="Premium whey protein concentrate with added amino acids",
        price=2299,
        weight="1kg",
        stock=60,
        image="/static/images/Protein/Avvatar/avvatar-whey.jpg"
    ),
    
    # Oats
    Product(
        name="Organic Rolled Oats",
        brand="Nature's Best",
        category="oats",
        description="Pure organic rolled oats - high in fiber and protein",
        price=399,
        weight="500g",
        stock=100,
        image="/static/images/oats/organic-oats.jpg"
    ),
    
    # Muesli
    Product(
        name="Alpha High Protein Muesli",
        brand="Alpha Labzz",
        category="muesli",
        description="",
        price=500,
        weight="1kg",
        stock=20,
        image="app/static/images/Muesli/Alpha.jpg"
    ),

    Product(
        name="Pintola High Protein Muesli",
        brand="Pintola",
        category="muesli",
        description="",
        price=500,
        weight="1kg",
        stock=20,
        image="app/static/images/Muesli/Pintola.jpg"
    ),
    
    # Peanut Butter
    Product(
        name="Natural Peanut Butter",
        brand="Pintola",
        category="peanut",
        description="100% natural peanut butter - no added sugar",
        price=299,
        weight="400g",
        stock=120,
        image="/static/images/Peanut butter/natural-pb.jpg"
    ),
]

try:
    # Add all products to database
    db.add_all(products)
    db.commit()
    print(f"✅ Successfully added {len(products)} products to the database!")
    
    # Display added products
    all_products = db.query(Product).all()
    print(f"\n📦 Total products in database: {len(all_products)}")
    print("\nProducts added:")
    for product in products:
        print(f"  ✓ {product.name} - ₹{product.price}")
        
except Exception as e:
    print(f"❌ Error adding products: {e}")
    db.rollback()
finally:
    db.close()
