# Pytests to test the MultiPolygon domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_multipolygon_domain(validator, multipolygon_domain):
    ''' Tests an example of a MultiPolygon domain '''

    validator.validate(multipolygon_domain)


def test_missing_composite_axis(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with missing 'composite' axis '''

    del multipolygon_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_empty_composite_axis(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with empty 'composite' axis '''

    multipolygon_domain["axes"]["composite"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_wrong_composite_axis_coordinates(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with invalid coordinates '''

    multipolygon_domain["axes"]["composite"]["coordinates"] = ["y", "x"]
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_wrong_composite_axis_type(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with primitive instead of polygon axis '''

    multipolygon_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_wrong_composite_axis_type2(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with tuple instead of polygon axis (invalid polygons) '''

    multipolygon_domain["axes"]["composite"]["values"] = [ [1, 1], [2, 2], [3, 3] ]
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_wrong_data_type(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with wrong data type '''

    multipolygon_domain["axes"]["composite"]["dataType"] = "tuple"
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_extra_axis(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with unrecognised extra axis '''

    multipolygon_domain["axes"]["composite2"] = \
        multipolygon_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_empty_z_axis(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with empty 'z' axis '''

    multipolygon_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_multivalued_z_axis(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with multi-valued 'z' axis '''

    multipolygon_domain["axes"]["z"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_empty_t_axis(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with empty 't' axis '''

    multipolygon_domain["axes"]["t"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)


def test_multivalued_t_axis(validator, multipolygon_domain):
    ''' Invalid: MultiPolygon domain with multi-valued 't' axis '''

    multipolygon_domain["axes"]["t"] = { "values" : ["2008-01-01T04:00:00Z", "2008-01-01T05:00:00Z"] }
    with pytest.raises(ValidationError):
        validator.validate(multipolygon_domain)
