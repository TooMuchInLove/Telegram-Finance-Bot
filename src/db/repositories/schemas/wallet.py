from datetime import datetime
from decimal import Decimal

from src.db.helpers import BaseModel


class WalletDB(BaseModel):
    name: str
    current_amount: Decimal
    account_id: int
    created_at: datetime
