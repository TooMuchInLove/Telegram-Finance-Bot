from datetime import datetime

from src.db.helpers import BaseModel


class CategoryDB(BaseModel):
    name: str
    account_id: int
    created_at: datetime

    detail_name: str | None = None
    detail_created_at: datetime | None = None
