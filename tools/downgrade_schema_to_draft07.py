# A tool that transforms a bundled schema as created by bundle_schema.py
# from 2020-12 to draft-07 JSON Schema dialect while only
# using local JSON Pointer references (most compatible).

# Note: This tool is specialized to the way schemas are written
# in this repository and is not intended to be used elsewhere.

import argparse
import json
import copy

JSON_SCHEMA_DRAFT_07 = "http://json-schema.org/draft-07/schema"


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


def downgrade_schema_to_draft07(root_schema):
    ''' Downgrades a schema to draft-07 JSON Schema dialect '''
    
    root_schema = copy.deepcopy(root_schema)

    schema_key = "$schema"
    if root_schema.get(schema_key) == JSON_SCHEMA_DRAFT_07:
        return root_schema
    
    # Change dialect declaration
    root_schema[schema_key] = JSON_SCHEMA_DRAFT_07

    # Move all "$defs" to top-level "definitions"
    definitions_key = "definitions"
    assert definitions_key not in root_schema
    root_schema[definitions_key] = definitions = {}

    defs_key = "$defs"
    id_key = "$id"
    def move_defs(obj, key, value):
        assert key == defs_key
        schema_id_prefix = "/schemas/"
        for name, schema in value.items():
            if id_key in schema:
                name = schema[id_key][len(schema_id_prefix):]
                del schema[id_key]
            assert name not in definitions, \
                f"Duplicate definition name '{name}'"
            definitions[name] = schema
        del obj[defs_key]
    
    walk_dict(root_schema, defs_key, move_defs)
    root_schema[definitions_key] = dict(sorted(definitions.items()))
    
    # Change all "$ref" values to use JSON pointer syntax
    ref_key = "$ref"
    def patch_ref(obj, key, value):
        assert key == ref_key
        definitions_prefix = "#/definitions/"
        new_value = value.replace("/schemas/", definitions_prefix)
        new_value = new_value.replace("#/$defs/", definitions_prefix)
        assert new_value.startswith(definitions_prefix), \
            f"Invalid $ref value '{value}', must start with '{definitions_prefix}'"
        definitions_name = new_value[len(definitions_prefix):]
        assert definitions_name in definitions, \
            f"Invalid $ref value '{value}', '{definitions_name}' not found " + \
            f"in definitions: {', '.join(definitions.keys())}"
        obj[key] = new_value

    walk_dict(root_schema, ref_key, patch_ref)

    # Rename "dependentSchemas" to "dependencies"
    dependent_schemas_key = "dependentSchemas"
    dependencies_key = "dependencies"

    def patch_dependent_schemas(obj, key, value):
        assert key == dependent_schemas_key
        assert dependencies_key not in obj
        obj[dependencies_key] = value
        del obj[dependent_schemas_key]

    walk_dict(root_schema, dependent_schemas_key, patch_dependent_schemas)
    
    return root_schema


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path')
    parser.add_argument('--out', dest='output_path',
                        help='Output file (default: input file)')
    args = parser.parse_args()
    if args.output_path is None:
        args.output_path = args.input_path
    
    with open(args.input_path) as f:
        schema = json.load(f)

    schema = downgrade_schema_to_draft07(schema)

    with open(args.output_path, "w") as f:
        json.dump(schema, f, indent=2)
