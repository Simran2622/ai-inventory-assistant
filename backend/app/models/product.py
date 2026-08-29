"""
This is the Product model — describes the "products" table.

Notice the "user_id" column: this is a FOREIGN KEY. It stores the id of
the user who owns this product, creating a link between the two tables.
This is what allows us to say "give me only this user's products" later.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key: links this product to a row in the "users" table.
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    category = Column(String, nullable=True)  # optional field

    current_stock = Column(Integer, nullable=False, default=0)
    minimum_stock_level = Column(Integer, nullable=False, default=0)
    supplier_lead_time_days = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", backref="products")
    