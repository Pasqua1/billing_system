from sqlalchemy import Column, String, Integer, UniqueConstraint, ForeignKey, \
    Numeric, CheckConstraint

from app.entity.base import Base


class Customers(Base):
    
    __tablename__= "customers"

    __table_args__ = (
        UniqueConstraint('customer_name'),
    )

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(255), index=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.company_id"))
    balance = Column(Numeric(20,2), CheckConstraint('balance>=0'), nullable=False)
    currency_type_id = Column(Integer, ForeignKey("currency_types.currency_type_id"))
