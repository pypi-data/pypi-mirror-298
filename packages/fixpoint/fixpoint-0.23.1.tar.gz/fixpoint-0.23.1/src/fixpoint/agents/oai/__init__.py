"""
The oai module contains the OpenAI-compatible interfaces for AI agents. That is,
you can make request like:

```
agent.chat.completions.create(...)
```
"""

__all__ = ["OpenAI", "AsyncOpenAI", "OpenAIClients", "AsyncOpenAIClients"]

from .openai import OpenAI
from ._async_openai import AsyncOpenAI
from .._openai_clients import OpenAIClients, AsyncOpenAIClients
