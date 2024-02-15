from sqlalchemy import Column, String, Integer, UniqueConstraint

from app.entity.base import Base


class TransactionStatuses(Base):
    
    __tablename__ = "transaction_statuses"

    __table_args__ = (
        UniqueConstraint('status_name'),
    )

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(63), index=True, nullable=False)
