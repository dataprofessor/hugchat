import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 HugChat App')
    
    st.header('Hugging Face Login')
    hf_email = st.text_input('Enter E-mail:', type='password')
    hf_pass = st.text_input('Enter password:', type='password')
    
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [HugChat](https://github.com/Soulter/hugging-chat-api)
    - [OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model

    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](https://youtube.com/dataprofessor)')


# Stores AI generated responses
if "messages" not in st.session_state.keys():
    st.session_state['messages'] = [{"role": "assistant", "content": "I'm HugChat, How may I help you?"}]

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the existing chat messages
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    sign.saveCookies()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    response = chatbot.chat(prompt)
    return response

# If last message is not from assistant, we need to generate a new response
if st.session_state['messages'][-1]["role"] != "assistant":
    # Call LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            #r = openai.ChatCompletion.create(
            #    model="gpt-3.5-turbo",
            #    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state['messages']],
            #)
            #response = r.choices[0].message.content
            response = generate_response(prompt, hf_email, hf_pass)
            st.write(response)

    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)

st.write(st.session_state['messages'])
