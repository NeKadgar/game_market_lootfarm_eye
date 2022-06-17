from sqlalchemy import select, desc, func
from sqlalchemy.orm import contains_eager
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.dota import CreateDotaItem
from models.dota_item import DotaItem, DotaItemHistory


async def create_item_history(new_item: CreateDotaItem, db_session: AsyncSession):
    dota_item, _ = await DotaItem.get_or_create(new_item.name, db_session=db_session)

    history = DotaItemHistory(
        price=new_item.price,
        count=new_item.count,
        max_count=new_item.max_count,
        site_rate=new_item.site_rate,
        in_trade=new_item.in_trade,
        in_reserve=new_item.in_reserve,
        dota_item_id=dota_item.id
    )
    await history.save(db_session)
    return dota_item.id


async def get_item_latest_info_by_id(item_id: int, db_session: AsyncSession):
    query = select(DotaItem).where(
        DotaItem.id == item_id
    ).join(DotaItem.latest_history).options(contains_eager(DotaItem.latest_history)) \
        .order_by(desc(DotaItemHistory.date)).limit(1)
    result = await db_session.execute(query)
    instance = result.scalar()
    return instance


async def get_item_latest_info_by_name(item_name: str, db_session: AsyncSession):
    query = select(DotaItem).where(
        DotaItem.name == item_name
    ).join(DotaItem.latest_history).options(contains_eager(DotaItem.latest_history)) \
        .order_by(desc(DotaItemHistory.date)).limit(1)
    result = await db_session.execute(query)
    instance = result.scalar()
    return instance


async def get_item_all_info_by_id(item_id: int, db_session: AsyncSession):
    query = select(DotaItem).where(
        DotaItem.id == item_id
    ).join(DotaItem.history).options(contains_eager(DotaItem.history)) \
        .order_by(desc(DotaItemHistory.date))
    result = await db_session.execute(query)
    instance = result.scalar()
    return instance


async def get_item_all_info_by_name(item_name: str, db_session: AsyncSession):
    query = select(DotaItem).where(
        DotaItem.name == item_name
    ).join(DotaItem.history).options(contains_eager(DotaItem.history)) \
        .order_by(desc(DotaItemHistory.date))
    result = await db_session.execute(query)
    instance = result.scalar()
    return instance


async def get_total_items_count(db_session: AsyncSession):
    result = await db_session.execute(func.count(DotaItem.id))
    return result.scalar()


async def get_total_history_items_count(db_session: AsyncSession):
    result = await db_session.execute(func.count(DotaItemHistory.id))
    return result.scalar()


async def get_latest_history_item(db_session: AsyncSession):
    query = select(DotaItemHistory).order_by(desc(DotaItemHistory.date))
    result = await db_session.scalar(query)
    return result
