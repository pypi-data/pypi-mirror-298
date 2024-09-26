"""FastAPI server for Fixpoint"""

from contextlib import asynccontextmanager
import json
import os
from typing import Optional, Union, AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from fixpoint.workflows.human.definitions import (
    HumanTaskEntry,
    CreateHumanTaskEntryRequest,
)
from fixpoint.workflows.human.human import ListHumanTaskEntriesResponse
from fixpoint.workflows.human.storage_integrations.postres import (
    PostgresHumanTaskStorage,
)
from fixpoint.workflows.imperative.document import (
    Document,
    CreateDocumentRequest,
    ListDocumentsResponse,
)
from fixpoint.workflows.imperative.document_storage_integrations.postgres import (
    PostgresDocStorage,
)
from fixpoint._auth import fastapi_auth
from fixpoint._auth.checkers import propel_auth_checker
from .endpoints.webresearcher import register_scrape_sites
from .config import Config, ConfigSingleton, get_config
from .routes.callcache import router as callcache_router
from .routes.workflows import router as workflows_router


def create_app(config: Optional[Config] = None) -> FastAPI:
    """Create the FastAPI app"""
    dotenv_path = os.environ.get("ENV_FILEPATH", ".env.local")
    load_dotenv(dotenv_path=dotenv_path)

    if config is not None:
        ConfigSingleton.set(config)
    config = ConfigSingleton.get()

    @asynccontextmanager
    async def lifespan(
        app: FastAPI,  # pylint: disable=unused-argument
    ) -> AsyncGenerator[None, None]:
        sync_pool = config.db.get_pool()
        sync_pool.open()
        async_pool = config.db.get_async_pool()
        if async_pool is not None:
            await async_pool.open()
        yield
        sync_pool.close()
        if async_pool is not None:
            await async_pool.close()

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    authenticator: fastapi_auth.Authenticator
    if config.auth_disabled:
        authenticator = fastapi_auth.SkipAuthenticator()
    else:
        authenticator = fastapi_auth.HeaderAuthenticator(
            auth_checker=propel_auth_checker,
            header_names=["api-key", "x-api-key"],
            additional_headers=["x-org-id"],
        )

    app.add_middleware(
        fastapi_auth.ApiKeyAuthenticationMiddleware,
        authenticator=authenticator,
        public_paths=["/docs", "/openapi.json"],
    )

    doc_storage = PostgresDocStorage(config.db.get_pool())
    human_task_storage = PostgresHumanTaskStorage(config.db.get_pool())

    @app.get("/documents", response_model=ListDocumentsResponse)
    async def list_docs(
        authn_info: fastapi_auth.AuthInfoDep,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        task: Optional[str] = None,
        step: Optional[str] = None,
    ) -> ListDocumentsResponse:
        """Get a list of documents."""
        items = doc_storage.list(
            authn_info.org_id(), path, workflow_id, workflow_run_id, task, step
        )
        return ListDocumentsResponse(data=items, next_page_token=None)

    @app.get("/documents/{doc_id:path}", response_model=Optional[Document])
    async def get_doc_with_id(
        authn_info: fastapi_auth.AuthInfoDep,
        doc_id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Union[Document, None]:
        """Get a document with a given ID."""
        return doc_storage.get(
            authn_info.org_id(), doc_id, workflow_id, workflow_run_id
        )

    @app.post("/documents", response_model=Document)
    async def create_doc(
        authn_info: fastapi_auth.AuthInfoDep,
        doc_req: CreateDocumentRequest,
    ) -> Document:
        """Create a document."""
        doc = Document(**doc_req.model_dump())
        doc_storage.create(authn_info.org_id(), doc)
        return doc

    @app.put("/documents/{doc_id}", response_model=Document)
    async def update_doc(
        authn_info: fastapi_auth.AuthInfoDep,
        doc_id: str,
        doc: Document,
    ) -> Document:
        """Update a document."""
        # Check that the ids match
        if doc.id != doc_id:
            raise HTTPException(status_code=400, detail="Document ID mismatch")

        doc_storage.update(authn_info.org_id(), doc)
        return doc

    @app.get("/human-task-entries", response_model=ListHumanTaskEntriesResponse)
    async def list_human_tasks_entries(
        authn_info: fastapi_auth.AuthInfoDep,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        sampling_size: Optional[int] = None,
        metadata: Optional[str] = None,
    ) -> ListHumanTaskEntriesResponse:
        """Get a list of tasks."""
        metadata_dict = json.loads(metadata) if metadata else None
        items = human_task_storage.list(
            authn_info.org_id(),
            path,
            workflow_id,
            workflow_run_id,
            sampling_size,
            metadata_dict,
        )
        return ListHumanTaskEntriesResponse(data=items, next_page_token=None)

    @app.get(
        "/human-task-entries/{task_entry_id}", response_model=Optional[HumanTaskEntry]
    )
    async def get_human_task_entry(
        authn_info: fastapi_auth.AuthInfoDep, task_entry_id: str
    ) -> Union[HumanTaskEntry, None]:
        """Get a task with a given ID."""
        return human_task_storage.get(authn_info.org_id(), task_entry_id)

    @app.post("/human-task-entries", response_model=HumanTaskEntry)
    async def create_human_task_entry(
        authn_info: fastapi_auth.AuthInfoDep, task_req: CreateHumanTaskEntryRequest
    ) -> HumanTaskEntry:
        """Create a task."""
        # we do this magic so that users cannot pass in an ID field
        task = HumanTaskEntry(**task_req.model_dump())
        human_task_storage.create(authn_info.org_id(), task)
        return task

    @app.put("/human-task-entries/{task_entry_id}", response_model=HumanTaskEntry)
    async def update_human_task_entry(
        authn_info: fastapi_auth.AuthInfoDep,
        task_entry_id: str,
        task_entry: HumanTaskEntry,
    ) -> HumanTaskEntry:
        """Update a human task entry"""
        if task_entry.id != task_entry_id:
            raise HTTPException(status_code=400, detail="Human Task Entry ID mismatch")
        human_task_storage.update(authn_info.org_id(), task_entry)
        return task_entry

    register_scrape_sites(app, "/agents/webresearcher/scrapes", get_config)
    app.include_router(callcache_router)
    app.include_router(workflows_router)

    return app
