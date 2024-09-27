import ast
import inspect
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple, Union

from tecton import (
    Attribute,
    DataSource,
    Entity,
    FeatureView,
    RequestSource,
    realtime_feature_view,
)
from tecton.framework.data_source import FilteredSource
from tecton.types import Bool, Field, Float32, Float64, Int32, Int64, String, Timestamp

from tecton_gen_ai.utils.tecton_utils import make_request_source, set_conf

from ..constants import _TECTON_MOCK_OBJECT_ATTR
from ._extra_attrs import get_attr, has_attr, set_attr

_REQUEST = make_request_source(name=str, input=str)


def is_local_source(source: Any) -> bool:
    src = _get_orig_source(source)
    return has_attr(src, _TECTON_MOCK_OBJECT_ATTR)


def get_local_source_attrs(sourcre: Any) -> Dict[str, Any]:
    src = _get_orig_source(sourcre)
    return get_attr(src, _TECTON_MOCK_OBJECT_ATTR)


def set_local_source_attrs(source: Any, attrs: Dict[str, Any]) -> None:
    src = _get_orig_source(source)
    set_attr(src, _TECTON_MOCK_OBJECT_ATTR, attrs)


def _get_orig_source(source: Any) -> DataSource:
    if isinstance(source, FilteredSource):
        return source.source
    if isinstance(source, DataSource):
        return source
    raise ValueError(f"{source} is not a DataSource or FilteredSource")


class FuncWrapper:
    def __init__(
        self,
        name: str,
        func: Callable,
        sources: Optional[List[FeatureView]] = None,
        assert_entity_defined: bool = False,
    ):
        self.name = name
        self.func = func
        self.sources = sources or []
        ap = _ArgumentParser(func, self.sources, assert_entity_defined)
        (
            self.views,
            self.llm_args,
            self.feature_args,
            self.entity_args,
            self.has_request_source,
            self.should_add_request_source,
        ) = (
            ap.views,
            ap.llm_args,
            ap.feature_args,
            ap.entitye_args,
            ap.has_request_source,
            ap.should_add_request_source,
        )

    def make_prompt(self, **rtfv_kwargs: Any) -> FeatureView:
        from tecton import prompt as tecton_prompt

        name = self.name
        func = self.func
        func_name = func.__name__
        doc = func.__doc__
        if not self.should_add_request_source:
            deco = tecton_prompt(
                name=name,
                description=doc,
                sources=self.sources,
                **rtfv_kwargs,
            )
            return deco(func)
        spec = inspect.getfullargspec(func)
        req = make_request_source(
            **{k: spec.annotations[k] for k in spec.args if k in self.llm_args}
        )
        fv_names = [fv.name for fv in self.views]
        deco = tecton_prompt(
            name=name,
            description=doc,
            sources=[req] + self.views,
            **rtfv_kwargs,
        )

        def service(request_context, *fvs):
            try:  # make tecton compiler embed this function
                f = func  # running locally
            except Exception:  # tecton runtime can't really get this function
                f = globals()[func_name]  # running on server
            params = dict(request_context)
            for key, fv in zip(fv_names, fvs):
                params[key] = fv
            return f(**params)

        return self._wrap(deco, service)

    def make_feature_view(self, **rtfv_kwargs: Any) -> FeatureView:
        name = self.name
        func = self.func
        func_name = func.__name__
        doc = func.__doc__
        has_request_source = self.has_request_source
        fv_names = [fv.name for fv in self.views]
        deco = realtime_feature_view(
            name=name,
            description=doc,
            sources=[_REQUEST] + self.views,
            mode="python",
            features=[Attribute("output", String)],
            **rtfv_kwargs,
        )

        def tool_service(request_context, *fvs):
            import json

            if name != request_context["name"]:
                return {"output": "{}"}
            if has_request_source:
                pos_args: List[Any] = [json.loads(request_context["input"])]
                params = {}
            else:
                pos_args: List[Any] = []
                params = json.loads(request_context["input"])
            try:  # make tecton compiler embed this function
                f = func  # running locally
            except Exception:  # tecton runtime can't really get this function
                f = globals()[func_name]  # running on server
            for key, fv in zip(fv_names, fvs):
                params[key] = fv
            try:
                res = f(*pos_args, **params)
                return {"output": json.dumps({"result": res})}
            except Exception:
                from traceback import format_exc

                return {"output": json.dumps({"error": format_exc()})}

        return self._wrap(deco, tool_service)

    def _wrap(self, deco: Any, func: Any) -> Any:
        with set_serialization():

            if len(self.views) == 0:

                def _wrapper(request_context):
                    return func(request_context)

                return deco(_wrapper)
            if len(self.views) == 1:

                def _wrapper(request_context, fv1):
                    return func(request_context, fv1)

                return deco(_wrapper)
            if len(self.views) == 2:

                def _wrapper(request_context, fv1, fv2):
                    return func(request_context, fv1, fv2)

                return deco(_wrapper)
            if len(self.views) == 3:

                def _wrapper(request_context, fv1, fv2, fv3):
                    return func(request_context, fv1, fv2, fv3)

                return deco(_wrapper)
            if len(self.views) == 4:

                def _wrapper(request_context, fv1, fv2, fv3, fv4):
                    return func(request_context, fv1, fv2, fv3, fv4)

                return deco(_wrapper)
            if len(self.views) == 5:

                def _wrapper(request_context, fv1, fv2, fv3, fv4, fv5):
                    return func(request_context, fv1, fv2, fv3, fv4, fv5)

                return deco(_wrapper)
        raise NotImplementedError("Too many sources")


def build_dummy_function(
    func: Callable, name: str, exclude_args: Optional[Iterator[str]] = None
):
    if not name.isidentifier():
        raise ValueError(f"{name} is not a valid identifier")
    code = _prepare_code(inspect.getsource(func))
    func_def = ast.parse(code).body[0]
    func_def.name = name
    func_def.body = [ast.Pass()]
    exclude = set(exclude_args or [])
    args: Any = []
    for arg in func_def.args.args:
        if arg.arg not in exclude:
            args.append(arg)
    func_def.args.args = args
    return ast.unparse(func_def)


@contextmanager
def set_serialization():
    import os
    import sys

    if "ipykernel" in sys.modules or os.environ.get("TECTON_GEN_AI_DEV_MODE") == "true":
        yield
    else:  # not in notebook
        with set_conf({"TECTON_FORCE_FUNCTION_SERIALIZATION": "true"}):
            yield


def entity_to_tool_schema(entity: Entity, fv_schema: Dict[str, Any]) -> Dict[str, str]:
    schema: Dict[str, str] = {}
    for name in entity.join_keys:
        if not name.isidentifier():
            raise ValueError(f"{name} is not a valid identifier")
        schema[name] = fv_schema[name]
    return schema


def fields_to_tool_schema(fields: List[Field]) -> Dict[str, str]:
    schema: Dict[str, str] = {}
    for item in fields:
        name = item.name
        if not name.isidentifier():
            raise ValueError(f"{name} is not a valid identifier")
        tp = item.dtype.tecton_type
        if String.tecton_type == tp:
            schema[name] = "str"
        elif Int32.tecton_type == tp:
            schema[name] = "int"
        elif Int64.tecton_type == tp:
            schema[name] = "int"
        elif Float32.tecton_type == tp:
            schema[name] = "float"
        elif Float64.tecton_type == tp:
            schema[name] = "float"
        elif Bool.tecton_type == tp:
            schema[name] = "bool"
        elif Timestamp.tecton_type == tp:
            schema[name] = "object"
        else:
            raise ValueError(f"Unsupported type {tp} for {name}")
    return schema


def _prepare_code(code):
    lines = code.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("def "):
            indent = line.index("def ")
            return "\n".join(x[indent:] for x in lines[i:])


class _ArgumentParser:
    def __init__(
        self,
        func: Callable,
        sources: List[Union[RequestSource, FeatureView]],
        assert_entity_defined: bool,
    ) -> Tuple[List[str], List[str], List[str], bool]:
        self.func = func
        self.orig_args = inspect.getfullargspec(func).args
        self.has_request_source = len(sources) > 0 and isinstance(
            sources[0], RequestSource
        )
        self.views: List[FeatureView] = (
            sources if not self.has_request_source else sources[1:]
        )
        if not self.has_request_source:
            self.llm_args, self.feature_args, self.entitye_args = (
                self._parse_arguments_no_request_sourcre(
                    self.orig_args,
                    assert_entity_defined,
                    assert_all_feature_args=False,
                )
            )
            self.view = sources
        else:
            _, self.feature_args, self.entitye_args = (
                self._parse_arguments_no_request_sourcre(
                    self.orig_args[1:],
                    assert_entity_defined,
                    assert_all_feature_args=True,
                )
            )
            self.llm_args = [x.name for x in sources[0].schema]
        self.should_add_request_source = (
            not self.has_request_source and len(self.llm_args) > 0
        )

    def _parse_arguments_no_request_sourcre(
        self,
        args: List[str],
        assert_entity_defined: bool,
        assert_all_feature_args: bool,
    ) -> Tuple[List[str], List[str], List[str]]:
        func = self.func
        feature_args = [source.name for source in self.views]
        if not set(feature_args).issubset(args):
            raise ValueError(
                f"All feature view names ({feature_args}) "
                f"must be defined in {func} arguments"
            )
        if len(self.views) == 0:
            entity_args: List[str] = []
        else:
            jk = self.views[0].join_keys
            for source in self.views[1:]:
                jk += source.join_keys
                # if set(jk) != set(source.join_keys):
                #    raise ValueError("All sources must have the same join keys")
            entity_args = list(dict.fromkeys(jk))
        if assert_entity_defined:
            if not set(entity_args).issubset(args):
                raise ValueError(
                    f"All entity keys ({entity_args}) must be defined in {func}"
                )
        llm_args = [x for x in args if x not in feature_args]
        if assert_all_feature_args and len(llm_args) > 0:
            raise ValueError(
                f"Only features and request source arguments are allowed: {llm_args}"
            )
        return llm_args, feature_args, entity_args
