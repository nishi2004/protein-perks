from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.database import SessionLocal
from app.models.product import Product
from app.services import cart_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Landing page with featured products"""
    db = SessionLocal()
    try:
        # Get featured products (first 4 products)
        featured_products = db.query(Product).limit(4).all()
        cart_count = cart_service.get_cart_count(request.session)
        
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "featured_products": featured_products,
                "cart_count": cart_count
            }
        )
    finally:
        db.close()

