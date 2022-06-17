from sqlalchemy import Column, Integer, String
from server.db import Base


class BaseItem(Base):
    """Base steam service model of item"""
    __abstract__ = True

    id = Column(Integer(), primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
