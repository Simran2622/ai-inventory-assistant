"""
Schema for the "insight" endpoint - the one that combines the demand
prediction AND the AI-generated recommendation into a single response.

We call it "insight" because it insight combines two things:
  1. Numbers we calculated ourselves (prediction)
  2. A sentence explaining those numbers (AI recommendation)
"""

from pydantic import BaseModel


class ProductInsight(BaseModel):
    product_id: int
    product_name: str

    current_stock: int
    supplier_lead_time_days: int

    average_daily_sales: float
    trend: str
    predicted_demand: float

    is_low_stock: bool

    ai_recommendation: str