"""Web Researcher"""

__all__ = [
    "AllResearchResults",
    "AllResearchResultsJson",
    "api",
    "Clients",
    "converters",
    "ResearchResultWithSite",
    "scrape_sites_json",
    "scrape_sites",
    "spawn_scrape_sites_json",
    "spawn_scrape_sites",
]

from ._scrape_agent import (
    scrape_sites,
    spawn_scrape_sites,
    ResearchResultWithSite,
    AllResearchResults,
)
from ._scrape_agent_json import (
    scrape_sites as scrape_sites_json,
    spawn_scrape_sites as spawn_scrape_sites_json,
    AllResearchResults as AllResearchResultsJson,
)
from ._shared import Clients

from . import _api as api
from . import converters
