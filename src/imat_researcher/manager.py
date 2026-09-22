"""Orchestrates the research pipeline: clarify -> plan -> search -> write -> deliver."""

import asyncio
import logging
from collections.abc import AsyncIterator, Sequence

from agents import Runner, gen_trace_id, trace

from imat_researcher.agents import (
    build_clarifier_agent,
    build_email_agent,
    build_planner_agent,
    build_search_agent,
    build_writer_agent,
)
from imat_researcher.models import (
    ClarificationPlan,
    ClarifiedAnswer,
    ReportData,
    WebSearchItem,
    WebSearchPlan,
)

logger = logging.getLogger(__name__)

TRACE_URL = "https://platform.openai.com/traces/trace?trace_id={trace_id}"


def build_brief(query: str, answers: Sequence[ClarifiedAnswer] | None = None) -> str:
    """Fold the user's clarifications into the query the other agents work from."""
    if not answers:
        return f"Query: {query}"

    lines = [f"Query: {query}", "", "The user clarified their request as follows:"]
    lines += [f"- {a.question}\n  {a.answer}" for a in answers]
    lines += [
        "",
        "Treat these clarifications as authoritative; they narrow the request.",
    ]
    return "\n".join(lines)


class ResearchManager:
    """Runs the pipeline for one query, streaming human-readable status as it goes."""

    async def clarify(self, query: str) -> ClarificationPlan:
        """Ask what needs pinning down before researching. Called before `run()`."""
        with trace("Clarification trace", trace_id=gen_trace_id()):
            result = await Runner.run(build_clarifier_agent(), f"Research request: {query}")
        plan: ClarificationPlan = result.final_output
        logger.info("Clarifier produced %d question(s)", len(plan.questions))
        return plan

    async def run(
        self, query: str, answers: Sequence[ClarifiedAnswer] | None = None
    ) -> AsyncIterator[str]:
        """Run the deep research process, yielding status updates then the final report."""
        brief = build_brief(query, answers)
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            yield f"Starting research. Trace: {TRACE_URL.format(trace_id=trace_id)}"

            if answers:
                yield f"Using your {len(answers)} clarification(s), planning searches..."

            search_plan = await self.plan_searches(brief)
            yield f"Searches planned, starting {len(search_plan.searches)} searches..."

            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."

            report = await self.write_report(brief, search_results)
            yield "Report written, sending email..."

            await self.send_email(report)
            yield "Email sent, research complete"

            yield report.markdown_report

    async def plan_searches(self, brief: str) -> WebSearchPlan:
        """Plan the searches to perform for the brief."""
        result = await Runner.run(build_planner_agent(), brief)
        return result.final_output

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Run every planned search concurrently."""
        tasks = [self.search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform a single search."""
        input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(build_search_agent(), input_message)
        return result.final_output

    async def write_report(self, brief: str, search_results: list[str]) -> ReportData:
        """Write the report for the brief."""
        input_message = f"{brief}\n\nSummarized search results: {search_results}"
        result = await Runner.run(build_writer_agent(), input_message)
        return result.final_output

    async def send_email(self, report: ReportData) -> None:
        """Hand the report to the email agent for delivery."""
        await Runner.run(build_email_agent(), report.markdown_report)
