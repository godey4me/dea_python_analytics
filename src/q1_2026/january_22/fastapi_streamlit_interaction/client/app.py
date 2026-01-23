import streamlit as st

# Helper Functions
from utils import retrieve_df_from_url

# Text box that has the URL
url = st.text_input(
                    label="Pass in a URL to retrieve data: ",
                    placeholder='https://jsonplaceholder.typicode.com/comments'
                    )


# Process button
if st.button(label="Process"):
    # Getting the DataFrame
    df = retrieve_df_from_url(url=url)

    # Render the DataFrame
    st.dataframe(data=df)
