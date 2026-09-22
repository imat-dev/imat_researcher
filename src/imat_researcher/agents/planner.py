"""Turns a user query into a plan of web searches."""

from functools import lru_cache

from agents import Agent

from imat_researcher.config import get_settings
from imat_researcher.models import WebSearchPlan

INSTRUCTIONS = """
You are a research assistant. Given a user query, come up with a set of web searches
to perform to best answer the query. Output {how_many} terms to query for.
"""


@lru_cache(maxsize=1)
def build_planner_agent() -> Agent:
    settings = get_settings()
    return Agent(
        name="Planner Agent",
        instructions=INSTRUCTIONS.format(how_many=settings.how_many_searches),
        model=settings.model_name,
        output_type=WebSearchPlan,
    )
