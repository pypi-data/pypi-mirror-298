"""Endpoints for the Web Researcher agent."""

from typing import Callable

from fastapi import FastAPI, Depends
from fixpoint.agents.webresearcher import (
    api as scrape_api,
    Clients as ScrapeClients,
    spawn_scrape_sites_json,
    converters as scrape_converters,
)
from fixpoint._auth import AuthnInfo, fastapi_auth
from fixpoint.workflows.structured import RunConfig
from ..config import Config


def register_scrape_sites(
    app: FastAPI, path: str, get_config: Callable[[], Config]
) -> None:
    """Register the Web Researcher scrape sites POST endpoint"""

    @app.post(path, response_model=scrape_api.ScrapeResult)
    async def scrape_sites(
        authn_info: fastapi_auth.AuthInfoDep,
        request: scrape_api.CreateScrapeRequest,
        config: Config = Depends(get_config),
    ) -> scrape_api.ScrapeResult:
        """Create a site scraping workflow"""
        return await _scrape_sites(authn_info, request, config)


async def _scrape_sites(
    authn_info: AuthnInfo,
    request: scrape_api.CreateScrapeRequest,
    config: Config,
) -> scrape_api.ScrapeResult:
    run_config = RunConfig.with_postgres(
        pg_pool=config.db.get_pool(),
        apg_pool=config.db.get_async_pool(),
    )
    handle = await spawn_scrape_sites_json(
        org_id=authn_info.org_id(),
        run_config=run_config,
        clients=ScrapeClients(
            firecrawl=config.clients.firecrawl,
            openai=config.clients.async_openai,
        ),
        workflow_id=request.workflow_id,
        run_id=request.run_id,
        sites=[str(request.site)],
        research_schema=request.research_schema,
        extra_instructions=request.extra_instructions,
    )
    all_result = await handle.result()
    return scrape_converters.convert_json_to_api(
        handle.workflow_id(),
        handle.workflow_run_id(),
        all_result,
    )
