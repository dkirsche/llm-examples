import openai
import streamlit as st
from gdrive import create_google_drive_file,share_with_me  

with st.sidebar:
    # Button to trigger file creation
    if st.button("Create Google Drive File"):
        file_title = "Project plan"
        file_content = "this is the start of a collaborative file to build out a project plan"
        file_id = create_google_drive_file(file_title, file_content)
        share_with_me(file_id)
        st.success(f"File created successfully with ID: {file_id}")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

openai_api_key ="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"
st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-4", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
