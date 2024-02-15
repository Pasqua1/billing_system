from sqlalchemy import Column, String, Integer, UniqueConstraint

from app.entity.base import Base


class Companies(Base):

    __tablename__= "companies"

    __table_args__ = (
        UniqueConstraint('company_name'),
    )

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), index=True, nullable=False)
