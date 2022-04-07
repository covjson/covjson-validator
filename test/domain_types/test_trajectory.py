# Pytests to test the Trajectory domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_trajectory_domain(validator, trajectory_domain):
    ''' Tests an example of a Trajectory domain '''

    validator.validate(trajectory_domain)


def test_missing_composite_axis(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with missing 'composite' axis '''

    del trajectory_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_empty_composite_axis(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with empty 'composite' axis '''

    trajectory_domain["axes"]["composite"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_wrong_composite_axis_type(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with primitive instead of tuple axis '''

    trajectory_domain["axes"]["composite"] = {
        "values": [1, 2, 3]
    }
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_composite_axis_with_2_values(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with composite axis with tuples of length 2 '''

    trajectory_domain["axes"]["composite"]["values"] = [
        ["2008-01-01T04:00:00Z", 1],
        ["2008-01-01T05:00:00Z", 2],
        ["2008-01-01T06:00:00Z", 3]
    ]
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_composite_axis_with_5_values(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with composite axis with tuples of length 5 '''

    trajectory_domain["axes"]["composite"]["values"] = [
        ["2008-01-01T04:00:00Z", 1, 1, 1, 1],
        ["2008-01-01T05:00:00Z", 2, 2, 2, 2],
        ["2008-01-01T06:00:00Z", 3, 3, 3, 3]
    ]
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_extra_axis(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with unrecognised extra axis '''

    trajectory_domain["axes"]["composite2"] = \
        trajectory_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_empty_z_axis(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with empty 'z' axis '''

    trajectory_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


def test_multivalued_z_axis(validator, trajectory_domain):
    ''' Invalid: Trajectory domain with multi-valued 'z' axis '''

    trajectory_domain["axes"]["z"] = { "values" : [1, 2] }
    with pytest.raises(ValidationError):
        validator.validate(trajectory_domain)


# TODO test coordinate identifiers of 'composite' axis
#      to be "t","x","y","z" or "t","x","y"
# TODO test there cannot be both 'z' in 'composite' and a 'z' axis
