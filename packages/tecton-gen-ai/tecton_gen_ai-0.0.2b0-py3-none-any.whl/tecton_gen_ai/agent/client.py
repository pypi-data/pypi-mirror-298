import json
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime
from functools import singledispatch

# for executing function declarations
from typing import Any, Dict, List, Optional, Tuple  # noqa

import pandas as pd
from tecton import RequestSource

from tecton_gen_ai.utils.log import NOOP_LOGGER

from ..utils._internal import get_local_source_attrs, is_local_source
from .service import AgentService

_DEFAULT_TOP_K = 5
_SEARCH_TOOL_PREFIX = "search_"


@singledispatch
def invoke_agent(
    llm,
    client: "AgentClient",
    message: str,
    system_prompt: Optional[str] = None,
    chat_history: Any = None,
    **kwargs: Any,
) -> str:
    """
    Invoke an agent. This is not for users to call directly.

    Args:

        llm: The language model object in a specific framework (e.g. LangChain)
        client: The agent client
        message: The message (question)
        system_prompt: The name of the system prompt in the service
        chat_history: The chat history
        **kwargs: Additional arguments for the agent

    Returns:

        str: The response
    """
    raise NotImplementedError(f"Unsupported type {type(llm)}")  # pragma: no cover


@singledispatch
def make_agent(
    llm,
    client: "AgentClient",
    system_prompt: Optional[str] = None,
    **kwargs: Any,
) -> Any:
    """
    Make an agent. This is not for users to call directly.

    Args:

        llm: The language model object in a specific framework (e.g. LangChain)
        client: The agent client
        system_prompt: The name of the system prompt in the service
        **kwargs: Additional arguments for creating the agent

    Returns:

        Any: The agent object
    """
    raise NotImplementedError(f"Unsupported type {type(llm)}")  # pragma: no cover


class AgentClient:
    """
    The client for Tecton agent service. The client should always be created using
    the static methods `from_remote` or `from_local`.
    """

    def __init__(self):
        self._current_context = ContextVar("current_context", default=None)
        self._current_logger = ContextVar("current_logger", default=NOOP_LOGGER)
        self.default_llm: Any = None
        self.default_system_prompt: Optional[str] = None

    @staticmethod
    def from_remote(
        url: str,
        workspace: str,
        service: str,
        api_key: str,
        default_system_prompt: Optional[str] = None,
        default_llm: Any = None,
    ) -> "AgentClient":
        """
        Create a client connecting to a deployed agent service.

        Args:

            url: The Tecton URL
            workspace: The workspace name
            service: The service name
            api_key: The API key
            default_system_prompt: The name of default system prompt, defaults to None (no system prompt)
            default_llm: The default language model, defaults to None

        Returns:

            AgentClient: The agent client
        """
        client = _AgentClientRemote(url, workspace, service, api_key)
        client.default_system_prompt = default_system_prompt
        client.default_llm = default_llm
        return client

    @staticmethod
    def from_local(
        service: AgentService,
        default_system_prompt: Optional[str] = None,
        default_llm: Any = None,
    ) -> "AgentClient":
        """
        Create a client for a local agent service. This is for testing
        and development purposes.

        Args:

            service: The agent service
            default_system_prompt: The name of default system prompt, defaults to None (no system prompt)
            default_llm: The default language model, defaults to None

        Returns:

            AgentClient: The agent client
        """
        client = _AgentClientLocal(service)
        client.default_system_prompt = default_system_prompt
        client.default_llm = default_llm
        return client

    @property
    def logger(self) -> logging.Logger:
        """
        Get the current logger of the client. The logger can be controlled
        using the context manager `set_logger`.

        Returns:

            logging.Logger: The logger
        """
        return self._current_logger.get()

    @contextmanager
    def set_logger(self, logger: Optional[logging.Logger]):
        """
        Set the logger for the client. This is a context manager.

        Args:

            logger: The new logger, or None to use the no-op logger

        Example:

            ```python
            with client.set_logger(logger):
                # do something
            ```
        """
        _logger = logger or NOOP_LOGGER
        token = self._current_logger.set(_logger)
        try:
            yield
        finally:
            self._current_logger.reset(token)

    @contextmanager
    def set_context(self, context: Optional[Dict[str, Any]]):
        """
        Set the context for the client. This is a context manager. The context
        will be used as the arguments for the prompts, tools and knowledge.

        Args:

            context: The new context, or None to clear the context

        Example:

            ```python
            conext = {"a":1, "b":2}
            new_args = {"b":3, "c":4}
            with client.set_context(context):
                # the context will be used as the arguments of my_tool
                # new_args will override the context
                # the final arguments for my_tool will be {"a":1, "b":3, "c":4}
                client.invoke_tool("my_tool", new_args)
            ```

        """
        self.logger.debug("Setting context to %s", context)
        token = self._current_context.set(context or {})
        try:
            yield
        finally:
            self._current_context.reset(token)

    @property
    def metastore(self) -> Dict[str, Any]:
        """
        Get the metastore of the client. The metastore contains the metadata of
        the tools, prompts, knowledge and other resources. This function should
        not be used directly.
        """
        return self._invoke("metastore", [], [], {})

    def make_agent(
        self, llm: Any = None, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """
        Make an agent for a specific LLM framework.

        Args:

            llm: The language model object in a specific framework (e.g. LangChain or LLamaIndex),
                defaults to None, which will use `client.default_llm`, if both are None, it will
                raise an error
            system_prompt: The name of the system prompt in the service, defaults to None, which
                will use `client.default_system_prompt`, if both are None, no system prompt will be used
            **kwargs: Additional arguments for creating the agent

        Returns:

            Any: The agent object

        Example:

            ```python
            from langchain_openai import ChatOpenAI

            openai = ChatOpenAI(model = "gpt-4o", temperature=0)

            from tecton_gen_ai.api import prompt, AgentService, AgentClient
            from tecton_gen_ai.utils.tecton_utils import make_request_source

            req = make_request_source(age=int)

            @prompt(sources=[req])
            def sys_prompt(req):
                return "You are talking to a "+str(req["age"])+" years old person."

            service = AgentService(
                "app",
                prompts=[sys_prompt],
            )

            client = AgentClient.from_local(service)
            agent = client.make_agent(openai, system_prompt="sys_prompt")
            with client.set_context({"age": 3}):
                print(agent.invoke({"input":"why sky is blue"}))
            with client.set_context({"age": 30}):
                print(agent.invoke({"input":"why sky is blue"}))
            ```
        """
        llm = llm or self.default_llm
        if llm is None:
            raise ValueError("No LLM provided")
        system_prompt = system_prompt or self.default_system_prompt
        _load_dependencies()
        return make_agent(llm, self, system_prompt=system_prompt, **kwargs)

    def invoke_agent(
        self,
        message: str,
        llm: Any = None,
        system_prompt: Optional[str] = None,
        chat_history: Any = None,
        context: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> str:
        """
        Invoke an agent for a specific LLM framework. Compared to `make_agent`, this
        function is simpler with unified input (str) and output (str), but it is less
        flexible than getting the agent object of the specific framework and invoking.

        Args:

            message: The message (question)
            llm: The language model object in a specific framework (e.g. LangChain or LLamaIndex),
                defaults to None, which will use `client.default_llm`, if both are None, it will
                raise an error
            system_prompt: The name of the system prompt in the service, defaults to None, which
                will use `client.default_system_prompt`, if both are None, no system prompt will be used
            chat_history: The chat history
            context: The context to run the agent, this will override the context set by `set_context`
            **kwargs: Additional arguments for invoking the agent

        Returns:

            str: The response

        Example:

            ```python
            from langchain_openai import ChatOpenAI

            openai = ChatOpenAI(model = "gpt-4o", temperature=0)

            from tecton_gen_ai.api import prompt, AgentService, AgentClient
            from tecton_gen_ai.utils.tecton_utils import make_request_source

            req = make_request_source(age=int)

            @prompt(sources=[req])
            def sys_prompt(req):
                return "You are talking to a "+str(req["age"])+" years old person."

            service = AgentService(
                "app",
                prompts=[sys_prompt],
            )

            client = AgentClient.from_local(service)
            client.default_llm = openai
            with client.set_context({"age": 3}):
                print(client.invoke_agent("why sky is blue", "sys_prompt"))
            with client.set_context({"age": 30}):
                print(client.invoke_agent("why sky is blue", "sys_prompt"))
            ```

        """
        llm = llm or self.default_llm
        if llm is None:
            raise ValueError("No LLM provided")
        system_prompt = system_prompt or self.default_system_prompt
        _load_dependencies()
        func = lambda: invoke_agent(  # noqa
            llm,
            self,
            message=message,
            system_prompt=system_prompt,
            chat_history=chat_history,
            **kwargs,
        )

        if context is not None:
            with self.set_context(context):
                res = func()
        else:
            res = func()
        self.logger.debug("Result of invoking agent: %s", res)
        return res

    def invoke_tool(self, name: str, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invoke a tool in the service.

        Args:

            name: The name of the tool
            kwargs: The arguments for the tool

        Returns:

            Any: The result of the tool

        Example:

            ```python
            from tecton_gen_ai.api import AgentService, AgentClient, tool

            @tool
            def get_price_of_fruit(fruit:str) -> int:
                '''
                Get the price of a fruit

                Args:

                    fruit: The name of the fruit

                Returns:

                    int: The price of the fruit
                '''
                return 10 if fruit == "apple" else 5

            service = AgentService(
                "app",
                tools=[get_price_of_fruit],
            )

            client = AgentClient.from_local(service)
            print(client.invoke_tool("get_price_of_fruit", {"fruit":"apple"}))
            ```
        """
        kwargs = kwargs or {}
        self.logger.debug("Invoking tool %s with %s", name, kwargs)
        meta = self.metastore[name]
        if meta["subtype"] == "fv":
            return self.invoke_feature_view(name, kwargs)
        if meta["subtype"] == "search":
            _filters = json.loads(kwargs.pop("filter", None) or "{}")
            _fctx = self._get_context()
            _fctx.update(_filters)
            kwargs["filter"] = json.dumps(_fctx)
        ctx = self._get_context()
        ctx.update(kwargs)
        entity_args = meta.get("entity_args", [])
        llm_args = meta.get("llm_args", [])
        return self._invoke(name, entity_args, llm_args, ctx)

    def invoke_feature_view(
        self, name: str, kwargs: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Invoke a feature view in the service.

        Args:

            name: The name of the feature view
            kwargs: The arguments for the feature view, the keys should match the entity
                schema of the feature view.

        Returns:

            Any: The result of the feature view

        Example:

            ```python
            from tecton_gen_ai.testing import make_local_feature_view, set_dev_mode

            set_dev_mode()

            bfv = make_local_feature_view(
                "user_age",
                {"user_id": 1, "age": 30},
                ["user_id"],
                description="The age of a user",
            )

            from tecton_gen_ai.api import AgentService, AgentClient

            service = AgentService(
                "app",
                tools=[bfv],
            )

            client = AgentClient.from_local(service)
            print(client.invoke_feature_view("user_age", {"user_id":1}))
            ```

        """
        kwargs = kwargs or {}
        self.logger.debug("Invoking feature view as tool %s with %s", name, kwargs)
        tool_name = "fv_tool_" + name
        tool = self.metastore[name]

        ctx = self._get_context()
        ctx.update(kwargs)
        key_map = {k: ctx[k] for k in tool["schema"].keys()}

        return self._get_feature_value(tool_name, key_map, {}, feature_type="tool")

    def invoke_prompt(self, name: str, kwargs: Optional[Dict[str, Any]] = None) -> str:
        """
        Invoke a prompt in the service.

        Args:

            name: The name of the prompt
            kwargs: The arguments for the prompt, it overrides the context set by `set_context`

        Returns:

            str: The result of the prompt

        Example:

            ```python
            from tecton_gen_ai.api import AgentService, AgentClient, prompt
            from tecton_gen_ai.utils.tecton_utils import make_request_source

            req = make_request_source(age=int)

            @prompt(sources=[req])
            def sys_prompt(req):
                return "You are talking to a "+str(req["age"])+" years old person."

            service = AgentService(
                "app",
                prompts=[sys_prompt],
            )

            client = AgentClient.from_local(service)
            print(client.invoke_prompt("sys_prompt", {"age": 3}))
            ```
        """
        kwargs = kwargs or {}
        ctx = self._get_context()
        ctx.update(kwargs)
        self.logger.debug("Invoking prompt %s with %s", name, ctx)
        metastore = self.metastore
        entity_args = metastore[name].get("entity_args", [])
        llm_args = metastore[name].get("llm_args", [])
        return self._invoke(name, entity_args, llm_args, ctx, feature_type="prompt")

    def search(
        self,
        name: str,
        query: str,
        top_k: int = _DEFAULT_TOP_K,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search a tool in the service.

        Args:

            name: The name of the search tool
            query: The query string
            top_k: The number of results to return, defaults to 5
            filter: The filter for the search, default to None (no filter)

        Returns:

            List[Dict[str, Any]]: The search results

        Example:

            ```python
            from tecton_gen_ai.testing import make_local_source
            from tecton_gen_ai.testing.utils import make_local_vector_db_config

            df = [
                {"zip":"98005", "item_id":1, "description":"pencil"},
                {"zip":"98005", "item_id":2, "description":"car"},
                {"zip":"98005", "item_id":3, "description":"paper"},
                {"zip":"10065", "item_id":4, "description":"boat"},
                {"zip":"10065", "item_id":5, "description":"cheese"},
                {"zip":"10065", "item_id":6, "description":"apple"},
            ]

            src = make_local_source(
                "for_sale",
                df,
                description="Items information",  # required for source_as_knowledge
            )
            vdb_conf = make_local_vector_db_config()

            # Create a knowledge base from the source
            from tecton_gen_ai.api import source_as_knowledge

            knowledge = source_as_knowledge(
                src,
                vector_db_config=vdb_conf,
                vectorize_column="description",
                filter = [("zip", str, "the zip code of the item for sale")]
            )

            # Serve the knowledge base
            from tecton_gen_ai.api import AgentService

            service = AgentService(
                "app",
                knowledge=[knowledge],
            )

            # Test locally
            from tecton_gen_ai.api import AgentClient

            client = AgentClient.from_local(service)
            # search without filter
            print(client.search("for_sale", query="fruit"))
            # search with filter
            print(client.search("for_sale", query="fruit", top_k=3, filter={"zip": "27001"}))
            print(client.search("for_sale", query="fruit", top_k=3, filter={"zip": "10065"}))
            ```
        """
        self.logger.debug("Searching %s with query %s filter %s", name, query, filter)
        if query == "":
            return []
        return self.invoke_tool(
            _SEARCH_TOOL_PREFIX + name,
            dict(query=query, top_k=top_k, filter=json.dumps(filter or {})),
        )

    def _invoke(self, name, entity_args, llm_args, kwargs, feature_type: str = "tool"):
        ctx_map = {}
        key_map = {}
        for k, v in kwargs.items():
            if k in entity_args:
                key_map[k] = v
            # elif k not in llm_args:
            #    raise ValueError(f"Unknown argument {k}")
            if k in llm_args:
                ctx_map[k] = v

        result = self._get_feature_value(name, key_map, ctx_map, feature_type=feature_type)
        self.logger.debug("Result of %s: %s", name, result)
        return result

    def _get_context(self) -> Dict[str, Any]:
        return (self._current_context.get() or {}).copy()

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any], feature_type: str
    ):
        raise NotImplementedError


class _AgentClientRemote(AgentClient):
    def __init__(self, url: str, workspace: str, service: str, api_key: str):
        super().__init__()
        from tecton_client import TectonClient

        self.client = TectonClient(
            url, api_key=api_key, default_workspace_name=workspace
        )
        self.service = service

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any], feature_type: str
    ):
        gf = self.client.get_features(
            feature_service_name=self.service + "_" + name,
            join_key_map=key_map,
            request_context_map={
                "name": name,
                "input": json.dumps(request_map),
            },
        )
        fd = gf.get_features_dict()
        if feature_type == "prompt":
            return fd[name + ".prompt"]
        else:
            resp = json.loads(fd[name + ".output"])
            if "error" in resp:
                raise Exception(resp["error"])
            result = resp["result"]
            return result


class _AgentClientLocal(AgentClient):
    def __init__(self, service: AgentService):
        super().__init__()
        self.service = service
        self.tool_map = {tool.name: tool for tool in service.online_fvs}
        for bfv in self.service.knowledge_bfvs:
            source = bfv.sources[0]
            if is_local_source(source):
                attrs = get_local_source_attrs(source)
                start = attrs["start_time"]
                end = attrs["end_time"]
                bfv.run_transformation(start, end).to_pandas()
                self.logger.info("Ingested knowledge %s to vector db", bfv.name)

    def _get_feature_value(
        self, name: str, key_map: Dict[str, Any], request_map: Dict[str, Any], feature_type: str
    ):
        fv = self.tool_map[name]
        res = dict(key_map)
        now = datetime.now()
        for source in fv.sources:
            if not isinstance(source, RequestSource):
                src = source.feature_definition
                res[src.get_timestamp_field()] = now
        if feature_type == "prompt":
            res.update(request_map)
            if len(res) == 0:
                res["dummy"] = 0
            output_df = fv.get_prompts_for_events(pd.DataFrame([res])).to_pandas()
            return output_df[name + "__prompt"].iloc[0]
        else:
            res.update(
                {
                    "name": name,
                    "input": json.dumps(request_map),
                }
            )
            output_df = fv.get_features_for_events(pd.DataFrame([res])).to_pandas()
            resp = json.loads(output_df[name + "__output"].iloc[0])
            if "error" in resp:
                raise Exception(resp["error"])
            result = resp["result"]
            return result


class _Agent:
    def __init__(self, client: AgentClient, llm, system_prompt=None) -> None:
        self.client = client
        self.llm = llm
        self._system_prompt = system_prompt
        self.tools = self._make_tools()

    def invoke(self, question, history=None, context=None, kwargs=None) -> str:
        raise NotImplementedError  # pragma: no cover

    def invoke_sys_prompt(self):
        context = self.client._get_context()
        if not self._system_prompt:
            raise ValueError("No system prompt provided.")
        name = self._system_prompt
        value = self.client.metastore.get(name)
        match = all(key in context for key in value.get("keys", [])) and all(
            key in context for key in value.get("args", [])
        )
        if not match:
            raise ValueError(
                f"Context does not have all required keys for system prompt {name}."
            )
        if len(context) > 0:
            prefix = f"All context in the system: {context}\n\n"
        else:
            prefix = ""
        prompt = self.client.invoke_prompt(name, context)
        return prefix + prompt

    def _add_sys_prompt(self, history):
        if not self._system_prompt:
            return history
        sys_prompt = ("system", self.invoke_sys_prompt())
        history.insert(0, sys_prompt)
        return history

    def _get_dummy_func(self, name):
        meta = self.client.metastore[name]
        if meta["subtype"] in ["tool", "search"]:
            code = meta["def"]
        elif meta["subtype"] == "fv":
            queryable = meta.get("queryable", True)
            schema = meta["schema"] if queryable else {}
            params = ",".join(f"{k}:{v}" for k, v in schema.items())
            code = f"def {name}({params}) -> 'Dict[str,Any]':\n    pass"
        else:
            raise ValueError(f"Unknown tool type {meta['type']}")
        exec(code, globals(), locals())
        description = meta.get("description")
        return locals()[name], description

    def _make_tool(self, name):
        raise NotImplementedError

    def _make_tools(self):
        return [
            self._make_tool(name)
            for name, value in self.client.metastore.items()
            if value["type"] == "tool"
        ]


def _load_dependencies():
    try:
        from tecton_gen_ai.integrations import langchain  # noqa
    except ImportError:
        pass

    try:
        from tecton_gen_ai.integrations import llama_index  # noqa
    except ImportError:
        pass
