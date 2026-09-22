"""Runs a single web search and summarizes what it finds."""

from functools import lru_cache

from agents import Agent, ModelSettings, WebSearchTool

from imat_researcher.config import get_settings

INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""


@lru_cache(maxsize=1)
def build_search_agent() -> Agent:
    return Agent(
        name="Search Agent",
        instructions=INSTRUCTIONS,
        tools=[WebSearchTool()],
        model=get_settings().model_name,
        model_settings=ModelSettings(tool_choice="required"),
    )
