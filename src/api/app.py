from loguru import logger
from aiohttp.web import (
    Application as WebApplication,
    run_app as web_run_app,
)
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from aiohttp_cors import (
    ResourceOptions as AiohttpCorsResourceOptions,
    setup as aiohttp_cors_setup,
)

from api.log import RequestLogger
from api.middlewares import suppress_cancelled_error_middleware
from api.routes import routes
from applications import AddAccountHandler, AddCategoryHandler, DeleteCategoryHandler, GetCategoriesHandler
from configs import config_map, setting_base, setting_data_base
from db.repositories import AccountRepository, CategoryRepository
from db.db import DbContext, get_db_pool
from external_clients import FinanceApiClient


async def _setup_db(app: WebApplication) -> None:
    app["db_pool"] = await get_db_pool(
        dsn=app["setting_data_base"].dsn,
        min_size=app["setting_data_base"].POOL_MIN_SIZE,
        max_size=app["setting_data_base"].POOL_MAX_SIZE,
        command_timeout=app["setting_data_base"].COMMAND_TIMEOUT,
    )


async def _setup_di(app: WebApplication) -> None:
    app["finance_api_client"] = FinanceApiClient(
        api_url=app["setting_base"].FINANCE_API_CLIENT_URL,
    )

    def resolve_account_repository(
        db_context: DbContext | None = None,
    ) -> AccountRepository:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return AccountRepository(db_context)

    app["account_repository"] = resolve_account_repository

    def resolve_category_repository(
        db_context: DbContext | None = None,
    ) -> CategoryRepository:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return CategoryRepository(db_context)

    app["category_repository"] = resolve_category_repository

    def resolve_add_account_handler(
        db_context: DbContext | None = None,
    ) -> AddAccountHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return AddAccountHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
        )

    app["add_account_handler"] = resolve_add_account_handler

    def resolve_add_category_handler(
        db_context: DbContext | None = None,
    ) -> AddCategoryHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return AddCategoryHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
            category_repository=app["category_repository"](db_context),
        )

    app["add_category_handler"] = resolve_add_category_handler

    def resolve_delete_category_handler(
        db_context: DbContext | None = None,
    ) -> DeleteCategoryHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return DeleteCategoryHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
            category_repository=app["category_repository"](db_context),
        )

    app["delete_category_handler"] = resolve_delete_category_handler

    def resolve_get_categories_handler(
        db_context: DbContext | None = None,
    ) -> GetCategoriesHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return GetCategoriesHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
            category_repository=app["category_repository"](db_context),
        )

    app["get_categories_handler"] = resolve_get_categories_handler


async def _close_db(app: WebApplication) -> None:
    await app["db_pool"].close()


async def _close_finance_api_client(app: WebApplication) -> None:
    if app.get("finance_api_client"):
        await app["finance_api_client"].close()


def get_app() -> WebApplication:
    app = WebApplication(
        middlewares=[
            suppress_cancelled_error_middleware,
            validation_middleware,
            normalize_path_middleware(),
        ],
    )

    app["setting_base"] = setting_base
    app["setting_data_base"] = setting_data_base
    app.add_routes(routes)

    app.on_startup.extend(
        [
            _setup_db,
            _setup_di,
        ],
    )
    app.on_shutdown.extend(
        [
            _close_db,
            _close_finance_api_client,
        ],
    )

    cors = aiohttp_cors_setup(
        app,
        defaults={
            "*": AiohttpCorsResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods="*",
            ),
        },
    )
    for route in list(app.router.routes()):
        cors.add(route)

    setup_aiohttp_apispec(
        app=app,
        title="Finance API",
        version="v1",
        request_data_name="validated_data",
        url="/api/docs/swagger.json",
        swagger_path="/api/docs/",
        securityDefinitions={
            "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "Authorization"},
        },
    )

    return app


if __name__ == "__main__":
    logger.configure(**config_map)
    logger.info("Starting..")

    web_run_app(
        get_app(),
        port=setting_base.WEB_PORT,
        access_log_class=RequestLogger,
    )
