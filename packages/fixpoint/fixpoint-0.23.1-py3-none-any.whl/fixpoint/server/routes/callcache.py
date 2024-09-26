"""Routes for the durable callcache"""

__all__ = [
    "StepCallcacheDep",
    "TaskCallcacheDep",
    "get_task_callcache_entry",
    "get_step_callcache_entry",
    "create_task_callcache_entry",
    "create_step_callcache_entry",
]

import json
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from fixpoint._auth import fastapi_auth
from fixpoint import callcache as callcache_lib
from fixpoint.types import CacheEntry, CreateCallcacheEntryRequest
from fixpoint.callcache import CallCache, TaskPostgresCallCache, StepPostgresCallCache
from ..config import ConfigDep


router = APIRouter(prefix="/callcache", tags=["callcache"])


async def step_callcache_client(config: ConfigDep) -> CallCache:
    """The dependency for a step callcache client"""
    sync_pool = config.db.get_pool()
    async_pool = config.db.get_async_pool()
    if async_pool is None:
        raise RuntimeError("no async database pool")
    return StepPostgresCallCache(sync_pool, async_pool)


StepCallcacheDep = Annotated[CallCache, Depends(step_callcache_client)]


async def task_callcache_client(config: ConfigDep) -> CallCache:
    """The dependency for a task callcache client"""
    async_pool = config.db.get_async_pool()
    if async_pool is None:
        raise RuntimeError("no async database pool")
    return TaskPostgresCallCache(config.db.get_pool(), async_pool)


TaskCallcacheDep = Annotated[CallCache, Depends(task_callcache_client)]


@router.get("/{run_id}/task/{task_id}/{cache_key:path}")
async def get_task_callcache_entry(
    authn_info: fastapi_auth.AuthInfoDep,
    callcache: TaskCallcacheDep,
    run_id: str,
    task_id: str,
    cache_key: str,
) -> CacheEntry:
    """Get a task callcache entry"""
    return _process_cache_result(
        cache_key,
        await callcache.async_check_cache(
            org_id=authn_info.org_id(),
            run_id=run_id,
            kind_id=task_id,
            serialized_args=cache_key,
        ),
    )


@router.get("/{run_id}/step/{step_id}/{cache_key:path}")
async def get_step_callcache_entry(
    authn_info: fastapi_auth.AuthInfoDep,
    callcache: StepCallcacheDep,
    run_id: str,
    step_id: str,
    cache_key: str,
) -> CacheEntry:
    """Get a step callcache entry"""
    return _process_cache_result(
        cache_key,
        await callcache.async_check_cache(
            org_id=authn_info.org_id(),
            run_id=run_id,
            kind_id=step_id,
            serialized_args=cache_key,
        ),
    )


def _process_cache_result(
    cache_key: str, res: callcache_lib.CacheResult[Any]
) -> CacheEntry:
    if not res.found:
        return CacheEntry(found=False, cache_key=cache_key, result=None)
    try:
        json_res = json.dumps(res.result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error serializing result: {e}",
        ) from e
    return CacheEntry(found=True, cache_key=cache_key, result=json_res)


@router.post("/{run_id}/task/{task_id}")
async def create_task_callcache_entry(
    authn_info: fastapi_auth.AuthInfoDep,
    callcache: TaskCallcacheDep,
    run_id: str,
    task_id: str,
    request: CreateCallcacheEntryRequest,
) -> CacheEntry:
    """Create a task callcache entry"""
    _check_json_deserializable(request.result)
    await callcache.async_store_result(
        org_id=authn_info.org_id(),
        run_id=run_id,
        kind_id=task_id,
        serialized_args=request.cache_key,
        res=request.result,
    )
    return CacheEntry(found=True, cache_key=request.cache_key, result=request.result)


@router.post("/{run_id}/step/{step_id}")
async def create_step_callcache_entry(
    authn_info: fastapi_auth.AuthInfoDep,
    callcache: TaskCallcacheDep,
    run_id: str,
    step_id: str,
    request: CreateCallcacheEntryRequest,
) -> CacheEntry:
    """Create a step callcache entry"""
    _check_json_deserializable(request.result)
    await callcache.async_store_result(
        org_id=authn_info.org_id(),
        run_id=run_id,
        kind_id=step_id,
        serialized_args=request.cache_key,
        res=request.result,
    )
    return CacheEntry(found=True, cache_key=request.cache_key, result=request.result)


def _check_json_deserializable(value: str) -> None:
    try:
        json.loads(value)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="cache value must be JSON-deserializable",
        ) from e
