"""A wrapper around the OpenAI client.

A wrapper around the OpenAI client that gives it some extra features like
caching, memory, pre-and-post inference callbacks, etc...
"""

__all__ = ["OpenAI", "AsyncOpenAI"]

from typing import (
    Any,
    Iterable,
    List,
    Optional,
    Type,
    TypeVar,
    overload,
)

from pydantic import BaseModel
import instructor

from fixpoint.completions import (
    ChatCompletion,
    ChatCompletionMessageParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from fixpoint.memory import SupportsMemory
from fixpoint._protocols.workflow_run import WorkflowRunData
from fixpoint.cache import SupportsChatCompletionCache
from ..openai import OpenAIAgent, OpenAIClients
from ..protocol import CompletionCallback, PreCompletionFn
from ._async_openai import AsyncOpenAI


T_contra = TypeVar("T_contra", bound=BaseModel, contravariant=True)


class OpenAI:
    """
    An agent that conforms to the OpenAI API.
    """

    fixp: OpenAIAgent
    _fixpchat: "OpenAI._Chat"
    _model_name: Optional[str]

    def __init__(
        self,
        agent_id: str,
        openai_clients: OpenAIClients,
        *,
        pre_completion_fns: Optional[List[PreCompletionFn]] = None,
        completion_callbacks: Optional[List[CompletionCallback]] = None,
        memory: Optional[SupportsMemory] = None,
        cache: Optional[SupportsChatCompletionCache] = None,
    ) -> None:
        self.fixp = OpenAIAgent(
            agent_id=agent_id,
            model_name="<NOT_SET>",
            openai_clients=openai_clients,
            pre_completion_fns=pre_completion_fns,
            completion_callbacks=completion_callbacks,
            memory=memory,
            cache=cache,
        )

        self._fixpchat = OpenAI._Chat(openai_clients.instructor.chat, self.fixp)

    @property
    def chat(self) -> "OpenAI._Chat":
        """Chat-related operations"""
        return self._fixpchat

    def __getattr__(self, name: str) -> Any:
        # Forward attribute access to the underlying client
        return getattr(self._fixpchat, name)

    class _Chat:
        _fixpchat: instructor.Instructor
        _fixpcompletions: "OpenAI._Completions"
        _agent: OpenAIAgent

        def __init__(
            self, openai_chat: instructor.Instructor, agent: OpenAIAgent
        ) -> None:
            self._fixpchat = openai_chat
            self._fixpcompletions = OpenAI._Completions(
                self._fixpchat.completions, agent
            )
            self._agent = agent

        @property
        def completions(self) -> "OpenAI._Completions":
            """Operations on chat completions"""
            return self._fixpcompletions

        def __getattr__(self, name: str) -> Any:
            # Forward attribute access to the underlying client
            return getattr(self._fixpchat, name)

    class _Completions:
        _fixpcompletions: instructor.Instructor
        _agent: OpenAIAgent

        def __init__(
            self, openai_completions: instructor.Instructor, agent: OpenAIAgent
        ) -> None:
            self._fixpcompletions = openai_completions
            self._agent = agent

        def __getattr__(self, name: str) -> Any:
            # Forward attribute access to the underlying client
            return getattr(self._fixpcompletions, name)

        @overload
        def create(
            self,
            messages: List[ChatCompletionMessageParam],
            *,
            model: str,
            response_model: None = None,
            tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = None,
            tools: Optional[Iterable[ChatCompletionToolParam]] = None,
            temperature: Optional[float] = None,
            workflow_run: Optional[WorkflowRunData] = None,
            **kwargs: Any,
        ) -> ChatCompletion[BaseModel]: ...

        @overload
        def create(
            self,
            messages: List[ChatCompletionMessageParam],
            *,
            model: str,
            response_model: Type[T_contra],
            tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = None,
            tools: Optional[Iterable[ChatCompletionToolParam]] = None,
            temperature: Optional[float] = None,
            workflow_run: Optional[WorkflowRunData] = None,
            **kwargs: Any,
        ) -> ChatCompletion[T_contra]: ...

        def create(
            self,
            messages: List[ChatCompletionMessageParam],
            *,
            model: str,
            response_model: Optional[Type[T_contra]] = None,
            temperature: Optional[float] = None,
            tool_choice: Optional[ChatCompletionToolChoiceOptionParam] = None,
            tools: Optional[Iterable[ChatCompletionToolParam]] = None,
            workflow_run: Optional[WorkflowRunData] = None,
            **kwargs: Any,
        ) -> ChatCompletion[T_contra]:
            """Create a chat completion"""
            return self._agent.create_completion(
                messages=messages,
                model=model,
                temperature=temperature,
                tool_choice=tool_choice,
                tools=tools,
                response_model=response_model,
                workflow_run=workflow_run,
                **kwargs,
            )
