"""

# Improvements:

- refactor by caching login
- add LLM model selection so one can compare responses from different model
- add button to summarize chat
- add button to share chat

# Issues



"""

import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# App title
st.set_page_config(page_title="🤗 HugChat 💬")

# see https://github.com/wgong/hugging-chat-api/blob/836b826bb434e9e8e5609981a5c189d677e9a3d0/src/hugchat/hugchat.py#L47
DEFAULT_MODEL = "OpenAssistant/oasst-sft-6-llama-30b-xor"

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
        # cache chatbot object in session_state
        st.session_state["chatbot"] = chatbot

    st.markdown(f"""📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/)!
    """, unsafe_allow_html=True)
    
    models = st.session_state.chatbot.get_available_llm_models()
    model_dict = {m:i for i,m in enumerate(models)}
    idx_default = model_dict.get(DEFAULT_MODEL)
    st.selectbox(f"Select Model: ", models, index=idx_default, key="hf_model")
    
    if st.button("Summarize chat"):
        summary = chatbot.summarize_conversation()
        st.write(summary)
    
    if st.button("Share chat"):
        url = chatbot.share_conversation()
        st.write(url)

def main():
    chatbot = st.session_state.chatbot
    selected_model = st.session_state.get("hf_model", DEFAULT_MODEL)
    if chatbot.active_model != selected_model:
        chatbot.switch_llm(model_dict.get(selected_model))
    
    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=(chatbot is None)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = chatbot.chat(prompt)
                    st.write(response)
                except Exception as ex:
                    st.error(str(ex))
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)

if __name__ == '__main__':
    main()