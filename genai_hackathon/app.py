import streamlit as st
from groq import Groq
import os

# Page configuration
st.set_page_config(page_title="Groq Streamlit App", page_icon="⚡")

st.title("⚡ Groq-Powered AI Assistant")
st.markdown("Enter your query below to get instant responses powered by Groq LPUs.")

# Sidebar for API Key and Settings
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    model = st.selectbox(
        "Choose a model:",
        ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
    )

# Initialize Session State for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your question?"):
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    else:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Initialize Groq client
        client = Groq(api_key=api_key)

        # Generate response
        with st.chat_message("assistant"):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    model=model,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                # Add assistant response to history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
