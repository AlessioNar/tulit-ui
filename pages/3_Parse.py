import os
import streamlit as st
from datetime import datetime
import shutil
import tempfile
import pandas as pd
import time


# Dummy function to simulate calling a parser
from ulit.parsers.formex import Formex4Parser  # Replace with actual import
from ulit.parsers.html import HTMLParser
from ulit.parsers.akomantoso import AkomaNtosoParser

def parse():
    """
    Parser
    """
    entry = st.session_state.file
    # Explicitly check if file exists before processing
    if not os.path.exists(entry):
        st.error(f"File not found: {entry}")
        return

    # Use absolute paths
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.abspath(os.path.join(temp_dir, os.path.basename(entry)))
    
    try:
        shutil.copy(entry, temp_file_path)
    except Exception as e:
        st.error(f"Error copying file: {e}")
            
    # Get directory contents
    # Create a clickable table
    st.write("### Contents")
    
    # Add a dropdown menu to select the parser type
    st.write(st.session_state.format)
    if st.session_state.format == "Formex 4":
        if st.button(f"Parse articles of Formex file {entry}"):        
            parser = Formex4Parser()        
            parser.parse(temp_file_path)
            try:
                st.session_state.data = parser.articles
                articles = pd.DataFrame(parser.articles)
                if len(articles) > 0:                            
                    # Display the DataFrame as a table
                    st.write("### Articles")                            
                    if st.button(f"Close table", key=True):
                        table.empty()
                    table = st.table(articles)
                else:
                    st.write("### Articles")
                    st.write("No articles found in this document")
            except:
                print('Error producing articles')
    elif st.session_state.format == "Akoma Ntoso":

        if st.button(f"Parse articles of Akoma Ntoso file {entry}", key=f"AkomaNtoso"):
            parser = AkomaNtosoParser()        
            parser.parse(temp_file_path)
            try:
                st.session_state.data = parser.articles
                articles = pd.DataFrame(parser.articles)
                if len(articles) > 0:                            
                    # Display the DataFrame as a table
                    st.write("### Articles")                            
                    if st.button(f"Close table", key=True):
                        table.empty()
                    table = st.table(articles)
                else:
                    st.write("### Articles")
                    st.write("No articles found in this document")
                    
                    
            except:
                print('Error producing articles')
    elif st.session_state.format == "XHTML":
        if st.button(f"Parse articles of XHTML file {entry}", key=f"XHTML"):
            parser = HTMLParser()        
            parser.parse(temp_file_path)
            try:
                st.session_state.data = parser.paragraphs
                articles = pd.DataFrame(list(parser.articles.items()), columns=['Article', 'Content'])
            
                
                if len(articles) > 0:                            
                    # Display the DataFrame as a table
                    st.write("### Articles")                            
                    if st.button(f"Close table", key=True):
                        table.empty()
                    table = st.table(articles)
                else:
                    st.write("### Articles")
                    st.write("No articles found in this document")
            except:
                print('Error producing articles')
    
   
        # Assuming you have your parser.articles dictionary                    
        # Convert the dictionary to a pandas DataFrame
        #df = pd.DataFrame.from_dict(parser.articles, orient='index').reset_index()
        #df.columns = ['Article', 'Value']  # Rename columns for clarity
            # Convert the dictionary to a pandas DataFrame
        return None
        try:
            if parser.preface:
                st.write("Preface:", parser.preface)
        except:
            print('Error identifying preface')
             
        #df.columns = ['eId', 'article_num', 'article_text']  # Rename columns for clarity
                                
        #if parser.meta is not None:
        #    st.write("Meta: ", parser.meta)
        try:
            if parser.meta_identification is not None:
                st.write("Meta Identification: ", parser.meta_identification)
        except:
            print('Error identifying preface')
            
        try:
            data = pd.DataFrame(parser.recitals)
            if len(data) > 0:                            
                # Display the DataFrame as a table
                st.write("#### Recitals") 
                if st.button(f"Close table", key=True):
                    recitals_table.empty()
                recitals_table = st.dataframe(data)
            else:
                st.write("### Recitals")
                st.write("No recitals found in this document")
        except:
            print('Error producing articles')
        try:
            citations_data = pd.DataFrame(parser.citations)
            if len(citations_data) > 0:                            
                # Display the DataFrame as a table
                st.write("#### Citations") 
                if st.button(f"Close table", key=True):
                    citations_table.empty()
                citations_table = st.dataframe(citations_data)
            else:
                st.write("### Citations")
                st.write("No citations found in this document")
        except:
            print('Error producing citations')
        
                        
        #st.write("Meta Proprietary: ", parser.meta_proprietary)
        #st.write("Meta References: ", parser.meta_references)
        #st.write("Preamble Formula: ", parser.preamble_formula)
        #st.write("Preamble Citations: ", parser.preamble_citations)
        #st.write("Preamble Recitals: ", parser.preamble_recitals)
        try:
            st.write("Chapters: ", parser.chapters)
        except:
            print('Error producing chapters')
        #st.write("Conclusions: ", parser.conclusions) 
    
def main():
    parse()

if __name__ == "__main__":
    main()
