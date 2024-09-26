"""Definitions for human in the loop tasks"""

__all__ = [
    "HumanTaskEntry",
    "CreateHumanTaskEntryRequest",
    "EditableConfig",
    "EntryField",
]

import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel, Field, field_serializer

from fixpoint._utils.ids import make_resource_uuid
from fixpoint.workflows.node_state import WorkflowStatus

BM = TypeVar("BM", bound=BaseModel)


class EditableConfig(BaseModel):
    """
    Configuration for whether a task entry field is editable.
    """

    is_editable: bool = Field(description="Whether the field is editable", default=True)
    is_required: bool = Field(
        description="Whether the field is required", default=False
    )
    human_contents: Any = Field(description="The human contents", default=None)


class EntryField(BaseModel):
    """
    A field in a task entry that can either be editable by a human or
    informational.
    """

    id: str = Field(description="The field id")
    display_name: Optional[str] = Field(description="The display name", default=None)
    description: Optional[str] = Field(description="The description", default=None)
    contents: Optional[Any] = Field(description="The contents", default=None)
    editable_config: EditableConfig = Field(
        description="The editable config",
        default_factory=EditableConfig,
    )


def _new_task_entry_id() -> str:
    """Create a new workflow run id"""
    return make_resource_uuid("ht")


class _HumanTaskEntryBase(BaseModel):
    task_id: str = Field(
        description="The task id (aka the task entry is an instance of this task definition)"
    )
    workflow_id: str = Field(description="The workflow id")
    workflow_run_id: str = Field(description="The workflow run id")
    source_node: Optional[str] = Field(
        description="Node that created the task entry", default=None
    )

    status: str = Field(
        description="The status of the task entry",
        default=WorkflowStatus.SUSPENDED.value,
    )
    entry_fields: List[EntryField] = Field(
        description="The fields of the task entry, which can be informational or editable by humans"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadata for document"
    )

    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The created at timestamp",
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
        description="The updated at timestamp",
    )

    @field_serializer("created_at", "updated_at")
    def _serialize_datetime(self, v: datetime.datetime, _info: Any) -> str:
        return v.isoformat()

    @classmethod
    def _pydantic_model_to_entry_fields(cls, model: BaseModel) -> List[EntryField]:
        """Converts a pydantic model into a list of entry fields"""
        entry_fields = []
        for field_name, field_info in model.model_fields.items():
            field_value = getattr(model, field_name)
            ef = EntryField(
                id=field_name,
                # TODO(jakub): Perhaps making display_name prettier is the solution?
                display_name=None,
                description=field_info.description,
                contents=field_value,
            )
            entry_fields.append(ef)

        return entry_fields


class CreateHumanTaskEntryRequest(_HumanTaskEntryBase):
    """
    Request object for creating a human task entry.
    """

    # We must define this class method on each class because it returns a class
    # instance that is not the base class.
    @classmethod
    def from_pydantic_model(
        cls,
        *,
        task_id: str,
        workflow_id: str,
        workflow_run_id: str,
        model: BaseModel,
        status: WorkflowStatus = WorkflowStatus.SUSPENDED,
    ) -> "CreateHumanTaskEntryRequest":
        """Creates a human task entry from a pydantic model"""
        entry_fields = cls._pydantic_model_to_entry_fields(model)
        return cls(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            entry_fields=entry_fields,
            status=status,
        )


class HumanTaskEntry(_HumanTaskEntryBase):
    """
    A task entry that a human can complete.
    """

    id: str = Field(
        description="The id of task entry", default_factory=_new_task_entry_id
    )

    # We must define this class method on each class because it returns a class
    # instance that is not the base class.
    @classmethod
    def from_pydantic_model(
        cls,
        *,
        task_id: str,
        workflow_id: str,
        workflow_run_id: str,
        model: BaseModel,
        status: WorkflowStatus = WorkflowStatus.SUSPENDED,
    ) -> "HumanTaskEntry":
        """Creates a human task entry from a pydantic model"""
        entry_fields = cls._pydantic_model_to_entry_fields(model)
        return cls(
            task_id=task_id,
            workflow_id=workflow_id,
            workflow_run_id=workflow_run_id,
            entry_fields=entry_fields,
            status=status,
        )

    def to_pydantic_model(self, model_cls: Type[BM]) -> BM:
        """Converts a human task into an instance of the type of the original model"""
        new_data = {
            item.id: item.editable_config.human_contents or item.contents
            # cast to a list so pylint doesn't yell
            for item in list(self.entry_fields)
        }

        return model_cls(**new_data)
