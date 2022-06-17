import datetime

from sqlalchemy import Column, Integer, select, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from models.base_item import BaseItem
from server.db import Base


class DotaItem(BaseItem):
    __tablename__ = 'dota_item'

    history = relationship('DotaItemHistory')
    latest_history = relationship('DotaItemHistory', viewonly=True, uselist=False)

    @classmethod
    async def get_or_create(cls, name: str, db_session: AsyncSession):
        get_query = select(DotaItem).where(
            name == name
        )
        result = await db_session.scalar(get_query)

        if result:
            return result, False

        new_instance = cls(
            name=name
        )
        await new_instance.save(db_session)
        return new_instance, True


class DotaItemHistory(Base):
    __tablename__ = 'dota_item_history'

    id = Column(Integer(), primary_key=True)
    price = Column(Integer, default=0)
    count = Column(Integer, default=0)
    max_count = Column(Integer, default=0)
    site_rate = Column(Integer, default=0)
    in_trade = Column(Integer, default=0)
    in_reserve = Column(Integer, default=0)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    dota_item_id = Column(Integer, ForeignKey(DotaItem.id), index=True)
