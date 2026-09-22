"""Asks the user a few questions before any searching happens."""

from functools import lru_cache

from agents import Agent

from imat_researcher.config import get_settings
from imat_researcher.models import ClarificationPlan

INSTRUCTIONS = """
You are a research assistant. Before researching a user's request, you ask exactly {how_many}
short questions whose answers would most improve the quality of the research.

Good questions resolve genuine ambiguity in the request. Target whichever of these the query
leaves open: scope and boundaries, time period, geography or market, the depth and audience of
the report, and which specific angle the user actually cares about.

Rules:
- Each question must be answerable in a single sentence. Never ask compound questions.
- Ask about different things; do not rephrase the same question twice.
- Never ask for information you could find by searching the web.
- Never ask the user to do the research for you.
- Phrase questions in plain, direct language, as a helpful colleague would.

For each question, also say briefly why the answer changes how you would research the topic.
"""


@lru_cache(maxsize=1)
def build_clarifier_agent() -> Agent:
    settings = get_settings()
    return Agent(
        name="Clarifier Agent",
        instructions=INSTRUCTIONS.format(how_many=settings.how_many_questions),
        model=settings.model_name,
        output_type=ClarificationPlan,
    )
