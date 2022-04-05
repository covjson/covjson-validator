# Pytests to test the referenceSystem.json schema file

# TODO: test that "calendar" is "Gregorian" or a URI

import pytest
from jsonschema.exceptions import ValidationError

pytestmark = pytest.mark.schema("/schemas/referenceSystem")


def test_geographic_rs(validator):
    ''' Tests a minimal geographic RS '''

    crs = {
        "type" : "GeographicCRS",
        "id" : "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
    }
    validator.validate(crs)


def test_projected_rs(validator):
    ''' Tests a minimal projected RS '''

    crs = {
        "type" : "ProjectedCRS",
        "id" : "http://www.opengis.net/def/crs/EPSG/0/27700"
    }
    validator.validate(crs)


def test_vertical_rs(validator):
    ''' Tests a minimal vertical RS '''

    crs = {
        "type" : "VerticalCRS",
        "id" : "http://www.opengis.net/def/crs/EPSG/0/5703"
    }
    validator.validate(crs)


def test_minimal_temporal_rs(validator):
    ''' Tests a minimal temporal RS '''

    crs = {
        "type" : "TemporalRS",
        "calendar" : "Gregorian"
    }
    validator.validate(crs)


def test_identifier_rs(validator):
    ''' Tests an example of an IdentifierRS '''

    crs = {
        "type": "IdentifierRS",
        "id": "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2",
        "label": { "en": "ISO 3166-1 alpha-2 codes" },
        "targetConcept": {
            "id": "http://dbpedia.org/resource/Country",
            "label": {"en": "Country", "de": "Land" }
        },
        "identifiers": {
            "de": {
                "id": "http://dbpedia.org/resource/Germany",
                "label": { "de": "Deutschland", "en": "Germany" }
            },
            "gb": {
                "id": "http://dbpedia.org/resource/United_Kingdom",
                "label": { "de": "Vereinigtes Königreich", "en": "United Kingdom" }
            }
        }
    }
    validator.validate(crs)


def test_missing_type(validator):
    ''' Tests an RS with a missing type '''

    crs = { "id" : "http://www.opengis.net/def/crs/OGC/1.3/CRS84" }
    with pytest.raises(ValidationError):
        validator.validate(crs)


def test_missing_calendar(validator):
    ''' Tests a TemporalRS with a missing calendar '''

    crs = { "type" : "TemporalRS" }
    with pytest.raises(ValidationError):
        validator.validate(crs)


def test_missing_target_concept(validator):
    ''' Tests an IdentifierRS with a missing targetConcept '''

    crs = {
        "type": "IdentifierRS",
        "id": "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2",
        "label": { "en": "ISO 3166-1 alpha-2 codes" },
        "identifiers": {
            "de": {
                "id": "http://dbpedia.org/resource/Germany",
                "label": { "de": "Deutschland", "en": "Germany" }
            },
            "gb": {
                "id": "http://dbpedia.org/resource/United_Kingdom",
                "label": { "de": "Vereinigtes Königreich", "en": "United Kingdom" }
            }
        }
    }
    with pytest.raises(ValidationError):
        validator.validate(crs)


def test_invalid_target_concept(validator):
    ''' Tests an IdentifierRS with an invalid targetConcept (missing label) '''

    crs = {
        "type": "IdentifierRS",
        "id": "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2",
        "label": { "en": "ISO 3166-1 alpha-2 codes" },
        "targetConcept": {
            "id": "http://dbpedia.org/resource/Country"
        },
        "identifiers": {
            "de": {
                "id": "http://dbpedia.org/resource/Germany",
                "label": { "de": "Deutschland", "en": "Germany" }
            },
            "gb": {
                "id": "http://dbpedia.org/resource/United_Kingdom",
                "label": { "de": "Vereinigtes Königreich", "en": "United Kingdom" }
            }
        }
    }
    with pytest.raises(ValidationError):
        validator.validate(crs)


def test_invalid_identifier(validator):
    ''' Tests an IdentifierRS with an invalid identifier (missing label) '''

    crs = {
        "type": "IdentifierRS",
        "id": "https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2",
        "label": { "en": "ISO 3166-1 alpha-2 codes" },
        "targetConcept": {
            "id": "http://dbpedia.org/resource/Country",
            "label": {"en": "Country", "de": "Land" }
        },
        "identifiers": {
            "de": {
                "id": "http://dbpedia.org/resource/Germany"
            },
            "gb": {
                "id": "http://dbpedia.org/resource/United_Kingdom",
                "label": { "de": "Vereinigtes Königreich", "en": "United Kingdom" }
            }
        }
    }
    with pytest.raises(ValidationError):
        validator.validate(crs)
