import os
import streamlit as st
from datetime import datetime
import shutil
import tempfile
import pandas as pd

# Dummy function to simulate calling a parser
from ulit.parsers.formex import Formex4Parser  # Replace with actual import
from ulit.parsers.html import HTMLParser
from ulit.parsers.akomantoso import AkomaNtosoParser


def choose_file():
    """
    Main Streamlit app for file system navigation and file selection.
    """
    st.title("File System Navigator and Content Viewer")
    
        
    # Navigation buttons
    st.write("### Navigation")    

    # Initialize session state for current path
    if 'current_path' not in st.session_state:
        st.session_state.current_path = os.path.expanduser('./database/data/')
        st.rerun()
    else:        
        if st.button("Go Up One Directory"):
            st.session_state.current_path = os.path.dirname(st.session_state.current_path)
            st.rerun()
    # Display current directory
    st.write(f"**Current Directory:** `{st.session_state.current_path}`")
    
    # List directory contents
    entries = list_files_and_dirs(st.session_state.current_path)
    
    if entries:
        st.write("### Contents")
        for idx, entry in enumerate(entries):
            # Create unique keys for buttons using index
            if entry["Type"] == "Directory":
                if st.button(f"📂 {entry['Name']}", key=f"{entry['Path']}_{idx}"):
                    # Update session state for navigation into a folder
                    st.session_state.current_path = os.path.expanduser(entry['Path'])
                    st.rerun()                   
                    # Use the new query_params API to trigger a refresh
                    
            elif entry["Type"] == "File":
                if st.button(f"📄 {entry['Name']}", key=f"{entry['Path']}_{idx}"):
                    st.write("Selected file: ", entry['Path'])
                    st.session_state.file = entry['Path']
            
    else:
        st.warning("No files or directories found in the current folder.")
        
    format_selected = st.selectbox("Select a file format:", ["Formex 4", "XHTML", "Akoma Ntoso"], key="format_select")
    if format_selected == 'Formex 4':
        st.session_state.format = 'Formex 4'
        st.write("Format selected: ", st.session_state.format)

    elif format_selected == 'XHTML':    
        st.session_state.format = 'XHTML'
        st.write("Format selected: ", st.session_state.format)

    elif format_selected == 'Akoma Ntoso':
        st.session_state.format = 'Akoma Ntoso'
        st.write("Format selected: ", st.session_state.format)


    
def list_files_and_dirs(path):
    """
    List files and directories in the given path.
    
    Args:
        path (str): The directory path to list contents from
    
    Returns:
        list: A list of dictionaries with details about files and directories
    """
    try:
        contents = os.listdir(path)
        entries = []
        for item in contents:
            full_path = os.path.join(path, item)
            entry = {
                "Name": item,
                "Type": "Directory" if os.path.isdir(full_path) else "File",
                "Path": full_path,
                "Size (bytes)": os.path.getsize(full_path) if os.path.isfile(full_path) else "-",
                "Last Modified": datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")
            }
            entries.append(entry)
        return entries
    except Exception as e:
        st.error(f"Error accessing directory: {e}")
        return []

def main():
    choose_file()

if __name__ == "__main__":
    main()
