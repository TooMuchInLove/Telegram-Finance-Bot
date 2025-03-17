from src.api.handlers.account import handlers as account_handlers
from src.api.handlers.category import handlers as category_handlers
from src.api.handlers.wallet import handlers as wallet_handlers

routes = (
    *account_handlers.routes,
    *category_handlers.routes,
    *wallet_handlers.routes,
)
