# pylint: disable=missing-function-docstring,missing-class-docstring

"""Command to scrape Reddit posts and run LLM Q&A

Run with:

```
OPENAI_API_KEY=$(cat .env | grep OPENAI_API_KEY | cut -d= -f2) \
    poetry run python -m src.fixpoint_experimental.webresearcher.cmd.reddit_ai
```

If you want to re-run with a specific run ID, set the RUN_ID environment
variable.
"""

import asyncio
import base64
import logging
import os
import pathlib
import sys
import tempfile
from typing import List, Optional

from playwright.async_api import async_playwright, Page
from pydantic import BaseModel

from fixpoint.agents.oai import AsyncOpenAI, AsyncOpenAIClients
from fixpoint.logging import callcache_logger
from fixpoint.utils.messages import umsg
from fixpoint.workflows import structured
from fixpoint.workflows.structured import CacheIgnored, WorkflowContext

from ..dom import parse_css_selector_from_untyped
from ..types import SiteResearchResult


URL = "https://www.reddit.com/r/LocalLLaMA/"
BROWSER_LOGGING_ENABLED = True


oai = AsyncOpenAI(
    agent_id="dom-agent",
    openai_clients=AsyncOpenAIClients.from_api_key(os.environ["OPENAI_API_KEY"]),
)


class ResearchResult(BaseModel):
    posts: List[SiteResearchResult]


@structured.workflow(id="find_reddit_ai_posts")
class FindRedditAIPosts:
    @structured.workflow_entrypoint()
    async def run(
        self, ctx: WorkflowContext, questions: List[str], subreddit_url: str
    ) -> ResearchResult:
        async with async_playwright() as playwright:
            webkit = playwright.webkit
            browser = await webkit.launch()
            context = await browser.new_context()
            page = await context.new_page()
            if BROWSER_LOGGING_ENABLED:
                page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
            result = await self.run_workflow(ctx, page, questions, subreddit_url)
            await browser.close()

            return result

    async def run_workflow(
        self,
        ctx: WorkflowContext,
        page: Page,
        _questions: List[str],
        subreddit_url: str,
    ) -> ResearchResult:
        _css_path = await structured.call(
            ctx,
            init_subreddit_crawl,
            args=[CacheIgnored(page), subreddit_url],
        )

        # now, in a loop, until we have k articles/posts:
        #     get all titles and links
        #     add them to a set (deduplicating based on title)

        # visit each post, and for each post:
        #     detect if the post's top-level contents have text or are links
        #     if it is a link, visit the link and process it
        #     otherwise, just grab the text
        #
        #     take the text, and apply the questions to it

        return ResearchResult(posts=[])


async def playwright_reddit_posts(org_id: str, run_id: Optional[str] = None) -> None:
    """Scrape Reddit posts with Playwright"""
    # TODO(dbmikus) turn questions into type used by InfoGatherer, or into a
    # BaseModel
    questions: List[str] = ["Is this post about LLM agents?"]

    run_config = structured.RunConfig.from_env(
        default_mode="disk",
        env_overrides=structured.RunConfigEnvOverrides(
            storage_path="/tmp/reddit-researcher",
        ),
    )

    kwargs = {
        "subreddit_url": URL,
        "questions": questions,
    }

    if run_id:
        run_handle = structured.respawn_workflow(
            FindRedditAIPosts.run,
            org_id=org_id,
            run_id=run_id,
            run_config=run_config,
            agents=[],
            kwargs=kwargs,
        )
    else:
        run_handle = structured.spawn_workflow(
            FindRedditAIPosts.run,
            org_id=org_id,
            run_config=run_config,
            agents=[],
            kwargs=kwargs,
        )

    run_handle.logger.info("Running workflow: %s", run_handle.workflow_id())

    if run_id:
        run_handle.logger.info("Run ID (respawned): %s", run_handle.workflow_run_id())
    else:
        run_handle.logger.info("Run ID (new): %s", run_handle.workflow_run_id())

    results = await run_handle.result()
    json_result = results.model_dump_json(indent=2)
    run_handle.logger.info("--------\n\n")
    run_handle.logger.info("Results: %s", json_result)


@structured.task(id="init_subreddit_crawl", cache_mode="skip_lookup")
async def init_subreddit_crawl(
    ctx: WorkflowContext,
    page: CacheIgnored[Page],
    subreddit_url: str,
) -> str:
    """Determines the CSS selector for the first post in the subreddit"""
    await page.value.goto(subreddit_url)
    # take a screenshot and save it to a temporary file
    temp_file_name = await structured.call(
        ctx,
        get_screenshot,
        args=[page],
    )

    # ask the LLM for the first post/article title in the screenshot
    first_title = await structured.call(
        ctx,
        get_first_post_title,
        args=[CacheIgnored(temp_file_name)],
    )
    ctx.logger.info('First post title: "%s"', first_title)

    css_path = await structured.call(ctx, get_post_css_path, args=[page, first_title])
    # TODO(dbmikus) in this case, the path is too specific to select all
    # articles.
    # We can combine this CSS selector with our original prompt and ask it to
    # clean up the selector.
    # Something like this:
    # https://claude.ai/chat/b6ed5cb5-a293-49a7-80a8-fdb20890f0aa
    return css_path


@structured.step("get_screenshot")
async def get_screenshot(
    ctx: WorkflowContext,
    page: CacheIgnored[Page],
) -> str:
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        await page.value.screenshot(path=temp_file.name)
        ctx.logger.info(f"Screenshot saved to: {temp_file.name}")
        ctx.workflow_run.docs.store(
            id="subreddit-first-screenshot", contents=temp_file.name
        )
        filename = temp_file.name
    return filename


def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


@structured.step("get_post_title_from_screenshot")
async def get_first_post_title(
    _ctx: WorkflowContext,
    screenshot_tmpfile: CacheIgnored[str],
) -> str:
    image_url = f"data:image/png;base64,{encode_image(screenshot_tmpfile.value)}"

    # TODO(dbmikus) replace this with our wrapper that records memories and
    # inference
    res = await oai.chat.completions.create(
        model="gpt-4o",
        messages=[
            umsg(
                "This is a screenshot of a subreddit homepage. There are a list"
                " of articles/posts in the screenshot. What is the title of the"
                " first article/post?\n"
                "\n"
                "Just give me the title, nothing else."
            ),
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    }
                ],
            },
        ],
    )
    ai_resp = res.choices[0].message.content
    if ai_resp is None:
        raise ValueError("No response from LLM")
    return ai_resp


@structured.step("get_post_xpath", cache_mode="skip_all")
async def get_post_css_path(
    ctx: WorkflowContext,
    page: CacheIgnored[Page],
    first_post_title: str,
) -> str:
    """Determines the CSS path for the first post in the subreddit"""
    ctx.logger.info('Looking up CSS path for post titled: "%s"', first_post_title)
    p = page.value
    loc = p.get_by_text(first_post_title)
    dom_walker_js = _load_dom_walker_js()
    dom_paths = await loc.evaluate_all(dom_walker_js)
    # Print the size of each list in dom_paths using ctx.logger.info
    for i, path in enumerate(dom_paths):
        ctx.logger.info("Path %d size: %d", i + 1, len(path))
    if not dom_paths:
        raise ValueError("No DOM paths found")
    css_selector = await parse_css_selector_from_untyped(dom_paths[1], with_ai=oai)
    ctx.logger.info("Parsed CSS selector: %s", css_selector)

    # TODO(dbmikus) try selecting via the selector, and see if elements are visible. If not,
    # try a different DOM path from the list

    return css_selector


def _load_dom_walker_js() -> str:
    # Get the current file's directory
    current_dir = pathlib.Path(__file__).parent.absolute()

    # Construct the path to dom-walker.js
    dom_walker_path = os.path.join(current_dir.parent, "js", "dom-walker.js")

    # Read the contents of dom-walker.js
    with open(dom_walker_path, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    # Uncomment these if you want callcache debug logs
    logging.basicConfig(stream=sys.stdout)
    callcache_logger.setLevel(logging.DEBUG)

    asyncio.run(
        playwright_reddit_posts(org_id="test_org_id", run_id=os.environ.get("RUN_ID"))
    )
