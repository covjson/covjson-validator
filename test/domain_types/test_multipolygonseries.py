# Pytests to test the MultiPolygonSeries domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_multipolygonseries_domain(validator, multipolygonseries_domain):
    ''' Tests an example of a MultiPolygonSeries domain '''

    validator.validate(multipolygonseries_domain)


def test_missing_composite_axis(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with missing 'composite' axis '''

    del multipolygonseries_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_empty_composite_axis(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with empty 'composite' axis '''

    multipolygonseries_domain["axes"]["composite"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_wrong_composite_axis_type(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with primitive instead of polygon axis '''

    multipolygonseries_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_wrong_composite_axis_type2(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with tuple instead of polygon axis (invalid polygons) '''

    multipolygonseries_domain["axes"]["composite"]["values"] = [ [1, 1], [2, 2], [3, 3] ]
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_composite_axis_with_2_values(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with composite axis with two polygons '''

    multipolygonseries_domain["axes"]["composite"]["values"] = [
        [ [ [101.0, 01.0], [102.0, 0.0], [102.0, 2.0], [101.0, 2.0], [101.0, 1.0] ] ],
        [ [ [101.0, 01.0], [102.0, 0.0], [102.0, 2.0], [101.0, 2.0], [101.0, 1.0] ] ]
    ]
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_wrong_data_type(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with wrong data type '''

    multipolygonseries_domain["axes"]["composite"]["dataType"] = "tuple"
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_extra_axis(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with unrecognised extra axis '''

    multipolygonseries_domain["axes"]["composite2"] = \
        multipolygonseries_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_empty_z_axis(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with empty 'z' axis '''

    multipolygonseries_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_multivalued_z_axis(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with multi-valued 'z' axis '''

    multipolygonseries_domain["axes"]["z"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


def test_empty_t_axis(validator, multipolygonseries_domain):
    ''' Invalid: MultiPolygonSeries domain with empty 't' axis '''

    multipolygonseries_domain["axes"]["t"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygonseries_domain)


# TODO do the `coordinates` have to be "x", "y" or can they also be "y", "x"?
