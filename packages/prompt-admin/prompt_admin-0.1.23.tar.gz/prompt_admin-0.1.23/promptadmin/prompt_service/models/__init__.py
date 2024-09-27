from .anthropic import AnthropicModelService
from .anthropic_bedrok import AnthropicBedrockModelService
from .openai_model import OpenaiModelService
from .base_model_service import BaseModelService
from ...types import ModelServiceInfo


def build_model(model_service_info: ModelServiceInfo) -> BaseModelService:
    if model_service_info.service == 'anthropic':
        return AnthropicModelService.from_info(model_service_info)
    elif model_service_info.service == 'anthropic_bedrock':
        return AnthropicBedrockModelService.from_info(model_service_info)
    elif model_service_info.service == 'openai':
        return OpenaiModelService.from_info(model_service_info)

    raise ValueError()


__all__ = [
    AnthropicModelService,
    build_model
]
