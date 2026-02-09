"""
Checkout Routes - Handle checkout flow and order creation
"""

from fastapi import APIRouter, Request
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
# PLACE ORDER (UPI / COD)
# ===============================

@router.post("/checkout/place-order")
async def place_order(request: Request):

    print("🔥 PLACE ORDER API HIT")

    form = await request.form()
    db = SessionLocal()

    try:

        # ================= CART =================

        cart_items, total = cart_service.get_cart_items(
            request.session, db
        )

        print("🛒 CART:", cart_items)

        if not cart_items:
            return {
                "success": False,
                "message": "Cart is empty"
            }


        # ================= CUSTOMER =================

        customer_data = {
            "name": form.get("name"),
            "email": form.get("email"),
            "phone": form.get("phone"),
            "address": form.get("address"),
            "city": form.get("city"),
            "state": form.get("state"),
            "pincode": form.get("pincode")
        }

        print("👤 CUSTOMER:", customer_data)


        # ================= PAYMENT =================

        payment_mode = form.get("payment_mode")   # UPI / COD
        txn_id = form.get("txn_id")


        if payment_mode == "UPI" and not txn_id:
            return {
                "success": False,
                "message": "Transaction ID required for UPI"
            }


        payment_info = {
            "order_id": txn_id if payment_mode == "UPI" else None,
            "payment_id": txn_id if payment_mode == "UPI" else None,
            "signature": None
        }


        # ================= SAVE ORDER =================

        order = order_service.create_order(
            db=db,
            customer_data=customer_data,
            cart_items=cart_items,
            payment_info=payment_info
        )

        print("✅ ORDER SAVED:", order.id)


        # ================= EMAIL =================

        items_text = ""

        for item in cart_items:

            product = item["product"]
            qty = item["quantity"]
            subtotal = item["subtotal"]

            items_text += f"{product.name} x {qty} = ₹{subtotal}\n"


        email_text = f"""
New Order - ProteinPerks

Order ID: {order.id}
Payment Mode: {payment_mode}

Customer: {customer_data['name']}
Phone: {customer_data['phone']}
Email: {customer_data['email']}

Total: ₹{order.total_amount}

Items:
{items_text}
"""


        send_order_email(email_text)

        print("📧 Email Sent")


        # ================= CLEAR CART =================

        cart_service.clear_cart(request.session)

        print("🧹 Cart Cleared")


        return {
            "success": True,
            "order_id": order.id,
            "message": "Order placed successfully"
        }


    except Exception as e:

        print("❌ ORDER ERROR:", e)

        return {
            "success": False,
            "message": "Server Error: " + str(e)
        }


    finally:

        db.close()
