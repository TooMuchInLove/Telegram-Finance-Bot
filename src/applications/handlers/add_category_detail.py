from datetime import datetime, timezone

from db.exceptions import AccountNotFoundException
from db.helpers import BaseModel
from db.repositories import AccountRepository, CategoryDetailDB, CategoryDetailRepository
from db.db import DbContext


class AddCategoryDetailCommand(BaseModel):
    telegram_user_id: int
    name: str
    category_name: str


class AddCategoryDetailHandler:
    def __init__(
        self,
        db_context: DbContext,
        account_repository: AccountRepository,
        category_detail_repository: CategoryDetailRepository,
    ) -> None:
        self._db_context = db_context
        self._account_repository = account_repository
        self._category_detail_repository = category_detail_repository

    async def handle(self, commands: AddCategoryDetailCommand) -> None:
        current_datetime = datetime.now(tz=timezone.utc)

        account = await self._account_repository.get_account_by_telegram_user_id(
            telegram_user_id=commands.telegram_user_id,
        )
        if account is None:
            raise AccountNotFoundException()

        await self._category_detail_repository.insert_category(
            item=CategoryDetailDB(
                name=commands.name,
                category_name=commands.category_name,
                account_id=account.id,
                created_at=current_datetime,
            ),
        )
