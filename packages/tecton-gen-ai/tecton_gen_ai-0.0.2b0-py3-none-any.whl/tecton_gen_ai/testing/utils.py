import logging
import os
import shutil
from tempfile import gettempdir
from typing import Any, Optional

from tecton_gen_ai.utils.config_wrapper import as_config


def set_dev_mode():
    """
    Set the dev mode for testing and local development. In dev mode, you
    don't need to connect to tecton.
    """
    os.environ["TECTON_GEN_AI_DEV_MODE"] = "true"
    os.environ["TECTON_SKIP_OBJECT_VALIDATION"] = "true"
    os.environ["TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE"] = "rift"
    os.environ["TECTON_BATCH_COMPUTE_MODE"] = "rift"
    os.environ["TECTON_FORCE_FUNCTION_SERIALIZATION"] = "false"
    os.environ["DUCKDB_EXTENSION_REPO"] = ""


def make_local_vector_db_config(
    path: Optional[str] = None, remove_if_exists: bool = True
) -> Any:
    """
    Create a local vector db configuration for testing.

    Args:

        path: The path to the local vector db, defaults to None (system temp directory / test.db).
        remove_if_exists: Whether to remove the existing db file, defaults to True.

    Returns:

        Any: The local vector db configuration

    Note:

        - The local vector db is a LanceDB with OpenAIEmbeddings, it requires Langchain to be installed.
        - You need an OpenAI API key to use OpenAIEmbeddings.
        - Specifying the path is recommended to avoid conflicts with other tests.
    """
    if path is None:
        _path = os.path.join(gettempdir(), "tecton_local_vector_db_for_test.db")
    else:
        _path = path
    if remove_if_exists:
        shutil.rmtree(_path, ignore_errors=True)

    from langchain_community.vectorstores.lancedb import LanceDB
    from langchain_openai import OpenAIEmbeddings

    LanceDBConf = as_config(LanceDB)
    OpenAIEmbeddingsConf = as_config(OpenAIEmbeddings)

    vdb = LanceDBConf(embedding=OpenAIEmbeddingsConf(), uri=_path)
    return vdb


def make_debug_logger(filter: Any = None) -> logging.Logger:
    """
    Create a logger for debugging.

    Args:

        filter: The filter functionto apply to the logger, defaults to None (no filter).

    Returns:

        logging.Logger: The logger

    Example:

        ```python
        from tecton_gen_ai.testing.utils import make_debug_logger

        logger = make_debug_logger(filter=lambda record: "invoking" in record.getMessage())
        ```
    """
    from rich.logging import RichHandler

    logger = logging.getLogger("rich_logger")
    logger.setLevel(logging.DEBUG)
    handler = RichHandler(show_time=False)
    logger.handlers.clear()
    logger.addHandler(handler)
    if filter is not None:
        logger.filters.clear()
        logger.addFilter(filter)
    return logger


def print_md(text: str) -> None:
    """
    Print markdown text in a rich format if rich is installed, otherwise use IPython.

    Args:

        text: The markdown text to print
    """
    try:
        import rich
        from rich.markdown import Markdown

        rich.print(Markdown(text))
    except ImportError:
        from IPython.display import Markdown, display

        display(Markdown(text))
