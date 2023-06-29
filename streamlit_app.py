import streamlit as st
from langchain.chains import ConversationChain
from hugchat import hugchat
from hugchat.login import Login

st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")
st.title('🤗💬 HugChat App')

# Hugging Face Credentials
with st.sidebar:
    st.header('Hugging Face Login')
    hf_email = st.text_input('Enter E-mail:', type='password')
    hf_pass = st.text_input('Enter password:', type='password')

# Store AI generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "I'm HugChat, How may I help you?"}]

# Display existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating LLM response
def generate_response(prompt, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    sign.saveCookies()
    # Create ChatBot                        
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    chain = ConversationChain(llm=chatbot)
    response = chain.run(input=prompt)
    return response

# Prompt for user input and save
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# If last message is not from assistant, we need to generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    # Call LLM
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass)
            st.write(response)
            
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
