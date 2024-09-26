# pylint: disable=missing-function-docstring,missing-class-docstring

"""Command to answer questions about a set of web pages.

Run with:

```
OPENAI_API_KEY=$(cat .env | grep OPENAI_API_KEY | cut -d= -f2) \
    FIRECRAWL_API_KEY=$(cat .env | grep FIRECRAWL_API_KEY | cut -d= -f2) \
    poetry run python -m src.fixpoint_experimental.webresearcher.cmd.web_ai
```

To run with Supabase:

```
OPENAI_API_KEY=$(cat .env | grep OPENAI_API_KEY | cut -d= -f2) \
    FIRECRAWL_API_KEY=$(cat .env | grep FIRECRAWL_API_KEY | cut -d= -f2) \
    RUN_MODE=supabase \
    SUPABASE_URL=$(supabase status -o env | grep 'API_URL' | cut -d= -f2 | sed s/\"//g) \
    SUPABASE_ANON_KEY=$(supabase status -o env | grep 'ANON_KEY' | cut -d= -f2 | sed s/\"//g) \
    poetry run python -m src.fixpoint_experimental.webresearcher.cmd.web_ai
```

If you want to re-run with a specific run ID, set the RUN_ID environment
variable.
"""

import asyncio
import os
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field

from fixpoint.config import RunMode
from fixpoint.workflows import structured
from fixpoint.workflows.structured import WorkflowRun
from fixpoint.agents.webresearcher import (
    Clients,
    spawn_scrape_sites,
    AllResearchResults,
    ResearchResultWithSite,
)


DEFAULT_RUN_MODE: RunMode = "supabase"


PROMPT = """
You are filling in a JSON schema. There is an "explanation" field in the schema.
Before filling in the rest of the schema, follow these instructions to fill in the "explanation" field:

1. think step-by-step through the information you need to answer the questions
2. Then list the steps and explain your reasoning
3. Fill in the rest of the schema with your answers
"""


class VerticalSaaSCategorization(BaseModel):
    kind: Literal["is_vertical_saas"]

    options: Literal["legal", "finance", "insurance", None] = Field(
        description=(
            "If the company is a vertical SaaS company, select one of the"
            ' options. If none of the options fit, select "None" and suggest an'
            ' "other_option" vertical SaaS category.'
        )
    )
    other_option: Union[str, None] = Field(
        description=(
            "if the company is a vertical SaaS company but does not match any of the"
            ' available "options", specify a new vertical SaaS category. If the'
            ' other options fit, set this to "None".'
        )
    )


class NotVerticalSaaS(BaseModel):
    kind: Literal["not_vertical_saas"]


class CategorizationStructure(BaseModel):
    explanation: str = Field(
        description=(
            "An explanation of your reasoning for how you filled in the JSON" " schema."
        )
    )
    site_result: Union[VerticalSaaSCategorization, NotVerticalSaaS] = Field(
        description=(
            'If the company is a vertical SaaS company, select the "site_result"'
            " with `kind=is_vertical_saas`. If the company is not a vertical SaaS"
            ' company, select the "site_result" with `kind=not_vertical_saas`.'
        )
    )


class ResearchTask(BaseModel):
    """Answer questions about a website to categorize the SaaS type."""

    answer: CategorizationStructure


class TableRow(BaseModel):
    site: str
    is_vertical_saas: bool
    vertical_saas_category: Optional[str]
    explanation: str


class TableResults(BaseModel):
    table: List[TableRow]


class DocumentReviewTask(BaseModel):
    """A human task for reviewing a document"""

    doc_to_review: str = Field(description="The ID of the document to review")


async def run_workflow(org_id: str, run_id: Optional[str] = None) -> None:
    run_config = structured.RunConfig.from_env(
        default_mode=DEFAULT_RUN_MODE,
        env_overrides=structured.RunConfigEnvOverrides(
            storage_path="/tmp/web-ai-researcher/",
        ),
    )
    clients = Clients.from_env()

    sites = [
        "https://www.harvey.ai/",
        "https://fixpoint.co/",
        "https://www.greenlite.ai/",
        "https://www.trysalient.com/",
        "https://latenthealth.com/",
    ]
    run_handle = await spawn_scrape_sites(
        org_id,
        run_config=run_config,
        clients=clients,
        run_id=run_id,
        workflow_id="web-ai-researcher",
        sites=sites,
        research_schema=ResearchTask,
        extra_instructions=[
            {"role": "system", "content": PROMPT},
        ],
    )

    run_handle.logger.info("Running workflow: %s", run_handle.workflow_id())

    if run_id:
        run_handle.logger.info("Run ID (respawned): %s", run_handle.workflow_run_id())
    else:
        run_handle.logger.info("Run ID (new): %s", run_handle.workflow_run_id())

    results = await run_handle.result()
    json_results = results.model_dump_json(indent=2)
    print("Results")
    print("-" * 80)
    print(json_results)

    store_results_doc(run_handle.workflow_run, results)
    send_human_review_tasks(run_handle.workflow_run, results)


def store_results_doc(
    wfr: WorkflowRun, results: AllResearchResults[ResearchTask]
) -> str:
    doc_id = "research-results.json"
    # TODO(dbmikus) convert this to TSV
    rows: List[TableRow] = []
    for result in results.results:
        rows.append(_get_row(result))
    table = TableResults(table=rows)
    doc = wfr.docs.store(doc_id, table.model_dump_json(indent=2))
    return doc.id


def _get_row(result: ResearchResultWithSite[ResearchTask]) -> TableRow:
    answer = result.result.answer.site_result
    if answer.kind == "is_vertical_saas":
        category: Optional[str] = answer.options
        if category is None:
            category = answer.other_option
    else:
        category = None

    return TableRow(
        site=result.site,
        is_vertical_saas=answer.kind == "is_vertical_saas",
        vertical_saas_category=category,
        explanation=result.result.answer.explanation,
    )


def send_human_review_tasks(
    wfr: WorkflowRun, results: AllResearchResults[ResearchTask]
) -> None:
    for result in results.results:
        row = _get_row(result)
        wfr.human.send_task_entry(
            wfr.org_id,
            "review-ai-web-research",
            row,
        )


if __name__ == "__main__":
    # Uncomment these if you want callcache debug logs
    # import logging
    # import sys
    # from fixpoint.logging import callcache_logger, fc_logger
    # logging.basicConfig(stream=sys.stdout)
    # callcache_logger.setLevel(logging.DEBUG)
    # fc_logger.setLevel(logging.DEBUG)

    asyncio.run(run_workflow(org_id="test_org_id", run_id=os.environ.get("RUN_ID")))
