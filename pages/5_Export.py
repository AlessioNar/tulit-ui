import os
import streamlit as st
from datetime import datetime
import shutil
import tempfile
import pandas as pd
import time
import zipfile


def export():
    """
    Export articles to JSON
    """
    st.title("Export to JSON")
    # Check for data in session state
    if 'data' not in st.session_state or not st.session_state.data:
        st.warning("No data available to export")
        return
    
    # Try to identify the data source
    # Assuming data is a list of dictionaries or a DataFrame
    data = st.session_state.data 
    
      
    # Display preview of articles
    st.write("### Data Preview")
    
    
    # Named based on
    celex = st.text_input(
                "Insert here the CELEX ID",
                placeholder="ex. 32024R0903",
                value='32024R0903'
            )
    
    # Create TXT Directory
    export_dir = "../database/data/txt"
    os.makedirs(export_dir, exist_ok=True)
    
    
    txt_files = []
    if st.button("Export"):
        document_path = os.path.join(export_dir, celex)
        os.makedirs(document_path, exist_ok=True) 
        # Handle different data types
        try:
            # If data is a list of simple values
            if isinstance(data, list):
                for index, item in enumerate(data):
                    filename = f"document_{index+1}.txt"
                    filepath = os.path.join(export_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(str(item))
                    
                    txt_files.append(filepath)
            
            # If data is a dictionary
            elif isinstance(data, dict):
                for key, value in data.items():
                    filename = f"{key}.txt"
                    filepath = os.path.join(export_dir, filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(str(value))
                    
                    txt_files.append(filepath)
                
            # Create ZIP file
            zip_path = os.path.join(document_path, "exported_documents.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in txt_files:
                    zipf.write(file, os.path.basename(file))
                
            # Provide download button
            with open(zip_path, 'rb') as f:
                st.download_button(
                        label="Download Exported Files",
                        data=f.read(),
                        file_name="exported_documents.zip",
                        mime="application/zip"
                    )
                    
                                
        except Exception as e:
            st.error(f"Export failed: {e}")

def main():
    export()

if __name__ == "__main__":
    main()