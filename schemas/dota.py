from typing import Optional
from pydantic import BaseModel


class CreateDotaItem(BaseModel):
    name: str
    price: int
    count: Optional[int]
    max_count: Optional[int]
    site_rate: Optional[int]
    in_trade: Optional[int]
    in_reserve: Optional[int]
