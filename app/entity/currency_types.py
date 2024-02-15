from sqlalchemy import Column, String, Integer, UniqueConstraint

from app.entity.base import Base


class CurrencyTypes(Base):

    __tablename__ = "currency_types"

    __table_args__ = (
        UniqueConstraint('currency_type_name'),
    )

    currency_type_id = Column(Integer, primary_key=True, autoincrement=True)
    currency_type_name = Column(String(15), index=True, nullable=False)
