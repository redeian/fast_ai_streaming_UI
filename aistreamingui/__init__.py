import streamlit as st
import random
import time
import requests
import json
import os

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Function to stream data from FastAPI
def stream_data_from_fastapi(prompt):
  # URL of the FastAPI endpoint
  url = "http://localhost:8000/chat/"
  api_key = os.environ.get("MARK_DIGITAL_API_KEY")

  try:
    # Create the JSON payload
    payload = {
      "api_key": api_key,
      "messages": prompt
    }

    # Make a POST request to the FastAPI app
    with requests.post(url, json=payload, stream=True) as response:
      for chunk in response.iter_content(chunk_size=None):
        if chunk:
          yield chunk.decode("utf-8")
  except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to FastAPI server: {e}")


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(stream_data_from_fastapi(st.session_state.messages))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})



