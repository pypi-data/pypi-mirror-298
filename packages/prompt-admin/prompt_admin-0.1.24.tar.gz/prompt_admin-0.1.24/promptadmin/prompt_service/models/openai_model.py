import logging
from typing import Literal, Generic

from openai.types.chat import ChatCompletion

from promptadmin.prompt_service.models.abstract_streamer import AbstractStreamer
from promptadmin.prompt_service.models.base_model_service import BaseModelService
from promptadmin.types import ModelResponse, Message, ModelServiceInfo
from promptadmin.types.model_response import T
from settings import SETTINGS
from openai import AsyncOpenAI, NOT_GIVEN

logger = logging.getLogger(__name__)


class OpenaiModelResponse(ModelResponse[T], Generic[T]):
    origin_message: ChatCompletion | None = None
    messages: list[dict[str, str]]


class OpenaiModelService(BaseModelService):
    def __init__(
            self,
            openai: AsyncOpenAI = None,
            prompt_position: Literal['system', 'user'] = None,
            max_tokens: int = None,
            model: str = None,
            temperature: float = None
    ):
        self.openai = openai or AsyncOpenAI(api_key=SETTINGS.prompt_admin_settings.openapi_key)
        self.prompt_position = prompt_position or 'system'
        self.max_tokens = max_tokens or 2048
        self.model = model or 'gpt-4o-mini'
        self.temperature = temperature or NOT_GIVEN

    def info(self) -> ModelServiceInfo:
        return ModelServiceInfo(
            service='openai',
            model=self.model,
            config={
                'max_tokens': self.max_tokens,
                'prompt_position': self.prompt_position,
                'temperature': None if self.temperature is NOT_GIVEN else self.temperature
            }
        )

    @staticmethod
    def from_info(model_service_info: ModelServiceInfo):
        return OpenaiModelService(
            prompt_position=model_service_info.config.get('prompt_position'),
            max_tokens=model_service_info.config.get('max_position'),
            model=model_service_info.model,
            temperature=model_service_info.config.get('temperature'),
        )

    async def execute(
            self,
            prompt: str,
            history: list[Message],
            streamer: AbstractStreamer = None
    ) -> OpenaiModelResponse:
        messages = []
        if self.prompt_position == 'user':
            history.append(Message(content=prompt, role='user'))
        elif self.prompt_position == 'system':
            history = [Message(content=prompt, role='system')] + history

        for message in history:
            if message.role == 'user':
                messages.append({'role': 'user', 'content': message.content})
            if message.role == 'assistant':
                messages.append({'role': 'assistant', 'content': message.content})
            if message.role == 'system':
                messages.append({'role': 'system', 'content': message.content})

        if streamer:
            async with self.openai.beta.chat.completions.stream(
                    max_tokens=self.max_tokens,
                    messages=messages,
                    model=self.model,
                    temperature=self.temperature
            ) as stream:
                async for event in stream:
                    if event.type == 'content.delta':
                        text = event.delta
                        await streamer.stream(text)
                openapi_message = await stream.get_final_completion()
        else:
            openapi_message = await self.openai.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
        return OpenaiModelResponse(
            raw_text=openapi_message.choices[0].message.content,
            origin_message=openapi_message,
            messages=messages
        )
