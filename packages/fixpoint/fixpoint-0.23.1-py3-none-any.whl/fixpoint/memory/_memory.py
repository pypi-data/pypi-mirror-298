"""Code for agent memory"""

__all__ = ["Memory", "OnDiskMemory", "SupabaseMemory", "PostgresMemory"]


import sqlite3
from typing import Iterator, List, Optional

from psycopg_pool import ConnectionPool
from pydantic import BaseModel

from fixpoint.constants import NO_AUTH_ORG_ID
from fixpoint._protocols.workflow_run import WorkflowRunData
from fixpoint.completions import ChatCompletionMessageParam, ChatCompletion
from .storage_integrations.supabase import SupabaseMemoryStorage
from .storage_integrations.postgres import PostgresMemoryStorage
from .storage_integrations.on_disk import OnDiskMemoryStorage
from .protocol import SupportsMemory, MemoryItem, MemoryMetadata
from ._mem_storage import MemoryStorage

# TODO(dbmikus) support org_id in memory [PRO-171]
# When we expose memory support from the API and are multi-tenant, we will need
# to segment memories by org_id


class Memory(SupportsMemory):
    """A composable class to add memory to an agent"""

    _memory: List[MemoryItem]
    _storage: Optional[MemoryStorage]

    def __init__(self, storage: Optional[MemoryStorage] = None) -> None:
        self._memory = []
        self._storage = storage

    def store_memory(
        self,
        agent_id: str,
        messages: List[ChatCompletionMessageParam],
        completion: ChatCompletion[BaseModel],
        workflow_run: Optional[WorkflowRunData] = None,
        metadata: Optional[MemoryMetadata] = None,
    ) -> str:
        """Store the memory

        Args:
            messages (List[ChatCompletionMessageParam]): List of message parameters.
            completion (Optional[ChatCompletion]): The completion object, if any.

        Returns:
            str: The ID of the memory item
        """
        mem_item = MemoryItem.from_workflow_run(
            agent_id=agent_id,
            messages=messages,
            completion=completion,
            workflow_run=workflow_run,
            metadata=metadata,
        )
        self._memory.append(mem_item)
        if self._storage is not None:
            self._storage.insert(NO_AUTH_ORG_ID, mem_item)
        return mem_item.id

    def memories(self) -> Iterator[MemoryItem]:
        """Get the list of memories"""
        cursor = None
        if self._storage is not None:
            resp = self._storage.list(NO_AUTH_ORG_ID, cursor=cursor)
            yield from resp.memories
            cursor = resp.next_cursor
            if cursor is None:
                return
        else:
            yield from self._memory

    def get(self, mem_id: str) -> Optional[MemoryItem]:
        """Get a memory item by ID"""
        if self._storage is None:
            for mem in self._memory:
                if mem.id == mem_id:
                    return mem
            return None
        return self._storage.get(NO_AUTH_ORG_ID, mem_id)

    def to_str(self) -> str:
        """Return the formatted string of messages. Useful for printing/debugging"""
        delim = "============================================================"
        lines = []
        for mem in self.memories():
            lines.extend(self._format_single_mem(mem))
            lines.append(delim)
        return "\n".join(lines)

    def _format_single_mem(self, memitem: MemoryItem) -> List[str]:
        """Return the formatted string of a single memory entry"""
        messages = memitem.messages
        completion = memitem.completion
        lines = [f'{m["role"]}: {m["content"]}' for m in messages]
        lines.append(f"assistant: {completion.choices[0].message.content}")
        return lines


class OnDiskMemory(Memory, SupportsMemory):
    """Memories, stored on disk"""

    def __init__(self, conn: sqlite3.Connection) -> None:
        super().__init__(storage=OnDiskMemoryStorage(conn))


class SupabaseMemory(Memory, SupportsMemory):
    """Memories, stored in Supabase"""

    def __init__(self, supabase_url: str, supabase_api_key: str) -> None:
        super().__init__(storage=SupabaseMemoryStorage(supabase_url, supabase_api_key))


class PostgresMemory(Memory, SupportsMemory):
    """Memories, stored in Postgres"""

    def __init__(self, pool: ConnectionPool) -> None:
        super().__init__(storage=PostgresMemoryStorage(pool))


# Check that we implement the protocol
def _check(_c: SupportsMemory) -> None:
    pass


_check(Memory())
