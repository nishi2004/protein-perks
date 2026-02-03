from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.routes.cart import router as cart_router
from app.routes.home import router as home_router
from app.routes.products import router as products_router
from app.routes.checkout import router as checkout_router
from app.routes.payment import router as payment_router
from app.core.database import init_db


app = FastAPI(title="Protein Perks - Premium Supplements Store")

# Session middleware for cart management
app.add_middleware(SessionMiddleware, secret_key="proteinperks_secret_key_2024")

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(home_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(payment_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    print("🚀 Starting Protein Perks...")
    init_db()
    print("✅ Application ready!")




