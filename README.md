# Imat Deep Research

Multi-agent deep research. You ask a question; four agents plan a set of web searches, run them in
parallel, synthesize the findings into a long-form report, and deliver it to your inbox — streaming
progress into a Gradio UI as it goes.

Built on the [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/).

## How it works

```
query
  │
  ├─▶ Planner Agent ──▶ WebSearchPlan (N × {query, reason})
  │
  ├─▶ Search Agent  ──▶ one concurrent run per planned search
  │                     (WebSearchTool, ~300-word summary each)
  │
  ├─▶ Writer Agent  ──▶ ReportData {short_summary, markdown_report, follow_up_questions}
  │
  └─▶ Email Agent   ──▶ HTML email via SMTP, or a Pushover notification
```

`ResearchManager.run()` drives all four stages. It is an async generator: every stage yields a
status line that streams straight into the UI, and the last yield is the finished report. The whole
run is wrapped in a single trace, and the first status line gives you a
`platform.openai.com/traces` link to inspect it.

## Setup

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
cp .env.example .env   # then fill in OPENAI_API_KEY and your delivery credentials
```

`uv sync` installs the dependencies *and* the package itself in editable mode. The code lives under
`src/`, so this step is required before anything imports.

## Usage

```bash
uv run imat-researcher              # styled UI on http://127.0.0.1:7860
uv run imat-researcher --simple     # unstyled UI, same pipeline
uv run imat-researcher --port 7861 --log-level DEBUG
uv run imat-researcher --share      # public Gradio link
uv run python -m imat_researcher    # equivalent to the console script
```

Type a question, press Enter, and watch the status updates land until the report renders.

## Configuration

All settings come from `.env` (see `.env.example`), read once at startup — changes need a restart.

| Variable | Default | Purpose |
| --- | --- | --- |
| `OPENAI_API_KEY` | — | **Required.** Used implicitly by the Agents SDK. |
| `DEFAULT_MODEL_NAME` | `gpt-5.4-mini` | Model for all four agents. |
| `HOW_MANY_SEARCHES` | `5` | How many searches the planner is asked to produce. |
| `USE_EMAIL` | `true` | Truthy sends email; anything else falls back to Pushover. |
| `EMAIL_ADDRESS` | — | Sender *and* recipient — the report is mailed to yourself. |
| `EMAIL_SMTP_SERVER` | — | SMTP host. |
| `EMAIL_SMTP_PORT` | `587` | SMTP port (STARTTLS). |
| `EMAIL_APP_PASSWORD` | — | App password, not your account password. |
| `PUSHOVER_USER` / `PUSHOVER_TOKEN` | — | Credentials for the push fallback. |

Set `USE_EMAIL=false` if you'd rather not configure SMTP; you'll get a push notification instead.
Either channel raises a descriptive error if its credentials are missing.

## Project layout

```
src/imat_researcher/
├── __main__.py       CLI entry point
├── manager.py        ResearchManager — the orchestrator
├── config.py         Settings, read from the environment exactly once
├── models.py         Pydantic contracts between pipeline stages
├── notifications.py  SMTP + Pushover delivery
├── agents/           One agent per file, each a cached build_*_agent() factory
└── ui/               Gradio front-ends (app.py, simple.py) + styles.py
```

Note on naming: the Agents SDK package is *also* called `agents`. The `imat_researcher.agents`
subpackage is safe because it's nested — never create a top-level `agents/` directory or put `src/`
itself on `sys.path`, or every `from agents import ...` will resolve here instead of to the SDK.

## Development

```bash
uvx ruff check src      # lint (configured in pyproject.toml; not a declared dependency)
uv add <package>        # add a dependency
```

There are no tests yet. The src-layout is set up so that a `tests/` directory at the repo root
would import the installed package rather than the source tree.
