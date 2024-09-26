"""Code for working with an HTML DOM."""

__all__ = ["parse_css_selector_from_untyped", "DOMPathNode", "parse_css_selector"]

from typing import Any, Dict, List, Optional, TypedDict, cast

from fixpoint.agents.oai import AsyncOpenAI


async def parse_css_selector_from_untyped(
    dom_path: List[Dict[str, Any]],
    with_classes: bool = False,
    with_ai: Optional[AsyncOpenAI] = None,
) -> str:
    """Parse a CSS selector from an untyped DOM path list."""
    for elem in dom_path:
        for key in ["tag", "id", "classes", "dataAttributes"]:
            if key not in elem:
                raise ValueError(f"Invalid DOM path node: {elem}")
    return await parse_css_selector(
        cast(List[DOMPathNode], dom_path), with_classes, with_ai
    )


class DOMPathNode(TypedDict):
    """A node in a DOM path."""

    tag: str
    id: str
    classes: List[str]
    dataAttributes: Dict[str, str]


# TODO(dbmikus) run a LLM prompt to optimize the CSS selector
# https://claude.ai/chat/84df7985-9024-446f-a85a-09279ee46fbd
async def parse_css_selector(
    dom_path: List[DOMPathNode],
    with_classes: bool = False,
    with_ai: Optional[AsyncOpenAI] = None,
) -> str:
    """Parse a CSS selector from a DOM path."""
    selector_parts = []
    for node in dom_path:
        part = ""
        # TODO(dbmikus) if a node ID looks auto-generated, use the tag instead
        if node["id"]:
            part = f"#{node['id']}"
        else:
            part = node["tag"]
            if with_classes and node["classes"]:
                part += "." + ".".join(node["classes"])

        selector_parts.append(part)

    if with_ai:
        selector_parts = await _optimize_css_selector(selector_parts, with_ai)

    return " > ".join(selector_parts)


_FIXP_TOKEN = "<FIXPOINT>"


async def _optimize_css_selector(
    selector_parts: List[str],
    oai: AsyncOpenAI,
) -> List[str]:
    selector_lines = "\n".join(selector_parts)
    # pylint: disable=line-too-long
    prompt = f"""Here is a list of CSS selectors. If any ID looks auto-generated (aka it is gibberish and not a descriptive word), replace the whole line with {_FIXP_TOKEN}.

You should print just the final list of selectors, no extra text.

Selectors:
{selector_lines}
"""

    response = await oai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    resp = response.choices[0].message.content
    if not resp:
        raise ValueError("No response from LLM")
    new_parts: List[str] = []
    for line in resp.splitlines():
        line = line.strip()
        if line and line != _FIXP_TOKEN:
            new_parts.append(line)

    return new_parts
