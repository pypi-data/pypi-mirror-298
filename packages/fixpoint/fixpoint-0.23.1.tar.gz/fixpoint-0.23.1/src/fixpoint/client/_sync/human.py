"""Synchronous interface for human-in-the-loop tasks."""

__all__ = ["Human"]

from fixpoint.workflows.human.definitions import (
    CreateHumanTaskEntryRequest,
    HumanTaskEntry,
)
from .._common import create_human_task, get_human_task
from ._config import Config


class Human:
    """Synchronous interface for human-in-the-loop tasks."""

    _config: Config
    _task_entries: "_HumanTaskEntries"

    def __init__(self, config: Config):
        self._config = config
        self._task_entries = _HumanTaskEntries(config)

    @property
    def task_entries(self) -> "_HumanTaskEntries":
        """Interface to human-in-the-loop task entries."""
        return self._task_entries


class _HumanTaskEntries:
    _config: Config

    def __init__(self, config: Config):
        self._config = config

    def create(self, task_entry: CreateHumanTaskEntryRequest) -> HumanTaskEntry:
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
                task entry.
        """
        return create_human_task(
            self._config.http_client,
            self._config.core,
            task_entry,
        )

    def get(self, task_entry_id: str) -> HumanTaskEntry:
        """Get a human-in-the-loop task entry by ID.

        Args:
            task_entry_id (str): The ID of the human-in-the-loop task entry to
                retrieve.

        Returns:
            HumanTaskEntry: The human task entry.
        """
        return get_human_task(
            self._config.http_client,
            self._config.core,
            task_entry_id,
        )
