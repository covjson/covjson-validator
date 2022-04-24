# Pytests to test the Polygon domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_polygon_domain(validator, polygon_domain):
    ''' Tests an example of a Polygon domain '''

    validator.validate(polygon_domain)


def test_missing_composite_axis(validator, polygon_domain):
    ''' Invalid: Polygon domain with missing 'composite' axis '''

    del polygon_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_empty_composite_axis(validator, polygon_domain):
    ''' Invalid: Polygon domain with empty 'composite' axis '''

    polygon_domain["axes"]["composite"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_wrong_composite_axis_type(validator, polygon_domain):
    ''' Invalid: Polygon domain with primitive instead of polygon axis '''

    polygon_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_wrong_composite_axis_type2(validator, polygon_domain):
    ''' Invalid: Polygon domain with tuple instead of polygon axis (invalid polygons) '''

    polygon_domain["axes"]["composite"]["values"] = [ [1, 1], [2, 2], [3, 3] ]
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_composite_axis_with_2_values(validator, polygon_domain):
    ''' Invalid: Polygon domain with composite axis with two polygons '''

    polygon_domain["axes"]["composite"]["values"] = [
        [ [ [100.0, 1.0], [101.0, 0.0], [101.0, 2.0], [100.0, 2.0], [100.0, 1.0] ] ],
        [ [ [101.0, 1.0], [102.0, 0.0], [102.0, 2.0], [101.0, 2.0], [101.0, 1.0] ] ]
    ]
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_wrong_composite_axis_coordinates(validator, polygon_domain):
    ''' Invalid: Polygon domain with invalid coordinates '''

    polygon_domain["axes"]["composite"]["coordinates"] = ["y", "x"]
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_wrong_data_type(validator, polygon_domain):
    ''' Invalid: Polygon domain with wrong data type '''

    polygon_domain["axes"]["composite"]["dataType"] = "tuple"
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_extra_axis(validator, polygon_domain):
    ''' Invalid: Polygon domain with unrecognised extra axis '''

    polygon_domain["axes"]["composite2"] = \
        polygon_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_empty_z_axis(validator, polygon_domain):
    ''' Invalid: Polygon domain with empty 'z' axis '''

    polygon_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_multivalued_z_axis(validator, polygon_domain):
    ''' Invalid: Polygon domain with multi-valued 'z' axis '''

    polygon_domain["axes"]["z"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_empty_t_axis(validator, polygon_domain):
    ''' Invalid: Polygon domain with empty 't' axis '''

    polygon_domain["axes"]["t"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)


def test_multivalued_t_axis(validator, polygon_domain):
    ''' Invalid: Polygon domain with multi-valued 't' axis '''

    polygon_domain["axes"]["t"] = { "values" : ["2008-01-01T04:00:00Z", "2008-01-01T05:00:00Z"] }
    with pytest.raises(ValidationError):
        validator.validate(polygon_domain)
