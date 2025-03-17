from functools import partial

from aiohttp.web import (
    Response as WebResponse,
    HTTPOk as WebHttpOk,
    HTTPCreated as WebHttpCreated,
    HTTPNotFound as WebHttpNotFound,
    post as web_post,
    get as web_get,
)
from aiohttp.abc import Request
from aiohttp_apispec import docs, headers_schema, json_schema, response_schema

from src.api.handlers.wallet import schemas
from src.applications import (
    AddWalletCommand,
    AddWalletHandler,
    GetWalletQuery,
    GetWalletHandler,
)
from src.db.exceptions import AccountNotFoundException

docs = partial(docs, tags=["Wallet"])


@docs()
@headers_schema(schemas.TelegramUserIdSchema)
@json_schema(schemas.WalletRequestSchema)
async def add_wallet_handler(request: Request) -> WebResponse:
    handler: AddWalletHandler = request.app["add_wallet_handler"]()

    try:
        await handler.handle(
            AddWalletCommand(
                telegram_user_id=request["headers"]["telegram_user_id"],
                name=request["json"]["name"],
                current_amount=request["json"]["current_amount"],
            ),
        )
    except AccountNotFoundException:
        return WebHttpNotFound()

    return WebHttpCreated()


@docs()
@headers_schema(schemas.TelegramUserIdSchema)
@response_schema(schemas.GetWalletResponseSchema(many=True))
async def get_wallet_handler(request: Request) -> WebResponse:
    handler: GetWalletHandler = request.app["get_wallet_handler"]()

    try:
        response = await handler.handle(
            GetWalletQuery(
                telegram_user_id=request["headers"]["telegram_user_id"],
            ),
        )
    except AccountNotFoundException:
        return WebHttpNotFound()

    return WebHttpOk(
        body=schemas.GetWalletResponseSchema(many=True).dumps(response),
        content_type="application/json",
    )


routes = (
    web_post(
        path="/api/v1/wallet/",
        handler=add_wallet_handler,
    ),
    web_get(
        path="/api/v1/wallet/",
        handler=get_wallet_handler,
        allow_head=False,
    ),
)
