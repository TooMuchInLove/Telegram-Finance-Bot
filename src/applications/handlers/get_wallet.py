from decimal import Decimal
from datetime import datetime

from src.db.helpers import BaseModel
from src.db.repositories import AccountRepository, WalletRepository
from src.db.db import DbContext


class GetWalletQuery(BaseModel):
    telegram_user_id: int


class Wallet(BaseModel):
    name: str
    # TODO: Временное решение (переделать на Decimal)
    current_amount: float
    account_id: int
    created_at: datetime


class GetWalletHandler:
    def __init__(
        self,
        db_context: DbContext,
        account_repository: AccountRepository,
        wallet_repository: WalletRepository,
    ) -> None:
        self._db_context = db_context
        self._account_repository = account_repository
        self._wallet_repository = wallet_repository

    async def handle(self, query: GetWalletQuery) -> list[Wallet]:
        account = await self._account_repository.get_account_by_telegram_user_id(
            telegram_user_id=query.telegram_user_id,
        )
        if not account:
            return []

        wallets = await self._wallet_repository.get_wallets_by_account_id(
            account_id=account.id,
        )
        print(f'# wallets: {wallets}')

        items = []
        for wallet in wallets:
            items.append(
                Wallet(
                    name=wallet.name,
                    # TODO: Временное решение (переделать на Decimal)
                    current_amount=float(wallet.current_amount),
                    account_id=wallet.account_id,
                    created_at=wallet.created_at,
                )
            )

        return items
