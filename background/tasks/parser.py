import requests
from decimal import Decimal

from sqlalchemy import select
from background.celery_app import app as celery_app
from models.dota_item import DotaItem, DotaItemHistory
from background.celery_app import SQLAlchemyTask


def get_lootfarm_data():
    url = "https://loot.farm/fullpriceDOTA.json"
    res = requests.get(url)
    return res.json()


def get_or_create_dota_item(name: str, db_session):
    query = select(DotaItem).where(
        DotaItem.name == name
    )
    item = db_session.scalar(query)

    if item:
        return item

    item = DotaItem(name=name)
    db_session.add(item)
    return item


@celery_app.task(base=SQLAlchemyTask, queue="lootfarm_queue", bind=True)
def parse(self):
    items: list = get_lootfarm_data()

    for dota_item in items[1:]:
        new_item = get_or_create_dota_item(dota_item.get("name"), self.session)
        item_history = DotaItemHistory(
            price=dota_item.get("price"),
            count=dota_item.get("have"),
            max_count=dota_item.get("max"),
            site_rate=dota_item.get("rate"),
            in_trade=dota_item.get("tr"),
            in_reserve=dota_item.get("res"),
        )
        new_item.history.append(item_history)

        self.session.commit()
        celery_app.send_task(
            name="update_service_price",
            queue="items_base_queue",
            kwargs={
                "game_id": 570,
                "item_hash_name": new_item.name,
                "price": Decimal(item_history.price/100),
                "service": "LOOT.FARM"
            }
        )
    return {
        "success": True,
        "updated": len(items)
    }
