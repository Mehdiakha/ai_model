import streamlit as st
import requests

# Set page title
st.set_page_config(page_title="Chat with Mistral AI", layout="wide")

st.title("💬 Chat with Mistral AI")

# Define FastAPI URL
API_URL = "http://127.0.0.1:8002/chat"  # Update this if needed

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input box
user_message = st.chat_input("Type your message...")

# When the user sends a message
if user_message:
    # Append user's message to chat history
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_message)

    try:
        # Send the user input to FastAPI backend
        response = requests.post(API_URL, json={"message": user_message})

        # Check if the response is successful
        if response.status_code == 200:
            chat_response = response.json().get("response", "Sorry, I couldn't process that.")
        else:
            chat_response = "Error: Unable to reach the server."

    except Exception as e:
        chat_response = f"An error occurred: {e}"

    # Append AI's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": chat_response})

    # Display AI's response
    with st.chat_message("assistant"):
        st.markdown(chat_response)
