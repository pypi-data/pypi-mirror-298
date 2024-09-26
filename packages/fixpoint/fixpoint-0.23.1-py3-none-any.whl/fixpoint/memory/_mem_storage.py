"""Memory storage protocol and implementations."""

__all__ = ["MemoryStorage"]

from dataclasses import dataclass
from typing import List, Protocol, Optional

from .protocol import MemoryItem


@dataclass
class _ListResponse:
    """A list memories response"""

    memories: List[MemoryItem]
    next_cursor: Optional[str] = None


class MemoryStorage(Protocol):
    """Protocol for storing memories"""

    def insert(self, org_id: str, memory: MemoryItem) -> None:
        """Insert a memory into the storage"""

    def list(
        self, org_id: str, cursor: Optional[str] = None, n: int = 100
    ) -> _ListResponse:
        """Get the list of memories"""

    def get(self, org_id: str, mem_id: str) -> Optional[MemoryItem]:
        """Get a memory item by ID"""
