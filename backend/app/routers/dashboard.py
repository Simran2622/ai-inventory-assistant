"""
Endpoint:
  GET /dashboard/summary   -> combined overview for the logged-in user

LOW STOCK RULE (kept simple for now):
  A product is "low stock" if its current_stock is less than or equal
  to its minimum_stock_level. Plain comparison, no AI or prediction
  involved yet — that comes in Day 4.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = db.query(Product).filter(Product.user_id == current_user.id).all()

    total_products = len(products)

    total_stock_units = 0
    for product in products:
        total_stock_units = total_stock_units + product.current_stock

    low_stock_products = []
    for product in products:
        if product.current_stock <= product.minimum_stock_level:
            low_stock_products.append(product)

    return DashboardSummary(
        total_products=total_products,
        total_stock_units=total_stock_units,
        low_stock_count=len(low_stock_products),
        low_stock_products=low_stock_products,
    )