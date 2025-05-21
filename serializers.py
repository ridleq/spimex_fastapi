from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TradeResultSerializer(BaseModel):
    id: int
    exchange_product_id: Optional[str] = None
    exchange_product_name: Optional[str] = None
    oil_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None
    delivery_basis_name: Optional[str] = None
    delivery_type_id: Optional[str] = None
    volume: Optional[float] = None
    total: Optional[float] = None
    count: Optional[int] = None
    date: Optional[datetime] = None
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None

    model_config = {
        "from_attributes": True
    }
