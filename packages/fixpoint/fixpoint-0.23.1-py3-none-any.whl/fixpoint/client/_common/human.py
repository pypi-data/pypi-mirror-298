"""Common code for human-in-the-loop tasks."""

__all__ = [
    "create_human_task",
    "async_create_human_task",
    "get_human_task",
    "async_get_human_task",
]

import datetime
from typing import Any, Dict

import httpx

from fixpoint.workflows.human.definitions import (
    CreateHumanTaskEntryRequest,
    HumanTaskEntry,
)
from .core import ApiCoreConfig


_HUMAN_TASK_ENTRIES_ROUTE = "/human-task-entries"

####
# Create human tasks
####


def create_human_task(
    http_client: httpx.Client,
    config: ApiCoreConfig,
    req: CreateHumanTaskEntryRequest,
) -> HumanTaskEntry:
    """Make a synchronous web research scrape request"""
    resp = http_client.post(
        config.route_url(_HUMAN_TASK_ENTRIES_ROUTE),
        json=_serialize_create_human_task_entry_req(req),
    )
    # only raises if we got an error response
    return _process_task_entry_resp(resp)


async def async_create_human_task(
    http_client: httpx.AsyncClient,
    config: ApiCoreConfig,
    req: CreateHumanTaskEntryRequest,
) -> HumanTaskEntry:
    """Make a synchronous web research scrape request"""
    resp = await http_client.post(
        config.route_url(_HUMAN_TASK_ENTRIES_ROUTE),
        json=_serialize_create_human_task_entry_req(req),
    )
    # only raises if we got an error response
    return _process_task_entry_resp(resp)


####
# Get a human task
####


def get_human_task(
    http_client: httpx.Client, config: ApiCoreConfig, task_id: str
) -> HumanTaskEntry:
    """Synchronously get a human task by ID"""
    resp = http_client.get(config.route_url(_HUMAN_TASK_ENTRIES_ROUTE, task_id))
    return _process_task_entry_resp(resp)


async def async_get_human_task(
    http_client: httpx.AsyncClient, config: ApiCoreConfig, task_id: str
) -> HumanTaskEntry:
    """Asynchronously get a human task by ID"""
    resp = await http_client.get(config.route_url(_HUMAN_TASK_ENTRIES_ROUTE, task_id))
    return _process_task_entry_resp(resp)


####
# Helpers
####


def _process_task_entry_resp(resp: httpx.Response) -> HumanTaskEntry:
    # only raises if we got an error response
    resp.raise_for_status()
    obj = HumanTaskEntry.model_validate(resp.json())
    if obj.created_at:
        # set the tzinfo to UTC
        obj.created_at = obj.created_at.replace(tzinfo=datetime.timezone.utc)
    if obj.updated_at:
        obj.updated_at = obj.updated_at.replace(tzinfo=datetime.timezone.utc)
    return obj


def _serialize_create_human_task_entry_req(
    hte: CreateHumanTaskEntryRequest,
) -> Dict[str, Any]:
    hte_dict = hte.model_dump()
    if hte.created_at:
        hte_dict["created_at"] = hte.created_at.isoformat()
    if hte.updated_at:
        hte_dict["updated_at"] = hte.updated_at.isoformat()
    return hte_dict
