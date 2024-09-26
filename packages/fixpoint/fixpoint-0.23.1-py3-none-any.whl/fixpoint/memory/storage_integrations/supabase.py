"""Supabase storage for memories"""

from typing import Optional
from fixpoint._storage import SupabaseStorage
from fixpoint.memory._mem_storage import _ListResponse, MemoryStorage
from fixpoint.memory.protocol import MemoryItem


class SupabaseMemoryStorage(MemoryStorage):
    """Store memories in Supabase"""

    _storage: SupabaseStorage[MemoryItem]
    _agent_id: str

    def __init__(
        self,
        supabase_url: str,
        supabase_api_key: str,
    ) -> None:
        self._storage = SupabaseStorage(
            url=supabase_url,
            key=supabase_api_key,
            table="memories",
            # TODO(dbmikus) what should we do about composite ID columns?
            # Personally, I think we should not use the generic SupabaseStorage
            # class for storing agent memories, and instead pass in an interface
            # that is resource-oriented around these memories
            order_key="agent_id",
            id_column="id",
            value_type=MemoryItem,
        )

    def insert(self, org_id: str, memory: MemoryItem) -> None:
        """Insert a memory into the storage"""
        self._storage.insert(memory)

    def list(
        self, org_id: str, cursor: Optional[str] = None, n: int = 100
    ) -> _ListResponse:
        """Get the list of memories"""
        # TODO(dbmikus) support paginating through memories
        entries = self._storage.fetch_latest()
        return _ListResponse(memories=entries, next_cursor=None)

    def get(self, org_id: str, mem_id: str) -> Optional[MemoryItem]:
        """Get a memory item by ID"""
        return self._storage.fetch(mem_id)
