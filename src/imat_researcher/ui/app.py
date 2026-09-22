"""The styled Gradio interface: ask, clarify, then research."""

from collections.abc import AsyncIterator

import gradio as gr

from imat_researcher.manager import ResearchManager
from imat_researcher.models import ClarifiedAnswer
from imat_researcher.ui.styles import CSS, EXAMPLES, HEADER_HTML, JS

# Gradio needs its components declared up front, so we keep a fixed pool of
# question boxes and reveal only as many as the clarifier actually asks for.
MAX_QUESTIONS = 3


async def start_clarification(query: str):
    """Phase one: ask the clarifier what it needs to know, and show those questions."""
    query = (query or "").strip()
    hidden = [gr.update(visible=False, value="") for _ in range(MAX_QUESTIONS)]

    if not query:
        yield ("Enter a research question to get started.", gr.update(visible=False), *hidden, [])
        return

    yield ("Working out what to ask you…", gr.update(visible=False), *hidden, [])

    plan = await ResearchManager().clarify(query)
    questions = plan.questions[:MAX_QUESTIONS]

    boxes = []
    for index in range(MAX_QUESTIONS):
        if index < len(questions):
            asked = questions[index]
            boxes.append(
                gr.update(visible=True, value="", label=asked.question, info=asked.why)
            )
        else:
            boxes.append(gr.update(visible=False, value=""))

    yield ("", gr.update(visible=True), *boxes, [asked.question for asked in questions])


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

        with gr.Group(visible=False, elem_id="dr-clarify") as clarify_group:
            gr.HTML(
                '<div class="dr-clarify-label">A few questions first '
                '<span>Answer what you can &mdash; blanks are fine</span></div>'
            )
            question_boxes = [
                gr.Textbox(visible=False, lines=1, elem_classes="dr-question")
                for _ in range(MAX_QUESTIONS)
            ]
            research_button = gr.Button(
                "Start research", variant="primary", elem_id="dr-go"
            )

        asked_state = gr.State([])

        gr.HTML('<div class="dr-examples-label">Try one</div>')
        gr.Examples(examples=EXAMPLES, inputs=query_textbox, elem_id="dr-examples")

        report = gr.Markdown(elem_id="dr-report")

        clarify_outputs = [status, clarify_group, *question_boxes, asked_state]
        clarify_button.click(start_clarification, query_textbox, clarify_outputs)
        query_textbox.submit(start_clarification, query_textbox, clarify_outputs)

        research_button.click(
            run_research,
            inputs=[query_textbox, asked_state, *question_boxes],
            outputs=report,
        )

    return ui


def launch(**kwargs) -> None:
    build_ui().launch(css=CSS, js=JS, theme=gr.themes.Base(), **kwargs)
