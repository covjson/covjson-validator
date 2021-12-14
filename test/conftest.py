import pytest
import jsonschema

import validator as validator_
from tools.bundle_schema import bundle_schema
from tools.downgrade_schema_to_draft07 import downgrade_schema_to_draft07


@pytest.fixture(scope="session")
def schema_store():
    return validator_.create_schema_store()

VALIDATOR_CACHE = {}

@pytest.fixture(scope="function", params=["native", "draft-07-bundle"])
def validator(request, schema_store):
    mode = request.param
    schema_marker = request.node.get_closest_marker("schema")
    assert schema_marker is not None
    schema_id = schema_marker.args[0]
    validator = VALIDATOR_CACHE.get((mode, schema_id))
    if validator:
        return validator
    schema = schema_store[schema_id]
    if mode == "native":
        resolver = jsonschema.RefResolver(None, referrer=None, store=schema_store)
        validator = jsonschema.Draft202012Validator(schema, resolver=resolver)
    elif mode == "draft-07-bundle":
        schema = bundle_schema(schema_store, schema_id)
        schema = downgrade_schema_to_draft07(schema)
        validator = jsonschema.Draft7Validator(schema)
    else:
        raise ValueError(f"Unknown mode {mode}")
    VALIDATOR_CACHE[(mode, schema_id)] = validator
    return validator
