"""

# Issues

module 'streamlit' has no attribute 'chat_message'

"""

import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="🤗💬 HugChat")

@st.cache_resource
def hf_login(hf_email, hf_pass):
    try:
        sign = Login(hf_email, hf_pass)
        cookies = sign.login()
        st.success(f'HuggingFace login as {hf_email}', icon='✅')
        return cookies
    except Exception as ex:
        err_msg = f"Failed to login: {str(ex)}"
        st.error(err_msg)
    return None

# Hugging Face Credentials
with st.sidebar:
    st.title('Welcome to 🤗 HugChat 💬')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        if not (hf_email and hf_pass):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    if hf_email and hf_pass:
        cookies = hf_login(hf_email, hf_pass)
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        st.session_state["chatbot"] = chatbot

    st.markdown(f"""📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!
    """, unsafe_allow_html=True)
    
    models = st.session_state.chatbot.get_available_llm_models()
    # st.write(f"models: {models}")
    st.selectbox(f"Select Model: ", models, index=0, key="hf_model")

# # Function for generating LLM response
# def generate_response(prompt_input, cookies):
#     # Hugging Face Login
#     # sign = Login(email, passwd)
#     # cookies = sign.login()
#     #sign.saveCookies()
#     # Create ChatBot
#     chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
#     return chatbot.chat(prompt_input)

def main():
    chatbot = st.session_state.chatbot
    
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    cookies = st.session_state.get("hf_cookies")
    if prompt := st.chat_input(disabled=(cookies is None)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        #with st.chat_message("assistant"):
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chatbot.chat(prompt)
                st.write(response) 
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

if __name__ == '__main__':
    main()