"""
Endpoints for managing products:
  POST   /products         -> create a product
  GET    /products          -> list this user's products
  GET    /products/{id}     -> get one product
  PUT    /products/{id}     -> update a product
  DELETE /products/{id}     -> delete a product

Every endpoint here requires the user to be logged in (we use
Depends(get_current_user), the same function we built on Day 1).

Every query is filtered so a user can only see or change THEIR OWN
products. This is done manually and simply, with plain if-statements,
so it's easy to explain in an interview.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_product = Product(
        user_id=current_user.id,
        name=product_data.name,
        category=product_data.category,
        current_stock=product_data.current_stock,
        minimum_stock_level=product_data.minimum_stock_level,
        supplier_lead_time_days=product_data.supplier_lead_time_days,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("", response_model=List[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    products = db.query(Product).filter(Product.user_id == current_user.id).all()
    return products


@router.get("/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    return product


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if product_data.name is not None:
        product.name = product_data.name

    if product_data.category is not None:
        product.category = product_data.category

    if product_data.current_stock is not None:
        product.current_stock = product_data.current_stock

    if product_data.minimum_stock_level is not None:
        product.minimum_stock_level = product_data.minimum_stock_level

    if product_data.supplier_lead_time_days is not None:
        product.supplier_lead_time_days = product_data.supplier_lead_time_days

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if product.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    db.delete(product)
    db.commit()

    return None