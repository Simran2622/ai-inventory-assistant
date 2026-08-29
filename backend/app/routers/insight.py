"""
Endpoint:
  GET /products/{product_id}/insight

This is the endpoint that ties everything from Day 4 together:
  1. Fetch the product and its sales history
  2. Calculate average daily sales, trend, and predicted demand
     (using forecasting.py - pure Python math)
  3. Send those calculated numbers to the AI to get a written
     recommendation (using recommendation.py)
  4. Return everything together in one response
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.models.sale import Sale
from app.models.user import User
from app.schemas.insight import ProductInsight
from app.auth.dependencies import get_current_user
from app.services.forecasting import (
    calculate_average_daily_sales,
    calculate_trend,
    predict_demand_over_lead_time,
)
from app.services.recommendation import generate_recommendation

router = APIRouter(prefix="/products/{product_id}/insight", tags=["insight"])


@router.get("", response_model=ProductInsight)
def get_product_insight(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Step 1: confirm the product exists and belongs to this user.
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    # Step 2: fetch this product's sales history, oldest first
    # (forecasting.py's trend calculation expects oldest -> newest order).
    sales = (
        db.query(Sale)
        .filter(Sale.product_id == product_id)
        .order_by(Sale.sale_date.asc())
        .all()
    )

    # Step 3: run the prediction math (pure Python, no AI).
    average_daily_sales = calculate_average_daily_sales(sales)
    trend = calculate_trend(sales)
    predicted_demand = predict_demand_over_lead_time(
        average_daily_sales, product.supplier_lead_time_days
    )

    is_low_stock = product.current_stock < predicted_demand

    # Step 4: ask the AI to explain these numbers in plain English.
    ai_recommendation = generate_recommendation(
        product_name=product.name,
        current_stock=product.current_stock,
        average_daily_sales=average_daily_sales,
        predicted_demand=predicted_demand,
        lead_time_days=product.supplier_lead_time_days,
        trend=trend,
    )

    # Step 5: return everything together.
    return ProductInsight(
        product_id=product.id,
        product_name=product.name,
        current_stock=product.current_stock,
        supplier_lead_time_days=product.supplier_lead_time_days,
        average_daily_sales=average_daily_sales,
        trend=trend,
        predicted_demand=predicted_demand,
        is_low_stock=is_low_stock,
        ai_recommendation=ai_recommendation,
    )