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

from src.api.log import RequestLogger
from src.api.middlewares import suppress_cancelled_error_middleware
from src.api.routes import routes
from src.applications import (
    AddAccountHandler,
    AddCategoryHandler,
    AddCategoryDetailHandler,
    AddWalletHandler,
    DeleteCategoryHandler,
    GetCategoryHandler,
    GetWalletHandler,
)
from src.configs import config_map, setting_base, setting_data_base
from src.db.repositories import AccountRepository, CategoryRepository, CategoryDetailRepository, WalletRepository
from src.db.db import DbContext, get_db_pool
from src.external_clients import FinanceApiClient


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

    def resolve_category_detail_repository(
        db_context: DbContext | None = None,
    ) -> CategoryDetailRepository:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return CategoryDetailRepository(db_context)

    app["category_detail_repository"] = resolve_category_detail_repository

    def resolve_wallet_repository(
        db_context: DbContext | None = None,
    ) -> WalletRepository:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return WalletRepository(db_context)

    app["wallet_repository"] = resolve_wallet_repository

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

    def resolve_get_category_handler(
        db_context: DbContext | None = None,
    ) -> GetCategoryHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return GetCategoryHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
            category_repository=app["category_repository"](db_context),
        )

    app["get_category_handler"] = resolve_get_category_handler

    def resolve_add_category_detail_handler(
        db_context: DbContext | None = None,
    ) -> AddCategoryDetailHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return AddCategoryDetailHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
            category_detail_repository=app["category_detail_repository"](db_context),
        )

    app["add_category_detail_handler"] = resolve_add_category_detail_handler

    def resolve_add_wallet_handler(
        db_context: DbContext | None = None,
    ) -> AddWalletHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return AddWalletHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
            wallet_repository=app["wallet_repository"](db_context),
        )

    app["add_wallet_handler"] = resolve_add_wallet_handler

    def resolve_get_wallet_handler(
        db_context: DbContext | None = None,
    ) -> GetWalletHandler:
        if not db_context:
            db_context = DbContext(app["db_pool"])
        return GetWalletHandler(
            db_context=db_context,
            account_repository=app["account_repository"](db_context),
            wallet_repository=app["wallet_repository"](db_context),
        )

    app["get_wallet_handler"] = resolve_get_wallet_handler


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
