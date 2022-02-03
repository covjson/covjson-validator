# Pytests to test the coverageCollection.json schema file

import pytest
from jsonschema.exceptions import ValidationError

import validator

VALIDATOR = validator.create_custom_validator("/schemas/coverageCollection")


def get_sample_coverage_collection():
    ''' Returns a sample of a valid collection collection '''

    return {
        "type" : "CoverageCollection",
        "parameters" : {
            "PSAL": {
                "type" : "Parameter",
                "description" : {
                    "en": "The measured salinity, in practical salinity units (psu) of the sea water"
                },
                "unit" : {
                    "symbol" : "psu"
                },
                "observedProperty" : {
                    "id": "http://vocab.nerc.ac.uk/standard_name/sea_water_salinity/",
                    "label" : {
                        "en": "Sea Water Salinity"
                    }
                }
            }
        },
        "referencing": [{
            "coordinates": ["x", "y"],
            "system": {
                "type": "GeographicCRS",
                "id": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            }
        }, {
            "coordinates": ["z"],
            "system": {
                "type": "VerticalCRS",
                "id": "http://www.opengis.net/def/crs/EPSG/0/5703"
            }
        }, {
            "coordinates": ["t"],
            "system": {
                "type": "TemporalRS",
                "calendar": "Gregorian"
            }
        }],
        "domainType" : "VerticalProfile",
        "coverages": [
            {
                "type" : "Coverage",
                "domain" : {
                    "type": "Domain",
                    "axes": {
                        "x": { "values": [-10.1] },
                        "y": { "values": [-40.2] },
                        "z": { "values": [ 5, 8, 14 ] },
                        "t": { "values": ["2013-01-13T11:12:20Z"] }
                    }
                },
                "ranges" : {
                    "PSAL" : {
                        "type" : "NdArray",
                        "dataType": "float",
                        "axisNames": ["z"],
                        "shape": [3],
                        "values" : [ 43.7, 43.8, 43.9 ]
                    }
                }
            }, {
                "type" : "Coverage",
                "domain" : {
                    "type": "Domain",
                    "axes": {
                        "x": { "values": [-11.1] },
                        "y": { "values": [-45.2] },
                        "z": { "values": [ 4, 7, 9 ] },
                        "t": { "values": ["2013-01-13T12:12:20Z"] }
                    }
                },
                "ranges" : {
                    "PSAL" : {
                        "type" : "NdArray",
                        "dataType": "float",
                        "axisNames": ["z"],
                        "shape": [3],
                        "values" : [ 42.7, 41.8, 40.9 ]
                    }
                }
            }
        ]
    }


def test_valid_coverage_collection():
    ''' Valid: Tests an example of a collection '''

    collection = get_sample_coverage_collection()
    VALIDATOR.validate(collection)


def test_parameters_per_coverage():
    ''' Valid: Collection with "parameters" embedded inside coverages '''

    collection = get_sample_coverage_collection()
    parameters = collection["parameters"]
    del collection["parameters"]
    for coverage in collection["coverages"]:
        coverage["parameters"] = parameters
    VALIDATOR.validate(collection)


def test_referencing_per_coverage():
    ''' Valid: Collection with "referencing" embedded inside coverage domains '''

    collection = get_sample_coverage_collection()
    referencing = collection["referencing"]
    del collection["referencing"]
    for coverage in collection["coverages"]:
        coverage["domain"]["referencing"] = referencing
    VALIDATOR.validate(collection)


def test_referencing_per_coverage_with_domain_url():
    ''' Valid: Collection with "referencing" embedded inside remote coverage domains '''

    collection = get_sample_coverage_collection()
    del collection["referencing"]
    for coverage in collection["coverages"]:
        coverage["domain"] = "http://example.com/domain.json"
    VALIDATOR.validate(collection)


def test_missing_type():
    ''' Invalid: Collection with missing "type" '''

    collection = get_sample_coverage_collection()
    del collection["type"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_misspelled_type():
    ''' Invalid: Collection with misspelled "type" '''

    collection = get_sample_coverage_collection()
    collection["type"] = "Collection"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_missing_coverages():
    ''' Invalid: Collection with missing "coverages" '''

    collection = get_sample_coverage_collection()
    del collection["coverages"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_incorrect_coverages_type():
    ''' Invalid: Collection with incorrect "coverages" type '''

    collection = get_sample_coverage_collection()
    collection["coverages"] = "http://example.com/coverages.json"
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_incorrect_coverages_member_type():
    ''' Invalid: Collection with incorrect "coverages" member type '''

    collection = get_sample_coverage_collection()
    collection["coverages"][0]["type"] = [ "NotACoverage" ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_incorrect_domain_type_type():
    ''' Invalid: Collection with incorrect "domainType" type '''

    collection = get_sample_coverage_collection()
    collection["domainType"] = [ "VerticalProfile" ]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_missing_parameters():
    ''' Invalid: Collection with missing "parameters" (incl. inside coverage) '''

    collection = get_sample_coverage_collection()
    del collection["parameters"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_incorrect_parameters_type():
    ''' Invalid: Collection with incorrect "parameters" type '''

    collection = get_sample_coverage_collection()
    collection["parameters"] = list(collection["parameters"].values())
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_incorrect_parameter_groups_type():
    ''' Invalid: Collection with incorrect "parameterGroups" type '''

    collection = get_sample_coverage_collection()
    collection["parameterGroups"] = collection["parameters"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_missing_referencing():
    ''' Invalid: Collection with missing "referencing" (incl. inside coverage) '''

    collection = get_sample_coverage_collection()
    del collection["referencing"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


def test_incorrect_referencing_type():
    ''' Invalid: Coverage with incorrect "referencing" type '''

    collection = get_sample_coverage_collection()
    del collection["referencing"][0]["coordinates"]
    with pytest.raises(ValidationError):
        VALIDATOR.validate(collection)


# TODO test that all coverage ranges reference a parameter in scope
