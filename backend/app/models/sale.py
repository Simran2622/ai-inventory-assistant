"""
This is the Sale model — describes the "sales" table.

Each sale row records: which product was sold, how many units, and on
what date. We link it to a product using a FOREIGN KEY, the same idea
as Day 2's Product -> User link.
"""

from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", backref="sales")