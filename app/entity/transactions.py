from sqlalchemy import Column, Integer, ForeignKey, Numeric, TIMESTAMP

from app.entity.base import Base
from datetime import datetime


class Transaction(Base):
    
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    amount = Column(Numeric(20,2), nullable=False)
    currency_type_id = Column(Integer,
                              ForeignKey("currency_types.currency_type_id"),
                              nullable=False)
    status_id = Column(Integer, ForeignKey("transaction_statuses.status_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
