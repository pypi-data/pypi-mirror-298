"""Postgres storage for memories"""

__all__ = ["PostgresMemoryStorage"]

import datetime
import json
from typing import Any, List, Optional

from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

from fixpoint.memory._mem_storage import _ListResponse, MemoryStorage
from fixpoint._storage.sql import ParamNameKind
from fixpoint.memory.protocol import MemoryItem
from .shared import (
    format_cursor,
    parse_cursor,
    new_insert_memory_query,
    new_list_memories_query,
    new_get_memory_query,
)


class PostgresMemoryStorage(MemoryStorage):
    """Store memories in Postgres"""

    _pool: ConnectionPool
    _agent_id: str
    _table: str = "fixpoint.memories"

    def __init__(
        self,
        pool: ConnectionPool,
    ) -> None:
        self._pool = pool

    def insert(self, org_id: str, memory: MemoryItem) -> None:
        """Insert a memory into the storage"""
        query, params = new_insert_memory_query(
            ParamNameKind.POSTGRES, self._table, org_id, memory
        )
        with self._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
            conn.commit()

    def list(
        self, org_id: str, cursor: Optional[str] = None, n: int = 100
    ) -> _ListResponse:
        """Get the list of memories"""
        cursor_obj = parse_cursor(cursor) if cursor else None
        query, params = new_list_memories_query(
            ParamNameKind.POSTGRES, self._table, org_id, n, cursor_obj
        )
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as dbcursor:
                dbcursor.execute(query, params)
                mems: List[MemoryItem] = []
                for row in dbcursor:
                    mems.append(self._load_row(row))
                return _ListResponse(
                    memories=mems,
                    next_cursor=format_cursor(mems) if len(mems) == n else None,
                )

    def get(self, org_id: str, mem_id: str) -> Optional[MemoryItem]:
        """Get a memory item by ID"""
        query, params = new_get_memory_query(
            ParamNameKind.POSTGRES, self._table, org_id, mem_id
        )
        with self._pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                if row:
                    return self._load_row(row)
                return None

    def _load_row(self, row: Any) -> MemoryItem:
        created_at: datetime.datetime = row["created_at"]

        row_dict = {
            "id": row["id"],
            "agent_id": row["agent_id"],
            # Postgres deserializes the json into objects, but the
            # MemoryItem.deserialize method expects strings
            "messages": json.dumps(row["messages"]),
            "completion": json.dumps(row["completion"]),
            "workflow_id": row["workflow_id"],
            "workflow_run_id": row["workflow_run_id"],
            "task_id": row["task_id"],
            "step_id": row["step_id"],
            "metadata": json.dumps(row["metadata"]),
            "created_at": created_at.isoformat(),
        }
        return MemoryItem.deserialize(row_dict)
