     
        
        # Additional queries
        st.button("Get me a list of all regulations published in the last year")
        st.button("Get me a list of all the proposed legal texts of 2021")
        
        # SPARQL Editor
        st.subheader("SPARQL Editor")
        sparql_query = st.text_area(
            "Query Editor",
            height=200,
            value="""PREFIX cdm: <http://publications.europa.eu/ontology/cdm#>
PREFIX purl: <http://purl.org/dc/elements/1.1/>

SELECT DISTINCT ?cellarURIs, ?manif, ?format, ?expr
WHERE {
    # Your SPARQL query here
}"""
        )
        
        # Results section
        st.subheader("Search results")
        if st.button("Execute Query"):
            # Mock results table
            data = {
                "Title": ["Regulation (EU) 2024/903", "Directive (EU) 2016/2102"],
                "Date": ["13/03/2024", "26/10/2016"],
                "Eurovoc": ["Digital, Public administration", "Digital, Public administration"],
            }
            df = pd.DataFrame(data)
            st.dataframe(df)

        # Create a sample DataFrame for demonstration
        data = {
            'Select': [False] * 4,
            'Title': [
                'Regulation (EU) 2024/903 of the European Parliament and of the Council of 13 March 2024 laying down measures for a high level of public sector interoperability across the Union (Interoperable Europe Act)',
                'Directive (EU) 2016/2102 of the European Parliament and of the Council of 26 October 2016 on the accessibility of the websites and mobile applications of public sector bodies (Text with EEA relevance )',
                'Username',
                'Username'
            ],
            'Date': ['13/03/2024', '26/10/2016', 'Content', 'Content'],
            'Eurovoc': [
                'Digital\nPublic administration',
                'Digital\nPublic administration',
                'New tag',
                'New tag'
            ]
        }
        df = pd.DataFrame(data)

        # Create the searchable table
        for idx, row in df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([0.5, 6, 2, 2, 1])
            
            with col1:
                st.checkbox("", key=f"select_{idx}")
            
            with col2:
                st.markdown(f"**{row['Title']}**")
            
            with col3:
                st.text(row['Date'])
            
            with col4:
                st.text(row['Eurovoc'])
            
            with col5:
                st.button("View", key=f"view_{idx}", type="secondary")
            
            # Add a subtle separator
            st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)
            
                        
        
        st.subheader("Filter Options")
    
        # Language selection
        language = st.selectbox(
            "Select Language",
            options=["English", "French", "German", "Italian", "Spanish"],
            index=None,
            placeholder="Select Language"
        )
        
        # Format selection
        format_options = [
            "FORMEX",
            "Akoma Ntoso",
            "HTML",
            "XHTML",
            "XML",
            "AKN4EU",
            "PDF"
        ]
        format_selection = st.selectbox(
            "Select Format",
            options=format_options,
            index=None,
            placeholder="Select Format: FORMEX, Akoma Ntoso, HTML, XHTML, XML, AKN4EU, PDF"
        )
        
        # Document type selection
        doc_type = st.selectbox(
            "Select Document Type",
            options=["Regulation", "Directive", "Decision", "Recommendation", "Opinion"],
            index=None,
            placeholder="Select Document Type"
        )
        
        # Extract options
        extract_options = [
            "preamble",
            "recitals",
            "citations",
            "notes",
            "articles",
            "paragraphs",
            "sentences",
            "title",
            "metadata"
        ]
        extracts = st.multiselect(
            "Select what you want to extract",
            options=extract_options,
            placeholder="Select what you want to extract (preamble, recitals, citations, notes, articles, paragraphs, sentences, title, metadata)"
        )
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button("BACK", use_container_width=True)
        with col2:
            st.button("NEXT", use_container_width=True)

        st.header("Export files to Annotation software")
        
        st.subheader("Select annotation software")
        
        # Annotation software options
        annotation_options = {
            "Lawnotation": False,
            "Doccano": False,
            "Inception": False,
            "Lime": False
        }
        
        # Create checkboxes for each option
        for software, default in annotation_options.items():
            st.checkbox(software, value=default)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            st.button("BACK", key="export_back", use_container_width=True)
        with col2:
            st.button("NEXT", key="export_next", use_container_width=True)
    
        # Export section
        
        st.markdown("""
            <h2>
                <svg style="vertical-align: middle; margin-right: 10px;" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                Export files to Annotation software
            </h2>
        """, unsafe_allow_html=True)

        # Export complete message
        st.header("Export complete")

        # Buttons section
        st.button("Download files", 
                key="download",
                use_container_width=False,
                type="secondary")

        st.button("Authenticate and send to annotation software",
                key="authenticate",
                use_container_width=False,
                type="secondary")