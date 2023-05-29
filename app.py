import streamlit as st
import requests
import json

# Claude functions
def send_message(prompts, creativity_level):
    api_url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": st.secrets["API_KEY"]  # Use the API key from Streamlit's secrets
    }

    # Define the body of the request
    body = {
        "prompt": prompts,
        "model": "claude-v1.3",
        "temperature": creativity_level,
        "max_tokens_to_sample": 1000,
        "stop_sequences": ["\n\nHuman:"]
    }

    # Make a POST request to the Claude API
    response = requests.post(api_url, headers=headers, data=json.dumps(body))
    response.raise_for_status()

    return response.json()

# Load documents

# Function to present general options
def transversal_options():
    #st.title('Transversal Options')

    # LLM Model
    llm_model = st.selectbox(
        'LLM Model',
        ['ChatGPT', 'Claude']
    )

    # If the user chooses 'ChatGPT', provide options for version
    if llm_model == 'ChatGPT':
        chatgpt_version = st.selectbox(
            'ChatGPT Version',
            ['3.5', '4']
        )

    # Intention
    intention = st.text_area('What is the intention? What do you want to happen? Ex: Prospect Customer books a call, Click on a link, etc.')
    
    # Language
    language = st.selectbox(
        'Which Language?',
        ['English', 'Spanish', 'Portuguese']
    )

    # Audience
    audience = st.selectbox(
        'Who is the audience?',
        ['Exchange', 'Trader', 'Partner', 'Investor', 'Kravata Team', 'Traditional financer', 'Other']
    )

    # If the user chooses 'Other', provide a text box for them to specify
    if audience == 'Other':
        other_audience = st.text_input('Please specify the audience:')

    # Tone
    tone = st.selectbox(
        'What is the tone?',
        ['Formal', 'Informal', 'Urgent']
    )

    # Creativity level
    creativity_level = st.number_input('Creativity level', min_value=0.0, max_value=1.0, step=0.1, format="%.1f")

    # Length in words
    length_in_words = st.number_input('How long in words?', min_value=1, format="%i")

    # Context
    context = st.text_area('Context', 'Paste any relevant information like previous communications or specific information it is important to take into account')

    if st.button('Create'):
        # Here you can call the function to create the content or communication piece
        
        # Define initial prompts
        if "prompts" not in st.session_state:
            st.session_state.prompts = []

        # Container for conversation history
        with st.container():
            # Display the entire conversation
            for prompt in st.session_state.prompts:
                if prompt['role'] == 'Human':
                    st.write(f"You: {prompt['content']}")
                else:  # prompt['role'] == 'Assistant'
                    st.write(f"Claude: {prompt['content']}")

        # Container for user input and Send button
        with st.container():
            with st.form(key='message_form'):
                user_message = st.text_input("You: ", key=f"user_input_{len(st.session_state.prompts)}")
                submit_button = st.form_submit_button(label='Send')

                if submit_button and user_message:
                    st.session_state.prompts.append({
                        "role": "Human",
                        "content": user_message
                    })

                    if st.session_state.prompts:
                        with st.spinner('Waiting for Claude...'):
                            try:
                                result = send_message(st.session_state.prompts)

                                # Append Claude's response to the prompts
                                st.session_state.prompts.append({
                                    "role": "Assistant",
                                    "content": result['completion']
                                })

                                # Rerun the script to update the chat
                                st.experimental_rerun()

                                # Display a success message
                                st.success("Message sent successfully!")

                            except requests.exceptions.HTTPError as errh:
                                st.error(f"HTTP Error: {errh}")
                            except requests.exceptions.ConnectionError as errc:
                                st.error(f"Error Connecting: {errc}")
                            except requests.exceptions.Timeout as errt:
                                st.error(f"Timeout Error: {errt}")
                            except requests.exceptions.RequestException as err:
                                st.error(f"Something went wrong: {err}")
                            except Exception as e:
                                st.error(f"Unexpected error: {e}")

# Function to create the prompt for the content generation
def prompt_creator_content(content_type, social_network, other_social_network, intention, language, audience, tone, word_count, context):
    prompts = f'''Role: You are an AI assistant expert in crafting {content_type} {social_network} {other_social_network} for Kravata and your answers needs to be always in {language}. 
                Your audience is {audience} and your tone should be {tone}, limit your response to {word_count} words. 
                The purpose is {intention}
                Here is some context: {context}'''

    return prompts

# Function to create the prompt for the communications generation
def prompt_creator_comms(communication_piece_type, other_communication_piece, name_receiver, language, audience, tone, word_count, intention, context):
    prompts = f'''Role: You are an AI assistant expert in crafting {communication_piece_type} {other_communication_piece} for Kravata and your answers needs to be always in {language}. 
                Your audience is {audience} and your tone should be {tone}, limit your response to {word_count} words. 
                The purpose is {intention} and you are writting to {name_receiver}
                Here is some context: {context}'''

    return prompts

# Define the pages
def home_page():
    st.title('Home')
    st.write('Welcome to our tool! Here you can create content or create a communications piece. Use the sidebar to navigate between the pages.')

def create_content_page():
    st.title('Create Content')

    # Ask the user what type of content they want to create
    content_type = st.selectbox(
        'What type of content do you want to create?',
        ['Post for Social Networks', 'Post for Newsletter', 'Article', 'Course', 'Deck', 'Brochure', 'Press release']
    )

    # If the user chooses 'Post for Social Networks', ask which social network
    if content_type == 'Post for Social Networks':
        social_network = st.selectbox(
            'Which Social Network?',
            ['Twitter', 'Instagram', 'LinkedIn', 'Facebook', 'TikTok', 'SnapChat', 'Telegram', 'Discord', 'Other']
        )

        # If the user chooses 'Other', provide a text box for them to specify
        if social_network == 'Other':
            other_social_network = st.text_input('Which one:')

    transversal_options()

def create_communications_piece_page():
    st.title('Create a Communications Piece')

    # Ask the user what type of communication piece they want to create
    communication_piece_type = st.selectbox(
        'What piece of communication do you want to create?',
        ['Email', 'Presentation Letter', 'Instant Message', 'SMS', 'Other']
    )

    # If the user chooses 'Other', provide a text box for them to specify
    if communication_piece_type == 'Other':
        other_communication_piece = st.text_input('Which other communications piece:')

    name_receiver = st.text_input('To whom are you writting for?')
    
    transversal_options()

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
