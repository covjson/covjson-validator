# A tool that patches properties of an existing schema.

# Note: This tool is specialized to the way schemas are stored and
# written in this repository and is not intended to be used elsewhere.

import argparse
import json
import copy

def patch_schema(schema: dict, set_id=None, drop_id=False):
    ''' Patches some properties of the given schema '''

    schema = copy.deepcopy(schema)

    if drop_id:
        schema.pop("$id", None)
    elif set_id:
        schema["$id"] = set_id

    return schema

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path')
    parser.add_argument('--out', dest='output_path',
                        help='Output file (default: input file)')
    parser.add_argument('--set-id', type=str, help='Set $id property value')
    parser.add_argument('--drop-id', action='store_true', help='Drop $id property')
    args = parser.parse_args()
    if args.output_path is None:
        args.output_path = args.input_path

    with open(args.input_path) as f:
        schema = json.load(f)

    schema = patch_schema(schema, args.set_id, args.drop_id)

    with open(args.output_path, "w") as f:
        json.dump(schema, f, indent=2)
