"""Postgres storage code"""

__all__ = [
    "DiskPaths",
    "get_env_api_url",
    "get_env_auth_disabled",
    "get_env_firecrawl_api_key",
    "get_env_openai_api_key",
    "get_env_or_fail",
    "get_env_runmode",
    "get_env_supabase_api_key",
    "get_env_supabase_url",
    "PGConfig",
    "PgConnection",
    "RunMode",
]

from dataclasses import dataclass
import os
from typing import Literal, Optional, Union
import urllib

from psycopg import Connection as PgConnection
from psycopg_pool import AsyncConnectionPool, ConnectionPool

from fixpoint.constants import API_BASE_URL
from fixpoint._utils import get_env_or_fail
from fixpoint.errors import ConfigError


class _Defaults:
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"


def _maybe_port(port: Optional[Union[str, int]]) -> str:
    if port is None:
        return _Defaults.DB_PORT
    if isinstance(port, str):
        return port
    return str(port)


@dataclass
class PGConfig:
    """Postgres connection configuration"""

    dbname: str
    user: str
    password: str
    host: str
    port: str

    @classmethod
    def from_env(cls, strict_env: bool = False) -> "PGConfig":
        """Create a PGConfig from environment variables

        Create a PGConfig from environment variables.

        If the user has set all of the individual Postgres environment variables
        (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT), prefer those.

        Otherwise, if the POSTGRES_URL environment variable is set, use that.

        Otherwise, fall back to creating the PGConfig from whatever individual
        env vars are present, filling in defaults for the missing values.

        If the user sets the STRICT_ENV=true environment variable, fail if we
        have not supplied enough environment variables to avoid using the coded
        defaults.
        """
        individual_vars = ["DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
        all_individual_vars_set = all(os.environ.get(key) for key in individual_vars)
        postgres_url = os.environ.get("POSTGRES_URL")
        if not all_individual_vars_set and postgres_url:
            return cls.from_url(postgres_url)

        if strict_env or os.environ.get("STRICT_ENV", "false").lower() == "true":
            if not all_individual_vars_set:
                raise ConfigError(
                    "Not all of the individual Postgres environment variables "
                    "are set, and POSTGRES_URL is not set. "
                    "Either set the individual variables "
                    "(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT), "
                    "or set POSTGRES_URL."
                )

        return cls(
            dbname=get_env_or_fail("DB_NAME", _Defaults.DB_NAME),
            user=get_env_or_fail("DB_USER", _Defaults.DB_USER),
            password=get_env_or_fail("DB_PASSWORD", _Defaults.DB_PASSWORD),
            host=get_env_or_fail("DB_HOST", _Defaults.DB_HOST),
            port=get_env_or_fail("DB_PORT", _Defaults.DB_PORT),
        )

    def conn_str(self) -> str:
        """Get the connection string"""
        return " ".join(
            [
                f"dbname={self.dbname}",
                f"user={self.user}",
                f"password={self.password}",
                f"host={self.host}",
                f"port={self.port}",
            ]
        )

    @classmethod
    def from_url(cls, url: str) -> "PGConfig":
        """Create a PGConfig from a URL"""
        parsed = urllib.parse.urlparse(url)
        return cls(
            dbname=parsed.path.lstrip("/"),
            user=parsed.username or _Defaults.DB_USER,
            password=parsed.password or _Defaults.DB_PASSWORD,
            host=parsed.hostname or _Defaults.DB_HOST,
            port=_maybe_port(parsed.port),
        )

    def new_async_pool(self) -> AsyncConnectionPool:
        """Create a new async connection pool"""
        return AsyncConnectionPool(self.conn_str())

    def new_pool(self) -> ConnectionPool:
        """Create a new sync connection pool"""
        return ConnectionPool(self.conn_str())


RunMode = Literal["supabase", "disk"]


def get_env_runmode(default: RunMode) -> RunMode:
    """Get the run mode from the environment"""
    run_mode = os.environ.get("RUN_MODE")
    if run_mode == "supabase":
        return "supabase"
    elif run_mode == "disk":
        return "disk"
    elif run_mode is None:
        return default
    else:
        raise ValueError(f"Invalid run mode: {run_mode}")


def get_env_api_url() -> str:
    """Get the API URL from the environment, or default value"""
    return os.environ.get("FIXPOINT_API_BASE_URL", API_BASE_URL)


def get_env_firecrawl_api_key(override: Optional[str] = None) -> str:
    """Get the Firecrawl API key from the environment"""
    return _get_required_env("FIRECRAWL_API_KEY", override=override)


def get_env_openai_api_key(override: Optional[str] = None) -> str:
    """Get the OpenAI API key from the environment"""
    return _get_required_env("OPENAI_API_KEY", override=override)


def get_env_supabase_url(override: Optional[str] = None) -> str:
    """Get the supabase URL from the environment"""
    return _get_required_env("SUPABASE_URL", override=override)


def get_env_supabase_api_key(override: Optional[str] = None) -> str:
    """Get the supabase API key from the environment"""
    return _get_required_env("SUPABASE_API_KEY", override=override)


def get_env_auth_disabled(fallback: Optional[str] = None) -> bool:
    """Get the auth disabled flag from the environment"""
    return _get_required_env("AUTH_DISABLED", fallback=fallback).lower() == "true"


def _get_required_env(
    key: str, *, override: Optional[str] = None, fallback: Optional[str] = None
) -> str:
    if override:
        return override
    value = os.environ.get(key, fallback)
    if not value:
        raise ValueError(f"{key} environment variable not set")
    return value


class DiskPaths:
    """Disk path for storage and config."""

    base_path: str

    def __init__(self, base_path: str):
        self.base_path = os.path.expanduser(base_path)

    def ensure_exists(self) -> None:
        """Ensure the base path exists"""
        os.makedirs(self.base_path, exist_ok=True)

    @property
    def agent_cache(self) -> str:
        """Path to the agent cache"""
        return os.path.join(self.base_path, "agent_cache")

    @property
    def callcache(self) -> str:
        """Path to the callcache"""
        return os.path.join(self.base_path, "callcache")

    @property
    def sqlite_path(self) -> str:
        """Path to the sqlite database"""
        return os.path.join(self.base_path, "db.sqlite")
