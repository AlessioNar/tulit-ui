import streamlit as st
import pandas as pd
from tulit.sparql import send_sparql_query
from tulit.download.cellar import CellarDownloader
from tulit.download.normattiva import NormattivaDownloader
from tulit.download.legilux import LegiluxDownloader
import tempfile
import os

def download():
    
    st.write("# TULIT")

    st.header("Download legal data")

    # Sidebar for selecting the source
    st.sidebar.header("Select Source")
    source = st.sidebar.selectbox("Choose the source of the file download:", ["Publications Office of the EU", "Normattiva", "Legilux"])

    if source == "Publications Office of the EU":
        celex = st.text_input(
            "Please introduce the CELEX number of the document you want to download",
            placeholder="ex. 32024R0903"
        )
        format_options = ["Formex 4", "XHTML"]
        st.session_state.format = st.selectbox("Select the format of the document", format_options)
    
    elif source == "Normattiva":
        publication_date = st.text_input("Insert the publication date of the document", placeholder="Enter the publication date in the format YYYYMMDD")
        codice_redazionale = st.text_input("Codice Redazionale", placeholder="Enter the Codice Redazionale of the document")
    
    elif source == "Legilux":
        eli = st.text_input("Please introduce the ELI number of the document you want to download", placeholder="ex. http://data.legilux.public.lu/eli/etat/leg/loi/2006/07/31/n2/jo")
        
    # Temporary file preparation
    if 'temp_dir' not in st.session_state or not st.session_state.temp_dir:
        temp_dir = tempfile.mkdtemp()
        st.session_state.temp_dir = temp_dir
            
    st.write(st.session_state.temp_dir)
    
    if st.button("Search", key="search"):
        if source == "Publications Office of the EU":
            if not celex:
                st.error("Please enter a CELEX number")
                st.stop()
            handle_eu_publications_office(celex, st.session_state.temp_dir)
        elif source == "Normattiva":
            if not publication_date or not codice_redazionale:
                st.error("Please enter the publication date and the Codice Redazionale")
                st.stop()
            handle_normattiva(publication_date, codice_redazionale, st.session_state.temp_dir)
        elif source == "Legilux":
            if not eli:
                st.error("Please enter an ELI number")
                st.stop()
            handle_legilux(eli, st.session_state.temp_dir)

def handle_eu_publications_office(celex, temp_dir):
    if celex not in st.session_state:
        st.session_state.celex = celex
    st.write(f'Searching and downloading file {st.session_state.celex}')

    query_file = './database/queries/formex_query.rq' if st.session_state.format == "Formex 4" else './database/queries/html_query.rq'
    
    results = send_sparql_query(query_file, celex)
    format_dir = 'formex' if st.session_state.format == "Formex 4" else 'html'
    downloader = CellarDownloader(download_dir=os.path.join(temp_dir, f'database/data/{format_dir}'), log_dir='./database/metadata/logs')
    
    downloaded_document_paths = downloader.download(
        results, format='fmx4' if st.session_state.format == "Formex 4" else 'xhtml'
    )
    display_download_results(downloaded_document_paths)

def handle_normattiva(publication_date, codice_redazionale, temp_dir):
    st.write(f'Searching and downloading file from Normattiva with Codice Redazionale {codice_redazionale} and published on {publication_date}')
    downloader = NormattivaDownloader(download_dir=os.path.join(temp_dir, 'database/data/akn/italy'), log_dir='./database/metadata/logs')
    downloaded_document_paths = downloader.download(publication_date, codice_redazionale)
    display_download_results(downloaded_document_paths)

def handle_legilux(eli, temp_dir):
    st.write(f'Searching and downloading file from Legilux with ELI {eli}')
    downloader = LegiluxDownloader(download_dir=os.path.join(temp_dir, 'database/data/akn/luxembourg'), log_dir='./database/metadata/logs')
    downloaded_document_paths = downloader.download(eli)
    display_download_results(downloaded_document_paths)

def display_download_results(downloaded_document_paths):
    st.session_state.documents = downloaded_document_paths
    st.write(f'{len(st.session_state.documents)} documents downloaded in {st.session_state.documents}')
    st.session_state.file = st.session_state.documents


def main():
    download()

if __name__ == "__main__":
    main()