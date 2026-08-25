"""
Schemas for the Sale feature — describes what data comes IN from the
frontend, and what shape goes OUT in responses.
"""

from pydantic import BaseModel, Field
from datetime import date, datetime


class SaleCreate(BaseModel):
    quantity_sold: int = Field(gt=0)
    sale_date: date


class SaleOut(BaseModel):
    id: int
    product_id: int
    quantity_sold: int
    sale_date: date
    created_at: datetime

    class Config:
        from_attributes = True