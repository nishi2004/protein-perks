from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./protein_perks.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """
    Initialize database with tables and seed data.
    Creates all tables and populates with realistic product data.
    """
    from app.models.product import Product
    from app.models.order import Order, OrderItem
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Check if products already exist
    db = SessionLocal()
    existing_products = db.query(Product).count()
    
    if existing_products == 0:
        print("Seeding database with products...")
        
        # Professional seed data for protein products
        products = [
            # Whey Protein
            Product(
                name="Gold Standard 100% Whey Protein",
                brand="Optimum Nutrition",
                category="protein",
                description="The world's best-selling whey protein powder. 24g protein per serving with 5.5g BCAAs for muscle recovery and growth.",
                price=4999,
                weight="1kg",
                stock=50,
                image="/static/images/products/on-whey.jpg"
            ),
            Product(
                name="Nitro-Tech Whey Protein",
                brand="MuscleTech",
                category="protein",
                description="Premium whey protein with added creatine and amino acids. 30g protein per serving for superior muscle building.",
                price=3799,
                weight="1kg",
                stock=45,
                image="/static/images/products/muscletech-nitro.jpg"
            ),
            Product(
                name="ISO 100 Hydrolyzed Protein",
                brand="Dymatize",
                category="protein",
                description="Fast-absorbing hydrolyzed whey isolate. 25g protein with zero fat and carbs for lean muscle gains.",
                price=5499,
                weight="900g",
                stock=30,
                image="/static/images/products/dymatize-iso.jpg"
            ),
            Product(
                name="Combat Protein Powder",
                brand="MusclePharm",
                category="protein",
                description="Time-released protein blend with 25g protein from 5 different sources for sustained muscle feeding.",
                price=3299,
                weight="1kg",
                stock=60,
                image="/static/images/products/musclepharm-combat.jpg"
            ),
            
            # Oats
            Product(
                name="Rolled Oats",
                brand="Saffola",
                category="oats",
                description="100% natural whole grain oats. Rich in fiber and protein for sustained energy throughout the day.",
                price=299,
                weight="1kg",
                stock=100,
                image="/static/images/products/saffola-oats.jpg"
            ),
            Product(
                name="Steel Cut Oats",
                brand="Quaker",
                category="oats",
                description="Premium steel-cut oats with a nutty flavor. High in fiber and perfect for a healthy breakfast.",
                price=349,
                weight="1kg",
                stock=80,
                image="/static/images/products/quaker-oats.jpg"
            ),
            
            # Muesli
            Product(
                name="Fruit & Nut Muesli",
                brand="Kellogg's",
                category="muesli",
                description="Crunchy muesli with real fruits, nuts, and whole grains. No added sugar for a healthy start.",
                price=399,
                weight="750g",
                stock=70,
                image="/static/images/products/kelloggs-muesli.jpg"
            ),
            Product(
                name="Protein Muesli",
                brand="Yogabar",
                category="muesli",
                description="High-protein muesli with 20g protein per 100g. Packed with nuts, seeds, and whole grains.",
                price=449,
                weight="500g",
                stock=55,
                image="/static/images/products/yogabar-muesli.jpg"
            ),
            
            # Peanut Butter
            Product(
                name="Crunchy Peanut Butter",
                brand="MyFitness",
                category="peanut",
                description="100% natural peanut butter with no added sugar or oil. 30g protein per 100g for muscle recovery.",
                price=399,
                weight="1kg",
                stock=90,
                image="/static/images/products/myfitness-pb.jpg"
            ),
            Product(
                name="Chocolate Peanut Butter",
                brand="Alpino",
                category="peanut",
                description="Delicious chocolate peanut butter with 25g protein per 100g. Perfect for post-workout snacking.",
                price=449,
                weight="1kg",
                stock=75,
                image="/static/images/products/alpino-choco-pb.jpg"
            ),
            Product(
                name="Organic Peanut Butter",
                brand="Pintola",
                category="peanut",
                description="Certified organic peanut butter made from premium roasted peanuts. High in protein and healthy fats.",
                price=499,
                weight="1kg",
                stock=65,
                image="/static/images/products/pintola-organic-pb.jpg"
            ),
        ]
        
        db.add_all(products)
        db.commit()
        print(f"✅ Added {len(products)} products to database")
    else:
        print(f"Database already contains {existing_products} products")
    
    db.close()
    print("✅ Database initialization complete")


if __name__ == "__main__":
    print("Initializing Protein Perks database...")
    init_db()

