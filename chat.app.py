import streamlit as st
import requests

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()

API_URL = "http://ec2-3-83-217-17.compute-1.amazonaws.com:3000/api/v1/prediction/6ce36d53-ed90-4759-877b-83aedadb617b"
# API_URL = "http://localhost:3000/api/v1/prediction/575f6659-23eb-4ccb-885c-d2d3632fb976"
st.title("Natural & Adabas Chatbot")
st.text("Based on 29 PDF guides")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question about Natural & Adabas?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response =  query({
        "question": prompt,
    })

#    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})


