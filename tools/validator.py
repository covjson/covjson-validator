# Creates a custom JSON schema validator with a reference resolver
# that can resolve any reference in the /schemas directory

import os
import json
import jsonschema


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


def create_custom_validator(schema_id, schema_store=None):
    ''' Creates a validator that uses the custom schema store '''

    if schema_store is None:
        schema_store = create_schema_store()
    schema = schema_store[schema_id]

    resolver = jsonschema.RefResolver(None, referrer=None, store=schema_store)
    # TODO: should be able to use validator_for(schema) to get an appropriate
    # validator, but the resulting validator doesn't seem to work
    validator = jsonschema.validators.Draft202012Validator(schema, resolver=resolver)

    return validator


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('covjson_path', type=str,
                        help='Path to CoverageJSON document')
    args = parser.parse_args()

    with open(args.covjson_path, encoding="utf-8") as f:
        obj = json.load(f)
    
    validator = create_custom_validator("/schemas/coveragejson")
    validator.validate(obj)
    print("Valid!")
