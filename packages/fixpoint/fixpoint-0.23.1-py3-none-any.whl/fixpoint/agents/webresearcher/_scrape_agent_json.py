"""The scrape agent performs web scraping research on sites"""

__all__ = [
    "scrape_sites",
    "spawn_scrape_sites",
    "Clients",
    "ResearchResultWithSite",
    "AllResearchResults",
    "new_workflow_entrypoint",
    "CtxEnv",
]

import asyncio
import copy
from dataclasses import dataclass
import json
from typing import Any, Dict, List, Literal, Optional, TypeVar, cast

from openai.lib._pydantic import _ensure_strict_json_schema
from openai.types.shared_params.response_format_json_schema import JSONSchema

from fixpoint.agents.oai import AsyncOpenAI
from fixpoint.types import AsyncFunc, Params
from fixpoint.workflows import structured
from fixpoint.workflows.structured import (
    WorkflowContext,
    RunConfig,
    WorkflowRunHandle,
)
from fixpoint.completions import ChatCompletionMessageParam
from ._shared import Clients
from ._types import (
    AllResearchResultsJson as AllResearchResults,
    ResearchResultWithSiteJson as ResearchResultWithSite,
)

SCRAPE_MODE: Literal["llm_extraction", "markdown"] = "markdown"
CRAWL_TYPE: Literal["single_scrape", "crawl_site"] = "single_scrape"


T = TypeVar("T")


@dataclass
class CtxEnv:
    """Context environment (extra variables) for the scrape agent."""

    clients: Clients
    research_result_format: Dict[str, Any]
    prefix_prompt_messages: Optional[List[ChatCompletionMessageParam]] = None
    skip_extra_docs: bool = True


_CTX_ENV_KEY = "__fixpoint_scrape_agent_ctx_env__"


def _get_ctx_env(ctx: WorkflowContext) -> CtxEnv:
    val = ctx.workflow_run.state[_CTX_ENV_KEY]
    if not isinstance(val, CtxEnv):
        raise ValueError("Context environment not properly set")
    return val


def _set_ctx_env(ctx: WorkflowContext, env: CtxEnv) -> None:
    ctx.workflow_run.state[_CTX_ENV_KEY] = env


async def spawn_scrape_sites(
    org_id: str,
    run_config: RunConfig,
    clients: Clients,
    workflow_id: str,
    sites: List[str],
    research_schema: Dict[str, Any],
    run_id: Optional[str] = None,
    extra_instructions: Optional[List[ChatCompletionMessageParam]] = None,
) -> WorkflowRunHandle[AllResearchResults]:
    """Spawn a workflow to scrape a list of sites and extract the research results.

    Args:
        run_config (RunConfig): Configuration for the workflow run.
        clients (Clients): Client instances for external services.
        workflow_id (str): Unique identifier for the workflow.
        sites (List[str]): List of URLs to scrape.
        research_schema (Dict[str, Any]): The expected format (JSON
            schema) of the research results, extracted per site.
        run_id (Optional[str]): If you want to retry a workflow run, this is the
            ID of an existing run to respawn.
        extra_instructions (Optional[List[ChatCompletionMessageParam]]):
            Additional instruction messages to prepend to the prompt.

    Returns:
        WorkflowRunHandle[AllResearchResults]: Handle for the spawned workflow run.
    """
    ctx_env = CtxEnv(
        clients=clients,
        research_result_format=research_schema,
        prefix_prompt_messages=extra_instructions,
    )

    async def no_op_post_proc(
        _ctx: WorkflowContext, res: AllResearchResults
    ) -> AllResearchResults:
        return res

    entrypoint: AsyncFunc[[WorkflowContext, List[str]], AllResearchResults] = (
        new_workflow_entrypoint(
            workflow_id,
            ctx_env,
            post_proc_fn=no_op_post_proc,
        )
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
    research_schema: Dict[str, Any],
    run_id: Optional[str] = None,
    extra_instructions: Optional[List[ChatCompletionMessageParam]] = None,
) -> AllResearchResults:
    """Scrape a list of sites and extract the research results.

    Args:
        run_config (RunConfig): Configuration for the workflow run.
        clients (Clients): Client instances for external services.
        workflow_id (str): Unique identifier for the workflow.
        sites (List[str]): List of URLs to scrape.
        research_schema (Dict[str, Any]): The expected format (JSON
            schema) of the research results, extracted per site.
        run_id (Optional[str]): If you want to retry a workflow run, this is the
            ID of an existing run to respawn.
        extra_instructions (Optional[List[ChatCompletionMessageParam]]):
            Additional instruction messages to prepend to the prompt.

    Returns:
        AllResearchResults: Aggregated results from all scraped sites.
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


def new_workflow_entrypoint(
    workflow_id: str,
    ctx_env: CtxEnv,
    post_proc_fn: AsyncFunc[[WorkflowContext, AllResearchResults], T],
) -> AsyncFunc[Params, T]:
    """Create a new workflow entrypoint for the scrape agent."""

    @structured.workflow(id=workflow_id)
    class _WebAIMultiSite:
        @structured.workflow_entrypoint()
        async def run_wrapper(self, ctx: WorkflowContext, sites: List[str]) -> T:
            """The entrypoint for the workflow"""
            _set_ctx_env(ctx, ctx_env)
            res = await self._run(ctx, sites)
            return await post_proc_fn(ctx, res)

        async def _run(
            self, ctx: WorkflowContext, sites: List[str]
        ) -> AllResearchResults:
            if CRAWL_TYPE == "single_scrape":
                results: AllResearchResults = await structured.call(
                    ctx,
                    # For some reason, the type checker gets mad, but if you
                    # just call `_scrape_all_sites` normally (without
                    # `structured.call`) then it doesn't complain. So silence
                    # the error.
                    _scrape_all_sites,
                    args=[sites, ctx_env.research_result_format],
                )
                return results
            else:
                raise ValueError(f"Crawl type not (yet) supported: {CRAWL_TYPE}")

    return cast(AsyncFunc[Params, T], _WebAIMultiSite.run_wrapper)


@structured.task(id="crawl_all_sites", cache_mode="skip_lookup")
async def _scrape_all_sites(
    ctx: WorkflowContext,
    sites: List[str],
    research_result_format: Dict[str, Any],
) -> AllResearchResults:
    crawl_tasks: List[asyncio.Task[ResearchResultWithSite]] = []
    async with asyncio.TaskGroup() as tg:
        for site in sites:
            crawl_tasks.append(
                tg.create_task(_scrape_and_parse(ctx, site, research_result_format))
            )

    return AllResearchResults(results=[t.result() for t in crawl_tasks])


async def _scrape_and_parse(
    ctx: WorkflowContext, site: str, research_result_format: Dict[str, Any]
) -> ResearchResultWithSite:
    return await _parse_result(
        ctx,
        site,
        await structured.call(ctx, _scrape_site, args=[site]),
        research_result_format,
    )


@structured.task(id="crawl_site")
async def _scrape_site(_ctx: WorkflowContext, site: str) -> Dict[str, Any]:
    ctx_env = _get_ctx_env(_ctx)
    fc = ctx_env.clients.firecrawl
    if SCRAPE_MODE == "llm_extraction":
        result = await fc.scrape_url_async(
            site,
            {
                "extractorOptions": {
                    "extractionPrompt": ctx_env.prefix_prompt_messages,
                    "extractionSchema": ctx_env.research_result_format,
                    "mode": "llm-extraction",
                },
            },
        )
        return cast(Dict[str, Any], result)
    else:
        result = await fc.scrape_url_async(site)
        return {"md": result}


async def _parse_result(
    ctx: WorkflowContext,
    site: str,
    result: Dict[str, Any],
    research_result_format: Dict[str, Any],
) -> ResearchResultWithSite:
    res = await _parse_result_helper(ctx, site, result, research_result_format)
    if "md" in result:
        await structured.call(
            ctx, _store_site_research, args=[result["md"]["markdown"], res]
        )
    return res


async def _parse_result_helper(
    ctx: WorkflowContext,
    site: str,
    result: Dict[str, Any],
    research_result_format: Dict[str, Any],
) -> ResearchResultWithSite:
    if "md" in result:
        res = await _parse_md_result(ctx, result, research_result_format)
        return ResearchResultWithSite(site=site, result=res)
    else:
        return _parse_llm_extraction_result(site, result, research_result_format)


async def _parse_md_result(
    ctx: WorkflowContext, result: Dict[str, Any], research_result_format: Dict[str, Any]
) -> Dict[str, Any]:
    md = result["md"]["markdown"]
    parsed: Dict[str, Any] = await structured.call(
        ctx, _parse_md_with_llm, args=[md, research_result_format]
    )
    return parsed


@structured.step("parse_md_with_llm")
async def _parse_md_with_llm(
    _ctx: WorkflowContext, md: str, research_result_format: Dict[str, Any]
) -> Dict[str, Any]:
    ctx_env = _get_ctx_env(_ctx)
    oai: AsyncOpenAI = ctx_env.clients.openai

    messages: List[ChatCompletionMessageParam] = list(
        ctx_env.prefix_prompt_messages or []
    )
    messages.extend(
        [
            {
                "role": "user",
                "content": f"Here is the content:\n\n<content>\n{md}\n</content>",
            },
            {"role": "user", "content": "Now fill in the JSON schema."},
        ]
    )

    completion = await oai.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        response_format={
            "type": "json_schema",
            # This is a plain dict, so OpenAI client gets confused unless we
            # cast it.
            "json_schema": _format_json_schema(research_result_format),
        },
    )
    content = completion.choices[0].message.content
    if not content:
        raise ValueError("No AI inference result")
    parsed: Dict[str, Any] = json.loads(content)
    return parsed


def _format_json_schema(research_result_format: Dict[str, Any]) -> JSONSchema:
    description = research_result_format.get("description", "")
    name = research_result_format.get("title", "")
    # If using strict mode, `additionalProperties: false` must always be set in objects
    # https://platform.openai.com/docs/guides/structured-outputs/additionalproperties-false-must-always-be-set-in-objects
    schema_copy = copy.deepcopy(research_result_format)
    valid_schema = _ensure_strict_json_schema(
        schema_copy,
        path=(),
        root=schema_copy,
    )
    return {
        "name": name,
        "description": description,
        "schema": valid_schema,
        # If we don't set strict mode, the model sometimes outputs results that
        # don't conform to our schema.
        "strict": True,
    }


def _parse_llm_extraction_result(
    site: str, result: Dict[str, Any], research_result_format: Dict[str, Any]
) -> ResearchResultWithSite:
    raise NotImplementedError("Not implemented")


@structured.step("store_site_research")
async def _store_site_research(
    ctx: WorkflowContext, md: str, result: ResearchResultWithSite
) -> None:
    ctx_env = _get_ctx_env(ctx)
    if ctx_env.skip_extra_docs:
        return
    md_doc_id = f"{result.site}:site-content.md"
    results_doc_id = f"{result.site}:research-results.json"
    ctx.workflow_run.docs.store(md_doc_id, md, metadata={"site": result.site})
    ctx.workflow_run.docs.store(
        results_doc_id, json.dumps(result, indent=2), metadata={"site": result.site}
    )
