"""
Checkout Routes - Handle checkout flow and order creation
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.services import cart_service, order_service
from app.utils.email_sender import send_order_email


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

COD_CHARGE = 80


# ===============================
# CHECKOUT PAGE
# ===============================

@router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):

    db = SessionLocal()

    try:

        cart_items, total = cart_service.get_cart_items(
            request.session, db
        )

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
                "cod_charge": COD_CHARGE
            }
        )

    finally:
        db.close()


# ===============================
# PLACE ORDER (COD / MANUAL UPI)
# ===============================

@router.post("/checkout/place-order")
async def place_order(request: Request):

    form = await request.form()
    db = SessionLocal()

    try:

        # 1️⃣ Get cart
        cart_items, total = cart_service.get_cart_items(
            request.session, db
        )

        if not cart_items:
            return JSONResponse({
                "success": False,
                "message": "Cart is empty"
            })


        # 2️⃣ Customer data
        customer_data = {
            "name": form.get("name"),
            "email": form.get("email"),
            "phone": form.get("phone"),
            "address": form.get("address"),
            "city": form.get("city"),
            "state": form.get("state"),
            "pincode": form.get("pincode")
        }


        # 3️⃣ Payment Info (COD / Manual)
        payment_info = {
            "order_id": None,
            "payment_id": None,
            "signature": None
        }


        # 4️⃣ Create Order
        order = order_service.create_order(
            db=db,
            customer_data=customer_data,
            cart_items=cart_items,
            payment_info=payment_info
        )


        # 5️⃣ Send Email
        items_text = ""

        for item in cart_items:
            product = item["product"]
            qty = item["quantity"]
            subtotal = item["subtotal"]

            items_text += f"{product.name} x {qty} = ₹{subtotal}\n"


        send_order_email(f"""
New Order - ProteinPerks

Order ID: {order.id}

Customer: {customer_data['name']}
Phone: {customer_data['phone']}
Email: {customer_data['email']}

Total: ₹{order.total_amount}

Items:
{items_text}
""")


        # 6️⃣ Clear Cart
        cart_service.clear_cart(request.session)


        return JSONResponse({
            "success": True,
            "message": "Order placed successfully",
            "order_id": order.id
        })


    except Exception as e:

        return JSONResponse({
            "success": False,
            "message": str(e)
        }, status_code=500)


    finally:
        db.close()
