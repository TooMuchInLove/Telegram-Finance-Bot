from db.db import DbContext
from src.db.repositories.schemas import WalletDB


class WalletRepository:
    def __init__(self, db_context: DbContext) -> None:
        self._db_context = db_context

    async def insert_wallet(self, item: WalletDB) -> None:
        query = (
            "INSERT INTO wallet (name, current_amount, account_id, created_at) "
            "VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING;"
        )

        async with self._db_context.get_connection() as connection:
            await connection.execute(
                query,
                item.name,
                item.current_amount,
                item.account_id,
                item.created_at.replace(tzinfo=None)
            )

    async def get_wallets_by_account_id(self, account_id: int) -> list[WalletDB]:
        query = (
            "SELECT w.* "
            "FROM wallet w "
            "WHERE w.account_id = $1;"
        )

        async with self._db_context.get_connection() as connection:
            rows = await connection.fetch(query, account_id)

        if not rows:
            return []

        return WalletDB.parse_list(rows)
