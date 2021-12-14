# A tool that bundles all referenced schemas into a root schema.
# Follows the method described in:
# https://datatracker.ietf.org/doc/html/draft-bhutton-json-schema-00#section-9.3.1
# Requires >= 2019-09 JSON Schema dialect.

# Note: This tool is specialized to the way schemas are stored and
# written in this repository and is not intended to be used elsewhere.

import argparse
import os
import json
import copy

JSON_SCHEMA_2019_09 = "http://json-schema.org/2019-09/schema"
JSON_SCHEMA_2020_12 = "http://json-schema.org/2020-12/schema"
SUPPORTED_SCHEMA_DIALECTS = [
    JSON_SCHEMA_2019_09,
    JSON_SCHEMA_2020_12,
]

def create_schema_store():
    ''' Creates a store that maps schema ids to schema documents '''

    # Find the directory with all the schemas in
    # TODO: find a neater way to get the file path
    schema_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../schemas')

    # Load all the schemas from this directory into the store
    schema_store = {}
    for f in os.scandir(schema_dir):
        if f.is_file() and f.path.endswith(".json"):
            abspath = os.path.abspath(f.path)
            with open(abspath) as schema_file:
                schema = json.load(schema_file)
            try:
                schema_store[schema["$id"]] = schema
            except KeyError:
                raise KeyError("$id not present in schema " + abspath)

    return schema_store


def walk_dict(obj, match_key, fn):
    for key, value in list(obj.items()):
        if key == match_key:
            fn(obj, key, value)
        elif isinstance(value, dict):
            walk_dict(value, match_key, fn)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    walk_dict(item, match_key, fn)


def bundle_schema(schema_store, root_schema_id):
    ''' Bundles all referenced schemas into the root schema '''

    root_schema = copy.deepcopy(schema_store[root_schema_id])

    # Check if the dialect is supported
    dialect = root_schema.get("$schema")
    if dialect is not None:
        assert dialect in SUPPORTED_SCHEMA_DIALECTS, \
            f"Root schema dialect must be one of {SUPPORTED_SCHEMA_DIALECTS}"
    
    # Locate referenced schemas recursively
    refs = set()
    ref_key = "$ref"
    def record_schema_reference(obj, key, value):
        assert key == ref_key
        if value in schema_store:
            refs.add(value)
    
    done = set()
    todo = set([root_schema_id])
    while todo:
        for schema_id in todo:
            schema = schema_store[schema_id]
            walk_dict(schema, ref_key, record_schema_reference)
            done.add(schema_id)
        todo = refs - done

    # Embed referenced schemas
    defs_key = "$defs"
    if defs_key not in root_schema:
        root_schema[defs_key] = {}
    defs = root_schema[defs_key]

    for schema_id in refs:
        schema = schema_store[schema_id]
        defs[schema_id] = schema

    return root_schema


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # TODO change the default to the top-level CovJSON schema
    parser.add_argument('--root', default='/schemas/domain')
    parser.add_argument('--out', default='bundle.json')
    args = parser.parse_args()
    
    store = create_schema_store()
    schema = bundle_schema(store, args.root)

    with open(args.out, "w") as f:
        json.dump(schema, f, indent=2)
