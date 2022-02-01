# Pytests to test the tiledNdArray.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/tiledNdArray")

def get_example_tiled_ndarray():
    return {
        "type" : "TiledNdArray",
        "dataType": "float",
        "axisNames": ["t", "y", "x"],
        "shape": [2, 5, 10],
        "tileSets": [{
            "tileShape": [None, None, None],
            "urlTemplate": "http://example.com/a/all.covjson"
        }, {
            "tileShape": [1, None, None],
            "urlTemplate": "http://example.com/b/{t}.covjson"
        }, {
            "tileShape": [None, 2, 3],
            "urlTemplate": "http://example.com/c/{y}-{x}.covjson"
        }]
    }

def test_valid_float_tiled_ndarray():
    ''' Valid: A tiled ndarray with float data type '''

    tiled_ndarray = get_example_tiled_ndarray()
    VALIDATOR.validate(tiled_ndarray)


def test_valid_integer_ndarray():
    ''' Valid: A simple integer ndarray '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["dataType"] = "integer"
    VALIDATOR.validate(tiled_ndarray)


def test_valid_string_ndarray():
    ''' Valid: A simple string ndarray '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["dataType"] = "string"
    VALIDATOR.validate(tiled_ndarray)


def test_missing_type():
    ''' Invalid: Tiled ndarray with missing "type" '''

    tiled_ndarray = get_example_tiled_ndarray()
    del tiled_ndarray["type"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_misspelled_type():
    ''' Invalid: Tiled ndarray with misspelled "type" '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["type"] = "TiledNdarray"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_missing_data_type():
    ''' Invalid: Tiled ndarray with missing "dataType" '''

    tiled_ndarray = get_example_tiled_ndarray()
    del tiled_ndarray["dataType"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_unknown_data_type():
    ''' Invalid: Tiled ndarray with unknown "dataType" '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["dataType"] = "float64"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_incorrect_shape_type():
    ''' Invalid: Tiled ndarray with incorrect "shape" type '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["shape"] = [ "4", "2" ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_missing_shape():
    ''' Invalid: Tiled ndarray with missing "shape" '''

    tiled_ndarray = get_example_tiled_ndarray()
    del tiled_ndarray["shape"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_empty_shape():
    ''' Invalid: Tiled ndarray with empty "shape" '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["shape"] = [ ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_incorrect_axis_names_type():
    ''' Invalid: Tiled ndarray with incorrect "axisNames" type '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["axisNames"] = [ 0, 1 ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_missing_axis_names():
    ''' Invalid: Tiled ndarray with missing "axisNames" '''

    tiled_ndarray = get_example_tiled_ndarray()
    del tiled_ndarray["axisNames"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_empty_axis_names():
    ''' Invalid: Tiled ndarray with empty "axisNames" '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["axisNames"] = []
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_empty_tilesets():
    ''' Invalid: Tiled ndarray with empty "tileSets" '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["tileSets"] = []
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_missing_tilesets():
    ''' Invalid: Tiled ndarray with missing "tileSets" '''

    tiled_ndarray = get_example_tiled_ndarray()
    del tiled_ndarray["tileSets"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_incorrect_tileset_type():
    ''' Invalid: Tiled ndarray with incorrect "tileSets" item type '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["tileSets"] = [ "http://example.com/c/{y}-{x}.covjson" ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_missing_tile_shape():
    ''' Invalid: Tiled ndarray with missing "tileShape" '''

    tiled_ndarray = get_example_tiled_ndarray()
    del tiled_ndarray["tileSets"][0]["tileShape"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_empty_tile_shape():
    ''' Invalid: Tiled ndarray with empty "tileShape" '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["tileSets"][0]["tileShape"] = []
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_incorrect_tile_shape_type():
    ''' Invalid: Tiled ndarray with incorrect "tileShape" type '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["tileSets"][0]["tileShape"] = 10
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_missing_url_template():
    ''' Invalid: Tiled ndarray with missing "urlTemplate" '''

    tiled_ndarray = get_example_tiled_ndarray()
    del tiled_ndarray["tileSets"][0]["urlTemplate"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)


def test_incorrect_url_template_type():
    ''' Invalid: Tiled ndarray with incorrect "urlTemplate" type '''

    tiled_ndarray = get_example_tiled_ndarray()
    tiled_ndarray["tileSets"][0]["urlTemplate"] = \
         [ tiled_ndarray["tileSets"][0]["urlTemplate"] ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(tiled_ndarray)



# TODO test that "shape" and "axisNames" have the same length
# TODO test that "tileShape" has the same length as "shape"
# TODO test that "urlTemplate" is a valid RFC 6570 Level 1 URI template
# TODO test that "urlTemplate" contains the right '{}' variables
