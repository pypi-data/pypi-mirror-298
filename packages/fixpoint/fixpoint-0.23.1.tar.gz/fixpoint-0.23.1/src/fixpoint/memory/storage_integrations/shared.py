"""Shared queries for memory storage"""

__all__ = [
    "new_insert_memory_query",
    "new_list_memories_query",
    "new_get_memory_query",
    "Cursor",
    "format_cursor",
    "parse_cursor",
]

import base64
import datetime
import json
from typing import Any, Dict, List, Optional, Tuple, TypedDict

from fixpoint._storage.sql import ParamNameKind, param
from fixpoint.memory.protocol import MemoryItem


class Cursor(TypedDict):
    """A cursor object for paginating through a list of memories"""

    id: str
    created_at: datetime.datetime


def format_cursor(memories: List[MemoryItem]) -> str:
    """Format a pagination cursor object into a string"""
    last_mem = memories[-1]
    return base64.urlsafe_b64encode(
        json.dumps(
            {"id": last_mem.id, "created_at": last_mem.created_at.isoformat()}
        ).encode()
    ).decode()


def parse_cursor(cursor: str) -> Cursor:
    """Parse a pagination cursor string into a Cursor object"""
    d = json.loads(base64.urlsafe_b64decode(cursor).decode())
    return {
        "id": d["id"],
        "created_at": datetime.datetime.fromisoformat(d["created_at"]),
    }


def new_insert_memory_query(
    kind: ParamNameKind, table: str, org_id: str, memory: MemoryItem
) -> Tuple[str, Dict[str, Any]]:
    """Make query and params for inserting a memory"""
    mem_dict = memory.serialize()

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
    INSERT INTO {table} (
        id, agent_id, messages, completion, workflow_id, workflow_run_id, task_id,
        step_id, metadata, created_at, org_id
    ) VALUES (
        {_param("id")}, {_param("agent_id")}, {_param("messages")},
        {_param("completion")}, {_param("workflow_id")}, {_param("workflow_run_id")},
        {_param("task_id")}, {_param("step_id")}, {_param("metadata")},
        {_param("created_at")}, {_param("org_id")}
    )
    """

    mem_dict.update({"org_id": org_id})
    return query, mem_dict


def new_list_memories_query(
    kind: ParamNameKind,
    table: str,
    org_id: str,
    n: int,
    cursor_obj: Optional[Cursor] = None,
) -> Tuple[str, Dict[str, Any]]:
    """Make query and params for listing memories"""
    params: Dict[str, Any] = {"n": n, "org_id": org_id}

    def _param(pn: str) -> str:
        return param(kind, pn)

    if cursor_obj:
        query = f"""
        SELECT
            id, agent_id, messages, completion, workflow_id, workflow_run_id,
            task_id, step_id, metadata, created_at
        FROM {table}
        WHERE (
            created_at < {_param("created_at")}
            OR (created_at = {_param("created_at")} AND id > {_param("id")})
        ) AND org_id = {_param("org_id")}
        ORDER BY created_at DESC, id ASC
        LIMIT {_param("n")}
        """
        params.update(
            {
                "created_at": cursor_obj["created_at"].isoformat(),
                "id": cursor_obj["id"],
            }
        )
    else:
        query = f"""
        SELECT
            id, agent_id, messages, completion, workflow_id, workflow_run_id,
            task_id, step_id, metadata, created_at
        FROM {table}
        WHERE org_id = {_param("org_id")}
        ORDER BY created_at DESC, id ASC
        LIMIT {_param("n")}
        """

    return query, params


def new_get_memory_query(
    kind: ParamNameKind, table: str, org_id: str, mem_id: str
) -> Tuple[str, Dict[str, str]]:
    """Make query and params for getting a memory"""

    def _param(pn: str) -> str:
        return param(kind, pn)

    query = f"""
    SELECT
        id, agent_id, messages, completion, workflow_id, workflow_run_id,
        task_id, step_id, metadata, created_at
    FROM {table}
    WHERE id = {_param("id")}
    AND org_id = {_param("org_id")}
    """

    return query, {"id": mem_id, "org_id": org_id}
