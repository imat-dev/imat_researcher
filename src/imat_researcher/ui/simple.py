"""A bare-bones Gradio interface over the same pipeline, useful for debugging."""

from collections.abc import AsyncIterator

import gradio as gr

from imat_researcher.manager import ResearchManager


async def run(query: str) -> AsyncIterator[str]:
    async for status_update in ResearchManager().run(query):
        yield status_update


def build_ui() -> gr.Blocks:
    with gr.Blocks() as ui:
        query_textbox = gr.Textbox(label="What topic would you like to research?")
        run_button = gr.Button("Run", variant="primary")
        report = gr.Markdown(label="Report")

        run_button.click(run, inputs=query_textbox, outputs=report)
        query_textbox.submit(run, inputs=query_textbox, outputs=report)

    return ui


def launch(**kwargs) -> None:
    build_ui().launch(theme=gr.themes.Default(primary_hue="sky"), **kwargs)
