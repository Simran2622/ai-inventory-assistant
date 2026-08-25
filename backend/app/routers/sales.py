"""
Endpoints for managing sales, always tied to one specific product:
  POST /products/{product_id}/sales   -> record a sale
  GET  /products/{product_id}/sales   -> view sales history for a product

Both endpoints require login, and both check that the product actually
belongs to the logged-in user before doing anything.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product import Product
from app.models.sale import Sale
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleOut
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/products/{product_id}/sales", tags=["sales"])


def get_owned_product(product_id: int, db: Session, current_user: User) -> Product:
    """
    Looks up a product and checks it belongs to the logged-in user.
    Used by both endpoints below.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    return product


@router.post("", response_model=SaleOut, status_code=status.HTTP_201_CREATED)
def record_sale(
    product_id: int,
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_product(product_id, db, current_user)

    new_sale = Sale(
        product_id=product_id,
        quantity_sold=sale_data.quantity_sold,
        sale_date=sale_data.sale_date,
    )

    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)

    return new_sale


@router.get("", response_model=List[SaleOut])
def list_sales(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_product(product_id, db, current_user)

    sales = (
        db.query(Sale)
        .filter(Sale.product_id == product_id)
        .order_by(Sale.sale_date.desc())
        .all()
    )
    return sales