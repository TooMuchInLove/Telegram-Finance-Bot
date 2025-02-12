from functools import partial

from aiohttp.web import (
    Response as WebResponse,
    HTTPOk as WebHttpOk,
    HTTPNotFound as WebHttpNotFound,
    post as web_post,
    get as web_get,
)
from aiohttp.abc import Request
from aiohttp_apispec import docs, headers_schema, json_schema, response_schema

from applications import AddCategoryCommand, AddCategoryHandler, GetCategoriesQuery, GetCategoriesHandler
from db.exceptions import AccountNotFoundException

from . import schemas

docs = partial(docs, tags=["Category"])


@docs()
@headers_schema(schemas.TelegramUserIdSchema)
@json_schema(schemas.AddCategoryRequestSchema)
async def add_category_handler(request: Request) -> WebResponse:
    handler: AddCategoryHandler = request.app["add_category_handler"]()

    try:
        await handler.handle(
            AddCategoryCommand(
                telegram_user_id=request["headers"]["telegram_user_id"],
                name=request["json"]["name"],
            ),
        )
    except AccountNotFoundException:
        return WebHttpNotFound()

    return WebHttpOk()


@docs()
@headers_schema(schemas.TelegramUserIdSchema)
@response_schema(schemas.GetCategoriesResponseSchema)
async def get_categories_handler(request: Request) -> WebResponse:
    handler: GetCategoriesHandler = request.app["get_categories_handler"]()

    try:
        response = await handler.handle(
            GetCategoriesQuery(
                telegram_user_id=request["headers"]["telegram_user_id"],
            ),
        )
    except AccountNotFoundException:
        return WebHttpNotFound()

    return WebHttpOk(
        body=schemas.GetCategoriesResponseSchema().dumps(response),
        content_type="application/json",
    )


routes = (
    web_post(
        path="/api/v1/category/",
        handler=add_category_handler,
    ),
    web_get(
        path="/api/v1/category/",
        handler=get_categories_handler,
        allow_head=False,
    ),
)
