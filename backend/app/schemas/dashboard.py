"""
Schema for the dashboard summary response. This one is a bit different
from our other schemas — it's not tied to a single database table,
because a dashboard COMBINES information from both products and sales.
"""

from pydantic import BaseModel
from typing import List
from app.schemas.product import ProductOut


class DashboardSummary(BaseModel):
    total_products: int
    total_stock_units: int
    low_stock_count: int
    low_stock_products: List[ProductOut]