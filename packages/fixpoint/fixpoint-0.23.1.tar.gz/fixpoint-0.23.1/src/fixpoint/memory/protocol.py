"""Protocols for memory"""

__all__ = ["MemoryItem", "SupportsMemory", "MemoryMetadata"]

import datetime
import json
from typing import Iterator, List, Optional, Any, Dict, Protocol, Union

from pydantic import BaseModel, Field, model_serializer

from fixpoint._protocols.workflow_run import WorkflowRunData
from fixpoint._utils.ids import make_resource_uuid
from fixpoint.completions import ChatCompletionMessageParam, ChatCompletion


def new_memory_item_id() -> str:
    """Generate a new memory item ID"""
    return make_resource_uuid("amem")


MemoryMetadata = dict[str, Union[str, int, float, bool]]

_default_created_at_factory = datetime.datetime.utcnow


class MemoryItem(BaseModel):
    """A single memory item"""

    # The ID field is useful when identifying this resource in storage, or in a
    # future HTTP-API
    id: str = Field(default_factory=new_memory_item_id)
    agent_id: str
    messages: List[ChatCompletionMessageParam]
    completion: ChatCompletion[BaseModel]
    embedding: Optional[List[float]] = None
    workflow_id: Optional[str] = None
    workflow_run_id: Optional[str] = None
    task_id: Optional[str] = None
    step_id: Optional[str] = None
    metadata: Optional[MemoryMetadata] = None
    created_at: datetime.datetime = Field(default_factory=_default_created_at_factory)

    @model_serializer
    def serialize(self) -> Dict[str, Any]:
        """Custom serialization logic"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "messages": json.dumps(self.messages),
            "completion": self.completion.serialize_json(),
            "embedding": self.embedding,
            "workflow_id": self.workflow_id,
            "workflow_run_id": self.workflow_run_id,
            "task_id": self.task_id,
            "step_id": self.step_id,
            "metadata": json.dumps(self.metadata) if self.metadata else None,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_workflow_run(
        cls,
        workflow_run: Optional[WorkflowRunData] = None,
        *,
        id: Optional[str] = None,  # pylint: disable=redefined-builtin
        agent_id: str,
        messages: List[ChatCompletionMessageParam],
        completion: ChatCompletion[BaseModel],
        embedding: Optional[List[float]] = None,
        metadata: Optional[MemoryMetadata] = None,
        created_at: Optional[datetime.datetime] = None,
    ) -> "MemoryItem":
        """Create a memory item scoped to a workflow run"""
        if workflow_run is None:
            wf_id = None
            wfr_id = None
            task_id = None
            step_id = None
        else:
            wf_id = workflow_run.workflow_id
            wfr_id = workflow_run.id
            task_id = workflow_run.node_info.task
            step_id = workflow_run.node_info.step

        # TODO(jakub): This is a workaround to fix the issue with pydantic not being able to
        # deserialize the completion. This needs to be fixed in the future.
        dumped_compl = completion.model_dump()
        completion = ChatCompletion[BaseModel].model_validate(obj=dumped_compl)

        return cls(
            id=id or new_memory_item_id(),
            agent_id=agent_id,
            messages=messages,
            completion=completion,
            embedding=embedding,
            metadata=metadata,
            created_at=created_at or _default_created_at_factory(),
            workflow_id=wf_id,
            workflow_run_id=wfr_id,
            task_id=task_id,
            step_id=step_id,
        )

    @classmethod
    def deserialize(cls, data: dict[str, Any]) -> "MemoryItem":
        """Deserialize a dictionary into a TLRUCacheItem"""
        return cls(
            id=data["id"],
            agent_id=data["agent_id"],
            messages=json.loads(data["messages"]),
            completion=ChatCompletion[BaseModel].deserialize_json(data["completion"]),
            workflow_id=data["workflow_id"],
            workflow_run_id=data["workflow_run_id"],
            created_at=datetime.datetime.fromisoformat(data["created_at"]),
            task_id=data["task_id"],
            step_id=data["step_id"],
            metadata=json.loads(data["metadata"]) if data["metadata"] else None,
            embedding=data.get("embedding"),
        )


class SupportsMemory(Protocol):
    """A protocol for adding memory to an agent"""

    def memories(self) -> Iterator[MemoryItem]:
        """Get the list of memories"""

    def store_memory(
        self,
        agent_id: str,
        messages: List[ChatCompletionMessageParam],
        completion: ChatCompletion[BaseModel],
        workflow_run: Optional[WorkflowRunData] = None,
        metadata: Optional[MemoryMetadata] = None,
    ) -> str:
        """Store the memory, returning the memory ID"""

    def get(self, mem_id: str) -> Optional[MemoryItem]:
        """Get a memory item by ID"""

    def to_str(self) -> str:
        """Return the formatted string of messages. Useful for printing/debugging"""
