from datetime import datetime

from src.db.helpers import BaseModel


class AccountDB(BaseModel):
    id: int | None = None
    telegram_user_id: int | None = None
    telegram_username: str | None = None
    created_at: datetime | None = None
