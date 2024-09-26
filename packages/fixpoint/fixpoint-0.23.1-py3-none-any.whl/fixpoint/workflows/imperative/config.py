"""Configuration for imperative workflows

Configuration for imperative workflows, such as setting up storage.
"""

from dataclasses import dataclass
from typing import Callable, List, Optional

import httpx
from pydantic import BaseModel
from psycopg_pool import ConnectionPool, AsyncConnectionPool
from supabase import Client as SupabaseClient

from fixpoint import cache, memory, _storage
from fixpoint.utils.storage import new_sqlite_conn
from fixpoint._constants import DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES
from fixpoint.config import get_env_api_url, DiskPaths
from fixpoint.workflows.human import HumanInTheLoop, SupabaseHumanInTheLoop
from fixpoint.workflows.human._unsupported_client import UnsupportedHumanInTheLoop
from fixpoint.workflows.human.human import PostgresHumanInTheLoop
from .document_storage_integrations.api import (
    ApiDocStorage,
)
from .form_storage_integrations import (
    OnDiskFormStorage,
    SupabaseFormStorage,
    PostgresFormStorage,
)
from .document_storage_integrations import (
    OnDiskDocStorage,
    SupabaseDocStorage,
    PostgresDocStorage,
)
from ._doc_storage import DocStorage
from ._form_storage import FormStorage
from ._workflow_storage import (
    WorkflowStorage,
    InMemWorkflowStorage,
    OnDiskWorkflowStorage,
    PostgresWorkflowStorage,
    ApiWorkflowStorage,
)
from .document import Document
from .form import Form

DEF_CHAT_CACHE_MAX_SIZE = 50000
DEF_CHAT_CACHE_TTL_S = 60 * 60 * 24 * 7


@dataclass
class StorageConfig:
    """Storage configuration for imperative workflows and its agents, etc."""

    forms_storage: Optional[FormStorage]
    docs_storage: Optional[DocStorage]
    workflow_storage: WorkflowStorage
    human_storage: HumanInTheLoop
    agent_cache: Optional[cache.SupportsChatCompletionCache]
    memory_factory: Callable[[str], memory.SupportsMemory]

    @classmethod
    def with_defaults(
        cls,
        chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "StorageConfig":
        """Configure default storage"""
        return cls.with_in_memory(chat_cache_maxsize, chat_cache_ttl_s)

    @classmethod
    def with_supabase(
        cls,
        supabase_url: str,
        supabase_api_key: str,
        pg_pool: ConnectionPool,
        apg_pool: Optional[AsyncConnectionPool],
        chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "StorageConfig":
        """Configure supabase storage"""
        forms_storage = create_form_supabase_storage(supabase_url, supabase_api_key)
        docs_storage = create_docs_postgres_storage(pg_pool)
        workflow_storage = _create_workflow_postgres_storage(pg_pool, apg_pool)

        agent_cache = cache.ChatCompletionTLRUCache(
            maxsize=chat_cache_maxsize,
            ttl_s=chat_cache_ttl_s,
            storage=create_chat_completion_cache_supabase_storage(
                supabase_url, supabase_api_key
            ),
        )

        # pylint: disable=unused-argument
        def memory_factory(agent_id: str) -> memory.SupportsMemory:
            """create memory collections per agent"""
            return memory.SupabaseMemory(
                supabase_url=supabase_url,
                supabase_api_key=supabase_api_key,
            )

        return cls(
            forms_storage=forms_storage,
            docs_storage=docs_storage,
            workflow_storage=workflow_storage,
            human_storage=SupabaseHumanInTheLoop(
                SupabaseClient(supabase_url, supabase_api_key)
            ),
            agent_cache=agent_cache,
            memory_factory=memory_factory,
        )

    @classmethod
    def with_postgres(
        cls,
        pg_pool: ConnectionPool,
        apg_pool: Optional[AsyncConnectionPool],
        _chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        _chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "StorageConfig":
        """Configure Postgres storage"""
        forms_storage = create_forms_postgres_storage(pg_pool)
        docs_storage = create_docs_postgres_storage(pg_pool)
        workflow_storage = _create_workflow_postgres_storage(pg_pool, apg_pool)
        # TODO(dbmikus) support Postgres agent cache
        agent_cache = None
        human_storage = _create_human_postgres_storage(pg_pool)

        # pylint: disable=unused-argument
        def memory_factory(agent_id: str) -> memory.SupportsMemory:
            """create memory collections per agent"""
            return memory.PostgresMemory(pg_pool)

        return cls(
            forms_storage=forms_storage,
            docs_storage=docs_storage,
            workflow_storage=workflow_storage,
            human_storage=human_storage,
            agent_cache=agent_cache,
            memory_factory=memory_factory,
        )

    @classmethod
    def with_disk(
        cls,
        *,
        storage_path: str,
        agent_cache_ttl_s: int,
        agent_cache_size_limit_bytes: int = DEFAULT_DISK_CACHE_SIZE_LIMIT_BYTES,
    ) -> "StorageConfig":
        """Configure disk storage"""
        disk_paths = DiskPaths(storage_path)
        disk_paths.ensure_exists()
        agent_cache_dir = disk_paths.agent_cache
        sqlite_conn = new_sqlite_conn(disk_paths.sqlite_path)
        mem_conn = sqlite_conn
        doc_conn = sqlite_conn
        form_conn = sqlite_conn

        # TODO(dbmikus) support on-disk memory storage
        # https://linear.app/fixpoint/issue/PRO-41/add-on-disk-memory-storage
        def memory_factory(_agent_id: str) -> memory.SupportsMemory:
            """create memory collections per agent"""
            return memory.OnDiskMemory(conn=mem_conn)

        agent_cache = cache.ChatCompletionDiskTLRUCache(
            cache_dir=agent_cache_dir,
            ttl_s=agent_cache_ttl_s,
            size_limit_bytes=agent_cache_size_limit_bytes,
        )

        return cls(
            # TODO(dbmikus) support on-disk storage for forms and docs
            # https://linear.app/fixpoint/issue/PRO-40/add-on-disk-step-and-task-storage-for-workflows
            forms_storage=OnDiskFormStorage(form_conn),
            docs_storage=OnDiskDocStorage(doc_conn),
            workflow_storage=OnDiskWorkflowStorage(sqlite_conn),
            human_storage=UnsupportedHumanInTheLoop(),
            agent_cache=agent_cache,
            memory_factory=memory_factory,
        )

    @classmethod
    def with_in_memory(
        cls,
        chat_cache_maxsize: int = DEF_CHAT_CACHE_MAX_SIZE,
        chat_cache_ttl_s: int = DEF_CHAT_CACHE_TTL_S,
    ) -> "StorageConfig":
        """Configure in-memory storage"""

        def memory_factory(_agent_id: str) -> memory.SupportsMemory:
            """create memory collections per agent"""
            return memory.Memory()

        agent_cache = cache.ChatCompletionTLRUCache(
            maxsize=chat_cache_maxsize,
            ttl_s=chat_cache_ttl_s,
        )

        return cls(
            forms_storage=None,
            docs_storage=None,
            workflow_storage=InMemWorkflowStorage(),
            human_storage=UnsupportedHumanInTheLoop(),
            agent_cache=agent_cache,
            memory_factory=memory_factory,
        )

    @classmethod
    def with_api(
        cls,
        api_key: str,
        api_url: str | None = None,
        http_client: Optional[httpx.Client] = None,
        ahttp_client: Optional[httpx.AsyncClient] = None,
    ) -> "StorageConfig":
        """Configure API storage"""
        if api_url is None:
            api_base_url = get_env_api_url()
        else:
            api_base_url = api_url

        return cls(
            forms_storage=None,
            docs_storage=ApiDocStorage(api_base_url=api_base_url, api_key=api_key),
            workflow_storage=ApiWorkflowStorage(
                api_key, api_url, http_client, ahttp_client
            ),
            # TODO(dbmikus) support API-based human-in-the-loop storage
            human_storage=UnsupportedHumanInTheLoop(),
            agent_cache=None,
            memory_factory=None,  # type: ignore[arg-type]
        )


_def_storage: List[Optional[StorageConfig]] = [None]


def get_default_storage_config() -> StorageConfig:
    """Gets the default storage config singleton"""
    if _def_storage[0] is None:
        storage_cfg = StorageConfig.with_defaults(
            chat_cache_maxsize=DEF_CHAT_CACHE_MAX_SIZE,
            chat_cache_ttl_s=DEF_CHAT_CACHE_TTL_S,
        )
        _def_storage[0] = storage_cfg
        return storage_cfg
    else:
        return _def_storage[0]


def create_form_supabase_storage(
    supabase_url: str, supabase_api_key: str
) -> FormStorage:
    """Create a supabase storage driver for forms"""
    supabase_storage = _storage.SupabaseStorage[Form[BaseModel]](
        url=supabase_url,
        key=supabase_api_key,
        table="forms_with_metadata",
        order_key="id",
        id_column="id",
        value_type=Form[BaseModel],
    )
    return SupabaseFormStorage(supabase_storage)


def create_docs_supabase_storage(
    supabase_url: str, supabase_api_key: str
) -> DocStorage:
    """Create a supabase storage driver for documents"""
    supabase_storage = _storage.SupabaseStorage[Document](
        url=supabase_url,
        key=supabase_api_key,
        table="documents",
        order_key="id",
        id_column="id",
        value_type=Document,
    )
    return SupabaseDocStorage(supabase_storage)


def create_docs_postgres_storage(
    pg_pool: ConnectionPool,
) -> DocStorage:
    """Create a postgres storage driver for documents"""
    return PostgresDocStorage(pg_pool)


def create_forms_postgres_storage(
    pg_pool: ConnectionPool,
) -> FormStorage:
    """Create a postgres storage driver for forms"""
    return PostgresFormStorage(pg_pool)


def _create_workflow_postgres_storage(
    pg_pool: ConnectionPool, apg_pool: Optional[AsyncConnectionPool]
) -> WorkflowStorage:
    """Create a supabase storage driver for workflows"""
    return PostgresWorkflowStorage(pg_pool, apg_pool)


def _create_human_postgres_storage(pg_pool: ConnectionPool) -> HumanInTheLoop:
    """Create a supabase storage driver for human-in-the-loop"""
    return PostgresHumanInTheLoop(pg_pool)


def create_chat_completion_cache_supabase_storage(
    supabase_url: str, supabase_api_key: str
) -> _storage.SupabaseStorage[cache.ChatCompletionTLRUCacheItem[BaseModel]]:
    """Create a supabase storage driver for chat completion caching"""
    return _storage.SupabaseStorage(
        url=supabase_url,
        key=supabase_api_key,
        table="completion_cache",
        order_key="expires_at",
        id_column="key",
        # We cannot not specify the generic type parameter for
        # TLRUCacheItem, because then when we try to do `isinstance(cls,
        # type)`, the class will actually be a `typing.GenericAlias` and not
        # a type (class definition).
        value_type=cache.ChatCompletionTLRUCacheItem,
    )


def create_str_cache_supabase_storage(
    supabase_url: str, supabase_api_key: str
) -> _storage.SupabaseStorage[cache.TLRUCacheItem[str]]:
    """Create a supabase storage driver for chat completion caching"""
    return _storage.SupabaseStorage(
        url=supabase_url,
        key=supabase_api_key,
        table="completion_cache",
        order_key="expires_at",
        id_column="key",
        value_type=cache.TLRUCacheItem[str],
    )


def _create_memory_supabase_storage(
    supabase_url: str,
    supabase_api_key: str,
    agent_id: str,  # pylint: disable=unused-argument
) -> _storage.SupabaseStorage[memory.MemoryItem]:
    """Create a supabase storage driver for agent memories"""
    # TODO(dbmikus) we need to make use of the agent_id
    # We put a id on the agent itself, so do we need an agent_id on the memory?
    # We can either attach agent IDs to the agents or to the memory, or perhaps
    # to both.

    return _storage.SupabaseStorage[memory.MemoryItem](
        url=supabase_url,
        key=supabase_api_key,
        table="memories",
        # TODO(dbmikus) what should we do about composite ID columns?
        # Personally, I think we should not use the generic SupabaseStorage
        # class for storing agent memories, and instead pass in an interface
        # that is resource-oriented around these memories
        order_key="agent_id",
        id_column="id",
        value_type=memory.MemoryItem,
    )
