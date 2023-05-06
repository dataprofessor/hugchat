import streamlit as st
from streamlit_chat import message
from hugchat import hugchat

st.title('🤗💬 HugChat App')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ","Hello, how are you?", key="input")
    return input_text 

def query(prompt):
    response = chatbot.chat(prompt)
    return response

response_container = st.container()
container = st.container()

with container:
    user_input = get_text()
    
chatbot = hugchat.ChatBot()

with response_container:
    if user_input:
        response = query(user_input)

        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))



