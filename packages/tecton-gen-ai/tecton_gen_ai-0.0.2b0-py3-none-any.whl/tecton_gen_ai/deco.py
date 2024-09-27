from typing import Any, Callable, Dict, List, Optional, TypeVar

from typing_extensions import ParamSpec

from tecton import FeatureView

from .utils._internal import FuncWrapper, build_dummy_function

_METASTORE: Dict[str, Any] = {}

T = TypeVar("T")
P = ParamSpec("P")


def _get_from_metastore(obj: Any) -> Dict[str, Any]:
    key = id(obj)
    if key not in _METASTORE:
        raise ValueError(
            f"{obj} not found in metastore, did you forget to decorate it?"
        )
    return _METASTORE[key]


def _set_metastore(key: Any, value: Any) -> None:
    _METASTORE[id(key)] = value


def prompt(
    func: Optional[Callable[P, T]] = None,
    name: Optional[str] = None,
    sources: Optional[List[FeatureView]] = None,
    **prompt_kwargs: Any,
) -> Callable[P, T]:
    """
    Decorator for creating a prompt.

    Args:

        func: The function to decorate.
        name: The name of the prompt.
        sources: The sources of the prompt.
        **prompt_kwargs: Other keyword arguments for Tecton's prompt.

    Examples:

        ```python
        # The simplest form without a feature dependency
        from tecton_gen_ai.api import prompt

        @prompt()
        def simple_prompt() -> str:
            return "Hello, world!"

        # With parameters but not a feature
        @prompt
        def prompt_with_params(zip:str) -> str:
            return "Hello, you zip code " + zip

        # With a feature dependency
        from tecton_gen_ai.testing import make_local_batch_feature_view

        my_bfv = make_local_batch_feature_view(
            "my_bfv",
            {"user_id":"u1", "name":"Bob"},
            ["user_id"],
            description="User information",
        )

        @prompt(sources=[my_bfv])
        def sys_prompt(zip:str, my_bfv) -> str:
            return "Hello, " + my_bfv["name"] + " with zip code " + zip

        # Serve the prompt
        from tecton_gen_ai.api import AgentService

        service = AgentService(
            "my_service",
            prompts=[sys_prompt],
        )

        # Test locally
        from tecton_gen_ai.api import AgentClient

        client = AgentClient.from_local(service)

        with client.set_context({"zip": "10065", "user_id": "u1"}):
            res = client.invoke_prompt("sys_prompt")
        ```
    """

    def wrapper(
        _func: Callable[P, T],
        _name: Optional[str],
        _features: Optional[List[FeatureView]],
    ) -> Callable[P, T]:
        if _name is None:
            _name = _func.__name__
        wrapper = FuncWrapper(_name, _func, _features)
        fv = wrapper.make_prompt(**prompt_kwargs)
        _set_metastore(
            _func,
            {
                "name": _name,
                "fv": fv,
                "type": "prompt",
                "llm_args": wrapper.llm_args,
                "entity_args": wrapper.entity_args,
                "feature_args": wrapper.feature_args,
            },
        )
        return _func

    if func is None:
        return lambda _func: wrapper(_func, name, sources)
    return wrapper(func, name, sources)


def tool(
    func: Optional[Callable[P, T]] = None,
    name: Optional[str] = None,
    sources: Optional[List[FeatureView]] = None,
    description: Optional[str] = None,
    subtype: str = "tool",
    **rtfv_kwargs: Any,
) -> Callable[P, T]:
    """
    Decorator for creating a tool. The tool can be used by different LLMs and
    frameworks such as Langchain and LlamaIndex.

    Args:

        func: The function to decorate.
        name: The name of the tool.
        sources: The sources of the tool.
        description: The description of the tool.
        subtype: The subtype of the tool.
        **rtfv_kwargs: Other keyword arguments for Tecton's realtime feature view.

    Note:

        The definition of tool is different from prompt:

        - The name of the tool should represent what the function does.
        - The docstring of the tool is required and it should contain the description and instructions of the tool.
        - If a feature view is a dependency, then the entity ids must be defined in the function signature.
        - All the arguments excluding feature view arguments must have type annotations.
        - The return type annotation is required.

    Examples:

        ```python
        # The simplest form without a feature dependency
        from tecton_gen_ai.api import tool

        @tool()
        def get_months_in_a_year() -> int:
            '''The total number months of a year'''
            return 12

        # With parameters but not a feature
        @tool()
        def add(a: int, b: int) -> int:
            '''Add two numbers

            Args:
                a (int): The first number
                b (int): The second number

            Returns:
                int: The sum of the two numbers
            '''
            return a + b

        # With a feature dependency
        from tecton_gen_ai.testing import make_local_batch_feature_view

        my_bfv = make_local_batch_feature_view(
            "my_bfv",
            {"user_id":"u1", "name":"Bob"},
            ["user_id"],
            description="User information",
        )

        @tool(sources=[my_bfv])
        def get_name(prefix:str, user_id:str, my_bfv) -> str:
            '''Get the name of a user with a prefix

            Args:

                prefix (str): The prefix of the name
                user_id (str): The user ID

            Returns:

                str: The name of the user with the prefix
            '''
            return prefix + " " + my_bfv["name"]

        # Serve the tool
        from tecton_gen_ai.api import AgentService

        service = AgentService(
            "my_service",
            tools=[get_name],
        )

        # Test locally
        from tecton_gen_ai.api import AgentClient

        client = AgentClient.from_local(service)
        with client.set_context({"user_id": "u1", "prefix": "Hello"}):
            res = client.invoke_tool("get_name")
        ```
    """

    def wrapper(
        _func: Callable[P, T],
        _name: Optional[str],
        _features: Optional[List[FeatureView]],
    ) -> Callable[P, T]:
        if _name is None:
            _name = _func.__name__
        wrapper = FuncWrapper(
            _name,
            _func,
            _features,
            assert_entity_defined=True,
        )
        fv = wrapper.make_feature_view(**rtfv_kwargs)
        _set_metastore(
            _func,
            {
                "name": _name,
                "fv": fv,
                "type": "tool",
                "subtype": subtype,
                "llm_args": wrapper.llm_args,
                "entity_args": wrapper.entity_args,
                "feature_args": wrapper.feature_args,
                "def": build_dummy_function(
                    _func,
                    _name,
                    exclude_args=wrapper.feature_args,
                ),
                "description": description or _func.__doc__,
            },
        )
        return _func

    if func is None:
        return lambda _func: wrapper(_func, name, sources)
    return wrapper(func, name, sources)
