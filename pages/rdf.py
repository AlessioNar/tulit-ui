from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS

# Define Namespaces based on the ELI guidance
eLI = Namespace("http://data.europa.eu/eli/ontology#")
dct = Namespace("http://purl.org/dc/terms/")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")

class RDFTriplesCreator:
    def __init__(self):
        """Initialize the graph and bind namespaces."""
        self.graph = Graph()
        self.graph.bind("eli", eLI)
        self.graph.bind("dct", dct)
        self.graph.bind("skos", skos)

    def add_legal_resource(self, resource_uri, title, document_type, language):
        """Add a LegalResource to the RDF graph."""
        resource = URIRef(resource_uri)
        self.graph.add((resource, RDF.type, eLI.LegalResource))
        self.graph.add((resource, eLI.type_document, Literal(document_type)))
        self.graph.add((resource, dct.title, Literal(title)))
        self.graph.add((resource, eLI.language, Literal(language)))

    def add_legal_subdivision(self, base_uri, article_uri, resource_uri, text, subdivision_type, language):
        """Add a LegalResource to the RDF graph."""
        resource = URIRef(base_uri + article_uri + '/' + resource_uri)
        self.graph.add((resource, RDF.type, eLI.LegalResourceSubdivision))
        self.graph.add((resource, dct.isPartOf, URIRef(base_uri)))
        self.graph.add((resource, eLI.type_subdivision, Literal(subdivision_type)))
        self.graph.add((resource, dct.hasAnnotation, Literal(text)))
        self.graph.add((resource, eLI.language, Literal(language)))

    def add_legal_expression(self, expression_uri, resource_uri, language, title):
        """Add a LegalExpression to the RDF graph linked to a LegalResource."""
        expression = URIRef(expression_uri)
        resource = URIRef(resource_uri)
        self.graph.add((expression, RDF.type, eLI.LegalExpression))
        self.graph.add((expression, eLI.realizes, resource))
        self.graph.add((expression, eLI.language, Literal(language)))
        self.graph.add((expression, dct.title, Literal(title)))

    def add_format(self, format_uri, expression_uri, format_type):
        """Add a Format to the RDF graph linked to a LegalExpression."""
        fmt = URIRef(format_uri)
        expression = URIRef(expression_uri)
        self.graph.add((fmt, RDF.type, eLI.Format))
        self.graph.add((fmt, eLI.embodies, expression))
        self.graph.add((fmt, eLI.format, Literal(format_type)))

    def save_graph(self, filepath):
        """Save the RDF graph to a file."""
        self.graph.serialize(destination=filepath, format="turtle")

# Example Usage
if __name__ == "__main__":
    creator = RDFTriplesCreator()

    # Add a Legal Resource
    creator.add_legal_resource(
        "http://example.org/eli/law/2025/1",
        "Example Law Title",
        "Law",
        "en"
    )

    # Add a Legal Expression
    creator.add_legal_expression(
        "http://example.org/eli/law/2025/1/en",
        "http://example.org/eli/law/2025/1",
        "en",
        "Example Law Title (English)"
    )

    # Add a Format
    #creator.add_format(
    #    "http://example.org/eli/law/2025/1/en/pdf",
    #    "http://example.org/eli/law/2025/1/en",
    #    "application/pdf"
    #)

    # Save the graph
    creator.save_graph("eli_triples.ttl")
