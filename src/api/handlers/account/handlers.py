from aiohttp.web import (
    Response as WebResponse,
    HTTPOk as WebHttpOk,
    post as web_post,
)
from aiohttp.abc import Request
from aiohttp_apispec import docs, json_schema
from functools import partial

from src.api.handlers.account import schemas
from src.applications import AddAccountCommand, AddAccountHandler

docs = partial(docs, tags=["Account"])


@docs()
@json_schema(schemas.SignInRequestSchema)
async def add_account_handler(request: Request) -> WebResponse:
    handler: AddAccountHandler = request.app["add_account_handler"]()

    await handler.handle(
        AddAccountCommand(
            telegram_user_id=request["json"]["telegram_user_id"],
            telegram_username=request["json"]["telegram_username"],
        ),
    )

    return WebHttpOk()


routes = (
    web_post(
        path="/api/v1/account/",
        handler=add_account_handler,
    ),
)
