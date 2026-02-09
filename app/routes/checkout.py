"""
Checkout Routes - Handle checkout flow and order creation
"""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.services import cart_service, order_service


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
# PLACE ORDER
# ===============================

@router.post("/checkout/place-order")
async def place_order(request: Request):

    print("🔥 PLACE ORDER API HIT")

    form = await request.form()
    print("📨 FORM:", dict(form))

    db = SessionLocal()

    try:

        # Get cart
        cart_items, total = cart_service.get_cart_items(
            request.session, db
        )

        print("🛒 CART:", cart_items)

        if not cart_items:
            return JSONResponse({
                "success": False,
                "message": "Cart is empty"
            })


        # Customer info
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


        # Payment info (manual UPI / COD)
        payment_info = {
            "order_id": None,
            "payment_id": form.get("txn_id"),
            "signature": None
        }


        # Create order in DB
        order = order_service.create_order(
            db=db,
            customer_data=customer_data,
            cart_items=cart_items,
            payment_info=payment_info
        )

        print("✅ ORDER CREATED:", order.id)


        # Clear cart
        cart_service.clear_cart(request.session)


        return JSONResponse({
            "success": True,
            "message": "Order placed successfully",
            "order_id": order.id
        })


    except Exception as e:

        print("❌ ERROR:", e)

        return JSONResponse({
            "success": False,
            "message": str(e)
        }, status_code=500)


    finally:
        db.close()
