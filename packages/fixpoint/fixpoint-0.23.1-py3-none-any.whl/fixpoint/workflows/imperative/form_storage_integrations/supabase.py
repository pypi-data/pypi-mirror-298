"""Supabase form storage for workflows"""

from typing import List, Optional
from pydantic import BaseModel
from fixpoint._storage import SupportsStorage
from fixpoint.workflows.imperative._form_storage import FormStorage
from fixpoint.workflows.imperative.form import Form


class SupabaseFormStorage(FormStorage):
    """Supabase form storage for workflows"""

    _storage: SupportsStorage[Form[BaseModel]]

    def __init__(self, storage: SupportsStorage[Form[BaseModel]]):
        self._storage = storage

    # pylint: disable=redefined-builtin
    def get(self, org_id: str, id: str) -> Optional[Form[BaseModel]]:
        return self._storage.fetch(id)

    def create(self, org_id: str, form: Form[BaseModel]) -> None:
        self._storage.insert(form)

    def update(self, org_id: str, form: Form[BaseModel]) -> None:
        self._storage.update(form)

    def list(
        self,
        org_id: str,
        path: Optional[str] = None,
        workflow_run_id: Optional[str] = None,
    ) -> List[Form[BaseModel]]:
        conditions = {"workflow_run_id": workflow_run_id}
        if path:
            conditions["path"] = path
        return self._storage.fetch_with_conditions(conditions)
