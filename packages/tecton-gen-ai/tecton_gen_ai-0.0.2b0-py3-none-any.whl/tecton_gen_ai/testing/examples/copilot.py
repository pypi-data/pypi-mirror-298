from typing import Any, List

from tecton_gen_ai.api import AgentService, prompt, tool
from tecton_gen_ai.utils.code_parser import get_declaration


def get_service(use_tools: bool = False) -> AgentService:

    prefix = """You are a copilot that helps users use tecton_gen_ai package to build AI projects.
Your main task is generating code based on user's input."""
    objects = [_FuncOrClass(obj) for obj in _get_objects()]

    if not use_tools:
        declarations = "\n\n".join([obj.declaration for obj in objects])

        @prompt()
        def sys_prompt() -> str:
            return f"""{prefix}

Here are the functions and classes you can use to generate code:

{declarations}
"""

        return AgentService("app", prompts=[sys_prompt])
    else:

        @prompt()
        def sys_prompt() -> str:
            return prefix

        tools = [obj.to_tool() for obj in objects]
        return AgentService("app", prompts=[sys_prompt], tools=tools)


def chat(llm: Any = None, use_tools: bool = False) -> None:
    """
    Chat with the copilot in notebook to generate code based on user's input.
    """
    if llm is None:
        from langchain_openai import ChatOpenAI

        llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0, max_tokens=1000)

    from tecton_gen_ai.api import AgentClient
    from tecton_gen_ai.testing.interactive import chat as _chat

    service = get_service(use_tools=use_tools)
    client = AgentClient.from_local(service)
    _chat(client, llm, "sys_prompt")


class _FuncOrClass:
    def __init__(self, obj: Any):
        self.declaration = get_declaration(obj)
        self.name = obj.__name__
        self.doc = (obj.__doc__ or "").split("Args:")[0].strip()

    @property
    def tool_description(self) -> str:
        return (
            f"Get the declaration of {self.name}. "
            f"The purpose of {self.name}:\n{self.doc}"
        )

    @property
    def tool_name(self) -> str:
        return f"get_declaration_of_{self.name}"

    def to_tool(self) -> Any:
        description = self.tool_description
        name = self.tool_name

        @tool(name=name, description=description)
        def _tool() -> str:
            return self.declaration

        return _tool


def _get_objects() -> List[Any]:
    from tecton_gen_ai.api import (
        AgentClient,
        AgentService,
        fv_as_tool,
        prompt,
        source_as_knowledge,
        tool,
    )
    from tecton_gen_ai.testing import (
        make_local_batch_feature_view,
        make_local_realtime_feature_view,
        make_local_source,
        make_local_stream_feature_view,
        set_dev_mode,
    )
    from tecton_gen_ai.utils.tecton_utils import make_request_source

    return [
        set_dev_mode,
        make_local_batch_feature_view,
        make_local_realtime_feature_view,
        make_local_source,
        make_local_stream_feature_view,
        make_request_source,
        prompt,
        tool,
        source_as_knowledge,
        fv_as_tool,
        AgentClient,
        AgentService,
    ]
