import streamlit as st
import pandas as pd
import shutil

def display_table(data, table_type="Articles"):
    """Display a table (articles, chapters, or other attributes)."""
    if not data or len(data) == 0:
        st.info(f"No {table_type.lower()} found in this document.")
        return

    df = pd.DataFrame(data)
    st.session_state.data = df  # Store the table in session state for persistence
    st.write(f"### {table_type} Table")
    st.dataframe(df)

def extract_articles(articles_data):
    """Extract and format articles/paragraphs."""
    data_list = []
    for article in articles_data:                
        data_list.append({
            'eId': article['eId'],
            'Article Number': article['num'],
            'Article Heading': article['heading']
        })
    return data_list

def extract_chapters(chapters_data):
    """Extract and format chapters."""
    data_list = []
    for chapter in chapters_data:
        data_list.append({
            'eId': chapter['eId'],
            'Chapter Heading': chapter.get('heading'),
            'Chapter Number': chapter.get('num')
        })
    return data_list

def extract_items(data):
    """Extract and format chapters."""
    data_list = []
    for item in data:
        data_list.append({
            'eId': item['eId'],
            'Row': item['text'],
        })
    return data_list


def view():
    """View Data Page"""
    st.title("Select Data")
    
    # Sidebar info
    st.sidebar.write(f"**Selected Format:** {st.session_state.get('format', 'Not selected')}")    
    st.sidebar.write(f"**Selected File:** {st.session_state.get('file', 'No file selected')}")

    # Ensure parser is loaded in session state
    if 'parser' not in st.session_state or not st.session_state.parser:
        st.error("No parsed data found. Please parse a file first.")
        st.stop()

    parser = st.session_state.parser  # Retrieve the parser object
    st.write("### Preface")
    if hasattr(parser, "preface") and parser.preface is not None:
        st.write(getattr(parser, "preface"))  # Display preface if available
    else:
        st.info("No preface found in this document.")

    # Attribute selection dropdown
    st.write("## Select Data to Visualize")
    view_option = st.selectbox(
        "Choose an attribute to view:",
        ["Citations", "Recitals",  "Articles", "Chapters"],
        key="view_option_select"
    )

    ## Different views according to the specific items
    if view_option == "Articles":
        if hasattr(parser, 'articles'):            
            articles_data = extract_articles(parser.articles)
            display_table(articles_data, table_type="Articles")
        else:
            st.info("No article data available in this document.")
    elif view_option == "Chapters":
        if hasattr(parser, 'chapters'):
            chapters_data = extract_chapters(parser.chapters)
            display_table(chapters_data, table_type="Chapters")
        else:
            st.info("No chapters data available in this document.")
    elif view_option == "Recitals":
        if hasattr(parser, 'recitals') and parser.recitals is not None:
            recitals_data = extract_items(parser.recitals)
            display_table(recitals_data, table_type="Recitals")
        else:
            st.info("No recitals data available in this document.")
    elif view_option == "Citations":
        if hasattr(parser, 'citations') and parser.citations is not None:
            citations_data = extract_items(parser.citations)
            display_table(citations_data, table_type="Citations")
        else:
            st.info("No citations data available in this document.")
        
    if st.session_state.get('data') is not None and not st.session_state['data'].empty:
        if st.button("Proceed to export data"):
            st.switch_page("pages/5_Export.py")
    

        
def main():
    view()

if __name__ == "__main__":
    main()
