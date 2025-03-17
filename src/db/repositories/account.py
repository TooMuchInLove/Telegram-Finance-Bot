from db.db import DbContext
from src.db.repositories.schemas import AccountDB


class AccountRepository:
    def __init__(self, db_context: DbContext) -> None:
        self._db_context = db_context

    async def insert_account(self, item: AccountDB) -> None:
        query = (
            "INSERT INTO account (telegram_user_id, telegram_username, created_at) "
            "VALUES ($1, $2, $3) ON CONFLICT DO NOTHING;"
        )

        async with self._db_context.get_connection() as connection:
            await connection.execute(
                query,
                item.telegram_user_id,
                item.telegram_username,
                item.created_at.replace(tzinfo=None)
            )

    async def get_account_by_telegram_user_id(self, telegram_user_id: int) -> AccountDB | None:
        query = (
            "SELECT a.* "
            "FROM account a "
            "WHERE a.telegram_user_id = $1;"
        )

        async with self._db_context.get_connection() as connection:
            row = await connection.fetchrow(query, telegram_user_id)

        if not row:
            return None

        return AccountDB.parse_obj(row)
