# Pytests to test the MultiPoint domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_multipoint_domain(validator, multipoint_domain):
    ''' Tests an example of a MultiPoint domain '''

    validator.validate(multipoint_domain)


def test_missing_composite_axis(validator, multipoint_domain):
    ''' Invalid: MultiPoint domain with missing 'composite' axis '''

    del multipoint_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipoint_domain)


def test_empty_composite_axis(validator, multipoint_domain):
    ''' Invalid: MultiPoint domain with empty 'composite' axis '''

    multipoint_domain["axes"]["composite"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipoint_domain)


def test_wrong_composite_axis_type(validator, multipoint_domain):
    ''' Invalid: MultiPoint domain with primitive instead of tuple axis '''

    multipoint_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(multipoint_domain)


def test_extra_axis(validator, multipoint_domain):
    ''' Invalid: MultiPoint domain with unrecognised extra axis '''

    multipoint_domain["axes"]["composite2"] = \
        multipoint_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipoint_domain)


def test_multivalued_t_axis(validator, multipoint_domain):
    ''' Invalid: MultiPoint domain with multi-valued 't' axis '''

    multipoint_domain["axes"]["t"] = { "values" : ["2008-01-01T04:00:00Z", "2008-01-01T05:00:00Z"] }
    with pytest.raises(ValidationError):
        validator.validate(multipoint_domain)


def test_empty_t_axis(validator, multipoint_domain):
    ''' Invalid: MultiPoint domain with empty 't' axis '''

    multipoint_domain["axes"]["t"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(multipoint_domain)


# TODO test coordinate identifiers of 'composite' axis
#      to be "x","y","z" or "x","y"
