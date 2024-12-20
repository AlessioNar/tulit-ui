import streamlit as st
import pandas as pd
from ulit.sparql import send_sparql_query
from ulit.download import download_documents
import os

def download():
    st.header("Download legal data")

    
    if 'format' not in st.session_state:
        st.session_state.format = None

    # Now you can safely use the 'format' attribute
    if st.session_state.format is None:
        st.session_state.format = st.selectbox("Select a file format:", ["Formex 4", "XHTML"])
    else:
        st.session_state.format = st.selectbox("Select a file format:", ["Formex 4", "XHTML"])
        
    celex = st.text_input(
            "Download file with CELEX",
            placeholder="ex. 32024R0903"
        )

    
    if st.button("Search", key="celex_search"):
        if celex not in st.session_state:
            st.session_state.celex = celex            
            
        st.write(f'Searching and downloading file {st.session_state.celex}')            
        
        if st.session_state.format == "Formex 4":
            results = send_sparql_query('./database/queries/formex_query.rq', celex)
            downloaded_document_paths = download_documents(
            results, 
            './database/data/formex', 
            log_dir='./database/metadata/logs', 
            format='fmx4'
        )
        elif st.session_state.format == "XHTML": 
            results = send_sparql_query('./database/queries/html_query.rq', celex)
            downloaded_document_paths = download_documents(
            results, 
            './database/data/html', 
            log_dir='./database/metadata/logs', 
            format='xhtml'
        )
        st.session_state.downloaded_document_paths = downloaded_document_paths
        st.session_state.documents = {
            "celex": st.session_state.celex,
            "documents": st.session_state.downloaded_document_paths
            
        }
        st.write(f'{len(st.session_state.downloaded_document_paths)} documents downloaded in {st.session_state.downloaded_document_paths}')
        
        # Save the variable in the session stage and move to the next page
        #st.session_state. = downloaded_document_paths
        st.session_state.file = st.session_state.downloaded_document_paths
    
    if st.button("Proceed to Choose File"):
        st.switch_page("pages/2_Choose_File.py")
            
def main():
    download()
            
            
       
if __name__ == "__main__":
    main()