"""The scrape agent performs web scraping research on sites"""

__all__ = [
    "scrape_sites",
    "spawn_scrape_sites",
    "Clients",
    "ResearchResultWithSite",
    "AllResearchResults",
]

from typing import List, Literal, Optional, Type, TypeVar

from pydantic import BaseModel

from fixpoint.workflows import structured
from fixpoint.workflows.structured import (
    WorkflowContext,
    RunConfig,
    WorkflowRunHandle,
)
from fixpoint.completions import ChatCompletionMessageParam
from ._shared import Clients
from ._scrape_agent_json import (
    new_workflow_entrypoint,
    AllResearchResults as AllResearchResultsJson,
    CtxEnv,
)
from ._types import (
    AllResearchResultsPydantic as AllResearchResults,
    ResearchResultWithSitePydantic as ResearchResultWithSite,
)
from .converters import convert_json_to_pydantic

T = TypeVar("T", bound=BaseModel)

SCRAPE_MODE: Literal["llm_extraction", "markdown"] = "markdown"
CRAWL_TYPE: Literal["single_scrape", "crawl_site"] = "single_scrape"


async def spawn_scrape_sites(
    org_id: str,
    run_config: RunConfig,
    clients: Clients,
    workflow_id: str,
    sites: List[str],
    research_schema: Type[T],
    run_id: Optional[str] = None,
    extra_instructions: Optional[List[ChatCompletionMessageParam]] = None,
) -> WorkflowRunHandle[AllResearchResults[T]]:
    """Spawn a workflow to scrape a list of sites and extract the research results.

    Args:
        run_config (RunConfig): Configuration for the workflow run.
        clients (Clients): Client instances for external services.
        workflow_id (str): Unique identifier for the workflow.
        sites (List[str]): List of URLs to scrape.
        research_schema (Type[T]): The expected format of the research results,
            extracted per site.
        run_id (Optional[str]): If you want to retry a workflow run, this is the
            ID of an existing run to respawn.
        extra_instructions (Optional[List[ChatCompletionMessageParam]]):
            Additional instruction messages to prepend to the prompt.

    Returns:
        WorkflowRunHandle[AllResearchResults[T]]: Handle for the spawned workflow run.
    """
    ctx_env = CtxEnv(
        clients=clients,
        research_result_format=research_schema.model_json_schema(),
        prefix_prompt_messages=extra_instructions,
    )

    async def post_proc_to_pydantic(
        _ctx: WorkflowContext, results: AllResearchResultsJson
    ) -> AllResearchResults[T]:
        return convert_json_to_pydantic(research_schema, results)

    entrypoint = new_workflow_entrypoint(
        workflow_id,
        ctx_env,
        post_proc_fn=post_proc_to_pydantic,
    )
    if run_id:
        run_handle = structured.respawn_workflow(
            entrypoint,
            org_id=org_id,
            run_id=run_id,
            run_config=run_config,
            agents=[],
            kwargs={"sites": sites},
        )
    else:
        run_handle = structured.spawn_workflow(
            entrypoint,
            org_id=org_id,
            run_config=run_config,
            agents=[],
            kwargs={"sites": sites},
        )
    return run_handle


async def scrape_sites(
    org_id: str,
    run_config: RunConfig,
    clients: Clients,
    workflow_id: str,
    sites: List[str],
    research_schema: Type[T],
    run_id: Optional[str] = None,
    extra_instructions: Optional[List[ChatCompletionMessageParam]] = None,
) -> AllResearchResults[T]:
    """Scrape a list of sites and extract the research results.

    Args:
        run_config (RunConfig): Configuration for the workflow run.
        clients (Clients): Client instances for external services.
        workflow_id (str): Unique identifier for the workflow.
        sites (List[str]): List of URLs to scrape.
        research_schema (Type[T]): The expected format of the research results,
        extracted per site.
        run_id (Optional[str]): If you want to retry a workflow run, this is the
            ID of an existing run to respawn.
        extra_instructions (Optional[List[ChatCompletionMessageParam]]):
        Additional instruction messages to prepend to the prompt.

    Returns:
        AllResearchResults[T]: Aggregated results from all scraped sites.
    """
    run_handle = await spawn_scrape_sites(
        org_id,
        run_config,
        clients,
        workflow_id,
        sites,
        research_schema,
        run_id,
        extra_instructions,
    )
    return await run_handle.result()
