"""
Quick script to check database connection and view products
"""
import sqlite3

# Connect to the database
conn = sqlite3.connect('protein_perks.db')
cursor = conn.cursor()

# Check products table
cursor.execute('SELECT COUNT(*) FROM products')
total_products = cursor.fetchone()[0]
print(f"✅ Database Connected Successfully!")
print(f"📦 Total products in database: {total_products}\n")

# Show all products
cursor.execute('SELECT id, name, brand, category, price, stock FROM products')
products = cursor.fetchall()

print("=" * 80)
print("CURRENT PRODUCTS IN DATABASE:")
print("=" * 80)

for product in products:
    product_id, name, brand, category, price, stock = product
    print(f"\n{product_id}. {name}")
    print(f"   Brand: {brand}")
    print(f"   Category: {category}")
    print(f"   Price: ₹{price/100:.2f}")
    print(f"   Stock: {stock} units")

# Check orders table
cursor.execute('SELECT COUNT(*) FROM orders')
total_orders = cursor.fetchone()[0]
print(f"\n{'=' * 80}")
print(f"📋 Total orders in database: {total_orders}")

conn.close()
print(f"\n✅ Database check complete!")
