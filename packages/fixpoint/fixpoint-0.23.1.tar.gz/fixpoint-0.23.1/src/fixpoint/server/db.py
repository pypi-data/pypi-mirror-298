"""Database connection utilities"""

__all__ = ["DatabasePoolSingleton"]

import asyncio
from typing import AsyncContextManager, ContextManager, Optional

from psycopg import Connection as PgConnection, AsyncConnection as AsyncPgConnection
from psycopg_pool import AsyncConnectionPool, ConnectionPool

from fixpoint.config import PGConfig


class DatabasePoolSingleton:
    """Singleton class for the database connection pool."""

    _pg_config: PGConfig = PGConfig.from_env()
    _pool: Optional[ConnectionPool] = None
    _apool: Optional[AsyncConnectionPool] = None

    @classmethod
    def set_pg_config(cls, pg_config: PGConfig) -> None:
        """Set the database connection."""
        cls._pg_config = pg_config
        cls._pool = cls._pg_config.new_pool()
        cls._ensure_async_pool()

    @classmethod
    def _ensure_async_pool(cls) -> None:
        # Check if we have an asyncio loop running
        try:
            loop = asyncio.get_running_loop()
            if loop and loop.is_running():
                cls._apool = cls._pg_config.new_async_pool()
            else:
                cls._apool = None
        except RuntimeError:
            # No running event loop
            cls._apool = None

    @classmethod
    def get_pg_config(cls) -> PGConfig:
        """Get the database connection."""
        return cls._pg_config

    @classmethod
    def get_pool(cls) -> ConnectionPool:
        """Get the database connection pool."""
        if cls._pool is None:
            raise ValueError("Database connection pool is not initialized")
        return cls._pool

    @classmethod
    def get_async_pool(cls) -> Optional[AsyncConnectionPool]:
        """Get the database connection pool.

        If there is no running event loop, we return None.
        """
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return None

        cls._ensure_async_pool()
        if cls._apool is None:
            raise ValueError("Database connection pool is not initialized")
        return cls._apool

    @classmethod
    def pool_conn(cls) -> ContextManager[PgConnection]:
        """Get a sync connection context manager from the pool."""
        if cls._pool is None:
            raise ValueError("Database connection pool is not initialized")
        return cls._pool.connection()

    @classmethod
    def async_pool_conn(cls) -> AsyncContextManager[AsyncPgConnection]:
        """Get an async connection context manager from the pool."""
        if cls._apool is None:
            raise ValueError("Database connection pool is not initialized")
        return cls._apool.connection()
