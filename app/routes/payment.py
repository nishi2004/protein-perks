"""
Payment Routes - Handle payment verification and order completion.
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.services import cart_service, payment_service, order_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/payment/verify")
async def verify_payment(
    request: Request,
    razorpay_order_id: str = Form(...),
    razorpay_payment_id: str = Form(...),
    razorpay_signature: str = Form(...)
):
    """
    Verify Razorpay payment and create order in database.
    """
    db = SessionLocal()
    try:
        # Verify payment signature
        is_valid = payment_service.verify_payment_signature(
            razorpay_order_id,
            razorpay_payment_id,
            razorpay_signature
        )
        
        if not is_valid:
            return JSONResponse({
                "success": False,
                "message": "Payment verification failed"
            }, status_code=400)
        
        # Get customer data from session
        customer_data = request.session.get("customer_data")
        if not customer_data:
            return JSONResponse({
                "success": False,
                "message": "Customer data not found"
            }, status_code=400)
        
        # Get cart items
        cart_items, total = cart_service.get_cart_items(request.session, db)
        
        if not cart_items:
            return JSONResponse({
                "success": False,
                "message": "Cart is empty"
            }, status_code=400)
        
        # Create order in database
        payment_info = {
            "order_id": razorpay_order_id,
            "payment_id": razorpay_payment_id,
            "signature": razorpay_signature
        }
        
        order = order_service.create_order(
            db=db,
            customer_data=customer_data,
            cart_items=cart_items,
            payment_info=payment_info
        )
        
        # Clear cart after successful order
        cart_service.clear_cart(request.session)
        
        # Clear customer data
        request.session.pop("customer_data", None)
        
        return JSONResponse({
            "success": True,
            "order_id": order.id,
            "redirect_url": f"/payment/success?order_id={order.id}"
        })
        
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": f"Order creation failed: {str(e)}"
        }, status_code=500)
    finally:
        db.close()


@router.get("/payment/success", response_class=HTMLResponse)
async def payment_success(request: Request, order_id: int):
    """
    Display order confirmation page after successful payment.
    """
    db = SessionLocal()
    try:
        order = order_service.get_order_by_id(db, order_id)
        
        if not order:
            return RedirectResponse("/", status_code=302)
        
        return templates.TemplateResponse(
            "success.html",
            {
                "request": request,
                "order": order,
                "cart_count": 0  # Cart is cleared after order
            }
        )
    finally:
        db.close()


@router.get("/payment/failure", response_class=HTMLResponse)
async def payment_failure(request: Request):
    """
    Display payment failure page.
    """
    return templates.TemplateResponse(
        "failure.html",
        {
            "request": request,
            "cart_count": cart_service.get_cart_count(request.session)
        }
    )
