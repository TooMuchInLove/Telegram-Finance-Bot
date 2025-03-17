from functools import partial

from aiohttp.web import (
    Response as WebResponse,
    HTTPOk as WebHttpOk,
    HTTPCreated as WebHttpCreated,
    HTTPNotFound as WebHttpNotFound,
    post as web_post,
    get as web_get,
    delete as web_delete,
)
from aiohttp.abc import Request
from aiohttp_apispec import docs, headers_schema, json_schema, response_schema

from src.api.handlers.category import schemas
from src.applications import (
    AddCategoryCommand,
    AddCategoryHandler,
    AddCategoryDetailCommand,
    AddCategoryDetailHandler,
    DeleteCategoryCommand,
    DeleteCategoryHandler,
    GetCategoriesQuery,
    GetCategoriesHandler,
)
from src.db.exceptions import AccountNotFoundException

docs = partial(docs, tags=["Category"])


@docs()
@headers_schema(schemas.TelegramUserIdSchema)
@json_schema(schemas.CategoryRequestSchema)
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

    return WebHttpCreated()


@docs()
@headers_schema(schemas.TelegramUserIdSchema)
@json_schema(schemas.CategoryRequestSchema)
async def delete_category_handler(request: Request) -> WebResponse:
    handler: DeleteCategoryHandler = request.app["delete_category_handler"]()

    try:
        await handler.handle(
            DeleteCategoryCommand(
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


@docs()
@headers_schema(schemas.TelegramUserIdSchema)
@json_schema(schemas.CategoryRequestSchema)
async def add_category_detail_handler(request: Request) -> WebResponse:
    handler: AddCategoryDetailHandler = request.app["add_category_detail_handler"]()

    try:
        await handler.handle(
            AddCategoryDetailCommand(
                telegram_user_id=request["headers"]["telegram_user_id"],
                name=request["json"]["name"],
            ),
        )
    except AccountNotFoundException:
        return WebHttpNotFound()

    return WebHttpCreated()


routes = (
    web_post(
        path="/api/v1/category/",
        handler=add_category_handler,
    ),
    web_delete(
        path="/api/v1/category/",
        handler=delete_category_handler,
    ),
    web_get(
        path="/api/v1/category/",
        handler=get_categories_handler,
        allow_head=False,
    ),
    web_post(
        path="/api/v1/category/detail/",
        handler=add_category_detail_handler,
    ),
)
