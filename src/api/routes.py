from .handlers.account import handlers as account_handlers
from .handlers.category import handlers as category_handlers

routes = (
    *account_handlers.routes,
    *category_handlers.routes,
)
