"""Supabase document storage for workflows"""

from typing import Dict, List, Optional

from fixpoint._storage import SupportsStorage
from fixpoint.constants import NULL_COL_ID
from fixpoint.workflows.imperative._doc_storage import DocStorage, _fix_doc_ids
from fixpoint.workflows.imperative.document import Document


def _transform_fetched_supabase_doc(doc: Document) -> Document:
    if doc.workflow_id == NULL_COL_ID:
        doc.workflow_id = None
    if doc.workflow_run_id == NULL_COL_ID:
        doc.workflow_run_id = None
    doc.id = doc.id.split("/")[-1]
    return doc


class SupabaseDocStorage(DocStorage):
    """Supabase document storage for workflows"""

    _storage: SupportsStorage[Document]

    def __init__(self, storage: SupportsStorage[Document]):
        self._storage = storage

    # pylint: disable=redefined-builtin
    def get(
        self,
        org_id: str,
        id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> Optional[Document]:
        doc_res = self._storage.fetch(
            self._transform_id(id, workflow_id, workflow_run_id)
        )
        if doc_res is None:
            return None
        return _transform_fetched_supabase_doc(doc_res)

    def create(self, org_id: str, document: Document) -> None:
        document = _fix_doc_ids(document)
        document.id = self._transform_id(
            document.id, document.workflow_id, document.workflow_run_id
        )
        self._storage.insert(document)

    def update(self, org_id: str, document: Document) -> None:
        document = _fix_doc_ids(document)
        document.id = self._transform_id(
            document.id, document.workflow_id, document.workflow_run_id
        )
        self._storage.update(document)

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
        task: Optional[str] = None,
        step: Optional[str] = None,
    ) -> List[Document]:
        conditions: Dict[str, str] = {}
        if workflow_id:
            conditions["workflow_id"] = workflow_id
        if workflow_run_id:
            conditions["workflow_run_id"] = workflow_run_id
        if path:
            conditions["path"] = path
        if task:
            conditions["task"] = task
        if step:
            conditions["step"] = step
        docs_list = self._storage.fetch_with_conditions(conditions)
        return [_transform_fetched_supabase_doc(doc) for doc in docs_list]

    def _transform_id(
        self,
        id: str,
        workflow_id: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> str:
        if workflow_id is None:
            workflow_id = NULL_COL_ID
        if workflow_run_id is None:
            workflow_run_id = NULL_COL_ID
        return f"{workflow_id}/{workflow_run_id}/{id}"
