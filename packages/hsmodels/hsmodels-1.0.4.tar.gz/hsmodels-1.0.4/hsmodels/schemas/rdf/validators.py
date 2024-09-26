from pydantic_core import Url

from hsmodels.schemas.enums import CoverageType, DateType
from hsmodels.schemas.languages_iso import languages


def rdf_parse_extended_metadata(cls, value):
    from hsmodels.schemas.rdf.fields import ExtendedMetadataInRDF

    assert isinstance(value, list)
    if len(value) > 0:
        if isinstance(value[0], ExtendedMetadataInRDF):
            return value
    return [{"key": key, "value": val} for key, val in value.items()]


def rdf_parse_identifier(cls, value):
    if isinstance(value, Url):
        return {"hydroshare_identifier": value}
    return value


def subjects_constraint(cls, subjects):
    """Removes empty/None and duplicates"""
    validated = []
    for subject in subjects:
        trimmed = subject.strip()
        if trimmed and trimmed not in validated:
            validated.append(trimmed)
    return validated


def language_constraint(cls, language):
    if language not in [code for code, verbose in languages]:
        raise ValueError("language '{}' must be a 3 letter iso language code".format(language))
    return language


def dates_constraint(cls, dates):
    assert len(dates) >= 2
    created = list(filter(lambda d: d.type == DateType.created, dates))
    assert len(created) == 1
    created = created[0]
    modified = list(filter(lambda d: d.type == DateType.modified, dates))
    assert len(modified) == 1
    modified = modified[0]

    assert modified.value >= created.value
    return dates


def coverages_constraint(cls, coverages):
    def one_or_none_of_type(type):
        cov = list(filter(lambda d: d.type == type, coverages))
        assert len(cov) <= 1

    one_or_none_of_type(CoverageType.point)
    one_or_none_of_type(CoverageType.period)
    one_or_none_of_type(CoverageType.box)
    return coverages


def coverages_spatial_constraint(cls, coverages):
    contains_point = any(c for c in coverages if c.type == CoverageType.point)
    contains_box = any(c for c in coverages if c.type == CoverageType.box)
    if contains_point:
        assert not contains_box, "Only one type of spatial coverage is allowed, point or box"
    return coverages


def sort_creators(cls, creators):
    if not creators:
        raise ValueError("creators list must have at least one creator")
    if isinstance(next(iter(creators)), dict):
        for index, creator in enumerate(creators):
            creator["creator_order"] = index + 1
        return creators
    else:
        # assign creator_order to creators that don't have it
        creator_order_numbers = [c.creator_order for c in creators if c.creator_order is not None]
        if creator_order_numbers:
            if len(creator_order_numbers) != len(set(creator_order_numbers)):
                raise ValueError("creator_order values must be unique")
            max_order_number = max(creator_order_numbers)
        else:
            max_order_number = 0

        creators_without_order = [c for c in creators if c.creator_order is None]
        for index, creator in enumerate(creators_without_order):
            creator.creator_order = max_order_number + index + 1
        return sorted(creators, key=lambda _creator: _creator.creator_order)


def sort_columns(table):
    if not table:
        raise ValueError("columns list must have at least one column")
    if "columns" in table and isinstance(next(iter(table["columns"])), dict):
        column_numbers = [col['column_number'] for col in table['columns']]
        # check that column number is in the range of 1 to the length of columns
        if any(c < 1 or c > len(table["columns"]) for c in column_numbers):
            raise ValueError("column_number values must be between 1 and the number of columns")
        if len(column_numbers) != len(set(column_numbers)):
            raise ValueError("column_number values must be unique")
        table['columns'] = sorted(table['columns'], key=lambda _column: _column['column_number'])
    else:
        # assign column_order to columns that don't have it
        column_numbers = [c.column_number for c in table.columns]
        # check that column number is in the range of 1 to the length of columns
        if any(c < 1 or c > len(table.columns) for c in column_numbers):
            raise ValueError("column_number values must be between 1 and the number of columns")
        if len(column_numbers) != len(set(column_numbers)):
            raise ValueError("column_number values must be unique")
        table.columns = sorted(table.columns, key=lambda _column: _column.column_number)

    return table
