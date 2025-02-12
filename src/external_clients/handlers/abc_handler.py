from abc import ABC, abstractmethod

from aiogram.types import CallbackQuery, Message


class AbcHandler(ABC):
    @abstractmethod
    async def handle(
        self,
        message: Message | CallbackQuery,
        is_update: bool = False,
    ) -> None:
        pass
