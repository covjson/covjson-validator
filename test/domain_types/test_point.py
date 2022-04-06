# Pytests to test the Point domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_point_domain(validator, point_domain):
    ''' Tests an example of a Point domain '''

    validator.validate(point_domain)


def test_missing_x_axis(validator, point_domain):
    ''' Invalid: Point domain with missing 'x' axis '''

    del point_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_missing_y_axis(validator, point_domain):
    ''' Invalid: Point domain with missing 'y' axis '''

    del point_domain["axes"]["y"]
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_empty_x_axis(validator, point_domain):
    ''' Invalid: Point domain with empty 'x' axis '''

    point_domain["axes"]["x"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_empty_y_axis(validator, point_domain):
    ''' Invalid: Point domain with empty 'y' axis '''

    point_domain["axes"]["y"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_multivalued_x_axis(validator, point_domain):
    ''' Invalid: Point domain with multi-valued 'x' axis '''

    point_domain["axes"]["x"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_multivalued_y_axis(validator, point_domain):
    ''' Invalid: Point domain with multi-valued 'y' axis '''

    point_domain["axes"]["y"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_multivalued_z_axis(validator, point_domain):
    ''' Invalid: Point domain with multi-valued 'z' axis '''

    point_domain["axes"]["z"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_multivalued_t_axis(validator, point_domain):
    ''' Invalid: Point domain with multi-valued 't' axis '''

    point_domain["axes"]["t"] = { "values" : ["2008-01-01T04:00:00Z", "2008-01-01T05:00:00Z"] }
    with pytest.raises(ValidationError):
        validator.validate(point_domain)


def test_extra_axis(validator, point_domain):
    ''' Invalid: Point domain with unrecognised extra axis '''

    point_domain["axes"]["x2"] = \
        point_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(point_domain)
