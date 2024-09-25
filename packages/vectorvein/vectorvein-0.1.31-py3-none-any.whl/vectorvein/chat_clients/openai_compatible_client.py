# @Author: Bi Ying
# @Date:   2024-07-26 14:48:55
import json
import random
from functools import cached_property
from typing import overload, Generator, AsyncGenerator, Any, Literal, Iterable

import httpx
from openai._streaming import Stream, AsyncStream
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai import OpenAI, AsyncOpenAI, AzureOpenAI, AsyncAzureOpenAI

from .base_client import BaseChatClient, BaseAsyncChatClient
from .utils import (
    cutoff_messages,
    get_message_token_counts,
    ToolCallContentProcessor,
    generate_tool_use_system_prompt,
)
from ..settings import settings
from ..types import defaults as defs
from ..types.enums import ContextLengthControlType, BackendType
from ..types.llm_parameters import (
    NotGiven,
    NOT_GIVEN,
    ToolParam,
    ToolChoice,
    ChatCompletionMessage,
    ChatCompletionDeltaMessage,
)


class OpenAICompatibleChatClient(BaseChatClient):
    DEFAULT_MODEL: str | None = ""
    BACKEND_NAME: BackendType

    def __init__(
        self,
        model: str = "",
        stream: bool = True,
        temperature: float = 0.7,
        context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
        random_endpoint: bool = True,
        endpoint_id: str = "",
        http_client: httpx.Client | None = None,
        **kwargs,
    ):
        super().__init__(
            model,
            stream,
            temperature,
            context_length_control,
            random_endpoint,
            endpoint_id,
            http_client,
            **kwargs,
        )

    @cached_property
    def raw_client(self) -> OpenAI | AzureOpenAI:
        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.endpoint.is_azure:
            return AzureOpenAI(
                azure_endpoint=self.endpoint.api_base,
                api_key=self.endpoint.api_key,
                api_version="2024-08-01-preview",
                http_client=self.http_client,
            )
        else:
            return OpenAI(
                api_key=self.endpoint.api_key,
                base_url=self.endpoint.api_base,
                http_client=self.http_client,
            )

    @overload
    def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: Literal[False] = False,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ) -> ChatCompletionMessage:
        pass

    @overload
    def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: Literal[True] = True,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ) -> Generator[ChatCompletionDeltaMessage, None, None]:
        pass

    @overload
    def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ) -> ChatCompletionMessage | Generator[ChatCompletionDeltaMessage, Any, None]:
        pass

    def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature

        self.model_setting = self.backend_settings.models[self.model]

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        if tools:
            if self.model_setting.function_call_available:
                tools_params = dict(tools=tools, tool_choice=tool_choice)
            else:
                tools_str = json.dumps(tools, ensure_ascii=False, indent=None)
                additional_system_prompt = generate_tool_use_system_prompt(tools=tools_str)
                if messages and messages[0].get("role") == "system":
                    messages[0]["content"] += "\n\n" + additional_system_prompt
                else:
                    messages.insert(0, {"role": "system", "content": additional_system_prompt})
                tools_params = {}
        else:
            tools_params = {}

        if max_tokens is None:
            max_output_tokens = self.model_setting.max_output_tokens
            token_counts = get_message_token_counts(messages=messages, tools=tools, model=self.model_setting.id)
            if max_output_tokens is not None:
                max_tokens = self.model_setting.context_length - token_counts - 64
                max_tokens = min(max(max_tokens, 1), max_output_tokens)
            else:
                max_tokens = self.model_setting.context_length - token_counts - 64

        if response_format and self.model_setting.response_format_available:
            self.response_format = {"response_format": response_format}
        else:
            self.response_format = {}

        if self.stream:
            stream_response: Stream[ChatCompletionChunk] = self.raw_client.chat.completions.create(
                model=self.model_setting.id,
                messages=messages,
                stream=True,
                temperature=self.temperature,
                max_tokens=max_tokens,
                **self.response_format,
                **tools_params,
                **kwargs,
            )

            def generator():
                full_content = ""
                result = {}
                for chunk in stream_response:
                    if len(chunk.choices) == 0:
                        continue
                    if not chunk.choices[0].delta:
                        continue
                    if self.model_setting.function_call_available:
                        if chunk.choices[0].delta.tool_calls:
                            for index, tool_call in enumerate(chunk.choices[0].delta.tool_calls):
                                tool_call.index = index
                        yield ChatCompletionDeltaMessage(**chunk.choices[0].delta.model_dump())
                    else:
                        message = chunk.choices[0].delta.model_dump()
                        full_content += message["content"] if message["content"] else ""
                        if tools:
                            tool_call_data = ToolCallContentProcessor(full_content).tool_calls
                            if tool_call_data:
                                message["tool_calls"] = tool_call_data["tool_calls"]
                        if full_content in ("<", "<|", "<|▶", "<|▶|") or full_content.startswith("<|▶|>"):
                            message["content"] = ""
                            result = message
                            continue
                        yield ChatCompletionDeltaMessage(**message)
                if result:
                    yield ChatCompletionDeltaMessage(**result)

            return generator()
        else:
            response: ChatCompletion = self.raw_client.chat.completions.create(
                model=self.model_setting.id,
                messages=messages,
                stream=False,
                temperature=self.temperature,
                max_tokens=max_tokens,
                **self.response_format,
                **tools_params,
                **kwargs,
            )

            result = {
                "content": response.choices[0].message.content,
                "usage": response.usage.model_dump() if response.usage else None,
            }
            if tools:
                if self.model_setting.function_call_available and response.choices[0].message.tool_calls:
                    result["tool_calls"] = [
                        {**tool_call.model_dump(), "type": "function"}
                        for tool_call in response.choices[0].message.tool_calls
                    ]
                else:
                    tool_call_content_processor = ToolCallContentProcessor(result["content"])
                    tool_call_data = tool_call_content_processor.tool_calls
                    if tool_call_data:
                        result["tool_calls"] = tool_call_data["tool_calls"]
                        result["content"] = tool_call_content_processor.non_tool_content

            return ChatCompletionMessage(**result)


class AsyncOpenAICompatibleChatClient(BaseAsyncChatClient):
    DEFAULT_MODEL: str | None = ""
    BACKEND_NAME: BackendType

    def __init__(
        self,
        model: str = "",
        stream: bool = True,
        temperature: float = 0.7,
        context_length_control: ContextLengthControlType = defs.CONTEXT_LENGTH_CONTROL,
        random_endpoint: bool = True,
        endpoint_id: str = "",
        http_client: httpx.AsyncClient | None = None,
        **kwargs,
    ):
        super().__init__(
            model,
            stream,
            temperature,
            context_length_control,
            random_endpoint,
            endpoint_id,
            http_client,
            **kwargs,
        )

    @cached_property
    def raw_client(self):
        if self.random_endpoint:
            self.random_endpoint = True
            self.endpoint_id = random.choice(self.backend_settings.models[self.model].endpoints)
            self.endpoint = settings.get_endpoint(self.endpoint_id)

        if self.endpoint.is_azure:
            return AsyncAzureOpenAI(
                azure_endpoint=self.endpoint.api_base,
                api_key=self.endpoint.api_key,
                api_version="2024-08-01-preview",
                http_client=self.http_client,
            )
        else:
            return AsyncOpenAI(
                api_key=self.endpoint.api_key,
                base_url=self.endpoint.api_base,
                http_client=self.http_client,
            )

    @overload
    async def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: Literal[False] = False,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ) -> ChatCompletionMessage:
        pass

    @overload
    async def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: Literal[True] = True,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ) -> AsyncGenerator[ChatCompletionDeltaMessage, Any]:
        pass

    @overload
    async def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ) -> ChatCompletionMessage | AsyncGenerator[ChatCompletionDeltaMessage, Any]:
        pass

    async def create_completion(
        self,
        messages: list,
        model: str | None = None,
        stream: bool | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        tools: Iterable[ToolParam] | NotGiven = NOT_GIVEN,
        tool_choice: ToolChoice | NotGiven = NOT_GIVEN,
        response_format: dict | None = None,
        **kwargs,
    ):
        if model is not None:
            self.model = model
        if stream is not None:
            self.stream = stream
        if temperature is not None:
            self.temperature = temperature

        self.model_setting = self.backend_settings.models[self.model]

        if self.context_length_control == ContextLengthControlType.Latest:
            messages = cutoff_messages(
                messages,
                max_count=self.model_setting.context_length,
                backend=self.BACKEND_NAME,
                model=self.model_setting.id,
            )

        if tools:
            if self.model_setting.function_call_available:
                tools_params = dict(tools=tools, tool_choice=tool_choice)
            else:
                tools_str = json.dumps(tools, ensure_ascii=False, indent=None)
                additional_system_prompt = generate_tool_use_system_prompt(tools=tools_str)
                if messages and messages[0].get("role") == "system":
                    messages[0]["content"] += "\n\n" + additional_system_prompt
                else:
                    messages.insert(0, {"role": "system", "content": additional_system_prompt})
                tools_params = {}
        else:
            tools_params = {}

        if response_format and self.model_setting.response_format_available:
            self.response_format = {"response_format": response_format}
        else:
            self.response_format = {}

        if max_tokens is None:
            max_output_tokens = self.model_setting.max_output_tokens
            token_counts = get_message_token_counts(messages=messages, tools=tools, model=self.model_setting.id)
            if max_output_tokens is not None:
                max_tokens = self.model_setting.context_length - token_counts - 64
                max_tokens = min(max(max_tokens, 1), max_output_tokens)
            else:
                max_tokens = self.model_setting.context_length - token_counts - 64

        if self.stream:
            stream_response: AsyncStream[ChatCompletionChunk] = await self.raw_client.chat.completions.create(
                model=self.model_setting.id,
                messages=messages,
                stream=self.stream,
                temperature=self.temperature,
                max_tokens=max_tokens,
                **self.response_format,
                **tools_params,
                **kwargs,
            )

            async def generator():
                full_content = ""
                result = {}
                async for chunk in stream_response:
                    if len(chunk.choices) == 0:
                        continue
                    if not chunk.choices[0].delta:
                        continue
                    if self.model_setting.function_call_available:
                        if chunk.choices[0].delta.tool_calls:
                            for index, tool_call in enumerate(chunk.choices[0].delta.tool_calls):
                                tool_call.index = index
                        yield ChatCompletionDeltaMessage(**chunk.choices[0].delta.model_dump())
                    else:
                        message = chunk.choices[0].delta.model_dump()
                        full_content += message["content"] if message["content"] else ""
                        if tools:
                            tool_call_data = ToolCallContentProcessor(full_content).tool_calls
                            if tool_call_data:
                                message["tool_calls"] = tool_call_data["tool_calls"]
                        if full_content in ("<", "<|", "<|▶", "<|▶|") or full_content.startswith("<|▶|>"):
                            message["content"] = ""
                            result = message
                            continue
                        yield ChatCompletionDeltaMessage(**message)
                if result:
                    yield ChatCompletionDeltaMessage(**result)

            return generator()
        else:
            response: ChatCompletion = await self.raw_client.chat.completions.create(
                model=self.model_setting.id,
                messages=messages,
                stream=self.stream,
                temperature=self.temperature,
                max_tokens=max_tokens,
                **self.response_format,
                **tools_params,
                **kwargs,
            )
            result = {
                "content": response.choices[0].message.content,
                "usage": response.usage.model_dump() if response.usage else None,
            }
            if tools:
                if self.model_setting.function_call_available and response.choices[0].message.tool_calls:
                    result["tool_calls"] = [
                        {**tool_call.model_dump(), "type": "function"}
                        for tool_call in response.choices[0].message.tool_calls
                    ]
                else:
                    tool_call_content_processor = ToolCallContentProcessor(result["content"])
                    tool_call_data = tool_call_content_processor.tool_calls
                    if tool_call_data:
                        result["tool_calls"] = tool_call_data["tool_calls"]
                        result["content"] = tool_call_content_processor.non_tool_content
            return ChatCompletionMessage(**result)
