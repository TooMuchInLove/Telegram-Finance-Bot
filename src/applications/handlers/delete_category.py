from src.db.exceptions import AccountNotFoundException
from src.db.helpers import BaseModel
from src.db.repositories import AccountRepository, CategoryRepository
from src.db.db import DbContext


class DeleteCategoryCommand(BaseModel):
    telegram_user_id: int
    name: str


class DeleteCategoryHandler:
    def __init__(
        self,
        db_context: DbContext,
        account_repository: AccountRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._db_context = db_context
        self._account_repository = account_repository
        self._category_repository = category_repository

    async def handle(self, commands: DeleteCategoryCommand) -> None:
        account = await self._account_repository.get_account_by_telegram_user_id(
            telegram_user_id=commands.telegram_user_id,
        )
        if account is None:
            raise AccountNotFoundException()

        await self._category_repository.delete_category(
            name=commands.name,
            account_id=account.id,
        )
