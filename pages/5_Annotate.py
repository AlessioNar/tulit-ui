import streamlit as st
import pandas as pd
import json

def display_table_with_filters(data, table_type="Articles"):
    """Display a table with filters and row selection via checkboxes."""

    df = pd.DataFrame(data)
    st.session_state.data = df  # Store the table in session state for persistence

    
    label  = st.text_input('Label')

    st.write(f"### {table_type} Table")

    
    if st.button("Submit"):
        selected_rows = df[df['selected']]
        selected_rows['Label'] = label
        st.write("### Selected Rows")
        st.write(selected_rows)
        st.session_state.selected = selected_rows
        return selected_rows
    
    # Create a table with checkbox in the first column and the rows of the dataframe in the second column.
    for index, row in df.iterrows():
        checkbox_value = st.checkbox(f"{row['text']}", key=f"row_{index}")
        df.at[index, 'selected'] = checkbox_value  # Add checkbox value to the dataframe


def view():
    """View Data Page"""
    
    st.write("# TULIT")
    st.title("Annotate")
    
    # Sidebar info
    st.sidebar.write(f"**Selected Format:** {st.session_state.get('format', 'Not selected')}")    
    st.sidebar.write(f"**Selected File:** {st.session_state.get('file', 'No file selected')}")
    
    # Ensure parser is loaded in session state
    if 'data' not in st.session_state or st.session_state.data.empty:
        st.error("No parsed data found. Please parse a file first.")
        st.stop()
        
    data = st.session_state.data
    st.write("### Preface")
    st.write(st.session_state.parser.preface)

    selected_data = display_table_with_filters(data, table_type="Articles")

    
    
    if st.button("Link the data"):
        st.switch_page("pages/6_Link.py")
    

        
def main():
    view()

if __name__ == "__main__":
    main()