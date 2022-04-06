# Pytests to test the PointSeries domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_pointseries_domain(validator, pointseries_domain):
    ''' Tests an example of a PointSeries domain '''

    validator.validate(pointseries_domain)


def test_missing_x_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with missing 'x' axis '''

    del pointseries_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_missing_y_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with missing 'y' axis '''

    del pointseries_domain["axes"]["y"]
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_missing_t_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with missing 't' axis '''

    del pointseries_domain["axes"]["t"]
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_empty_x_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with empty 'x' axis '''

    pointseries_domain["axes"]["x"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_empty_y_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with empty 'y' axis '''

    pointseries_domain["axes"]["y"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_empty_t_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with empty 't' axis '''

    pointseries_domain["axes"]["t"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_multivalued_x_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with multi-valued 'x' axis '''

    pointseries_domain["axes"]["x"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_multivalued_y_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with multi-valued 'y' axis '''

    pointseries_domain["axes"]["y"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_multivalued_z_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with multi-valued 'z' axis '''

    pointseries_domain["axes"]["z"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)


def test_extra_axis(validator, pointseries_domain):
    ''' Invalid: PointSeries domain with unrecognised extra axis '''

    pointseries_domain["axes"]["x2"] = \
        pointseries_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(pointseries_domain)
