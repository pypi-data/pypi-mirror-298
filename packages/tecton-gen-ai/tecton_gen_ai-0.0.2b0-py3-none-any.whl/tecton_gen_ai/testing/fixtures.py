from pytest import fixture


@fixture
def tecton_unit_test():
    from ..utils.tecton_utils import set_conf
    import os

    os.environ["TECTON_GEN_AI_DEV_MODE"] = "true"

    with set_conf(
        {
            "TECTON_FORCE_FUNCTION_SERIALIZATION": "false",
            "DUCKDB_EXTENSION_REPO": "",
            "TECTON_SKIP_OBJECT_VALIDATION": "true",
            "TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE": "rift",
            "TECTON_BATCH_COMPUTE_MODE": "rift",
        }
    ):
        yield


@fixture
def tecton_vector_db_test_config(tmp_path):
    from .utils import make_local_vector_db_config

    path = str(tmp_path / "test.db")
    return make_local_vector_db_config(path, remove_if_exists=True)
