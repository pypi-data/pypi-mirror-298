"""Types for the Fixpoint package"""

__all__ = [
    "AsyncFunc",
    "AwaitableRet",
    "CacheEntry",
    "CreateCallcacheEntryRequest",
    "WorkflowRunAttemptData",
    "ListResponse",
    "Params",
    "Ret_co",
    "Ret",
]

import datetime
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Generic,
    List,
    Literal,
    Optional,
    ParamSpec,
    TypeVar,
)

from pydantic import BaseModel, Field


BM = TypeVar("BM", bound=BaseModel)
Params = ParamSpec("Params")
Ret = TypeVar("Ret")
Ret_co = TypeVar("Ret_co", covariant=True)
AwaitableRet = TypeVar("AwaitableRet", bound=Awaitable[Any])
AsyncFunc = Callable[Params, Coroutine[Any, Any, Ret]]


# TODO(jakub): Add total number of results and pages to the API below
class ListResponse(BaseModel, Generic[BM]):
    """An API list response"""

    data: List[BM] = Field(description="The list of items")
    next_page_token: Optional[str] = Field(
        default=None,
        description="Token to get the next page of results. If no more pages, it is None",
    )
    kind: Literal["list"] = "list"


class CacheEntry(BaseModel):
    """The result of a callcache lookup"""

    found: bool = Field(description="Whether the cache was found")
    cache_key: str = Field(description="The cache key")
    result: Optional[str] = Field(
        description="The cached value if found, as a JSON string"
    )


class CreateCallcacheEntryRequest(BaseModel):
    """The request to create a callcache entry"""

    cache_key: str = Field(
        description="The cache key (normally the serialized args of the function we are caching)"
    )
    result: str = Field(description="The result to cache. Must be JSON-serializable.")


class WorkflowRunAttemptData(BaseModel):
    """Data about a workflow run attempt"""

    attempt_id: str
    workflow_id: str
    workflow_run_id: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
