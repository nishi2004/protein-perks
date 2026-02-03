from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.database import SessionLocal
from app.models.product import Product
from app.services import cart_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ---------------- ALL PRODUCTS ----------------
@router.get("/products", response_class=HTMLResponse)
def all_products(request: Request):

    db = SessionLocal()
    products = db.query(Product).all()
    cart_count = cart_service.get_cart_count(request.session)
    db.close()

    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products, "title": "All Products", "cart_count": cart_count}
    )


# ---------------- PROTEIN ----------------
@router.get("/protein", response_class=HTMLResponse)
def protein(request: Request):
    db = SessionLocal()
    products = db.query(Product).filter(Product.category == "protein").all()
    cart_count = cart_service.get_cart_count(request.session)
    db.close()

    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products, "title": "Protein", "cart_count": cart_count}
    )


# ---------------- OATS ----------------
@router.get("/oats", response_class=HTMLResponse)
def oats(request: Request):
    db = SessionLocal()
    products = db.query(Product).filter(Product.category == "oats").all()
    cart_count = cart_service.get_cart_count(request.session)
    db.close()

    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products, "title": "Oats", "cart_count": cart_count}
    )


# ---------------- MUESLI ----------------
@router.get("/muesli", response_class=HTMLResponse)
def muesli(request: Request):
    db = SessionLocal()
    products = db.query(Product).filter(Product.category == "muesli").all()
    cart_count = cart_service.get_cart_count(request.session)
    db.close()

    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products, "title": "Muesli", "cart_count": cart_count}
    )


# ---------------- PEANUT BUTTER ----------------
@router.get("/peanut", response_class=HTMLResponse)
def peanut_butter(request: Request):
    db = SessionLocal()
    products = db.query(Product).filter(Product.category == "peanut").all()
    cart_count = cart_service.get_cart_count(request.session)
    db.close()

    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products, "title": "Peanut Butter", "cart_count": cart_count}
    )
