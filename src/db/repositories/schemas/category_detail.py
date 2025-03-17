from datetime import datetime

from db.helpers import BaseModel


class CategoryDetailDB(BaseModel):
    name: str
    category_name: str
    account_id: int
    created_at: datetime
