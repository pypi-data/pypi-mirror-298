from openg2p_fastapi_common.config import Settings as BaseSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="workflow_test_", env_file=".env", extra="allow"
    )

    openapi_title: str = "Workflow Test"
    openapi_description: str = """
        ***********************************
        Further details goes here
        ***********************************
        """
    openapi_version: str = __version__

