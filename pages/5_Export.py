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
    st.sidebar.write(f"**Selected Format:** {st.session_state.get('format', 'Not selected')}")
    st.sidebar.write(f"**Selected File:** {st.session_state.get('file', 'No file selected')}")

    st.title("Export data")
    # Check for data in session state
    if 'data' not in st.session_state:
        st.warning("No data available to export")
        return
    
    # Try to identify the data source
    # Assuming data is a list of dictionaries or a DataFrame
    data = st.session_state.data 
    
    # Display preview of articles
    st.write("### Data Preview")
    table = st.dataframe(data)  # Use `st.dataframe` for an interactive table

    
    # Named based on
    file_name = st.text_input(
                "Name of the file",
                placeholder="ex. 32024R0903",
                value='document'
            )
    
    # Create TXT Directory
    export_dir = "../database/data/txt"
    os.makedirs(export_dir, exist_ok=True)
    
    
    txt_files = []
    if st.button("Export"):
        document_path = os.path.join(export_dir, file_name)
        os.makedirs(document_path, exist_ok=True) 
        # Handle different data types
        try:
            for index, item in data.iterrows():
                # Determine filename based on 'Paragraph ID' or fallback to 'Article eId'
                if pd.notna(item.get('eId')):  # Check for valid 'Paragraph ID'
                    filename = f"{item['eId']}.txt"
                    content = str(item.get('Paragraph Text', ''))  # Default to empty if missing
                else:
                    filename = f"{item.get('eId', index)}.txt"  # Fallback to index if 'Article eId' missing
                    content = str(item.get('Article Text', ''))  # Default to empty if missing

                # Construct file path
                filepath = os.path.join(export_dir, filename)

                # Write content to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Track the generated file
                txt_files.append(filepath)
                
            # Create ZIP file
            zip_path = os.path.join(document_path, f"{file_name}zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in txt_files:
                    zipf.write(file, os.path.basename(file))
                
            # Provide download button
            with open(zip_path, 'rb') as f:
                st.download_button(
                        label="Download Exported Files",
                        data=f.read(),
                        file_name=f"{file_name}.zip",
                        mime="application/zip"
                    )
                    
                                
        except Exception as e:
            st.error(f"Export failed: {e}")

def main():
    export()

if __name__ == "__main__":
    main()