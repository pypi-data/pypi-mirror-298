"""Shared types and helpers for the web researcher agent."""

__all__ = ["Clients"]

from typing import Union

import instructor
from openai import AsyncOpenAI

from fixpoint.agents.oai import AsyncOpenAIClients, AsyncOpenAI as FPAsyncOpenAI
from fixpoint.config import get_env_firecrawl_api_key, get_env_openai_api_key
from fixpoint._integrations.fc import FirecrawlClient, FirecrawlNormal


class Clients:
    """Clients for external services."""

    firecrawl: FirecrawlClient
    openai: FPAsyncOpenAI

    def __init__(
        self, firecrawl: FirecrawlClient, openai: Union[AsyncOpenAI, FPAsyncOpenAI]
    ):
        self.firecrawl = firecrawl
        if isinstance(openai, FPAsyncOpenAI):
            self.openai = openai
        else:
            oai_clients = AsyncOpenAIClients(
                openai=openai,
                instructor=instructor.from_openai(openai),
            )
            self.openai = FPAsyncOpenAI(
                agent_id="webresearcher", openai_clients=oai_clients
            )

    @classmethod
    def from_keys(cls, *, firecrawl_api_key: str, openai_api_key: str) -> "Clients":
        """Instantiate the clients from API keys."""
        return cls(
            firecrawl=FirecrawlNormal(api_key=firecrawl_api_key),
            openai=AsyncOpenAI(api_key=openai_api_key),
        )

    @classmethod
    def from_env(cls) -> "Clients":
        """Instantiate the clients from environment variables."""
        firecrawl_api_key = get_env_firecrawl_api_key()
        openai_api_key = get_env_openai_api_key()
        return cls.from_keys(
            firecrawl_api_key=firecrawl_api_key, openai_api_key=openai_api_key
        )
