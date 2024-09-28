STEP_SOURCE_DEFAULT = [
    "http://cambridgesemantics.com/ontologies/Graphmarts#Self",
    "http://cambridgesemantics.com/ontologies/Graphmarts#AllPrevious"
]

# Dataset API
COMPONENT_TYPES = [
    "DatasetComponent",
    "RdfDatasetComponent",
    "StructuredDatasetComponent",
    "OntDatasetComponent",
    "MaterializedDatasetComponent",
    "MaterializedStructuredDatasetComponent"
]

CONFLICT_RESOLUTION_OPTIONS = [
    "rename",
    "replace"
]

DEFAULT_ROLE_URI_REF = {
    "Anzo Administrator": "http://openanzo.org/Role/datalakeadmin",
    "Data Analyst": "http://openanzo.org/Role/data-analyst",
    "Data Citizen": "http://openanzo.org/Role/data-citizen",
    "Data Curator": "http://openanzo.org/Role/data-curator",
    "Data Governor": "http://openanzo.org/Role/data-governor",
    "Data Scientist": "http://openanzo.org/Role/data-scientist"
}

QUERY_TEMPLATE = """PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX s:       <http://cambridgesemantics.com/ontologies/DataToolkit#>

# targetGraph is replaced with the Layers URI at runtime
# usingSources is replaced with the URIs of the Layer's Sources at runtime
DELETE {
    GRAPH ${targetGraph} {

    }
}
INSERT {
    GRAPH ${targetGraph} {

    }
}
${usingSources}
WHERE {

}"""

DIRECT_LOAD_TEMPLATE = """PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>
PREFIX s:       <http://cambridgesemantics.com/ontologies/DataToolkit#>

# targetGraph is replaced with the Layers URI at runtime
# usingSources is replaced with the URIs of the Layer's Sources at runtime
DELETE {
    GRAPH ${targetGraph} {

    }
}
INSERT {
    GRAPH ${targetGraph} {

    }
}
${usingSources}
WHERE {
    SERVICE <http://cambridgesemantics.com/services/DataToolkit> {

    }
}"""

VIEW_TEMPLATE = """PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX s: <http://cambridgesemantics.com/ontologies/DataToolkit#>
#fromSources is replaced with the URIs of the Layer's Sources at runtime
CONSTRUCT{

}
${fromSources}
WHERE{
    SERVICE <http://cambridgesemantics.com/services/DataToolkitView>(${targetGraph}) {

    }
}"""