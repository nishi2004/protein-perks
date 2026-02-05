"""
Checkout Routes - Handle checkout flow and order creation.
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.services import cart_service, payment_service
from app.models.order import Order, OrderItem
from app.utils.email_sender import send_order_email


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

COD_CHARGE = 80   # COD Extra Charge


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
                "razorpay_key_id": payment_service.get_razorpay_key_id(),
                "cod_charge": COD_CHARGE
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
                "message": "Cart empty"
            })


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


        # Create Razorpay Order
        razorpay_order = payment_service.create_razorpay_order(
            amount=total,
            receipt=f"order_{email}"
        )


        return JSONResponse({
            "success": True,
            "order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "key_id": payment_service.get_razorpay_key_id()
        })


    except Exception as e:

        return JSONResponse({
            "success": False,
            "message": str(e)
        })


    finally:
        db.close()


# ===============================
# ONLINE PAYMENT SUCCESS
# ===============================

@router.post("/checkout/payment-success")
async def payment_success(request: Request):

    db = SessionLocal()

    try:

        data = await request.json()

        customer = request.session.get("customer_data")
        cart = cart_service.get_cart(request.session)


        if not customer or not cart:
            return JSONResponse({
                "success": False,
                "message": "Session expired"
            })


        total_amount = 0
        order_details = ""


        for item in cart.values():

            subtotal = item["price"] * item["quantity"]
            total_amount += subtotal

            order_details += f"{item['name']} x {item['quantity']} = ₹{subtotal}\n"


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

            razorpay_order_id=data.get("razorpay_order_id"),
            razorpay_payment_id=data.get("razorpay_payment_id"),
            razorpay_signature=data.get("razorpay_signature"),

            payment_status="success",
            order_status="confirmed"
        )


        db.add(order)
        db.commit()
        db.refresh(order)


        # Save Items
        for item in cart.values():

            subtotal = item["price"] * item["quantity"]

            db.add(OrderItem(

                order_id=order.id,

                product_id=item["id"],
                product_name=item["name"],
                product_brand=item["brand"],
                product_weight=item["weight"],
                product_image=item["image"],

                quantity=item["quantity"],
                price_per_unit=item["price"],
                subtotal=subtotal
            ))


        db.commit()


        # Send Email
        send_order_email(f"""
New Online Order - ProteinPerks

Order ID: {order.id}

Customer: {customer['name']}
Phone: {customer['phone']}
Email: {customer['email']}

Total: ₹{total_amount}

Items:
{order_details}
""")


        # Clear Cart
        cart_service.clear_cart(request.session)
        request.session.pop("customer_data", None)


        return JSONResponse({
            "success": True,
            "message": "Order confirmed"
        })


    finally:
        db.close()


# ===============================
# CASH ON DELIVERY
# ===============================

@router.post("/checkout/cod")
async def cod_order(request: Request):

    db = SessionLocal()

    try:

        customer = request.session.get("customer_data")
        cart = cart_service.get_cart(request.session)


        if not customer or not cart:
            return JSONResponse({
                "success": False,
                "message": "Session expired"
            })


        total_amount = COD_CHARGE
        order_details = ""


        for item in cart.values():

            subtotal = item["price"] * item["quantity"]
            total_amount += subtotal

            order_details += f"{item['name']} x {item['quantity']} = ₹{subtotal}\n"


        # Create COD Order
        order = Order(

            customer_name=customer["name"],
            customer_email=customer["email"],
            customer_phone=customer["phone"],

            shipping_address=customer["address"],
            city=customer["city"],
            state=customer["state"],
            pincode=customer["pincode"],

            total_amount=total_amount,

            payment_status="COD",
            order_status="confirmed"
        )


        db.add(order)
        db.commit()
        db.refresh(order)


        # Save Items
        for item in cart.values():

            subtotal = item["price"] * item["quantity"]

            db.add(OrderItem(

                order_id=order.id,

                product_id=item["id"],
                product_name=item["name"],
                product_brand=item["brand"],
                product_weight=item["weight"],
                product_image=item["image"],

                quantity=item["quantity"],
                price_per_unit=item["price"],
                subtotal=subtotal
            ))


        db.commit()


        # Send Email
        send_order_email(f"""
New COD Order - ProteinPerks

Order ID: {order.id}

Customer: {customer['name']}
Phone: {customer['phone']}
Email: {customer['email']}

Total (Including COD ₹{COD_CHARGE}): ₹{total_amount}

Items:
{order_details}
""")


        # Clear Cart
        cart_service.clear_cart(request.session)
        request.session.pop("customer_data", None)


        return JSONResponse({
            "success": True,
            "message": "Your order is confirmed!"
        })


    finally:
        db.close()
