# Protein Perks - E-Commerce Platform

A professional e-commerce website for protein supplements and nutrition products built with FastAPI, Jinja2 templates, and Razorpay payment integration.

## Features

✅ **Product Catalog** - Browse protein powders, oats, muesli, and peanut butter  
✅ **Shopping Cart** - Add products with quantity management  
✅ **Checkout Flow** - Customer details form with validation  
✅ **Payment Integration** - Razorpay payment gateway (test mode)  
✅ **Order Management** - Orders saved to database with full details  
✅ **Responsive Design** - Mobile-friendly UI with Tailwind CSS  

## Tech Stack

- **Backend**: Python 3.x, FastAPI
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Templating**: Jinja2
- **Database**: SQLite with SQLAlchemy ORM
- **Payment**: Razorpay (test mode)
- **Session Management**: Starlette SessionMiddleware

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Razorpay API Keys

Edit the `.env` file and add your Razorpay test API keys:

```env
RAZORPAY_KEY_ID=your_razorpay_test_key_id_here
RAZORPAY_KEY_SECRET=your_razorpay_test_key_secret_here
```

Get your test keys from: https://dashboard.razorpay.com/app/keys

### 3. Run the Application

```bash
uvicorn app.main:app --reload --port 8001
```

The database will be automatically initialized with sample products on first run.

### 4. Access the Application

Open your browser and navigate to: **http://localhost:8001**

## Project Structure

```
protein perks/
├── app/
│   ├── core/
│   │   └── database.py          # Database setup + seed data
│   ├── models/
│   │   ├── product.py           # Product model
│   │   └── order.py             # Order & OrderItem models
│   ├── services/
│   │   ├── cart_service.py      # Cart business logic
│   │   ├── order_service.py     # Order management
│   │   └── payment_service.py   # Razorpay integration
│   ├── routes/
│   │   ├── home.py              # Landing page
│   │   ├── products.py          # Product listing
│   │   ├── cart.py              # Cart operations
│   │   ├── checkout.py          # Checkout flow
│   │   └── payment.py           # Payment handling
│   ├── templates/               # Jinja2 HTML templates
│   ├── static/
│   │   ├── css/main.css
│   │   └── js/
│   │       ├── cart.js
│   │       └── checkout.js
│   └── main.py                  # FastAPI app
├── .env                         # Environment variables
├── requirements.txt
└── protein_perks.db            # SQLite database
```

## Testing Payment Flow

Use Razorpay test cards for testing:

- **Card Number**: 4111 1111 1111 1111
- **CVV**: Any 3 digits
- **Expiry**: Any future date

## Features Breakdown

### Cart Management
- Add products to cart with AJAX
- Update quantities without page reload
- Remove items from cart
- Session-based cart persistence

### Checkout Process
1. Customer fills shipping details
2. Order summary displayed
3. Razorpay payment modal opens
4. Payment verification on backend
5. Order saved to database
6. Redirect to success page

### Database Schema
- **Products**: id, name, brand, category, description, price, weight, stock, image
- **Orders**: id, customer details, payment info, status, timestamps
- **OrderItems**: id, order_id, product details snapshot, quantity, subtotal

## API Endpoints

### Pages
- `GET /` - Landing page
- `GET /products` - All products
- `GET /protein` - Protein category
- `GET /cart` - Shopping cart
- `GET /checkout` - Checkout page
- `GET /payment/success` - Order confirmation

### APIs
- `POST /cart/add` - Add to cart
- `POST /cart/update` - Update quantity
- `POST /cart/remove` - Remove item
- `POST /checkout/create-order` - Create Razorpay order
- `POST /payment/verify` - Verify payment

## Notes for Interviews

This project demonstrates:
- ✅ Clean architecture with separation of concerns (routes, services, models)
- ✅ RESTful API design
- ✅ Database modeling and relationships
- ✅ Payment gateway integration
- ✅ Session management
- ✅ Form validation
- ✅ AJAX for better UX
- ✅ Responsive design
- ✅ Production-ready code structure

## Future Enhancements

- User authentication and profiles
- Order tracking
- Email notifications
- Product reviews and ratings
- Admin dashboard
- Inventory management
- Multiple payment methods
- Coupon codes and discounts
