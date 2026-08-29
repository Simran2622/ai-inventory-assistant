"""
This file handles the AI part: taking already-calculated numbers and
asking an LLM (Claude, by Anthropic) to turn them into a short, plain
English recommendation.

IMPORTANT: this file does NOT calculate anything itself. It only
formats numbers into a prompt, sends that prompt to the AI, and returns
the AI's written response. All the real math happens in forecasting.py.
"""

import os
import anthropic

# Reads the API key from our .env file (same pattern as DATABASE_URL
# and SECRET_KEY - never hardcoded, never committed to GitHub).
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def generate_recommendation(
    product_name: str,
    current_stock: int,
    average_daily_sales: float,
    predicted_demand: float,
    lead_time_days: int,
    trend: str,
) -> str:
    """
    Sends the calculated numbers to Claude and asks for a short,
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

    # This is the actual API call - sending our prompt to Claude and
    # waiting for a response.
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # The response comes back as a list of "content blocks" - we expect
    # just one block of text, so we grab its .text value.
    recommendation_text = response.content[0].text

    return recommendation_text