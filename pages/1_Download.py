import streamlit as st
import pandas as pd
from ulit.sparql import send_sparql_query
from ulit.download import download_documents
import os

def download():
    
    st.write("# TULIT")

    st.header("Download legal data")

    # Sidebar for selecting the source
    st.sidebar.header("Select Source")
    source = st.sidebar.selectbox("Choose the source of the file download:", ["Publications Office of the EU", "Normattiva"])

    if source == "Publications Office of the EU":
        celex = st.text_input(
            "Please introduce the CELEX number of the document you want to download",
            placeholder="ex. 32024R0903"
        )
        format_options = ["Formex 4", "XHTML"]
    elif source == "Normattiva":
        celex = None
        date = st.date_input("Select Date")
        official_journal = st.text_input("Official Journal", placeholder="Enter the Official Journal")
        format_options = ["PDF", "DOCX"]  # Example formats for Normattiva

    if 'format' not in st.session_state:
        st.session_state.format = None

    st.session_state.format = st.selectbox("Select a file format:", format_options)

    if st.button("Search", key="search"):
        if source == "Publications Office of the EU":
            handle_eu_publications_office(celex)
        elif source == "Normattiva":
            handle_normattiva(date, official_journal)

def handle_eu_publications_office(celex):
    if celex not in st.session_state:
        st.session_state.celex = celex
    st.write(f'Searching and downloading file {st.session_state.celex}')

    query_file = './database/queries/formex_query.rq' if st.session_state.format == "Formex 4" else './database/queries/html_query.rq'
    results = send_sparql_query(query_file, celex)
    format_dir = 'formex' if st.session_state.format == "Formex 4" else 'html'
    downloaded_document_paths = download_documents(
        results,
        f'./database/data/{format_dir}',
        log_dir='./database/metadata/logs',
        format='fmx4' if st.session_state.format == "Formex 4" else 'xhtml'
    )
    display_download_results(downloaded_document_paths)

def handle_normattiva(date, official_journal):
    st.write(f'Searching and downloading file from {official_journal} on {date}')
    # Add your search logic here for Normattiva

def display_download_results(downloaded_document_paths):
    st.session_state.downloaded_document_paths = downloaded_document_paths
    st.session_state.documents = {
        "celex": st.session_state.celex,
        "documents": st.session_state.downloaded_document_paths
    }
    st.write(f'{len(st.session_state.downloaded_document_paths)} documents downloaded in {st.session_state.downloaded_document_paths}')
    st.session_state.file = st.session_state.downloaded_document_paths


def main():
    download()

if __name__ == "__main__":
    main()