"""Protocols shared across the package"""

__all__ = ["WorkflowStatus", "NodeInfo"]

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, computed_field

from fixpoint.constants import TASK_MAIN_ID, STEP_MAIN_ID


class WorkflowStatus(Enum):
    """The status of a node within the workflow"""

    RUNNING = "RUNNING"  # OPEN
    SUSPENDED = "SUSPENDED"  # OPEN
    FAILED = "FAILED"  # CLOSED
    CANCELLED = "CANCELLED"  # CLOSED
    COMPLETED = "COMPLETED"  # CLOSED
    TERMINATED = "TERMINATED"  # CLOSED
    TIMED_OUT = "TIMED_OUT"  # CLOSED
    CONTINUED_AS_NEW = "CONTINUED_AS_NEW"  # CLOSED


class NodeInfo(BaseModel):
    """
    Each task or step in a workflow run is a "node". This keeps track of which
    node the workflow run is in.
    """

    task: str = Field(description="The task that the node is in", default=TASK_MAIN_ID)
    step: str = Field(description="The step that the node is in", default=STEP_MAIN_ID)
    status: Optional[WorkflowStatus] = Field(
        description="The status of the node", default=WorkflowStatus.RUNNING
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> str:
        """The node's identifier within the workflow run"""
        return f"{self.task}/{self.step}"
