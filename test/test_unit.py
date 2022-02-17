# Tests unit.json schema

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/unit")


def test_unit_with_symbol_string(validator):
    ''' Tests a unit where we use a string for the symbol '''

    unit = { "symbol" : "m" }
    validator.validate(unit)


def test_unit_with_typed_symbol(validator):
    ''' Tests a unit where we use a typed symbol '''

    unit = {
        "label" : { "en" : "Degree Celsius" },
        "symbol" :
        {
            "type" : "http://www.opengis.net/def/uom/UCUM/",
            "value" : "Cel"
        }
    }
    validator.validate(unit)


def test_unit_with_label_only(validator):
    ''' Tests a unit where we only have a label, no symbol '''

    unit = { "label" : { "en" : "Degree Celsius" } }
    validator.validate(unit)


def test_unit_with_label_and_symbol(validator):
    ''' Tests a unit where we have both a label and a symbol '''

    unit = {
        "label" : { "en" : "Degree Celsius" },
        "symbol" :
        {
            "type" : "http://www.opengis.net/def/uom/UCUM/",
            "value" : "Cel"
        }
    }
    validator.validate(unit)


def test_no_label_or_symbol(validator):
    ''' Invalid: unit must have either label or symbol'''

    unit = { "id" : "http://example.com/my_unit" }
    with pytest.raises(ValidationError):
        validator.validate(unit)


def test_unit_with_typed_symbol_missing_type(validator):
    ''' Invalid: typed symbol must have "type" property '''

    unit = { "symbol" : { "value" : "Cel" } }
    with pytest.raises(ValidationError):
        validator.validate(unit)


def test_unit_with_typed_symbol_missing_value(validator):
    ''' Invalid: typed symbol must have "label" property '''

    unit = { "symbol" : { "type" : "http://www.opengis.net/def/uom/UCUM/" } }
    with pytest.raises(ValidationError):
        validator.validate(unit)
