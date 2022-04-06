# Pytests to test the VerticalProfile domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_verticalprofile_domain(validator, verticalprofile_domain):
    ''' Tests an example of a VerticalProfile domain '''

    validator.validate(verticalprofile_domain)


def test_missing_x_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with missing 'x' axis '''

    del verticalprofile_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_missing_y_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with missing 'y' axis '''

    del verticalprofile_domain["axes"]["y"]
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_missing_z_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with missing 'z' axis '''

    del verticalprofile_domain["axes"]["z"]
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_empty_x_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with empty 'x' axis '''

    verticalprofile_domain["axes"]["x"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_empty_y_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with empty 'y' axis '''

    verticalprofile_domain["axes"]["y"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_empty_z_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with empty 'z' axis '''

    verticalprofile_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_multivalued_x_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with multi-valued 'x' axis '''

    verticalprofile_domain["axes"]["x"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_multivalued_y_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with multi-valued 'y' axis '''

    verticalprofile_domain["axes"]["y"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)


def test_extra_axis(validator, verticalprofile_domain):
    ''' Invalid: VerticalProfile domain with unrecognised extra axis '''

    verticalprofile_domain["axes"]["x2"] = \
        verticalprofile_domain["axes"]["x"]
    with pytest.raises(ValidationError):
        validator.validate(verticalprofile_domain)
