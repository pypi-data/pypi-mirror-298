# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from typing import AsyncGenerator

from fireworks.client import Fireworks

from llama_models.llama3.api.chat_format import ChatFormat

from llama_models.llama3.api.datatypes import Message, StopReason
from llama_models.llama3.api.tokenizer import Tokenizer
from llama_models.sku_list import resolve_model

from llama_stack.apis.inference import *  # noqa: F403
from llama_stack.providers.utils.inference.prepare_messages import prepare_messages

from .config import FireworksImplConfig

FIREWORKS_SUPPORTED_MODELS = {
    "Meta-Llama3.1-8B-Instruct": "fireworks/llama-v3p1-8b-instruct",
    "Meta-Llama3.1-70B-Instruct": "fireworks/llama-v3p1-70b-instruct",
    "Meta-Llama3.1-405B-Instruct": "fireworks/llama-v3p1-405b-instruct",
}


class FireworksInferenceAdapter(Inference):
    def __init__(self, config: FireworksImplConfig) -> None:
        self.config = config
        tokenizer = Tokenizer.get_instance()
        self.formatter = ChatFormat(tokenizer)

    @property
    def client(self) -> Fireworks:
        return Fireworks(api_key=self.config.api_key)

    async def initialize(self) -> None:
        return

    async def shutdown(self) -> None:
        pass

    async def completion(
        self,
        model: str,
        content: InterleavedTextMedia,
        sampling_params: Optional[SamplingParams] = SamplingParams(),
        stream: Optional[bool] = False,
        logprobs: Optional[LogProbConfig] = None,
    ) -> AsyncGenerator:
        raise NotImplementedError()

    def _messages_to_fireworks_messages(self, messages: list[Message]) -> list:
        fireworks_messages = []
        for message in messages:
            if message.role == "ipython":
                role = "tool"
            else:
                role = message.role
            fireworks_messages.append({"role": role, "content": message.content})

        return fireworks_messages

    def resolve_fireworks_model(self, model_name: str) -> str:
        model = resolve_model(model_name)
        assert (
            model is not None
            and model.descriptor(shorten_default_variant=True)
            in FIREWORKS_SUPPORTED_MODELS
        ), f"Unsupported model: {model_name}, use one of the supported models: {','.join(FIREWORKS_SUPPORTED_MODELS.keys())}"

        return FIREWORKS_SUPPORTED_MODELS.get(
            model.descriptor(shorten_default_variant=True)
        )

    def get_fireworks_chat_options(self, request: ChatCompletionRequest) -> dict:
        options = {}
        if request.sampling_params is not None:
            for attr in {"temperature", "top_p", "top_k", "max_tokens"}:
                if getattr(request.sampling_params, attr):
                    options[attr] = getattr(request.sampling_params, attr)

        return options

    async def chat_completion(
        self,
        model: str,
        messages: List[Message],
        sampling_params: Optional[SamplingParams] = SamplingParams(),
        tools: Optional[List[ToolDefinition]] = None,
        tool_choice: Optional[ToolChoice] = ToolChoice.auto,
        tool_prompt_format: Optional[ToolPromptFormat] = ToolPromptFormat.json,
        stream: Optional[bool] = False,
        logprobs: Optional[LogProbConfig] = None,
    ) -> AsyncGenerator:
        request = ChatCompletionRequest(
            model=model,
            messages=messages,
            sampling_params=sampling_params,
            tools=tools or [],
            tool_choice=tool_choice,
            tool_prompt_format=tool_prompt_format,
            stream=stream,
            logprobs=logprobs,
        )

        messages = prepare_messages(request)

        # accumulate sampling params and other options to pass to fireworks
        options = self.get_fireworks_chat_options(request)
        fireworks_model = self.resolve_fireworks_model(request.model)

        if not request.stream:
            r = await self.client.chat.completions.acreate(
                model=fireworks_model,
                messages=self._messages_to_fireworks_messages(messages),
                stream=False,
                **options,
            )
            stop_reason = None
            if r.choices[0].finish_reason:
                if r.choices[0].finish_reason == "stop":
                    stop_reason = StopReason.end_of_turn
                elif r.choices[0].finish_reason == "length":
                    stop_reason = StopReason.out_of_tokens

            completion_message = self.formatter.decode_assistant_message_from_content(
                r.choices[0].message.content, stop_reason
            )

            yield ChatCompletionResponse(
                completion_message=completion_message,
                logprobs=None,
            )
        else:
            yield ChatCompletionResponseStreamChunk(
                event=ChatCompletionResponseEvent(
                    event_type=ChatCompletionResponseEventType.start,
                    delta="",
                )
            )

            buffer = ""
            ipython = False
            stop_reason = None

            async for chunk in self.client.chat.completions.acreate(
                model=fireworks_model,
                messages=self._messages_to_fireworks_messages(messages),
                stream=True,
                **options,
            ):
                if chunk.choices[0].finish_reason:
                    if stop_reason is None and chunk.choices[0].finish_reason == "stop":
                        stop_reason = StopReason.end_of_turn
                    elif (
                        stop_reason is None
                        and chunk.choices[0].finish_reason == "length"
                    ):
                        stop_reason = StopReason.out_of_tokens
                    break

                text = chunk.choices[0].delta.content
                if text is None:
                    continue

                # check if its a tool call ( aka starts with <|python_tag|> )
                if not ipython and text.startswith("<|python_tag|>"):
                    ipython = True
                    yield ChatCompletionResponseStreamChunk(
                        event=ChatCompletionResponseEvent(
                            event_type=ChatCompletionResponseEventType.progress,
                            delta=ToolCallDelta(
                                content="",
                                parse_status=ToolCallParseStatus.started,
                            ),
                        )
                    )
                    buffer += text
                    continue

                if ipython:
                    if text == "<|eot_id|>":
                        stop_reason = StopReason.end_of_turn
                        text = ""
                        continue
                    elif text == "<|eom_id|>":
                        stop_reason = StopReason.end_of_message
                        text = ""
                        continue

                    buffer += text
                    delta = ToolCallDelta(
                        content=text,
                        parse_status=ToolCallParseStatus.in_progress,
                    )

                    yield ChatCompletionResponseStreamChunk(
                        event=ChatCompletionResponseEvent(
                            event_type=ChatCompletionResponseEventType.progress,
                            delta=delta,
                            stop_reason=stop_reason,
                        )
                    )
                else:
                    buffer += text
                    yield ChatCompletionResponseStreamChunk(
                        event=ChatCompletionResponseEvent(
                            event_type=ChatCompletionResponseEventType.progress,
                            delta=text,
                            stop_reason=stop_reason,
                        )
                    )

            # parse tool calls and report errors
            message = self.formatter.decode_assistant_message_from_content(
                buffer, stop_reason
            )
            parsed_tool_calls = len(message.tool_calls) > 0
            if ipython and not parsed_tool_calls:
                yield ChatCompletionResponseStreamChunk(
                    event=ChatCompletionResponseEvent(
                        event_type=ChatCompletionResponseEventType.progress,
                        delta=ToolCallDelta(
                            content="",
                            parse_status=ToolCallParseStatus.failure,
                        ),
                        stop_reason=stop_reason,
                    )
                )

            for tool_call in message.tool_calls:
                yield ChatCompletionResponseStreamChunk(
                    event=ChatCompletionResponseEvent(
                        event_type=ChatCompletionResponseEventType.progress,
                        delta=ToolCallDelta(
                            content=tool_call,
                            parse_status=ToolCallParseStatus.success,
                        ),
                        stop_reason=stop_reason,
                    )
                )

            yield ChatCompletionResponseStreamChunk(
                event=ChatCompletionResponseEvent(
                    event_type=ChatCompletionResponseEventType.complete,
                    delta="",
                    stop_reason=stop_reason,
                )
            )
