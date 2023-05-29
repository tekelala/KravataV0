import streamlit as st

# Define the pages
def home_page():
    st.title('Home')
    st.write('Welcome to our tool! Here you can create content or create a communications piece. Use the sidebar to navigate between the pages.')

def create_content_page():
    st.title('Create Content')
    st.write('Here you can create content.')

def create_communications_piece_page():
    st.title('Create a Communications Piece')
    st.write('Here you can create a communications piece.')

# Create a dictionary of pages
pages = {
    'Home': home_page,
    'Create Content': create_content_page,
    'Create a Communications Piece': create_communications_piece_page
}

# Use the sidebar to select the page
page = st.sidebar.selectbox('Choose a page', options=list(pages.keys()))

# Display the selected page with the help of dictionary
pages[page]()
