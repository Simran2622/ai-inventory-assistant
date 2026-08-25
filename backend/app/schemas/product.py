"""
Schemas for the Product feature — same idea as user schemas from Day 1:
these describe what shape of data comes IN from the frontend, and what
shape goes OUT in responses. They are separate from the database model.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    current_stock: int = Field(ge=0)
    minimum_stock_level: int = Field(ge=0)
    supplier_lead_time_days: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    current_stock: Optional[int] = Field(default=None, ge=0)
    minimum_stock_level: Optional[int] = Field(default=None, ge=0)
    supplier_lead_time_days: Optional[int] = Field(default=None, ge=0)


class ProductOut(BaseModel):
    id: int
    name: str
    category: Optional[str]
    current_stock: int
    minimum_stock_level: int
    supplier_lead_time_days: int
    created_at: datetime

    class Config:
        from_attributes = True