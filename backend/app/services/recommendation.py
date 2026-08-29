"""
This file handles the AI part: taking already-calculated numbers and
asking an LLM (Google's Gemini) to turn them into a short, plain
English recommendation.

IMPORTANT: this file does NOT calculate anything itself. It only
formats numbers into a prompt, sends that prompt to the AI, and returns
the AI's written response. All the real math happens in forecasting.py.
"""

import os
from google import genai

# Reads the API key from our .env file (same pattern as DATABASE_URL
# and SECRET_KEY - never hardcoded, never committed to GitHub).
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_recommendation(
    product_name: str,
    current_stock: int,
    average_daily_sales: float,
    predicted_demand: float,
    lead_time_days: int,
    trend: str,
) -> str:
    """
    Sends the calculated numbers to Gemini and asks for a short,
    plain-English recommendation. The AI is only allowed to explain
    these numbers - it is explicitly told not to invent new numbers.
    """

    # This is the PROMPT - the exact instructions and data we send to
    # the AI. Notice every number here was already calculated by our
    # own code (forecasting.py) - we are not asking the AI to calculate
    # anything itself.
    prompt = f"""You are helping a small business owner understand their inventory situation.

Here is the data for one product:
- Product name: {product_name}
- Current stock: {current_stock} units
- Average daily sales: {average_daily_sales} units/day
- Sales trend: {trend}
- Predicted demand over the next {lead_time_days} days (supplier lead time): {predicted_demand} units

Write a short recommendation (2-3 sentences) telling the business owner
whether they should reorder this product, and roughly how many units,
based ONLY on the numbers above. Do not invent any numbers that are not
given to you above. Keep the tone plain and simple."""

    # This is the actual API call - sending our prompt to Gemini and
    # waiting for a response.
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    recommendation_text = response.text

    return recommendation_text
