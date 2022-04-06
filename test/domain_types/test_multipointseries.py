# Pytests to test the MultiPointSeries domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_multipointseries_domain(validator, multipointseries_domain):
    ''' Tests an example of a MultiPointSeries domain '''

    validator.validate(multipointseries_domain)


def test_missing_composite_axis(validator, multipointseries_domain):
    ''' Invalid: MultiPointSeries domain with missing 'composite' axis '''

    del multipointseries_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipointseries_domain)


def test_missing_t_axis(validator, multipointseries_domain):
    ''' Invalid: MultiPointSeries domain with missing 't' axis '''

    del multipointseries_domain["axes"]["t"]
    with pytest.raises(ValidationError):
        validator.validate(multipointseries_domain)


def test_wrong_composite_axis_type(validator, multipointseries_domain):
    ''' Invalid: MultiPointSeries domain with primitive instead of tuple axis '''

    multipointseries_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(multipointseries_domain)


def test_extra_axis(validator, multipointseries_domain):
    ''' Invalid: MultiPointSeries domain with unrecognised extra axis '''

    multipointseries_domain["axes"]["composite2"] = \
        multipointseries_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(multipointseries_domain)


# TODO test coordinate identifiers of 'composite' axis
#      to be "x","y","z" or "x","y"
# TODO test that all values in 'composite' axis are valid and consistent tuples
