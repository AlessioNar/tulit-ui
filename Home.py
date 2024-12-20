import streamlit as st
import pandas as pd

def main():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# TULIT - The Universal Legal Informatics Toolkit 👋")
    st.sidebar.write("### Session Summary")
    st.sidebar.write(f"**Selected Format:** {st.session_state.get('format', 'Not selected')}")
    st.sidebar.write(f"**Current Path:** {st.session_state.get('current_path', 'Not set')}")
    st.sidebar.write(f"**Selected File:** {st.session_state.get('file', 'No file selected')}")

    st.sidebar.success("Select a demo above.")
    tabs = st.tabs(["Home", "About", "Contribute", "Contact"])        
    with tabs[0]:
        st.markdown(
            """
            The Universal Legal Informatics Toolkit is an open-source web app that aims to
            overcome technical interoperability barriers of legal data to enable additional use cases.
            
            It provides functionalities to:
            - Download a document from Cellar
            - Parse legal documents in various standard formats (Akoma Ntoso, FORMEX4, and XHTML)
            
            **👈 Select a demo from the sidebar** to see some examples
            of what ULIT can do!
            
            ### Want to learn more?
            - Open an issue on [Github](https://github.com/AlessioNar/ulit) 
            
        """
        )
    with tabs[3]:
               st.markdown(
            """
            AlessioNar
            
        """
        )
if __name__ == "__main__":
    main()