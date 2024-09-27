from pytest import fixture

from tecton_gen_ai.api import source_as_knowledge
from tecton_gen_ai.testing import make_local_source


@fixture
def mock_knowledge(tecton_unit_test, tecton_vector_db_test_config):
    data = [
        {"zip": 98005, "item_id": 1, "description": "pencil"},
        {"zip": 98005, "item_id": 2, "description": "car"},
        {"zip": 98005, "item_id": 3, "description": "paper"},
        {"zip": 10065, "item_id": 4, "description": "boat"},
        {"zip": 10065, "item_id": 5, "description": "cheese"},
        {"zip": 10065, "item_id": 6, "description": "apple"},
    ]
    knowledge_src = make_local_source(
        "knowledge", data, auto_timestamp=True, description="Items for sale"
    )
    return source_as_knowledge(
        knowledge_src,
        tecton_vector_db_test_config,
        vectorize_column="description",
        filter=[("zip", int, "Zip code")],
    )
