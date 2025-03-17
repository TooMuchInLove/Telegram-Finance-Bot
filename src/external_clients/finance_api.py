from src.external_clients.base_client import ApiClient

ResponseType = str | list | dict | dict[str, list]


class FinanceApiClient(ApiClient):
    def __init__(self, api_url: str) -> None:
        super().__init__(base_url=api_url, raise_for_status=True)

    async def add_account(
        self,
        user_id: int,
        user_name: str,
    ) -> ResponseType:
        return await self._post(
            path="api/v1/account/",
            telegramUserId=user_id,
            telegramUsername=user_name,
        )

    async def add_category(
        self,
        user_id: int,
        category_name: str,
    ) -> ResponseType:
        return await self._post(
            path="api/v1/category/",
            headers={"telegramUserId": f"{user_id}"},
            name=category_name,
        )

    async def delete_category(
        self,
        user_id: int,
        category_name: str,
    ) -> ResponseType:
        return await self._delete(
            path="api/v1/category/",
            headers={"telegramUserId": f"{user_id}"},
            name=category_name,
        )

    async def get_category(
        self,
        user_id: int,
    ) -> ResponseType:
        return await self._get(
            path="api/v1/category/",
            headers={"telegramUserId": f"{user_id}"},
        )
