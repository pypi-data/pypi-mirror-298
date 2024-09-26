"""Human task storage for workflows"""

__all__ = ["HumanTaskStorage"]

from typing import List, Optional, Protocol
from fixpoint.workflows.human.definitions import HumanTaskEntry


class HumanTaskStorage(Protocol):
    """Human task storage for workflows"""

    # pylint: disable=redefined-builtin
    def get(
        self,
        org_id: str,
        id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[HumanTaskEntry]:
        """Get the given human task"""

    def create(self, org_id: str, task: HumanTaskEntry) -> None:
        """Create a new human task"""

    def update(self, org_id: str, task: HumanTaskEntry) -> None:
        """Update an existing human task"""

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> List[HumanTaskEntry]:
        """List all human tasks

        If path is provided, list human tasks in the given path.
        """
