import inspect
from enum import Enum

from pydantic import BaseModel
from pydantic_core import Url
from rdflib import Graph, Literal, URIRef

from hsmodels.namespaces import DC, HSTERMS, ORE, RDF, RDFS1
from hsmodels.schemas.aggregations import (
    FileSetMetadata,
    GeographicFeatureMetadata,
    GeographicRasterMetadata,
    ModelInstanceMetadata,
    ModelProgramMetadata,
    MultidimensionalMetadata,
    ReferencedTimeSeriesMetadata,
    SingleFileMetadata,
    TimeSeriesMetadata,
    CSVFileMetadata,
)
from hsmodels.schemas.enums import TermEnum
from hsmodels.schemas.rdf.aggregations import (
    FileSetMetadataInRDF,
    GeographicFeatureMetadataInRDF,
    GeographicRasterMetadataInRDF,
    ModelInstanceMetadataInRDF,
    ModelProgramMetadataInRDF,
    MultidimensionalMetadataInRDF,
    ReferencedTimeSeriesMetadataInRDF,
    SingleFileMetadataInRDF,
    TimeSeriesMetadataInRDF,
    CSVFileMetadataInRDF,
)
from hsmodels.schemas.rdf.resource import CollectionMetadataInRDF, ResourceMap, ResourceMetadataInRDF
from hsmodels.schemas.resource import CollectionMetadata, ResourceMetadata

rdf_schemas = {
    ORE.ResourceMap: ResourceMap,
    HSTERMS.CompositeResource: ResourceMetadataInRDF,
    HSTERMS.CollectionResource: CollectionMetadataInRDF,
    HSTERMS.GeographicRasterAggregation: GeographicRasterMetadataInRDF,
    HSTERMS.GeographicFeatureAggregation: GeographicFeatureMetadataInRDF,
    HSTERMS.MultidimensionalAggregation: MultidimensionalMetadataInRDF,
    HSTERMS.ReferencedTimeSeriesAggregation: ReferencedTimeSeriesMetadataInRDF,
    HSTERMS.FileSetAggregation: FileSetMetadataInRDF,
    HSTERMS.SingleFileAggregation: SingleFileMetadataInRDF,
    HSTERMS.TimeSeriesAggregation: TimeSeriesMetadataInRDF,
    HSTERMS.ModelProgramAggregation: ModelProgramMetadataInRDF,
    HSTERMS.ModelInstanceAggregation: ModelInstanceMetadataInRDF,
    HSTERMS.CSVFileAggregation: CSVFileMetadataInRDF,
}

user_schemas = {
    ResourceMetadataInRDF: ResourceMetadata,
    CollectionMetadataInRDF: CollectionMetadata,
    GeographicRasterMetadataInRDF: GeographicRasterMetadata,
    GeographicFeatureMetadataInRDF: GeographicFeatureMetadata,
    MultidimensionalMetadataInRDF: MultidimensionalMetadata,
    ReferencedTimeSeriesMetadataInRDF: ReferencedTimeSeriesMetadata,
    FileSetMetadataInRDF: FileSetMetadata,
    SingleFileMetadataInRDF: SingleFileMetadata,
    TimeSeriesMetadataInRDF: TimeSeriesMetadata,
    ModelProgramMetadataInRDF: ModelProgramMetadata,
    ModelInstanceMetadataInRDF: ModelInstanceMetadata,
    CSVFileMetadataInRDF: CSVFileMetadata,
}


def load_rdf(rdf_str, file_format='xml'):
    g = Graph().parse(data=rdf_str, format=file_format)
    for target_class, schema in rdf_schemas.items():
        subject = g.value(predicate=RDF.type, object=target_class)
        if subject:
            if target_class == ResourceMap:
                return _parse(schema, g)
            else:
                rdf_metadata = _parse(schema, g)
                if schema in user_schemas.keys():
                    return user_schemas[schema](**rdf_metadata.model_dump(exclude_none=True))
                return rdf_metadata
    raise Exception("Could not find schema for \n{}".format(rdf_str))


def parse_file(schema, file, file_format='xml', subject=None):
    metadata_graph = Graph().parse(file, format=file_format)
    return _parse(schema, metadata_graph, subject)


def rdf_graph(schema):
    for rdf_schema, user_schema in user_schemas.items():
        if isinstance(schema, user_schema):
            return _rdf_graph(rdf_schema(**schema.model_dump(to_rdf=True)), Graph())
    return _rdf_graph(schema, Graph())


def rdf_string(schema, rdf_format='pretty-xml'):
    return rdf_graph(schema).serialize(format=rdf_format).decode()


def _rdf_fields(schema):
    for fname, finfo in schema.model_fields.items():
        if fname not in ['rdf_subject', 'rdf_type', 'label', 'dc_type']:
            predicate = None
            if finfo.json_schema_extra:
                predicate = finfo.json_schema_extra.get('rdf_predicate', None)
            if not predicate:
                raise Exception(
                    "Schema configuration error for {}, all fields must specify a rdf_predicate".format(schema)
                )
            yield finfo, fname, predicate


def _rdf_graph(schema, graph=None):
    for f, fname, predicate in _rdf_fields(schema):
        values = getattr(schema, fname, None)
        if values is not None:
            if not isinstance(values, list):
                # handle single values as a list to simplify
                values = [values]
            for value in values:
                if isinstance(value, BaseModel):
                    assert hasattr(value, "rdf_subject")
                    # nested class
                    graph.add((schema.rdf_subject, predicate, value.rdf_subject))
                    graph = _rdf_graph(value, graph)
                else:
                    # primitive value
                    if isinstance(value, Url):
                        value = URIRef(str(value))
                    elif isinstance(value, TermEnum):
                        value = URIRef(value.value)
                    elif isinstance(value, Enum):
                        value = Literal(value.value)
                    else:
                        value = Literal(value)
                    graph.add((schema.rdf_subject, predicate, value))
    if hasattr(schema, 'rdf_type'):
        graph.add((schema.rdf_subject, RDF.type, schema.rdf_type))
    if hasattr(schema, 'dc_type'):
        graph.add((schema.rdf_subject, DC.type, schema.dc_type))
    if hasattr(schema, 'label'):
        graph.add((URIRef(str(schema.rdf_type)), RDFS1.label, Literal(schema.label)))
        graph.add((URIRef(str(schema.rdf_type)), RDFS1.isDefinedBy, URIRef("https://www.hydroshare.org/terms/")))
    return graph


def get_args(t):
    return getattr(t, "__args__", None)


def _parse(schema, metadata_graph, subject=None):
    def get_nested_class(field):
        origin = field.annotation
        if origin:
            if inspect.isclass(origin) and issubclass(origin, BaseModel):
                return origin
            if get_args(origin):
                clazz = get_args(origin)[0]
                if inspect.isclass(clazz) and issubclass(clazz, BaseModel):
                    return clazz
        return None

    def class_rdf_type(schema):
        if schema.model_fields['rdf_type']:
            return schema.model_fields['rdf_type'].default
        return None

    if not subject:
        # lookup subject using RDF.type specified in the schema
        target_class = class_rdf_type(schema)
        if not target_class:
            raise Exception("Subject must be provided, no RDF.type specified on class {}".format(schema))
        subject = metadata_graph.value(predicate=RDF.type, object=target_class)
        if not subject:
            raise Exception("Could not find subject for predicate=RDF.type, object={}".format(target_class))

    kwargs = {}
    for f, name, predicate in _rdf_fields(schema):
        parsed = []
        for value in metadata_graph.objects(subject=subject, predicate=predicate):
            nested_clazz = get_nested_class(f)
            if nested_clazz:
                parsed_class = _parse(nested_clazz, metadata_graph, value)
                if parsed_class:
                    parsed.append(parsed_class)
            else:
                # not a nested class (primitive class and not a subclass of BaseModel)

                origin = f.annotation
                origin_clazz = getattr(origin, '__origin__', None)
                parsed_value = None
                if origin_clazz is list:
                    clazz = origin.__args__[0]
                    if issubclass(clazz, BaseModel):
                        parsed_class = _parse(clazz, metadata_graph, value)
                        if parsed_class:
                            parsed.append(parsed_class)
                    else:
                        # primitive value
                        parsed_value = str(value.toPython())
                else:
                    # primitive value
                    parsed_value = str(value.toPython())

                if parsed_value:
                    parsed.append(parsed_value)

        if len(parsed) > 0:
            origin = f.annotation
            origin_clazz = getattr(origin, '__origin__', None)
            if origin_clazz is list:
                # list
                kwargs[name] = parsed
            else:
                # single
                kwargs[name] = parsed[0]
    if kwargs:
        instance = schema(**kwargs, rdf_subject=subject)
        return instance
    return None
