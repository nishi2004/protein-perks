from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from app.core.database import SessionLocal
from app.models.product import Product

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/search", response_class=HTMLResponse, name="search_products")
def search_products(request: Request, q: str = ""):
    db = SessionLocal()

    if q:
        products = db.query(Product).filter(
            or_(
                Product.name.ilike(f"%{q}%"),
                Product.brand.ilike(f"%{q}%")
            )
        ).all()
    else:
        products = []

    db.close()

    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": products,
            "query": q
        }
    )