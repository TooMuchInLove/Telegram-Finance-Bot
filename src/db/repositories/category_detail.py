from db.db import DbContext
from .schemas import CategoryDetailDB


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

    # async def delete_category(self, name: str, account_id: int) -> None:
    #     query = (
    #         "DELETE FROM category c "
    #         "WHERE c.account_id = $1 AND c.name = $2;"
    #     )
    #
    #     async with self._db_context.get_connection() as connection:
    #         await connection.execute(query, account_id, name)
    #
    # async def get_categories_by_account_id(self, account_id: int) -> list[CategoryDB]:
    #     query = (
    #         "SELECT c.* "
    #         "FROM category c "
    #         "WHERE c.account_id = $1;"
    #     )
    #
    #     async with self._db_context.get_connection() as connection:
    #         rows = await connection.fetch(query, account_id)
    #
    #     if not rows:
    #         return []
    #
    #     return CategoryDB.parse_list(rows)
