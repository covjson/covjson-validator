# Tests unit.json schema

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/unit")


def test_unit_with_symbol_string():
    ''' Tests a unit where we use a string for the symbol '''

    unit = { "symbol" : "m" }
    VALIDATOR.validate(unit)


def test_unit_with_typed_symbol():
    ''' Tests a unit where we use a typed symbol '''

    unit = {
        "label" : { "en" : "Degree Celsius" },
        "symbol" :
        {
            "type" : "http://www.opengis.net/def/uom/UCUM/",
            "value" : "Cel"
        }
    }
    VALIDATOR.validate(unit)


def test_unit_with_label_only():
    ''' Tests a unit where we only have a label, no symbol '''

    unit = { "label" : { "en" : "Degree Celsius" } }
    VALIDATOR.validate(unit)


def test_no_label_or_symbol():
    ''' Invalid: unit must have either label or symbol'''

    unit = { "id" : "http://example.com/my_unit" }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(unit)


def test_unit_with_typed_symbol_missing_type():
    ''' Invalid: typed symbol must have "type" property '''

    unit = { "symbol" : { "value" : "Cel" } }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(unit)


def test_unit_with_typed_symbol_missing_value():
    ''' Invalid: typed symbol must have "label" property '''

    unit = { "symbol" : { "type" : "http://www.opengis.net/def/uom/UCUM/" } }
    with pytest.raises(ValidationError):
        VALIDATOR.validate(unit)
