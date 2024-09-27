import pandas as pd
import pyarrow as pa
from tecton.types import Array, Bool, Float64, Int32, Int64, Map, String, Timestamp


import datetime
from typing import Any, get_args, get_origin


def to_tecton_type(type: Any) -> Any:
    """
    Convert an object to a Tecton type

    Args:

        type: The Python type annotation

    Returns:

        Any: The Tecton type
    """
    if isinstance(type, pa.DataType):
        if pa.types.is_string(type):
            return String
        if pa.types.is_int32(type):
            return Int32
        if pa.types.is_integer(type):
            return Int64
        if pa.types.is_floating(type):
            return Float64
        if pa.types.is_boolean(type):
            return Bool
        if pa.types.is_timestamp(type):
            return Timestamp
        if pa.types.is_list(type):
            return Array(to_tecton_type(type.value_type))
        raise ValueError(f"Unsupported type {type}")
    if type is str:
        return String
    if type is int:
        return Int64
    if type is float:
        return Float64
    if type is bool:
        return Bool
    if type is pd.Timestamp or type is datetime.datetime:
        return Timestamp
    if get_origin(type) is list:
        return Array(to_tecton_type(get_args(type)[0]))
    if get_origin(type) is dict:
        k = to_tecton_type(get_args(type)[0])
        v = to_tecton_type(get_args(type)[1])
        return Map(k, v)
    raise ValueError(f"Unsupported type {type}")
