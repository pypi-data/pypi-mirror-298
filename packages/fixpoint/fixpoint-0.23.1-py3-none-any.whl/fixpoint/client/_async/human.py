"""Asynchronous interface for human-in-the-loop tasks."""

__all__ = ["AsyncHuman"]

from fixpoint.workflows.human.definitions import (
    CreateHumanTaskEntryRequest,
    HumanTaskEntry,
)
from .._common import async_create_human_task, async_get_human_task
from ._config import AsyncConfig


class AsyncHuman:
    """Asynchronous interface for human-in-the-loop tasks."""

    _config: AsyncConfig
    _task_entries: "_AsyncHumanTaskEntries"

    def __init__(self, config: AsyncConfig):
        self._config = config
        self._task_entries = _AsyncHumanTaskEntries(config)

    @property
    def task_entries(self) -> "_AsyncHumanTaskEntries":
        """Interface to human-in-the-loop task entries."""
        return self._task_entries


class _AsyncHumanTaskEntries:
    _config: AsyncConfig

    def __init__(self, config: AsyncConfig):
        self._config = config

    async def create(self, task_entry: CreateHumanTaskEntryRequest) -> HumanTaskEntry:
        """Create a human-in-the-loop task entry.

        Args:
            task_entry (HumanTaskEntry): The task entry containing details for the
                human-in-the-loop task.

        Returns:
            HumanTaskEntry: The created human task entry, which includes the
                task details and any additional information provided by the
                system.

        Raises:
            HTTPException: If there's an error in the HTTP request to create the
                task.
        """
        return await async_create_human_task(
            self._config.http_client,
            self._config.core,
            task_entry,
        )

    async def get(self, task_entry_id: str) -> HumanTaskEntry:
        """Get a human-in-the-loop task entry by ID.

        Args:
            task_entry_id (str): The ID of the human-in-the-loop task entry to retrieve.

        Returns:
            HumanTaskEntry: The human task entry.
        """
        return await async_get_human_task(
            self._config.http_client,
            self._config.core,
            task_entry_id,
        )
