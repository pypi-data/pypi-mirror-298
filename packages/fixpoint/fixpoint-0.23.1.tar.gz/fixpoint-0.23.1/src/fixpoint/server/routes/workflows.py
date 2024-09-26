"""Routes for the workflow data"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from fixpoint._auth import fastapi_auth
from fixpoint.types import WorkflowRunAttemptData
from fixpoint.workflows.imperative.workflow import new_workflow_run_attempt_id
from fixpoint.workflows.imperative._workflow_storage import (
    WorkflowStorage,
    PostgresWorkflowStorage,
)
from ..config import ConfigDep


router = APIRouter(tags=["workflows"])


async def workflow_storage_client(config: ConfigDep) -> WorkflowStorage:
    """The dependency for a workflow storage client"""
    sync_pool = config.db.get_pool()
    async_pool = config.db.get_async_pool()
    if async_pool is None:
        raise RuntimeError("no async database pool")
    return PostgresWorkflowStorage(sync_pool, async_pool)


WorkflowStorageDep = Annotated[WorkflowStorage, Depends(workflow_storage_client)]


@router.get("/workflows/{workflow_id}/runs/{run_id}/attempts/latest")
async def get_latest_workflow_run_attempt(
    authn_info: fastapi_auth.AuthInfoDep,
    workflow_storage: WorkflowStorageDep,
    workflow_id: str,
    run_id: str,
) -> WorkflowRunAttemptData:
    """Get the latest workflow run attempt"""
    data = await workflow_storage.async_get_workflow_run(
        authn_info.org_id(), workflow_id, run_id
    )
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow run attempt not found",
        )
    return data


@router.post("/workflows/{workflow_id}/runs/{run_id}/attempts")
async def create_workflow_run_attempt(
    authn_info: fastapi_auth.AuthInfoDep,
    workflow_storage: WorkflowStorageDep,
    workflow_id: str,
    run_id: str,
) -> WorkflowRunAttemptData:
    """Create a workflow run attempt"""
    attempt_data = WorkflowRunAttemptData(
        attempt_id=new_workflow_run_attempt_id(),
        workflow_id=workflow_id,
        workflow_run_id=run_id,
    )
    await workflow_storage.async_store_workflow_run(authn_info.org_id(), attempt_data)
    return attempt_data
