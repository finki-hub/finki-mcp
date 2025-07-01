from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings.
    """

    APP_TITLE: str = "FINKI Chat Bot Content API"
    APP_DESCRIPTION: str = (
        "API for FINKI Chat Bot, providing external context via MCP."
    )
    API_VERSION: str = "1.0.0"

    HOST: str = "0.0.0.0"  # noqa: S104
    PORT: int = 8808
