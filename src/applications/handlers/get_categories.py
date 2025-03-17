from datetime import datetime

from db.helpers import BaseModel
from db.repositories import AccountRepository, CategoryRepository
from db.db import DbContext


class GetCategoriesQuery(BaseModel):
    telegram_user_id: int


class CategoryDetail(BaseModel):
    name: str
    created_at: datetime


class Category(BaseModel):
    name: str
    account_id: int
    created_at: datetime
    details: list[CategoryDetail]


class GetCategoriesResponse(BaseModel):
    items: list[Category]


class GetCategoriesHandler:
    def __init__(
        self,
        db_context: DbContext,
        account_repository: AccountRepository,
        category_repository: CategoryRepository,
    ) -> None:
        self._db_context = db_context
        self._account_repository = account_repository
        self._category_repository = category_repository

    async def handle(self, query: GetCategoriesQuery) -> GetCategoriesResponse:
        account = await self._account_repository.get_account_by_telegram_user_id(
            telegram_user_id=query.telegram_user_id,
        )
        if not account:
            return GetCategoriesResponse(items=[])

        categories = await self._category_repository.get_categories_by_account_id(
            account_id=account.id,
        )

        items = {}
        for category in categories:
            if category.name not in items:
                items[category.name] = Category(
                    name=category.name,
                    account_id=account.id,
                    created_at=category.created_at,
                    details=[],
                )
            items[category.name].details.append(
                CategoryDetail(
                    name=category.detail_name,
                    created_at=category.detail_created_at,
                )
            )

        return GetCategoriesResponse(items=list(items.values()))
