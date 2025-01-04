import os
import streamlit as st

# Dummy parsers - replace these imports with your actual parsers
from tulit.parsers.xml.formex import Formex4Parser
from tulit.parsers.html.cellar import CellarHTMLParser
from tulit.parsers.xml.akomantoso import AkomaNtosoParser
import io
import sys

def parse_document(file_path):
    """
    Parse a legal document.
    
    Args:
        file_path (str): The path to the document to parse.
    """
    # Code to parse the document
    st.write(f"Parsing document at {file_path}")

def parse_file(parser_cls, file_path):
    """Parse the file using the given parser class."""
    parser = parser_cls()
    # Capture the output of the parse method
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    try:
        parser.parse(file_path)
        output = new_stdout.getvalue()
        
    finally:
        sys.stdout = old_stdout

    # Prettify the captured output
    return parser, output

def parse():
    """Parser Page"""
    
    st.write("# TULIT")

    st.title("Parse the file")

    # Sidebar info
    st.sidebar.write(f"**Selected Format:** {st.session_state.get('format', 'Not selected')}")
    st.sidebar.write(f"**Selected File:** {st.session_state.get('file', 'No file selected')}")

    # Check for file selection
    entry = st.session_state.get('file')
    if not entry or not os.path.exists(entry):
        st.error("No valid file selected. Please upload a file.")
        st.stop()

    file = st.session_state.get('file')

    # File format selection
    format_options = ["Formex 4", "XHTML", "Akoma Ntoso"]
    format_selected = st.selectbox("Select a file format:", format_options, key="format_select")
    st.session_state.format = format_selected

    parser = None
    parse_button_label = f"Parse {format_selected} File"
    if st.button(parse_button_label):
        try:
            # Call the appropriate parser based on format @todo improve error handling
            if format_selected == "Formex 4":
                parser, output = parse_file(Formex4Parser, file)
                
            elif format_selected == "XHTML":
                parser, output = parse_file(CellarHTMLParser, file)
            
            elif format_selected == "Akoma Ntoso":
                parser, output = parse_file(AkomaNtosoParser, file)
            
                
            else:
                raise ValueError("Invalid format selected.")

            # Store parsed data in session state
            st.session_state.parser = parser
            st.session_state.output = output
            
            # Verify the parser output            
            if (hasattr(parser, "valid")) and (parser.valid is False):
                # Print the error message prettified                
                for error in parser.validation_errors:
                    st.error(f"Validation Error: {error}")
                    
                raise RuntimeError("Parser failed or returned invalid data.")

            st.success("File parsed successfully!")


            
            
                        
        except Exception as e:
            # Display the error message
            st.error(f"Error during parsing: {e}")

    if st.button("Show output"):
        if 'parser' in st.session_state and 'output' in st.session_state:
            st.code(f"Parser output: {st.session_state.output}")
        else:
            st.error("No parser output available.")
            
    # Proceed to view results
    if st.session_state.get('parser') and st.button("Proceed to View Results"):
        st.switch_page("pages/4_Visualise.py")

def main():
    if "parser" not in st.session_state:
        st.session_state.parser = None
    if "data" not in st.session_state:
        st.session_state.data = None
    parse()

if __name__ == "__main__":
    main()
