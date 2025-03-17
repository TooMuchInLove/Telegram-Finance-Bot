from asyncpg import Connection, Pool, create_pool as asyncpg_create_pool
from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal
from typing import AsyncIterator, Any
from ujson import loads as ujson_loads, dumps as ujson_dumps

from src.db.helpers import BaseModel


class DbContext:
    def __init__(self, db_pool: Pool) -> None:
        self._db_pool = db_pool
        self._connection: Connection | None = None

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[Connection]:
        if self._connection and not self._connection.is_closed():
            yield self._connection
        else:
            async with self._db_pool.acquire() as connection:
                yield connection

    @asynccontextmanager
    async def start_transaction(self, isolation: str = None) -> None:
        if self._connection and not self._connection.is_closed():
            yield self._connection
            return
        self._connection: Connection = await self._db_pool.acquire()
        tr = self._connection.transaction(isolation=isolation)
        await tr.start()
        try:
            yield tr
        except:
            await tr.rollback()
            raise
        else:
            await tr.commit()
        finally:
            if self._connection:
                await self._db_pool.release(self._connection)
                self._connection = None

    async def close(self) -> None:
        if self._connection:
            await self._db_pool.release(self._connection)
        await self._db_pool.close()


async def _init_connection(connection: Connection) -> None:
    await connection.set_type_codec(
        "json",
        encoder=_encoder,
        decoder=ujson_loads,
        schema="pg_catalog",
    )
    await connection.set_type_codec(
        "jsonb",
        encoder=_encoder,
        decoder=ujson_loads,
        schema="pg_catalog",
    )


async def get_db_pool(**kwargs: dict) -> Pool:
    """Creates postgres pool."""

    kwargs.setdefault("command_timeout", 10)
    return await asyncpg_create_pool(**kwargs, init=_init_connection)


def _encoder(obj: Decimal | datetime | BaseModel) -> Any:
    return ujson_dumps(obj, default=default_handler)


def default_handler(obj: Decimal | datetime | BaseModel) -> float | str | dict:
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, datetime):
        return str(obj)
    if isinstance(obj, BaseModel):
        return obj.dict()
    raise TypeError
