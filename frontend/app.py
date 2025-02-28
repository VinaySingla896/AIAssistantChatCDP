import streamlit as st
import requests
import json
import sseclient
import time
import os

st.set_page_config(
    page_title="CDP Support Chatbot",
    page_icon="💬",
    layout="wide",
    menu_items={
        'About': None,
        'Report a bug': None,
        'Get help': None
    }
)

# Load custom CSS
with open("frontend/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

initialize_session_state()

st.title("CDP Support Chatbot")

# Main chat interface
st.markdown("### Chat with your CDP Assistant")
st.markdown("Ask questions about Segment, mParticle, Lytics, and Zeotap")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your question here..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create assistant message placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            # Send request to backend
            response = requests.post(
                "http://localhost:8000/chat",
                json={
                    "message": prompt,
                    "conversation_history": st.session_state.messages[:-1]
                },
                stream=True
            )

            client = sseclient.SSEClient(response)
            for event in client.events():
                full_response += event.data
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")