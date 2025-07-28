from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class WaitingListCreate(BaseModel):
    user_id: int
    representation_id: str
    offer_id: str
    quantity: int

class WaitingListOut(BaseModel):
    id: int
    user_id: int
    representation_id: str
    offer_id: str
    quantity: int
    timestamp: datetime
    position: Optional[int] = None

    class Config:
        from_attributes = True
