from decimal import Decimal
from datetime import datetime, timezone

from src.db.exceptions import AccountNotFoundException
from src.db.helpers import BaseModel
from src.db.repositories import AccountRepository, WalletDB, WalletRepository
from src.db.db import DbContext


class AddWalletCommand(BaseModel):
    telegram_user_id: int
    name: str
    current_amount: Decimal


class AddWalletHandler:
    def __init__(
        self,
        db_context: DbContext,
        account_repository: AccountRepository,
        wallet_repository: WalletRepository,
    ) -> None:
        self._db_context = db_context
        self._account_repository = account_repository
        self._wallet_repository = wallet_repository

    async def handle(self, commands: AddWalletCommand) -> None:
        current_datetime = datetime.now(tz=timezone.utc)

        account = await self._account_repository.get_account_by_telegram_user_id(
            telegram_user_id=commands.telegram_user_id,
        )
        if account is None:
            raise AccountNotFoundException()

        await self._wallet_repository.insert_wallet(
            item=WalletDB(
                name=commands.name,
                current_amount=commands.current_amount,
                account_id=account.id,
                created_at=current_datetime,
            ),
        )
