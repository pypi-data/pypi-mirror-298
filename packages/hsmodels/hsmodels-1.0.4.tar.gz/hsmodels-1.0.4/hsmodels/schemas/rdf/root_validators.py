from rdflib import URIRef

from hsmodels.schemas.enums import CoverageType, DateType, MultidimensionalSpatialReferenceType, SpatialReferenceType
from hsmodels.utils import to_coverage_value_string


def parse_coverages(cls, values):
    if "coverages" in values:
        return values
    if "spatial_coverage" in values or "period_coverage" in values:
        assert "coverages" not in values
        values["coverages"] = []
    if "spatial_coverage" in values:
        sc = values["spatial_coverage"]
        del values["spatial_coverage"]
        if sc:
            value = to_coverage_value_string(sc)
            cov_type = CoverageType[sc["type"]]
            values["coverages"].append({"type": cov_type, "value": value})
    if "period_coverage" in values:
        pc = values["period_coverage"]
        del values["period_coverage"]
        if pc:
            value = to_coverage_value_string(pc)
            cov_type = CoverageType.period
            values["coverages"].append({"type": cov_type, "value": value})
    return values


def parse_rdf_spatial_reference(cls, values):
    if "spatial_reference" not in values:
        return values
    if not isinstance(values["spatial_reference"], dict):
        return values
    sr = values["spatial_reference"]
    value = to_coverage_value_string(sr)
    cov_type = SpatialReferenceType[sr["type"]]
    values["spatial_reference"] = {"type": cov_type, "value": value}
    return values


def parse_rdf_multidimensional_spatial_reference(cls, values):
    assert "spatial_reference" in values
    if not isinstance(values["spatial_reference"], dict):
        return values
    sr = values["spatial_reference"]
    value = to_coverage_value_string(sr)
    cov_type = MultidimensionalSpatialReferenceType[sr["type"]]
    values["spatial_reference"] = {"type": cov_type, "value": value}
    return values


def rdf_parse_description(cls, values):
    if "abstract" in values:
        values["description"] = {"abstract": values["abstract"]}
        del values["abstract"]
    return values


def rdf_parse_utc_offset(cls, values):
    if "value" in values:
        values["utc_offset"] = {"value": values["value"]}
        del values["value"]
    return values


def rdf_parse_rdf_subject(cls, values):
    if "url" in values:
        values["rdf_subject"] = URIRef(str(values["url"]))
        del values["url"]
    return values


def rdf_parse_file_types(cls, values):
    if "file_types" in values:
        for entry in values["file_types"]:
            file_type = entry["type"]
            if file_type.name not in values:
                values[file_type.name] = []
            values[file_type.name].append(entry["url"])
        del values["file_types"]
    return values


def parse_rdf_extended_metadata(cls, values):
    if "additional_metadata" in values:
        if type(values["additional_metadata"] is list):
            values["extended_metadata"] = values["additional_metadata"]
        else:
            assert type(values["additional_metadata"]) is dict
            em = []
            for key, value in values["additional_metadata"].items():
                em.append({"key": key, "value": value})
            values["extended_metadata"] = em
        del values["additional_metadata"]

    return values


def parse_rdf_dates(cls, values):
    if "dates" in values:
        return values

    dates = []
    assert "created" in values
    assert values["created"]
    dates.append({"type": DateType.created, "value": values["created"]})
    del values["created"]

    assert "modified" in values
    assert values["modified"]
    dates.append({"type": DateType.modified, "value": values["modified"]})
    del values["modified"]

    if "review_started" in values and values["review_started"]:
        dates.append({"type": DateType.review_started, "value": values["review_started"]})
        del values["review_started"]

    if "published" in values and values["published"]:
        dates.append({"type": DateType.published, "value": values["published"]})
        del values["published"]

    values["dates"] = dates
    return values


def parse_relation_rdf(cls, values):
    if "type" in values and "value" in values:
        values[values["type"].name] = values["value"]
    return values


def split_user_identifiers(cls, values):
    if "identifiers" in values:
        identifiers = values["identifiers"]
        for id_type, id_value in identifiers.items():
            values[id_type.name] = id_value
    return values
