from db.db import DbContext
from src.db.repositories.schemas import CategoryDetailDB


class CategoryDetailRepository:
    def __init__(self, db_context: DbContext) -> None:
        self._db_context = db_context

    async def insert_category(self, item: CategoryDetailDB) -> None:
        query = (
            "INSERT INTO category_detail (name, category_name, account_id, created_at) "
            "VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING;"
        )

        async with self._db_context.get_connection() as connection:
            await connection.execute(
                query,
                item.name,
                item.category_name,
                item.account_id,
                item.created_at.replace(tzinfo=None)
            )
