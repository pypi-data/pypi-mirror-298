"""Configuration for the API server"""

__all__ = ["Config", "ConfigSingleton", "get_config", "ConfigDep"]

from dataclasses import dataclass
from typing import Annotated, Any, Dict, Literal, Optional, Type

from fastapi import Depends

from fixpoint.agents.oai import AsyncOpenAI, AsyncOpenAIClients
from fixpoint._integrations.fc import (
    FirecrawlClient,
    FirecrawlNormal,
    FirecrawlDiskCachedClient,
    MockFirecrawlClient,
)
from fixpoint.config import (
    PGConfig,
    get_env_firecrawl_api_key,
    get_env_openai_api_key,
    get_env_auth_disabled,
)
from .db import DatabasePoolSingleton

FirecrawlClientType = Literal["normal", "disk_cached", "mocked"]
_DEFAULT_FIRECRAWL_CLIENT_TYPE: FirecrawlClientType = "normal"

_fc_scrape_counter = [0]


def _fc_scrape_generator(url: str, params: Dict[str, Any] | None) -> Dict[str, Any]:
    res = {"url": url, "params": params, "counter": _fc_scrape_counter[0]}
    _fc_scrape_counter[0] += 1
    return res


@dataclass
class FirecrawlDiskCacheOpts:
    """Options for the firecrawl disk cache"""

    cache_dir: str
    ttl_s: float = 60 * 60 * 24 * 1  # 1 day
    size_limit_bytes: int = 1024 * 1024 * 256  # 256 MB


@dataclass
class Clients:
    """Clients for external services."""

    firecrawl: FirecrawlClient
    async_openai: AsyncOpenAI

    @classmethod
    def from_keys(
        cls,
        *,
        firecrawl_api_key: str,
        openai_api_key: str,
        firecrawl_client_type: FirecrawlClientType = _DEFAULT_FIRECRAWL_CLIENT_TYPE,
        firecrawl_disk_cache_opts: Optional[FirecrawlDiskCacheOpts] = None,
    ) -> "Clients":
        """Instantiate the clients from API keys."""
        firecrawl: FirecrawlClient
        if firecrawl_client_type == "normal":
            firecrawl = FirecrawlNormal(api_key=firecrawl_api_key)
        elif firecrawl_client_type == "disk_cached":
            if not firecrawl_disk_cache_opts:
                raise ValueError(
                    "firecrawl_disk_cache_opts must be provided when "
                    "firecrawl_client_type is 'disk_cached'"
                )
            firecrawl = FirecrawlDiskCachedClient(
                cache_dir=firecrawl_disk_cache_opts.cache_dir,
                cache_size_limit_bytes=firecrawl_disk_cache_opts.size_limit_bytes,
                ttl_s=firecrawl_disk_cache_opts.ttl_s,
                fc_client=FirecrawlNormal(api_key=firecrawl_api_key),
            )
        elif firecrawl_client_type == "mocked":
            firecrawl = MockFirecrawlClient(_fc_scrape_generator)
        else:
            raise ValueError(f"Invalid firecrawl client type: {firecrawl_client_type}")

        return cls(
            firecrawl=firecrawl,
            async_openai=AsyncOpenAI(
                agent_id="api-server-agent",
                openai_clients=AsyncOpenAIClients.from_api_key(api_key=openai_api_key),
            ),
        )

    @classmethod
    def from_env(
        cls,
        firecrawl_client_type: FirecrawlClientType = _DEFAULT_FIRECRAWL_CLIENT_TYPE,
        firecrawl_disk_cache_opts: Optional[FirecrawlDiskCacheOpts] = None,
    ) -> "Clients":
        """Instantiate the clients from environment variables."""
        fc_api_key_default: Optional[str] = None
        if firecrawl_client_type == "mocked":
            # When using a mocked firecrawl client, the API key is not needed.
            # We set it here so our code doesn't complain about its absence.
            fc_api_key_default = "test"
        firecrawl_api_key = get_env_firecrawl_api_key(fc_api_key_default)
        openai_api_key = get_env_openai_api_key()
        return cls.from_keys(
            firecrawl_api_key=firecrawl_api_key,
            openai_api_key=openai_api_key,
            firecrawl_client_type=firecrawl_client_type,
            firecrawl_disk_cache_opts=firecrawl_disk_cache_opts,
        )


class Config:
    """Configuration for the API server."""

    clients: Clients
    db: Type[DatabasePoolSingleton] = DatabasePoolSingleton
    auth_disabled: bool = False

    def __init__(
        self,
        clients: Clients,
        db: Type[DatabasePoolSingleton],
        pg_config: PGConfig,
        auth_disabled: bool = False,
    ):
        DatabasePoolSingleton.set_pg_config(pg_config)
        self.clients = clients
        self.db = db
        self.auth_disabled = auth_disabled

    @classmethod
    def from_env(
        cls,
        firecrawl_client_type: FirecrawlClientType = _DEFAULT_FIRECRAWL_CLIENT_TYPE,
        firecrawl_disk_cache_opts: Optional[FirecrawlDiskCacheOpts] = None,
    ) -> "Config":
        """Instantiate the config from environment variables."""
        return cls(
            clients=Clients.from_env(
                firecrawl_client_type=firecrawl_client_type,
                firecrawl_disk_cache_opts=firecrawl_disk_cache_opts,
            ),
            db=DatabasePoolSingleton,
            pg_config=PGConfig.from_env(),
            auth_disabled=get_env_auth_disabled("false"),
        )


class ConfigSingleton:
    """Singleton instance of Config."""

    _config: Optional[Config] = None

    @classmethod
    def get(cls) -> Config:
        """Get the singleton instance of Config."""
        if cls._config is None:
            cls._config = Config.from_env()
        return cls._config

    @classmethod
    def set(cls, config: Config) -> None:
        """Set the singleton instance of Config."""
        cls._config = config


def get_config() -> Config:
    """Get the singleton instance of Config."""
    return ConfigSingleton.get()


ConfigDep = Annotated[Config, Depends(get_config)]
