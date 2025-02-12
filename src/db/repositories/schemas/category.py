from datetime import datetime

from db.helpers import BaseModel


class CategoryDB(BaseModel):
    name: str
    account_id: int
    created_at: datetime
