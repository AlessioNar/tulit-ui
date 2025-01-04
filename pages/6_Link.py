import streamlit as st
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore
from pages.rdf import RDFTriplesCreator

# Function to convert DataFrame to RDF
def dataframe_to_rdf(df, base_eli):    
    creator = RDFTriplesCreator()    
    creator.add_legal_resource(resource_uri=base_eli, 
                                title=st.session_state.parser.preface, 
                                document_type='Law', 
                                language="en")
    
    for index, row in df.iterrows():
        creator.add_legal_subdivision(
            base_uri = base_eli, 
            article_uri= row['Article eId'],
            resource_uri= str(row['eId']),            
            subdivision_type='Paragraph', 
            text=row['text'], 
            language='en'
        )

    return creator


# Function to generate nodes and edges from RDF graph
def generate_graph_elements(rdf_graph):
    nodes = []
    edges = []
    EX = Namespace("http://example.org/")
    ELI = Namespace("http://data.europa.eu/eli/ontology#")
    DCTERMS = Namespace("http://purl.org/dc/terms/")
    added_nodes = set()

    for s, p, o in rdf_graph:
        if p == RDF.type and o == ELI.SubSection:
            if str(s) not in added_nodes:
                identifier = rdf_graph.value(s, ELI.identifier)
                nodes.append(Node(id=str(s), label=str(identifier), size=25, title=str(identifier)))
                added_nodes.add(str(s))
        elif p == DCTERMS.isPartOf:
            edges.append(Edge(source=str(o), target=str(s), label="isPartOf"))
        elif p in [ELI.date_publication, ELI.title, DCTERMS.creator, DCTERMS.subject]:
            edges.append(Edge(source=str(s), label=str(p).split('/')[-1], target=str(o)))
    
    return nodes, edges

# Main function to run the Streamlit app
def main():
    st.title("Create ELI")
    if 'selected' in st.session_state:
        data = st.session_state.selected
        df = pd.DataFrame(data)


        # Initialize TripleStore and add RDF graph to triple store
        store = TripleStore()
        #for s, p, o in rdf_graph:
        #    store.add_triple(s, p, o)

        #nodes, edges = generate_graph_elements(rdf_graph)
        # Add ELI as user input
        base_eli = st.text_input(
            "Please introduce the ELI number of the document you want to download",
            placeholder="ex. http://",
            value='https://data.europa.eu/eli/reg/2024/900/oj/article/'
        )
        
        creator = dataframe_to_rdf(df, base_eli)
        # Save RDF graph to file providing a download link
        rdf_data = creator.graph.serialize(format="turtle")
        st.code(rdf_data, language="turlte", wrap_lines=True)
        st.download_button(
            label="Download RDF",
            data=rdf_data,
            file_name='test.ttl',
            mime='text/turtle'
            )

        
        # Display DataFrame
        st.write('## Data')
        
        # Process each row individually
        for index, row in df.iterrows():
            st.write(f"###  {row['Article Number']} {row['Article Heading']}")
            st.write(f"{base_eli}{row['Article eId']}/paragraph/{row['eId']}")            
            st.write(f"{row['text']}")
            # Add any additional processing or display logic here
        
        # Display dataframe focusing on the eId and text columns
        
        # Display RDF Graph
        #st.write("RDF Graph:")
        #config = Config(width=750, height=300, directed=True, physics=True, hierarchical=False)
        #agraph(nodes=nodes, edges=edges, config=config)

        # Display RDF Triples
        st.write("RDF Triples:")
        #for s, p, o in rdf_graph:
        #    st.write(f"{s} -- {p} --> {o}")

if __name__ == "__main__":
    main()
