# Pytests to test the PolygonSeries domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_polygonseries_domain(validator, polygonseries_domain):
    ''' Tests an example of a PolygonSeries domain '''

    validator.validate(polygonseries_domain)


def test_missing_composite_axis(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with missing 'composite' axis '''

    del polygonseries_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_empty_composite_axis(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with empty 'composite' axis '''

    polygonseries_domain["axes"]["composite"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_wrong_composite_axis_type(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with primitive instead of polygon axis '''

    polygonseries_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_wrong_composite_axis_coordinates(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with invalid coordinates '''

    polygonseries_domain["axes"]["composite"]["coordinates"] = ["y", "x"]
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_wrong_composite_axis_type2(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with tuple instead of polygon axis (invalid polygons) '''

    polygonseries_domain["axes"]["composite"]["values"] = [ [1, 1], [2, 2], [3, 3] ]
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_composite_axis_with_2_values(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with composite axis with two polygons '''

    polygonseries_domain["axes"]["composite"]["values"] = [
        [ [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ] ],
        [ [ [101.0, 1.0], [102.0, 0.0], [102.0, 2.0], [101.0, 2.0], [101.0, 1.0] ] ]
    ]
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_wrong_data_type(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with wrong data type '''

    polygonseries_domain["axes"]["composite"]["dataType"] = "tuple"
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_extra_axis(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with unrecognised extra axis '''

    polygonseries_domain["axes"]["composite2"] = \
        polygonseries_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_empty_z_axis(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with empty 'z' axis '''

    polygonseries_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_multivalued_z_axis(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with multi-valued 'z' axis '''

    polygonseries_domain["axes"]["z"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)


def test_empty_t_axis(validator, polygonseries_domain):
    ''' Invalid: PolygonSeries domain with empty 't' axis '''

    polygonseries_domain["axes"]["t"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(polygonseries_domain)
