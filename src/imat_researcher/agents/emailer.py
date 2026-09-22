"""Delivers the finished report, as HTML email or a push notification."""

from functools import lru_cache

from agents import Agent, ModelSettings, function_tool

from imat_researcher.config import get_settings
from imat_researcher.notifications import push, send_email

INSTRUCTIONS = """
You are provided with a detailed report. Use your tool to send an email, converting the report into
a clean, well presented HTML email with an appropriate subject line.
"""


@function_tool
def send_email_tool(subject: str, text_body: str, html_body: str) -> str:
    """
    Send out an email with the given subject and body

    Args:
        subject: The subject of the email
        text_body: The body of the email as plain text
        html_body: The HTML body of the email
    """
    if get_settings().use_email:
        send_email(subject, text_body, html_body)
    else:
        push(f"Subject: {subject}\n\n{text_body}")
    return "Email sent successfully"


@lru_cache(maxsize=1)
def build_email_agent() -> Agent:
    return Agent(
        name="Email Agent",
        instructions=INSTRUCTIONS,
        tools=[send_email_tool],
        model=get_settings().model_name,
        model_settings=ModelSettings(tool_choice="required"),
    )
