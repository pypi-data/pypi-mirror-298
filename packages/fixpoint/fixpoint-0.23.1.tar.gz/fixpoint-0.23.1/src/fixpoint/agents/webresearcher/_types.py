"""Types for the Web Researcher agent."""

__all__ = [
    "ResearchResultWithSitePydantic",
    "AllResearchResultsPydantic",
    "ResearchResultWithSiteJson",
    "AllResearchResultsJson",
]

from typing import Generic, List, TypeVar, Dict, Any

from pydantic import BaseModel

BM = TypeVar("BM", bound=BaseModel)


class ResearchResultWithSitePydantic(BaseModel, Generic[BM]):
    """Your research results, tagged with the site they came from."""

    site: str
    result: BM


class AllResearchResultsPydantic(BaseModel, Generic[BM]):
    """The research results per site, across all sites."""

    results: List[ResearchResultWithSitePydantic[BM]]


class ResearchResultWithSiteJson(BaseModel):
    """Your research results, tagged with the site they came from."""

    site: str
    result: Dict[str, Any]


class AllResearchResultsJson(BaseModel):
    """The research results per site, across all sites."""

    results: List[ResearchResultWithSiteJson]
