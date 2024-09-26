"""Abstraction around the Firecrawl API

Note that we named this module `fc` so that it doesn't conflict with the
external `firecrawl` package.
"""

__all__ = [
    "FirecrawlNormal",
    "FirecrawlDiskCachedClient",
    "FirecrawlClient",
    "MockFirecrawlClient",
]

from typing import Any, Awaitable, Callable, Coroutine, Dict, Optional, Protocol

import asyncer
import diskcache
from firecrawl import FirecrawlApp

from fixpoint import callcache
from fixpoint.logging import fc_logger as logger
from fixpoint.config import DiskPaths


class FirecrawlClient(Protocol):
    """Protocol for a Firecrawl client"""

    def scrape_url(self, url: str, params: Dict[str, Any] | None = None) -> Any:
        """Scrape the specified URL using the Firecrawl API.

        Args:
            url (str): The URL to scrape.
            params (Optional[Dict[str, Any]]): Additional parameters for the scrape request.

        Returns:
            Any: The scraped data if the request is successful.

        Raises:
            Exception: If the scrape request fails.
        """

    async def scrape_url_async(
        self, url: str, params: Dict[str, Any] | None = None
    ) -> Any:
        """Asynchronously scrape the specified URL using the Firecrawl API.

        Same API as `scrape_url`, but returns a coroutine.
        """


class FirecrawlNormal(FirecrawlClient):
    """The normal Firecrawl client"""

    _api_key: str
    _client: FirecrawlApp

    _async_scrape_url: Callable[[str, Dict[str, Any] | None], Awaitable[Any]]

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._client = FirecrawlApp(api_key=self._api_key)
        self._async_scrape_url = asyncer.asyncify(self._client.scrape_url)

    def scrape_url(self, url: str, params: Dict[str, Any] | None = None) -> Any:
        logger.info("Scraping URL: %s", url)
        res = self._client.scrape_url(url, params)
        logger.info("Finished scraping URL: %s", url)
        return res

    async def scrape_url_async(
        self, url: str, params: Dict[str, Any] | None = None
    ) -> Any:
        logger.info("Scraping URL: %s", url)
        res = await self._async_scrape_url(url, params)
        logger.info("Finished scraping URL: %s", url)
        return res


class FirecrawlDiskCachedClient(FirecrawlClient):
    """A Firecrawl client that caches results on disk"""

    _api_key: str
    _client: FirecrawlClient
    _cache: callcache.CallCache

    _cached_scrape_url: Callable[[str, Dict[str, Any] | None], Any]
    _cached_async_scrape_url: Callable[
        [str, Dict[str, Any] | None], Coroutine[Any, Any, Any]
    ]

    def __init__(
        self,
        cache_dir: str,
        cache_size_limit_bytes: int,
        ttl_s: float,
        fc_client: FirecrawlClient,
    ):
        """Create a new Firecrawl disk cached client

        We let the caller pass in another Firecrawl client so that we can apply
        caching to any of our other Firecrawl client implementations.
        """
        disk_paths = DiskPaths(cache_dir)
        disk_paths.ensure_exists()
        cache = diskcache.Cache(
            directory=disk_paths.callcache, size_limit=cache_size_limit_bytes
        )
        self._cache = callcache.FuncDiskCallCache(cache, ttl_s=ttl_s)
        self._client = fc_client

        ###
        # Configure the synchronous cached scrape
        ###

        @callcache.cacheit(
            kind=callcache.CallCacheKind.FUNC,
            kind_id="__fixpoint__FirecrawlCache",
            callcache=self._cache,
        )
        def cached_scrape_url(url: str, params: Dict[str, Any] | None = None) -> Any:
            return self._client.scrape_url(url, params)

        self._cached_scrape_url = cached_scrape_url

        ###
        # Configure the asynchronous cached scrape
        ###

        @callcache.async_cacheit(
            kind=callcache.CallCacheKind.FUNC,
            kind_id="__fixpoint__FirecrawlCache",
            callcache=self._cache,
        )
        async def cached_async_scrape_url(
            url: str, params: Dict[str, Any] | None = None
        ) -> Any:
            return await self._client.scrape_url_async(url, params)

        self._cached_async_scrape_url = cached_async_scrape_url

    @classmethod
    def from_api_key(
        cls, cache_dir: str, cache_size_limit_bytes: int, ttl_s: float, api_key: str
    ) -> "FirecrawlDiskCachedClient":
        """Create a new Firecrawl disk-cached client from an API key"""
        fc_client = FirecrawlNormal(api_key)
        return cls(cache_dir, cache_size_limit_bytes, ttl_s, fc_client)

    def scrape_url(self, url: str, params: Dict[str, Any] | None = None) -> Any:
        return self._cached_scrape_url(url, params)

    async def scrape_url_async(
        self, url: str, params: Dict[str, Any] | None = None
    ) -> Any:
        return await self._cached_async_scrape_url(url, params)


_DEFAULT_MOCK_CONTENT = (
    "This is Acme Inc.'s website. We sell devices to kill roadrunners."
)


class MockFirecrawlClient(FirecrawlClient):
    """Protocol for a Firecrawl client"""

    _result_generator: Callable[[str, Dict[str, Any] | None], Dict[str, Any]]
    _async_result_generator: Callable[
        [str, Dict[str, Any] | None], Awaitable[Dict[str, Any]]
    ]
    _default_content: str

    def __init__(
        self,
        result_generator: Callable[[str, Dict[str, Any] | None], Dict[str, Any]],
        default_content: Optional[str] = None,
    ):
        self._result_generator = result_generator
        self._async_result_generator = asyncer.asyncify(result_generator)
        self._default_content = default_content or _DEFAULT_MOCK_CONTENT

    def scrape_url(self, url: str, params: Dict[str, Any] | None = None) -> Any:
        """Scrape the specified URL using the Firecrawl API.

        Args:
            url (str): The URL to scrape.
            params (Optional[Dict[str, Any]]): Additional parameters for the scrape request.

        Returns:
            Any: The scraped data if the request is successful.

        Raises:
            Exception: If the scrape request fails.
        """
        return self._new_default_results(self._result_generator(url, params))

    async def scrape_url_async(
        self, url: str, params: Dict[str, Any] | None = None
    ) -> Any:
        """Asynchronously scrape the specified URL using the Firecrawl API.

        Same API as `scrape_url`, but returns a coroutine.
        """
        return self._new_default_results(
            await self._async_result_generator(url, params)
        )

    def _new_default_results(self, gen_res: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure that the results are compatible with the output we expect"""
        gen_res = gen_res.copy()
        content = _parse_mock_gen_content(self._default_content, gen_res)
        gen_res["content"] = content
        gen_res["markdown"] = content
        return gen_res


def _parse_mock_gen_content(default_content: str, gen_res: Dict[str, Any]) -> str:
    content: Optional[str]
    content = gen_res.get("content")
    if content:
        return str(content)
    content = gen_res.get("markdown")
    if content:
        return str(content)
    return default_content
