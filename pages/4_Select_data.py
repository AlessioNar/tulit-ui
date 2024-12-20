import streamlit as st
import pandas as pd

def display_table(data, table_type="Articles"):
    """Display a table (articles, chapters, or other attributes)."""
    if not data or len(data) == 0:
        st.info(f"No {table_type.lower()} found in this document.")
        return

    df = pd.DataFrame(data)
    st.session_state.data = df  # Store the table in session state for persistence
    st.write(f"### {table_type} Table")
    st.dataframe(df)

def extract_articles(articles_data, is_paragraph=False):
    """Extract and format articles/paragraphs."""
    data_list = []
    for article in articles_data:
        if is_paragraph:  # Handle XHTML or Akoma Ntoso format (with paragraphs)
            for paragraph in article['article_text']:
                data_list.append({                    
                    'eId': paragraph['eId'],
                    'Article eId': article['eId'],
                    'Article Number': article['article_num'],
                    'Article Title': article.get('article_title', ''),
                    'Paragraph Text': paragraph['text']
                })
        else:  # Handle Formex format
            data_list.append({
                'eId': article['eId'],
                'Article Number': article['article_num'],
                'Article Text': article['article_text']
            })
    return data_list

def extract_chapters(chapters_data):
    """Extract and format chapters."""
    data_list = []
    for chapter in chapters_data:
        data_list.append({
            'eId': chapter['eId'],
            'Chapter Heading': chapter.get('chapter_heading'),
            'Chapter Number': chapter.get('chapter_num')
        })
    return data_list

def extract_recitals(recitals_data):
    """Extract and format chapters."""
    data_list = []
    for recital in recitals_data:
        data_list.append({
            'eId': recital['eId'],
            'Recital text': recital['recital_text'],
        })
    return data_list

def extract_citations(citations_data):
    """Extract and format chapters."""
    data_list = []
    for citation in citations_data:
        data_list.append({
            'eId': citation['eId'],
            'Citation text': citation['citation_text']          
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
    format_selected = st.session_state.format  # Get selected format
    st.write("### Preface")
    st.write(getattr(parser, "preface", "No preface available."))  # Display preface if available

    # Attribute selection dropdown
    st.write("## Select Data to Visualize")
    view_option = st.selectbox(
        "Choose an attribute to view:",
        ["Recitals", "Citations", "Articles", "Chapters"],
        key="view_option_select"
    )

    ## Different views according to the specific items
    if view_option == "Articles":
        if hasattr(parser, 'articles'):
            is_paragraph = format_selected in ["XHTML", "Akoma Ntoso"]
            articles_data = extract_articles(parser.articles, is_paragraph)
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
        if hasattr(parser, 'recitals'):
            recitals_data = extract_recitals(parser.recitals)
            display_table(recitals_data, table_type="Recitals")
        else:
            st.info("No recitals data available in this document.")
    elif view_option == "Citations":
        if hasattr(parser, 'citations'):
            citations_data = extract_citations(parser.citations)
            display_table(citations_data, table_type="Citations")
        else:
            st.info("No recitals data available in this document.")
        
    if st.session_state.get('data') is not None and not st.session_state['data'].empty:
        if st.button("Proceed to export data"):
            st.switch_page("pages/5_Export.py")
        
def main():
    view()

if __name__ == "__main__":
    main()
