"""WorkflowRun protocol definition"""

__all__ = ["WorkflowRunData", "WorkflowRunDataclass"]

from typing import Protocol

from pydantic import BaseModel

from fixpoint.protocols import NodeInfo, WorkflowStatus


class WorkflowRunData(Protocol):
    """A simple data container for workflow run info.

    A simple data container for workflow run info. Technically, you could also
    pass in `fixpoint.workflows.WorkflowRun`.

    This class helps avoid circular imports.
    """

    @property
    def id(self) -> str:
        """The workflow run ID"""

    @property
    def workflow_id(self) -> str:
        """The workflow ID"""

    @property
    def status(self) -> WorkflowStatus:
        """The status of the workflow run"""

    @property
    def node_info(self) -> NodeInfo:
        """The currently executing node's info"""


# We cannot inherit from the Protocol also because Pydantic complains about
# different metaclasses
class WorkflowRunDataclass(BaseModel):
    """A dataclass implementation of WorkflowRunData

    Just contains data, doesn't have any ability to change it.
    """

    id: str
    workflow_id: str
    node_info: NodeInfo
    status: WorkflowStatus = WorkflowStatus.RUNNING
