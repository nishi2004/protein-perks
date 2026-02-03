"""
Cart Routes - Handle shopping cart operations.
Provides both page rendering and JSON API endpoints.
"""
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.services import cart_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.post("/cart/add")
async def add_to_cart_api(request: Request, product_id: int = Form(...), quantity: int = Form(1)):
    """
    API endpoint to add product to cart.
    Returns JSON response for AJAX calls.
    """
    try:
        cart_service.add_to_cart(request.session, product_id, quantity)
        cart_count = cart_service.get_cart_count(request.session)
        
        return JSONResponse({
            "success": True,
            "message": "Product added to cart",
            "cart_count": cart_count
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": str(e)
        }, status_code=400)


@router.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request):
    """
    Display shopping cart page with all items.
    """
    db = SessionLocal()
    try:
        cart_items, total = cart_service.get_cart_items(request.session, db)
        cart_count = cart_service.get_cart_count(request.session)
        
        return templates.TemplateResponse(
            "cart.html",
            {
                "request": request,
                "cart_items": cart_items,
                "total": total,
                "cart_count": cart_count
            }
        )
    finally:
        db.close()


@router.post("/cart/update")
async def update_cart_quantity(request: Request, product_id: int = Form(...), quantity: int = Form(...)):
    """
    Update quantity of a product in cart.
    """
    try:
        cart_service.update_quantity(request.session, product_id, quantity)
        
        # Recalculate totals
        db = SessionLocal()
        try:
            cart_items, total = cart_service.get_cart_items(request.session, db)
            cart_count = cart_service.get_cart_count(request.session)
            
            return JSONResponse({
                "success": True,
                "message": "Cart updated",
                "total": total,
                "cart_count": cart_count
            })
        finally:
            db.close()
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": str(e)
        }, status_code=400)


@router.post("/cart/remove")
async def remove_from_cart_api(request: Request, product_id: int = Form(...)):
    """
    Remove a product from cart.
    """
    try:
        cart_service.remove_from_cart(request.session, product_id)
        
        # Recalculate totals
        db = SessionLocal()
        try:
            cart_items, total = cart_service.get_cart_items(request.session, db)
            cart_count = cart_service.get_cart_count(request.session)
            
            return JSONResponse({
                "success": True,
                "message": "Product removed from cart",
                "total": total,
                "cart_count": cart_count
            })
        finally:
            db.close()
    except Exception as e:
        return JSONResponse({
            "success": False,
            "message": str(e)
        }, status_code=400)


@router.get("/cart/count")
async def get_cart_count_api(request: Request):
    """
    Get current cart item count.
    """
    cart_count = cart_service.get_cart_count(request.session)
    return JSONResponse({"cart_count": cart_count})

