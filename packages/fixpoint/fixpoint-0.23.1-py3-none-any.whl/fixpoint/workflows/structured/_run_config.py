"""Configuration for running workflows."""

from dataclasses import dataclass
from typing import Optional

import diskcache
import httpx
from psycopg_pool import ConnectionPool, AsyncConnectionPool

from fixpoint._constants import DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES
from fixpoint._utils import prefer_val_or_must_get_env
from fixpoint.callcache import (
    CallCache,
    StepInMemCallCache,
    TaskInMemCallCache,
    StepDiskCallCache,
    TaskDiskCallCache,
    StepApiCallCache,
    TaskApiCallCache,
    StepPostgresCallCache,
    TaskPostgresCallCache,
)
from fixpoint.config import (
    RunMode,
    get_env_runmode,
    get_env_api_url,
    PGConfig,
    DiskPaths,
)
from ..imperative import StorageConfig
from ..imperative.config import (
    DEF_CHAT_CACHE_MAX_SIZE,
    DEF_CHAT_CACHE_TTL_S,
)

_ONE_WEEK = 60 * 60 * 24 * 7


@dataclass
class CallCacheConfig:
    """Configuration for task and step call caches."""

    steps: CallCache
    tasks: CallCache


@dataclass
class RunConfigEnvOverrides:
    """Environment variable overrides for RunConfig"""

    storage_path: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None


@dataclass
class RunConfig:
    """Configuration for running workflows.

    Configuration for running workflows, such as the storage backends to use.
    """

    storage: StorageConfig
    call_cache: CallCacheConfig

    @classmethod
    def from_env(
        cls,
        default_mode: RunMode,
        env_overrides: Optional[RunConfigEnvOverrides] = None,
    ) -> "RunConfig":
        """Create a RunConfig from environment variables"""
        if env_overrides is None:
            env_overrides = RunConfigEnvOverrides()

        run_mode = get_env_runmode(default_mode)

        if run_mode == "supabase":
            _supabase_url = prefer_val_or_must_get_env(
                "SUPABASE_URL", env_overrides.supabase_url
            )
            _supabase_api_key = prefer_val_or_must_get_env(
                "SUPABASE_ANON_KEY", env_overrides.supabase_anon_key
            )
            pg_config = PGConfig.from_env()
            return RunConfig.with_supabase(
                supabase_url=_supabase_url,
                supabase_api_key=_supabase_api_key,
                pg_pool=pg_config.new_pool(),
                apg_pool=pg_config.new_async_pool(),
            )
        elif run_mode == "disk":
            return RunConfig.with_disk(
                storage_path=prefer_val_or_must_get_env(
                    "STORAGE_PATH", env_overrides.storage_path
                ),
                agent_cache_ttl_s=_ONE_WEEK,
                callcache_ttl_s=_ONE_WEEK,
            )
        else:
            raise ValueError(f"Invalid run mode: {run_mode}")

    @classmethod
    def with_defaults(
        cls,
        chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "RunConfig":
        """Configure run for default backend"""
        return cls.with_in_memory(chat_cache_maxsize, chat_cache_ttl_s)

    @classmethod
    def with_supabase(
        cls,
        supabase_url: str,
        supabase_api_key: str,
        pg_pool: ConnectionPool,
        apg_pool: AsyncConnectionPool,
        chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "RunConfig":
        """Configure run for Supabase backend"""
        storage = StorageConfig.with_supabase(
            supabase_url,
            supabase_api_key,
            pg_pool,
            apg_pool,
            chat_cache_maxsize,
            chat_cache_ttl_s,
        )
        # TODO(dbmikus) support Supabase storage
        call_cache = CallCacheConfig(
            steps=StepPostgresCallCache(pg_pool, apg_pool),
            tasks=TaskPostgresCallCache(pg_pool, apg_pool),
        )
        return cls(storage, call_cache)

    @classmethod
    def with_postgres(
        cls,
        pg_pool: ConnectionPool,
        apg_pool: Optional[AsyncConnectionPool],
        chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "RunConfig":
        """Configure run for Postgres backend"""
        storage = StorageConfig.with_postgres(
            pg_pool, apg_pool, chat_cache_maxsize, chat_cache_ttl_s
        )
        call_cache = CallCacheConfig(
            steps=StepPostgresCallCache(pg_pool, apg_pool),
            tasks=TaskPostgresCallCache(pg_pool, apg_pool),
        )
        return cls(storage, call_cache)

    @classmethod
    def with_disk(
        cls,
        *,
        storage_path: str,
        agent_cache_ttl_s: int,
        agent_cache_size_limit_bytes: int = DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES,
        callcache_ttl_s: int,
        callcache_size_limit_bytes: int = DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES,
    ) -> "RunConfig":
        """Configure run for disk storage"""
        disk_paths = DiskPaths(storage_path)
        disk_paths.ensure_exists()
        storage_config = StorageConfig.with_disk(
            storage_path=storage_path,
            agent_cache_ttl_s=agent_cache_ttl_s,
            agent_cache_size_limit_bytes=agent_cache_size_limit_bytes,
        )
        callcache_dir = disk_paths.callcache
        call_cache = diskcache.Cache(
            directory=callcache_dir, size_limit=callcache_size_limit_bytes
        )
        call_cache_config = CallCacheConfig(
            steps=StepDiskCallCache(cache=call_cache, ttl_s=callcache_ttl_s),
            tasks=TaskDiskCallCache(cache=call_cache, ttl_s=callcache_ttl_s),
        )
        return cls(storage_config, call_cache_config)

    @classmethod
    def with_in_memory(
        cls,
        chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "RunConfig":
        """Configure run for in-memory storage"""
        storage = StorageConfig.with_in_memory(chat_cache_maxsize, chat_cache_ttl_s)
        call_cache = CallCacheConfig(
            steps=StepInMemCallCache(),
            tasks=TaskInMemCallCache(),
        )
        return cls(storage, call_cache)

    @classmethod
    def with_api(
        cls,
        api_key: str,
        api_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        ahttp_client: Optional[httpx.AsyncClient] = None,
    ) -> "RunConfig":
        """Configure run for API backend"""
        if api_url is None:
            api_url = get_env_api_url()

        storage = StorageConfig.with_api(api_key, api_url, http_client, ahttp_client)
        call_cache = CallCacheConfig(
            steps=StepApiCallCache(api_key, api_url, http_client, ahttp_client),
            tasks=TaskApiCallCache(api_key, api_url, http_client, ahttp_client),
        )
        return cls(storage, call_cache)
