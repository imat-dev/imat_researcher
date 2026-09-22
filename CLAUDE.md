# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Dependencies and the package itself are managed with `uv` (Python 3.12, src-layout, hatchling backend).

```bash
uv sync                          # install deps + the package in editable mode
uv run imat-researcher           # launch the styled Gradio UI
uv run imat-researcher --simple  # launch the bare-bones UI (same pipeline)
uv run imat-researcher --port 7861 --log-level DEBUG
uv run python -m imat_researcher # equivalent to the console script
uv add <package>                 # add a dependency
```

`uv sync` must have been run at least once before imports resolve — the code lives under `src/` and
is only importable via the editable install, not from the working directory.

There are no tests. Ruff config lives in `pyproject.toml` but ruff is not a declared dependency;
`uvx ruff check src` runs it without installing.

## The `agents` name collision

The OpenAI Agents SDK package is itself named `agents` (`from agents import Agent, Runner`). This
project also has an `imat_researcher.agents` subpackage. That is safe **only** because the
subpackage is nested — never create a top-level `agents/` directory or put `src/` itself on
`sys.path`, or every `from agents import ...` will resolve to this project instead of the SDK and
the app will break. Inside `src/imat_researcher/agents/*.py`, `from agents import Agent` is an
absolute import that reaches the SDK; sibling modules are imported by full path
(`from imat_researcher.models import ...`), never relatively.

## Architecture

A "deep research" pipeline: a clarifier agent puts a few questions to the user, the answers narrow
the brief, that brief fans out into parallel web searches, the summaries are written up as a
report, and the report is emailed or pushed.

```
src/imat_researcher/
├── manager.py        ResearchManager — the orchestrator, start here
├── config.py         Settings, read from the environment exactly once
├── models.py         Pydantic contracts between pipeline stages
├── notifications.py  SMTP + Pushover delivery mechanics
├── agents/           One agent per file, each a cached build_*_agent() factory
└── ui/               Gradio front-ends (app.py styled, simple.py bare) + styles.py
```

**The flow is two-phase, because the clarifier has to wait for the user.** `ResearchManager.clarify()`
is a separate call the UI makes *first*; `run()` then takes the answers. Keeping clarification out
of `run()` is what preserves the streaming contract below — do not fold it in.

**Researchability is gated in two places.** `looks_like_a_query()` is a cheap local screen that
rejects only definite junk (too short, no letters) so obvious nonsense never costs an API call;
the clarifier then returns `is_researchable` with a `rejection` sentence for anything that reads
like a request but cannot be researched. When either says no, the UI leaves the clarification
panel hidden, which makes the *Start research* button unreachable rather than merely disabled.
`run()` re-checks locally as well, so bypassing the UI still cannot start a run on junk. The
clarifier prompt is deliberately permissive: vague and broad requests are researchable, since
resolving vagueness is the whole point of the questions.

`ResearchManager.run()` is an **async generator**: each `yield` is a status string that Gradio
streams straight into the output Markdown box, and the final `yield` is the full report. Anything
added to the pipeline must keep that contract — yield a human-readable status, not a data
structure. The whole run is wrapped in `trace("Research trace", trace_id=...)`, and the first
status line hands the user a `platform.openai.com/traces` link for that trace.

`build_brief()` folds the query and the answers into the single string that both the planner and
the writer receive. `run(query)` with no answers still works and yields the bare query — that is
the path `simple.py` uses, which has no clarification step.

Five single-purpose agents, each built by an `@lru_cache`d factory rather than created at import
time — importing a module must not construct an agent or read config:

| Module | Factory | Shape |
| --- | --- | --- |
| [agents/clarifier.py](src/imat_researcher/agents/clarifier.py) | `build_clarifier_agent` | `output_type=ClarificationPlan` — `is_researchable` + `rejection` + `ClarifyingQuestion(question, why)` list |
| [agents/planner.py](src/imat_researcher/agents/planner.py) | `build_planner_agent` | `output_type=WebSearchPlan` — list of `WebSearchItem(query, reason)` |
| [agents/search.py](src/imat_researcher/agents/search.py) | `build_search_agent` | `WebSearchTool()` with `tool_choice="required"`; returns a <300-word summary |
| [agents/writer.py](src/imat_researcher/agents/writer.py) | `build_writer_agent` | `output_type=ReportData(short_summary, markdown_report, follow_up_questions)` |
| [agents/emailer.py](src/imat_researcher/agents/emailer.py) | `build_email_agent` | `send_email_tool` function tool with `tool_choice="required"` |

Searches run concurrently via `asyncio.gather` over `Runner.run(build_search_agent(), ...)`. The
Pydantic models in [models.py](src/imat_researcher/models.py) are the contract between stages, so
changing a field means updating the `ResearchManager` method that consumes it.

Gradio cannot create components dynamically, so [ui/app.py](src/imat_researcher/ui/app.py) keeps a
fixed pool of `MAX_QUESTIONS` textboxes and reveals only as many as the clarifier returns. Every
yield from `start_clarification()` must therefore carry exactly one value per wired output
(`status`, the group, each box, the state) — a mismatched tuple fails at runtime, not import time.

[notifications.py](src/imat_researcher/notifications.py) holds the raw delivery mechanics:
`send_email()` (SMTP + STARTTLS, sends from and to the same `EMAIL_ADDRESS`) and `push()`
(Pushover). `send_email_tool` picks between them based on `USE_EMAIL`, so an unconfigured SMTP
setup can fall back to push notifications; both raise a descriptive `RuntimeError` when their
credentials are missing.

## Configuration

[config.py](src/imat_researcher/config.py) is the single place that touches the environment.
`get_settings()` calls `load_dotenv(override=True)` and is `@lru_cache`d, so `.env` is read once per
process and changes require a restart. Read config through `get_settings()` — do not add
`os.getenv` calls to other modules. `.env` is gitignored; `.env.example` documents the keys.

- `OPENAI_API_KEY` — required; used implicitly by the Agents SDK.
- `DEFAULT_MODEL_NAME` — model for all four agents (default `gpt-5.4-mini`).
- `HOW_MANY_SEARCHES` — number of searches the planner is told to produce (default 5).
- `HOW_MANY_QUESTIONS` — clarifying questions to ask (default 2). The UI shows at most
  `app.MAX_QUESTIONS` (3) of them, so this can be raised to 3 without a code change; past 3 the
  extra questions are never displayed.
- `USE_EMAIL` — truthy sends SMTP mail, otherwise routes to Pushover.
- `EMAIL_ADDRESS`, `EMAIL_SMTP_SERVER`, `EMAIL_SMTP_PORT` (default 587), `EMAIL_APP_PASSWORD`.
- `PUSHOVER_USER`, `PUSHOVER_TOKEN`.
