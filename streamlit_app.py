import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat

with st.sidebar:
    st.title('🤗💬 HugChat App')
    st.markdown('''
    ## About
    This app is built using:
    - [Streamlit](https://streamlit.io/)
    - [HugChat](https://github.com/Soulter/hugging-chat-api)
    
    💡 Note: No API key required!
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](https://youtube.com/dataprofessor)')

# Generate empty lists for generated and past values
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']
if 'text_input' not in st.session_state:
    st.session_state['text_input'] = ['']
    
# Location of input/response containers
input_container = st.container()
colored_header(
    label='',
    description='',
    color_name='blue-30')
response_container = st.container()

# User input
def text_submit():
    st.session_state.text_input = st.session_state.input
    st.session_state.input = ''
##def get_text():
##    input_text = st.text_input("You: ", "", key="input", on_change=text_submit)
##    return input_text

with input_container:
    ## user_input = get_text()
    st.text_input("You: ", "", key="input", on_change=text_submit)
    
# Response output
def query(prompt):
    chatbot = hugchat.ChatBot()
    response = chatbot.chat(prompt)
    return response

with response_container:
    ## if user_input:
    if st.session_state.text_input:
        #response = query(user_input)
        #st.session_state.past.append(user_input)
        response = query(st.session_state.text_input)
        st.session_state.past.append(st.session_state.text_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        #for i in range(len(st.session_state['generated'])-1, -1, -1):
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))

st.write(st.session_state['text_input'])
