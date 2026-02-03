"""
Checkout Routes - Handle checkout flow and order creation.
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.services import cart_service, payment_service
from app.models.order import Order, OrderItem


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ===============================
# CHECKOUT PAGE
# ===============================

@router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):

    db = SessionLocal()

    try:
        cart_items, total = cart_service.get_cart_items(request.session, db)

        if not cart_items:
            return RedirectResponse("/cart", status_code=302)

        cart_count = cart_service.get_cart_count(request.session)

        return templates.TemplateResponse(
            "checkout.html",
            {
                "request": request,
                "cart_items": cart_items,
                "total": total,
                "cart_count": cart_count,
                "razorpay_key_id": payment_service.get_razorpay_key_id()
            }
        )

    finally:
        db.close()


# ===============================
# CREATE RAZORPAY ORDER
# ===============================

@router.post("/checkout/create-order")
async def create_checkout_order(
    request: Request,

    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    pincode: str = Form(...)
):

    db = SessionLocal()

    try:
        cart_items, total = cart_service.get_cart_items(request.session, db)

        if not cart_items:
            return JSONResponse({
                "success": False,
                "message": "Cart is empty"
            }, status_code=400)

        # Save customer in session
        request.session["customer_data"] = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "pincode": pincode
        }

        try:
            razorpay_order = payment_service.create_razorpay_order(
                amount=total,
                receipt=f"order_{email}_{int(total)}"
            )

            return JSONResponse({
                "success": True,
                "order_id": razorpay_order["id"],
                "amount": razorpay_order["amount"],
                "currency": razorpay_order["currency"],
                "key_id": payment_service.get_razorpay_key_id()
            })

        except Exception as e:

            return JSONResponse({
                "success": False,
                "message": str(e)
            }, status_code=500)

    finally:
        db.close()


# ===============================
# SAVE ORDER AFTER PAYMENT
# ===============================

@router.post("/checkout/payment-success")
async def payment_success(request: Request):

    db = SessionLocal()

    try:
        data = await request.json()

        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_signature = data.get("razorpay_signature")

        # Get customer info
        customer = request.session.get("customer_data")

        if not customer:
            return JSONResponse({
                "success": False,
                "message": "Customer data missing"
            }, status_code=400)

        # Get cart
        cart = cart_service.get_cart(request.session)

        if not cart:
            return JSONResponse({
                "success": False,
                "message": "Cart empty"
            }, status_code=400)

        # Calculate total
        total_amount = 0

        for item in cart.values():
            total_amount += item["price"] * item["quantity"]

        # Create Order
        order = Order(
            customer_name=customer["name"],
            customer_email=customer["email"],
            customer_phone=customer["phone"],
            shipping_address=customer["address"],
            city=customer["city"],
            state=customer["state"],
            pincode=customer["pincode"],

            total_amount=total_amount,

            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,

            payment_status="success",
            order_status="confirmed"
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        # Save items
        for item in cart.values():

            subtotal = item["price"] * item["quantity"]

            order_item = OrderItem(
                order_id=order.id,

                product_id=item["id"],
                product_name=item["name"],
                product_brand=item["brand"],
                product_weight=item["weight"],
                product_image=item["image"],

                quantity=item["quantity"],
                price_per_unit=item["price"],
                subtotal=subtotal
            )

            db.add(order_item)

        db.commit()

        # Clear cart
        cart_service.clear_cart(request.session)
        request.session.pop("customer_data", None)

        return JSONResponse({
            "success": True,
            "message": "Order saved"
        })

    finally:
        db.close()
