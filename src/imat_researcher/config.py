"""Process-wide settings, loaded once from the environment."""

from dataclasses import dataclass
from functools import lru_cache
import os

from dotenv import load_dotenv


def _flag(name: str, default: str) -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    model_name: str
    how_many_searches: int
    use_email: bool
    email_address: str | None
    email_smtp_server: str | None
    email_smtp_port: int
    email_app_password: str | None
    pushover_user: str | None
    pushover_token: str | None

    @property
    def email_configured(self) -> bool:
        return all((self.email_address, self.email_smtp_server, self.email_app_password))

    @property
    def pushover_configured(self) -> bool:
        return all((self.pushover_user, self.pushover_token))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Read .env and the environment once; cached for the life of the process."""
    load_dotenv(override=True)
    return Settings(
        model_name=os.getenv("DEFAULT_MODEL_NAME", "gpt-5.4-mini"),
        how_many_searches=int(os.getenv("HOW_MANY_SEARCHES", "5")),
        use_email=_flag("USE_EMAIL", "true"),
        email_address=os.getenv("EMAIL_ADDRESS"),
        email_smtp_server=os.getenv("EMAIL_SMTP_SERVER"),
        email_app_password=os.getenv("EMAIL_APP_PASSWORD"),
        email_smtp_port=int(os.getenv("EMAIL_SMTP_PORT", "587")),
        pushover_user=os.getenv("PUSHOVER_USER"),
        pushover_token=os.getenv("PUSHOVER_TOKEN"),
    )
