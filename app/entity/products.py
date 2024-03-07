from sqlalchemy import Column, String, Integer, UniqueConstraint, ForeignKey, Numeric

from app.entity.base import Base


class Product(Base):
    
    __tablename__ = "products"

    __table_args__ = (
        UniqueConstraint('product_name'),
    )

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), index=True, nullable=False)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    price = Column(Numeric(20,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    currency_type_id = Column(Integer,
                              ForeignKey("currency_types.currency_type_id"),
                              nullable=False)
