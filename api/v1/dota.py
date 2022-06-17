from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.dota import CreateDotaItem
from repository.dota import create_item_history, get_item_latest_info_by_id, get_item_all_info_by_id, \
    get_item_latest_info_by_name, get_item_all_info_by_name, get_total_items_count, get_total_history_items_count, \
    get_latest_history_item
from server.db import get_db
from background.tasks.parser import parse

router = APIRouter()


@router.get("/info")
async def get_general_info_endpoint(db_session: AsyncSession = Depends(get_db)):
    count = await get_total_items_count(db_session)
    history_count = await get_total_history_items_count(db_session)
    latest_history_item = await get_latest_history_item(db_session)
    parse.delay()
    return {
        "total items": count,
        "total history items": history_count,
        "latest_history": latest_history_item.date
    }


@router.post("/items/add")
async def add_dota_item_endpoint(item: CreateDotaItem, db_session: AsyncSession = Depends(get_db)):
    item_id = await create_item_history(item, db_session=db_session)
    return item_id


@router.get("/items/{item_id}/latest")
async def get_item_by_id_endpoint(item_id: int, db_session: AsyncSession = Depends(get_db)):
    item = await get_item_latest_info_by_id(item_id, db_session=db_session)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {
        "id": item.id,
        "price": item.latest_history.price,
        "date": item.latest_history.date
    }


@router.get("/items/{item_id}/all")
async def get_item_by_id_endpoint(item_id: int, db_session: AsyncSession = Depends(get_db)):
    item = await get_item_all_info_by_id(item_id, db_session=db_session)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {
        "id": item.id,
        "price": item.latest_history.price,
        "date": item.latest_history.date
    }


@router.get("/items/name/{item_name}/latest")
async def get_item_by_id_endpoint(item_name: str, db_session: AsyncSession = Depends(get_db)):
    item = await get_item_latest_info_by_name(item_name, db_session=db_session)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {
        "id": item.id,
        "price": item.latest_history.price,
        "date": item.latest_history.date
    }


@router.get("/items/name/{item_name}/all")
async def get_item_by_id_endpoint(item_name: str, db_session: AsyncSession = Depends(get_db)):
    item = await get_item_all_info_by_name(item_name, db_session=db_session)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return {
        "id": item.id,
        "history": [
            {
                "price": history.price,
                "count": history.count,
                "max_count": history.max_count,
                "site_rate": history.site_rate,
                "in_trade": history.in_trade,
                "in_reserve": history.in_reserve,
                "date": history.date
            } for history in item.history
        ]
    }
