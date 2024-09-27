import logging
from typing import Literal

from anthropic.lib.bedrock import AsyncAnthropicBedrock

from promptadmin.prompt_service.models.anthropic import AnthropicModelService
from promptadmin.types import ModelServiceInfo
from settings import SETTINGS

logger = logging.getLogger(__name__)


class AnthropicBedrockModelService(AnthropicModelService):
    def __init__(
            self,
            anthropic: AsyncAnthropicBedrock = None,
            prompt_position: Literal['system', 'user'] = None,
            max_tokens: int = None,
            model: str = None,
            temperature: float = None
    ):
        super().__init__(
            anthropic or AsyncAnthropicBedrock(
                aws_secret_key=SETTINGS.prompt_admin_settings.aws_secret_key,
                aws_access_key=SETTINGS.prompt_admin_settings.aws_access_key,
                aws_region=SETTINGS.prompt_admin_settings.aws_region
            ),
            prompt_position,
            max_tokens,
            model or 'anthropic.claude-3-5-sonnet-20240620-v1:0',
            temperature)

    def info(self, _service='anthropic_bedrock') -> ModelServiceInfo:
        return super().info(_service)

    @staticmethod
    def from_info(model_service_info: ModelServiceInfo):
        return AnthropicBedrockModelService(
            prompt_position=model_service_info.config.get('prompt_position'),
            max_tokens=model_service_info.config.get('max_position'),
            model=model_service_info.model,
            temperature=model_service_info.config.get('temperature'),
        )
