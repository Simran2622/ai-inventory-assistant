"""
This file contains the demand forecasting logic. It is PURE PYTHON MATH -
no AI, no external API calls. Given a list of past sales, it calculates:

  1. Average daily sales
  2. A simple trend (increasing / decreasing / stable)
  3. Predicted demand over the supplier's lead time

This logic lives in its own "service" file (not in a router) because it
is not tied to a web request or a database table - it's just a
calculation that any part of the app could reuse.
"""

from app.models.sale import Sale


def calculate_average_daily_sales(sales: list[Sale]) -> float:
    """
    Adds up all units sold across the given sales records, and divides
    by the number of records to get an average.

    Example: sales of 5, 7, 6, 8, 9 units -> average = 35 / 5 = 7.0
    """
    if len(sales) == 0:
        return 0.0

    total_units_sold = 0
    for sale in sales:
        total_units_sold = total_units_sold + sale.quantity_sold

    average = total_units_sold / len(sales)
    return average


def calculate_trend(sales: list[Sale]) -> str:
    """
    A simple trend check: compares the average of the FIRST half of the
    sales list to the average of the SECOND half.

    Sales are expected to be ordered oldest -> newest when passed in here.

    If the second half's average is clearly higher, we call it "increasing".
    If clearly lower, "decreasing". Otherwise, "stable".
    """
    if len(sales) < 4:
        # Not enough data points to meaningfully split into two halves.
        return "not enough data"

    midpoint = len(sales) // 2
    first_half = sales[:midpoint]
    second_half = sales[midpoint:]

    first_half_avg = calculate_average_daily_sales(first_half)
    second_half_avg = calculate_average_daily_sales(second_half)

    # We use a small threshold (10%) so tiny fluctuations don't get
    # labeled as a "trend" - only a meaningfully different average does.
    if second_half_avg > first_half_avg * 1.1:
        return "increasing"
    elif second_half_avg < first_half_avg * 0.9:
        return "decreasing"
    else:
        return "stable"


def predict_demand_over_lead_time(average_daily_sales: float, lead_time_days: int) -> float:
    """
    Multiplies average daily sales by the number of lead time days,
    to estimate how much will be sold before a new order could arrive.

    Example: 7 units/day average, 7 day lead time -> 49 units predicted.
    """
    predicted_demand = average_daily_sales * lead_time_days
    return predicted_demand