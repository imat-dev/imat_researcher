"""Synthesizes the search summaries into the final report."""

from functools import lru_cache

from agents import Agent

from imat_researcher.config import get_settings
from imat_researcher.models import ReportData

INSTRUCTIONS = """
You are a senior researcher tasked with writing a cohesive report for a research query.
You will be provided with the original query, and some research.
Generate a comprehensive report based on the research and the query.
The final output should be in markdown format, and it should be lengthy and detailed. Aim
for 5-10 pages of content, at least 1000 words.
"""


@lru_cache(maxsize=1)
def build_writer_agent() -> Agent:
    return Agent(
        name="Writer Agent",
        instructions=INSTRUCTIONS,
        model=get_settings().model_name,
        output_type=ReportData,
    )
