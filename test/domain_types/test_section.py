# Pytests to test the Section domain type in the domain.json schema file

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/domain")


@pytest.mark.exhaustive
def test_valid_section_domain(validator, section_domain):
    ''' Tests an example of a Section domain '''

    validator.validate(section_domain)


def test_missing_composite_axis(validator, section_domain):
    ''' Invalid: Section domain with missing 'composite' axis '''

    del section_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_empty_composite_axis(validator, section_domain):
    ''' Invalid: MultiPointSeries domain with empty 'composite' axis '''

    section_domain["axes"]["composite"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_composite_axis_with_2_values(validator, section_domain):
    ''' Invalid: Section domain with composite axis with tuples of length 2 '''

    section_domain["axes"]["composite"]["values"] = [
        ["2008-01-01T04:00:00Z", 1],
        ["2008-01-01T05:00:00Z", 2],
        ["2008-01-01T06:00:00Z", 3]
    ]
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_composite_axis_with_4_values(validator, section_domain):
    ''' Invalid: Section domain with composite axis with tuples of length 4 '''

    section_domain["axes"]["composite"]["values"] = [
        ["2008-01-01T04:00:00Z", 1, 1, 1],
        ["2008-01-01T05:00:00Z", 2, 2, 2],
        ["2008-01-01T06:00:00Z", 3, 3, 3]
    ]
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_wrong_composite_axis_type(validator, section_domain):
    ''' Invalid: Section domain with primitive instead of tuple axis '''

    section_domain["axes"]["composite"]["values"] = [1, 2, 3]
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_wrong_composite_axis_coordinates(validator, section_domain):
    ''' Invalid: Section domain with invalid coordinates '''

    section_domain["axes"]["composite"]["coordinates"] = ["t", "y", "x"]
    print(section_domain)
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_extra_axis(validator, section_domain):
    ''' Invalid: Section domain with unrecognised extra axis '''

    section_domain["axes"]["composite2"] = \
        section_domain["axes"]["composite"]
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_missing_z_axis(validator, section_domain):
    ''' Invalid: Section domain with missing 'z' axis '''

    del section_domain["axes"]["z"]
    with pytest.raises(ValidationError):
        validator.validate(section_domain)


def test_empty_z_axis(validator, section_domain):
    ''' Invalid: Section domain with empty 'z' axis '''

    section_domain["axes"]["z"] = { "values" : [] }
    with pytest.raises(ValidationError):
        validator.validate(section_domain)
