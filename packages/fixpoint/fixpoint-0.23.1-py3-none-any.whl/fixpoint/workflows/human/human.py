"""Human in the loop functionality"""

__all__ = [
    "ListHumanTaskEntriesResponse",
    "HumanInTheLoop",
    "SupabaseHumanInTheLoop",
]

from typing import List, Protocol
from psycopg_pool import ConnectionPool

from pydantic import BaseModel, Field
from supabase import Client

from fixpoint.types import ListResponse
from fixpoint.workflows.human.definitions import HumanTaskEntry
from fixpoint.workflows.human.storage_integrations.postres import (
    PostgresHumanTaskStorage,
)


class ListHumanTaskEntriesResponse(ListResponse[HumanTaskEntry]):
    """
    The response from listing human task entries
    """

    data: List[HumanTaskEntry] = Field(description="The list of human task entries")


class HumanInTheLoop(Protocol):
    """Human-in-the-loop client"""

    def send_task_entry(
        self,
        org_id: str,
        workflow_id: str,
        workflow_run_id: str,
        task_id: str,
        data: BaseModel,
    ) -> HumanTaskEntry:
        """Sends a task entry"""

    def get_task_entry(self, org_id: str, task_entry_id: str) -> HumanTaskEntry | None:
        """Retrieves a task"""


class SupabaseHumanInTheLoop(HumanInTheLoop):
    """Human-in-the-loop client that uses Supabase"""

    _db_client: Client

    def __init__(self, db_client: Client) -> None:
        self._db_client = db_client

    def send_task_entry(
        self,
        org_id: str,
        workflow_id: str,
        workflow_run_id: str,
        task_id: str,
        data: BaseModel,
    ) -> HumanTaskEntry:
        """Sends a task entry"""
        task = HumanTaskEntry.from_pydantic_model(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            model=data,
        )
        model_dump = task.model_dump()
        self._db_client.table("task_entries").insert(model_dump).execute()
        return task

    def get_task_entry(self, org_id: str, task_entry_id: str) -> HumanTaskEntry | None:
        """Retrieves a task"""
        response = (
            self._db_client.table("task_entries")
            .select("*")
            .eq("id", task_entry_id)
            .execute()
        )
        if len(response.data) == 0:
            return None
        task = HumanTaskEntry(**response.data[0])
        return task


class PostgresHumanInTheLoop(HumanInTheLoop):
    """Human-in-the-loop client that uses Supabase"""

    _pool: ConnectionPool

    def __init__(self, pool: ConnectionPool) -> None:
        self._pool = pool

    def send_task_entry(
        self,
        org_id: str,
        workflow_id: str,
        workflow_run_id: str,
        task_id: str,
        data: BaseModel,
    ) -> HumanTaskEntry:
        """Sends a task entry"""
        task = HumanTaskEntry.from_pydantic_model(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            model=data,
        )
        PostgresHumanTaskStorage(self._pool).create(org_id, task)
        return task

    def get_task_entry(self, org_id: str, task_entry_id: str) -> HumanTaskEntry | None:
        """Retrieves a task"""
        return PostgresHumanTaskStorage(self._pool).get(org_id, task_entry_id)
