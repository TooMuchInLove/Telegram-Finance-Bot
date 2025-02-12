from datetime import datetime, timezone

from db.helpers import BaseModel
from db.repositories import AccountDB, AccountRepository
from db.db import DbContext


class AddAccountCommand(BaseModel):
    telegram_user_id: int
    telegram_username: str | None = None


class AddAccountHandler:
    def __init__(
        self,
        db_context: DbContext,
        account_repository: AccountRepository,
    ) -> None:
        self._db_context = db_context
        self._account_repository = account_repository

    async def handle(self, commands: AddAccountCommand) -> None:
        current_datetime = datetime.now(tz=timezone.utc)

        await self._account_repository.insert_account(
            item=AccountDB(
                telegram_user_id=commands.telegram_user_id,
                telegram_username=commands.telegram_username,
                created_at=current_datetime,
            ),
        )
