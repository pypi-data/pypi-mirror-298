"""On-disk memory storage for workflows"""

import sqlite3
from typing import Any, List, Optional

from fixpoint._storage.definitions import MEMORIES_SQLITE_TABLE
from fixpoint._storage.sql import ParamNameKind
from fixpoint.memory._mem_storage import _ListResponse, MemoryStorage
from fixpoint.memory.protocol import MemoryItem
from .shared import (
    format_cursor,
    parse_cursor,
    new_insert_memory_query,
    new_list_memories_query,
    new_get_memory_query,
)


class OnDiskMemoryStorage(MemoryStorage):
    """Store memories on disk"""

    _conn: sqlite3.Connection
    _table: str = "memories"

    def __init__(
        self,
        conn: sqlite3.Connection,
    ) -> None:
        self._conn = conn
        with self._conn:
            self._conn.execute(MEMORIES_SQLITE_TABLE)

    def insert(self, org_id: str, memory: MemoryItem) -> None:
        """Insert a memory into the storage"""
        query, params = new_insert_memory_query(
            ParamNameKind.SQLITE, self._table, org_id, memory
        )
        with self._conn:
            self._conn.execute(query, params)

    def list(
        self, org_id: str, cursor: Optional[str] = None, n: int = 100
    ) -> _ListResponse:
        """Get the list of memories"""
        cursor_obj = parse_cursor(cursor) if cursor else None
        query, params = new_list_memories_query(
            ParamNameKind.SQLITE, self._table, org_id, n, cursor_obj
        )

        with self._conn:
            dbcursor = self._conn.execute(query, params)
            mems: List[MemoryItem] = []
            for row in dbcursor.fetchall():
                mems.append(self._load_row(row))
            return _ListResponse(
                memories=mems,
                next_cursor=format_cursor(mems) if len(mems) == n else None,
            )

    def get(self, org_id: str, mem_id: str) -> Optional[MemoryItem]:
        """Get a memory item by ID"""
        query, params = new_get_memory_query(
            ParamNameKind.SQLITE, self._table, org_id, mem_id
        )
        with self._conn:
            dbcursor = self._conn.execute(query, params)
            row = dbcursor.fetchone()
            if row:
                return self._load_row(row)
            return None

    def _load_row(self, row: Any) -> MemoryItem:
        row_dict = {
            "id": row[0],
            "agent_id": row[1],
            "messages": row[2],
            "completion": row[3],
            "workflow_id": row[4],
            "workflow_run_id": row[5],
            "task_id": row[6],
            "step_id": row[7],
            "metadata": row[8],
            "created_at": row[9],
        }
        return MemoryItem.deserialize(row_dict)
