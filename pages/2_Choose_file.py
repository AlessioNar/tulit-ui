import os
import streamlit as st
from datetime import datetime
import tempfile
def choose_file():
    """
    Main Streamlit app for file system navigation and file selection.
    """
    
    st.write("# TULIT")

    st.header("Choose a File")
    
    # Initialize session state for current path
    if 'temp_dir' not in st.session_state or not st.session_state.temp_dir:
        st.session_state.temp_dir = tempfile.mkdtemp()
    
    if 'current_path' not in st.session_state or not st.session_state.current_path:
        st.session_state.current_path = st.session_state.temp_dir
        st.rerun()
        
    st.sidebar.write(f"**Current Path:** {st.session_state.get('current_path', 'Not set')}")
    st.sidebar.write(f"**Selected File:** {st.session_state.get('file', 'No file selected')}")

    # Provide a way to upload a file to the current directory
    uploaded_file = st.file_uploader("Upload a file to the current directory")
    if uploaded_file:
        file_path = os.path.join(st.session_state.current_path, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved: {file_path}")
        st.session_state.file = file_path
        st.stop()
    
    # Navigation buttons
    st.write("### Navigation") 
    if st.session_state.current_path != st.session_state.temp_dir:
        if st.button("⬆️ Go Up"):
            parent_dir = os.path.dirname(st.session_state.current_path)
            if parent_dir != st.session_state.current_path:  # Check if we are not at the root directory
                st.session_state.current_path = parent_dir
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
                    # Proceed to view results
        if st.session_state.get('file') and st.button("Proceed to parse file"):
            st.switch_page("pages/3_Parse.py")
            
    else:
        st.warning("No files or directories found in the current folder.")
    if 'file' not in st.session_state or not st.session_state.file:
        st.warning("Please select a file first ")
        st.stop()

    
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
