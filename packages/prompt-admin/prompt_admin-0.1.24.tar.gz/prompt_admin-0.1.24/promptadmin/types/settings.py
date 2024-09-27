import os

from pydantic import BaseModel


class PromptAdminSettings(BaseModel):
    router_secret: str = os.getenv('PROMPT_ADMIN_ROUTER_SECRET')
    var_connection: str = os.getenv('PROMPT_ADMIN_VAR_CONNECTION')
    test_rerun_timeout: int = 60 * 60 * 6

    anthropic_key: str | None = os.getenv('PA_ANTHROPIC_KEY')
    aws_secret_key: str | None = os.getenv('AWS_SECRET_KEY')
    aws_access_key: str | None = os.getenv('AWS_ACCESS_KEY')
    aws_region: str | None = os.getenv('AWS_REGION')
    openapi_key: str | None = os.getenv('PA_OPENAI_KEY')


class Settings(BaseModel):
    prompt_admin_settings: PromptAdminSettings = PromptAdminSettings()
