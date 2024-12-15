import streamlit as st
import pandas as pd

def main():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# TULIT - The Universal Legal Informatics Toolkit 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        The Universal Legal Informatics Toolkit is an open-source web app that aims to
        overcome technical interoperability barriers to enable semantic, organisational and legal interoperability use cases.
        
        It provides functionalities to:
        - Download a document from Cellar
        - Parse legal documents in various standard formats (Akoma Ntoso, FORMEX4, and XHTML)
        
        **👈 Select a demo from the sidebar** to see some examples
        of what ULIT can do!
        
        ### Want to learn more?
        - Open an issue on [Github](https://github.com/AlessioNar/ulit) 
        
    """
    )
       
if __name__ == "__main__":
    main()