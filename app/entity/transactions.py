from sqlalchemy import Column, Integer, ForeignKey, Numeric, CheckConstraint, TIMESTAMP

from app.entity.base import Base
from datetime import datetime


class Transaction(Base):
    
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, CheckConstraint('quantity>=0'), nullable=False)
    amount = Column(Numeric(20,2), CheckConstraint('price>0'), nullable=False)
    currency_type_id = Column(Integer, ForeignKey("currency_types.currency_type_id"))
    status_id = Column(Integer, ForeignKey("transaction_statuses.status_id"))
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    created_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    updated_at = Column(TIMESTAMP, default=datetime.now(), nullable=False)
