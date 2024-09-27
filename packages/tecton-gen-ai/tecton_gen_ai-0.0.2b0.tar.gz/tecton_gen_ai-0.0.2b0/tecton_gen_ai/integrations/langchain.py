from functools import singledispatch
from typing import Any, List, Optional

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chains.base import Chain
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import VectorStore

from ..agent.client import _Agent, AgentClient, invoke_agent, make_agent


@invoke_agent.register(BaseChatModel)
def _invoke_langchain(
    llm: BaseChatModel,
    client: AgentClient,
    message: str,
    system_prompt: Optional[str] = None,
    chat_history: Any = None,
    **kwargs: Any,
) -> str:
    executor = make_langchain_agent_executor(llm, client, system_prompt, **kwargs)
    client.logger.debug(
        "Invoking LangChain agent with message: %s, chat_history: %s",
        message,
        chat_history,
    )
    input = {"input": message}
    if chat_history:
        input["chat_history"] = chat_history
    output = executor.invoke(input)["output"]
    if isinstance(output, str):
        return output
    if isinstance(output, list):
        return output[0]["text"]
    raise ValueError(f"Unexpected output type: {type(output)}, {output}")


@make_agent.register(BaseChatModel)
def make_langchain_agent_executor(
    llm: BaseChatModel,
    client: AgentClient,
    system_prompt: Optional[str] = None,
    **executor_kwargs: Any,
) -> Chain:
    if system_prompt:
        if client.metastore.get(system_prompt).get("type") != "prompt":
            raise ValueError(f"{system_prompt} is not a prompt.")
    agent = _LangChainAgent(client, llm, system_prompt=system_prompt)
    return agent.make_executor(**executor_kwargs)


@singledispatch
def unified_langchain_vector_search(
    vdb: VectorStore, query: str, top_k: int, **params: Any
) -> List[Document]:
    return vdb.similarity_search(query, top_k, **params)


def langchain_vector_search(
    vdb: VectorStore, query: str, top_k: int, **params: Any
) -> List[Document]:
    try:
        from .lancedb import _lancedb_vector_search  # noqa
    except ImportError:
        pass

    return unified_langchain_vector_search(vdb, query, top_k, **params)


class _LangChainAgent(_Agent):
    def make_executor(self, **kwargs) -> Chain:
        templates = [
            MessagesPlaceholder("system_prompt"),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
        ]
        if len(self.tools) > 0:
            templates.append(MessagesPlaceholder("agent_scratchpad"))
        prompt = ChatPromptTemplate.from_messages(templates)
        prompt = prompt.partial(
            system_prompt=lambda: (
                [("system", self.invoke_sys_prompt())] if self._system_prompt else []
            )
        )
        if len(self.tools) > 0:
            agent = create_tool_calling_agent(self.llm, self.tools, prompt)
            return AgentExecutor(agent=agent, tools=self.tools, **kwargs)
        else:

            def parse(message: AIMessage) -> str:
                return {"output": message.content}

            return prompt | self.llm | parse

    def _make_messages(self, question, history):
        history = history or []
        history = self._add_sys_prompt(history)
        return history + [("human", question)]

    def _make_tool(self, name):
        from langchain_core.tools import StructuredTool

        f, description = self._get_dummy_func(name)
        _tool = StructuredTool.from_function(name=name, func=f, description=description)
        _tool.func = lambda **kwargs: self.client.invoke_tool(name, kwargs)
        return _tool
