import streamlit as st
from streamlit_chat import message
from hugchat import hugchat

st.sidebar.title('🤗💬 HugChat App')

# Generate empty lists for generated and past values
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# Location of input/response containers
input_container = st.container()
response_container = st.container()

# User input
def get_text():
    input_text = st.text_input("You: ","Hello", key="input")
    return input_text

with input_container:
    user_input = get_text()

# Response output
def query(prompt):
    chatbot = hugchat.ChatBot()
    response = chatbot.chat(prompt)
    return response

with response_container:
    if user_input:
        response = query(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

            

