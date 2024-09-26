"""Type definitions for web research workflows"""

__all__ = ["CitedAnswer", "SiteResearchResult", "MultiSiteQuestions"]

from typing import Literal, List

from pydantic import BaseModel


class MultiSiteQuestions(BaseModel):
    """For each site, a list of questions to ask"""

    sites: List[str]
    questions: List[str]


class AnswerPlainText(BaseModel):
    """A plain text answer to a question"""

    kind: Literal["plain_text"]
    answer: str


class AnswerOneOf(BaseModel):
    """A multiple-choice answer to a question"""

    kind: Literal["one_of"]
    options: List[str]


class CitedAnswer(BaseModel):
    """An answer to a question that is cited from a specific URL."""

    question: str
    answer: str
    cited_url: str
    cited_text: str


class SiteResearchResult(BaseModel):
    """The research results for a set of questions on a website"""

    site: str
    questions: List[str]
    answers: List[CitedAnswer]
