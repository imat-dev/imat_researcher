"""The styled Gradio interface: ask, clarify, then research."""

from collections.abc import AsyncIterator
from html import escape

import gradio as gr

from imat_researcher.manager import ResearchManager, looks_like_a_query
from imat_researcher.models import ClarifiedAnswer
from imat_researcher.ui.styles import CSS, EXAMPLES, HEADER_HTML, JS

# Gradio needs its components declared up front, so we keep a fixed pool of
# question slots and reveal only as many as the clarifier actually asks for.
MAX_QUESTIONS = 3

# The question and its rationale are rendered as our own markup rather than as
# Gradio's label/info, so the typography is ours to control.
QUESTION_HTML = """
<div class="dr-q">
    <p class="dr-q-text">{question}</p>
    <p class="dr-q-why">{why}</p>
</div>
"""

NOTICE_HTML = '<div class="dr-notice">{message}</div>'


async def start_clarification(query: str):
    """Phase one: ask the clarifier what it needs to know, and show those questions."""
    query = (query or "").strip()
    blank_prompts = [gr.update(visible=False, value="") for _ in range(MAX_QUESTIONS)]
    blank_boxes = [gr.update(visible=False, value="") for _ in range(MAX_QUESTIONS)]

    def notice(message: str):
        """Say why we are not proceeding, with the questionnaire left hidden."""
        return (
            NOTICE_HTML.format(message=escape(message)),
            gr.update(visible=False),
            *blank_prompts,
            *blank_boxes,
            [],
        )

    if not query:
        yield notice("Enter a research question to get started.")
        return

    if not looks_like_a_query(query):
        yield notice("That does not look like a research question. Try a topic or a question.")
        return

    yield (
        "Working out what to ask you…",
        gr.update(visible=False),
        *blank_prompts,
        *blank_boxes,
        [],
    )

    plan = await ResearchManager().clarify(query)

    # Not researchable: leave the panel hidden, so Start research is unreachable.
    if not plan.is_researchable:
        yield notice(plan.rejection or "That is not something I can research. Try a topic instead.")
        return

    questions = plan.questions[:MAX_QUESTIONS]

    prompts, boxes = [], []
    for index in range(MAX_QUESTIONS):
        if index < len(questions):
            asked = questions[index]
            prompts.append(
                gr.update(
                    visible=True,
                    value=QUESTION_HTML.format(
                        question=escape(asked.question), why=escape(asked.why)
                    ),
                )
            )
            boxes.append(gr.update(visible=True, value=""))
        else:
            prompts.append(gr.update(visible=False, value=""))
            boxes.append(gr.update(visible=False, value=""))

    yield (
        "" if questions else NOTICE_HTML.format(
            message="No clarification needed — go ahead and research it."
        ),
        gr.update(visible=True),
        *prompts,
        *boxes,
        [asked.question for asked in questions],
    )


async def run_research(query: str, questions: list[str], *answers: str) -> AsyncIterator[str]:
    """Phase two: research the query, narrowed by whichever questions were answered."""
    clarifications = [
        ClarifiedAnswer(question=question, answer=answer.strip())
        # fewer questions than boxes is normal, so truncating to the shorter is intended
        for question, answer in zip(questions, answers, strict=False)
        if answer and answer.strip()
    ]
    async for status_update in ResearchManager().run(query, clarifications):
        yield status_update


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Imat Deep Research") as ui:
        gr.HTML(HEADER_HTML)

        with gr.Row(elem_classes="dr-query-row"):
            query_textbox = gr.Textbox(
                placeholder="Type a research question...",
                show_label=False,
                container=False,
                autofocus=True,
                elem_id="dr-query",
                scale=5,
            )
            clarify_button = gr.Button(
                "Continue", variant="primary", elem_id="dr-run", scale=1
            )

        status = gr.Markdown("", elem_id="dr-status")

        with gr.Column(visible=False, elem_id="dr-clarify") as clarify_panel:
            gr.HTML(
                '<div class="dr-clarify-head">'
                "<h2>A few questions first</h2>"
                "<p>Answer what you can &mdash; blanks are fine.</p>"
                "</div>"
            )

            prompts, question_boxes = [], []
            for _ in range(MAX_QUESTIONS):
                with gr.Column(elem_classes="dr-qitem"):
                    prompts.append(gr.HTML(visible=False))
                    question_boxes.append(
                        gr.Textbox(
                            visible=False,
                            show_label=False,
                            container=False,
                            lines=1,
                            max_lines=3,
                            placeholder="Your answer",
                            elem_classes="dr-answer",
                        )
                    )

            with gr.Row(elem_classes="dr-actions"):
                research_button = gr.Button(
                    "Start research", variant="primary", elem_id="dr-go"
                )

        asked_state = gr.State([])

        gr.HTML('<div class="dr-examples-label">Try one</div>')
        gr.Examples(examples=EXAMPLES, inputs=query_textbox, elem_id="dr-examples")

        report = gr.Markdown(elem_id="dr-report")

        clarify_outputs = [status, clarify_panel, *prompts, *question_boxes, asked_state]
        clarify_button.click(start_clarification, query_textbox, clarify_outputs)
        query_textbox.submit(start_clarification, query_textbox, clarify_outputs)

        # Hide the questionnaire first, then research. The answers are read by
        # the second step from the (now hidden) boxes, which keep their values.
        research_button.click(
            lambda: (gr.update(visible=False), ""),
            outputs=[clarify_panel, status],
        ).then(
            run_research,
            inputs=[query_textbox, asked_state, *question_boxes],
            outputs=report,
        )

    return ui


def launch(**kwargs) -> None:
    build_ui().launch(css=CSS, js=JS, theme=gr.themes.Base(), **kwargs)
