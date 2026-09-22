"""The styled Gradio interface."""

from collections.abc import AsyncIterator

import gradio as gr

from imat_researcher.manager import ResearchManager
from imat_researcher.ui.styles import CSS, EXAMPLES, HEADER_HTML, JS


async def run(query: str) -> AsyncIterator[str]:
    async for status_update in ResearchManager().run(query):
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
            run_button = gr.Button(
                "Investigate", variant="primary", elem_id="dr-run", scale=1
            )

        gr.HTML('<div class="dr-examples-label">Try one</div>')
        gr.Examples(examples=EXAMPLES, inputs=query_textbox, elem_id="dr-examples")

        report = gr.Markdown(elem_id="dr-report")

        run_button.click(run, inputs=query_textbox, outputs=report)
        query_textbox.submit(run, inputs=query_textbox, outputs=report)

    return ui


def launch(**kwargs) -> None:
    build_ui().launch(css=CSS, js=JS, theme=gr.themes.Base(), **kwargs)
