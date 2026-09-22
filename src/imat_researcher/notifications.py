"""Outbound delivery channels: SMTP email and Pushover."""

import logging
import smtplib
from email.message import EmailMessage

import requests

from imat_researcher.config import get_settings

logger = logging.getLogger(__name__)

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"
REQUEST_TIMEOUT_SECONDS = 10


def send_email(subject: str, text_body: str, html_body: str) -> None:
    """Send the report to the configured address, from that same address."""
    settings = get_settings()
    if not settings.email_configured:
        raise RuntimeError(
            "Email delivery requires EMAIL_ADDRESS, EMAIL_SMTP_SERVER and EMAIL_APP_PASSWORD. "
            "Set USE_EMAIL=false to fall back to Pushover."
        )

    msg = EmailMessage()
    msg["From"] = settings.email_address
    msg["To"] = settings.email_address
    msg["Subject"] = subject
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(settings.email_smtp_server, settings.email_smtp_port) as server:
        server.starttls()
        server.login(settings.email_address, settings.email_app_password)
        server.send_message(msg)

    logger.info("Sent report email: %s", subject)


def push(message: str) -> None:
    """Send a Pushover notification. Used as the fallback when USE_EMAIL is off."""
    settings = get_settings()
    if not settings.pushover_configured:
        raise RuntimeError("Push delivery requires PUSHOVER_USER and PUSHOVER_TOKEN.")

    response = requests.post(
        PUSHOVER_URL,
        data={
            "user": settings.pushover_user,
            "token": settings.pushover_token,
            "message": message,
        },
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    logger.info("Sent push notification (%d chars)", len(message))
