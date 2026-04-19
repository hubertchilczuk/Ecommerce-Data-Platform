"""Pydantic schemas for e-commerce events."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    VIEW = "view"
    CART = "cart"
    PURCHASE = "purchase"


class Product(BaseModel):
    product_id: str
    category: str
    price: float = Field(ge=0)


class Event(BaseModel):
    event_id: str
    event_type: EventType
    event_time: datetime
    user_id: str
    session_id: str
    product: Product
    quantity: int = Field(default=1, ge=1)
    revenue: Optional[float] = Field(default=None, ge=0)
