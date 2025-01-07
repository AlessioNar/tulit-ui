import streamlit as st
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from streamlit_agraph import agraph, Node, Edge, Config, TripleStore
from tulit.rdf import RDFTriplesCreator

# Function to convert DataFrame to RDF
def dataframe_to_rdf(df, base_eli):
    creator = RDFTriplesCreator()    
    creator.add_legal_resource(resource_uri=base_eli, 
                                    title=st.session_state.parser.preface, 
                                    document_type='Law', 
                                    language="en")
    if st.session_state.get('table_type') == 'Articles':    
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
    elif st.session_state.get('table_type') == 'Citations':
        for index, row in df.iterrows():
            creator.add_legal_subdivision(
                base_uri = base_eli, 
                article_uri= row['Article eId'],
            )
        
        
        


# Function to generate nodes and edges from RDF graph
def generate_graph_elements(rdf_graph):
    nodes = []
    edges = []
    node_ids = set()

    for subj, pred, obj in rdf_graph:
        subj_id = str(subj)
        obj_id = str(obj)

        if subj_id not in node_ids:
            nodes.append(Node(id=subj_id, label=subj_id))
            node_ids.add(subj_id)
        
        if obj_id not in node_ids:
            nodes.append(Node(id=obj_id, label=obj_id))
            node_ids.add(obj_id)
        
        edges.append(Edge(source=subj_id, target=obj_id, label=str(pred)))

    return nodes, edges

# Main function to run the Streamlit app
def main():
    st.title("Annotate with ELI")
    if 'selected' in st.session_state:
        data = st.session_state.selected
        df = pd.DataFrame(data)
    elif 'data' in st.session_state:
        data = st.session_state.data
        df = pd.DataFrame(data)

    # Add ELI as user input
    base_eli = st.text_input(
        "Please introduce the ELI number of the document you are working on",
        placeholder="ex. http://",
        value='https://data.europa.eu/eli/reg/2024/903/oj/'
    )
    
    creator = dataframe_to_rdf(df, base_eli)
    # Save RDF graph to file providing a download link
    rdf_data = creator.graph.serialize(format="turtle")
    st.download_button(
        label="Download RDF",
        data=rdf_data,
        file_name='test.ttl',
        mime='text/turtle'
        )
        
    st.code(rdf_data, language="turtle", wrap_lines=True)
    
    rdf_graph = creator.graph
    nodes, edges = generate_graph_elements(rdf_graph)
        
    # Display RDF Graph
    st.write("RDF Graph:")
    config = Config(width=750, height=500, directed=True, physics=False, hierarchical=False, nodeSpacing=200)#, levelSeparation=150)
    
    # Display the RDF graph using the agraph component
    agraph(nodes=nodes, edges=edges, config=config)
    st.write('test')
    

if __name__ == "__main__":
    main()
