"""Common code for sync and async Fixpoint clients."""

__all__ = ["ApiCoreConfig"]

from dataclasses import dataclass
from typing import Optional, TypeVar

import httpx
from pydantic import BaseModel

from fixpoint.config import get_env_api_url
from fixpoint.utils import route_url
from fixpoint.workflows.structured import RunConfig
from fixpoint.workflows.imperative import StorageConfig


BM = TypeVar("BM", bound=BaseModel)


@dataclass
class ApiCoreConfig:
    """Configuration for the Fixpoint API"""

    api_key: str
    api_url: str
    run_config: RunConfig
    storage_config: StorageConfig

    @classmethod
    def from_api_info(
        cls,
        api_key: str,
        api_url: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        ahttp_client: Optional[httpx.AsyncClient] = None,
    ) -> "ApiCoreConfig":
        """Create an ApiConfig from an API key and API URL"""
        if api_url is None:
            api_url = get_env_api_url()
        run_config = RunConfig.with_api(
            api_key=api_key,
            api_url=api_url,
            http_client=http_client,
            ahttp_client=ahttp_client,
        )
        storage_config = run_config.storage
        return cls(api_key, api_url, run_config, storage_config)

    def route_url(self, *route_parts: str) -> str:
        """Join the base URL with the given route."""
        return route_url(self.api_url, *route_parts)
